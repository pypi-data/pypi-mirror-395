import os
import multiprocessing as mp
import queue
from threading import Thread
from traceback import print_exc
from time import sleep

"""
A simple yet quite generic tasks distribution system using multiprocessing.
There are lots of task distribution frameworks (dask_distributed, ray, etc),
but here the needs is really simple: distribute independent tasks on a few processes, without inter-process communication.
"""


# Possible improvements
#   future.error : bool indicating whether something went wrong
#   __repr__ / __str__  to inspect a future object at glance


class Future:
    """
    A dummy future-like object that mimics concurrent.futures.
    We don't use concurrent.futures because it is tightly coupled to its own executors (ThreadPoolExecutor and ProcessPoolExecutor).
    A concurrent.futures.Future is not a free-standing object that can be safely complete yourself.
    It's designed to be managed by an executor which handles the worker lifecycle, task submission, and result propagation.
    Executors use their own internal queues and bookkeeping; they won't integrate cleanly in this case because
    we use a multiprocessing.Queue-based protocol and persistent per-GPU processes.
    """

    def __init__(self):
        self._result = None
        self._done = mp.Event()
        self._callbacks = []

    def set_result(self, value):
        self._result = value
        self._done.set()
        for cb in self._callbacks:
            cb(self)

    def result(self, timeout=None):
        self._done.wait(timeout)
        return self._result

    def done(self):
        return self._done.is_set()

    def add_done_callback(self, fn):
        if self.done():
            fn(self)
        else:
            self._callbacks.append(fn)


def worker_entrypoint(
    tasks_queue, results_queue, processing_class, worker_id=None, proc_class_init_args=None, proc_class_init_kwargs=None
):
    """
    Persistent CPU worker.

    Work is submitted to this worker by submitting a non-empty tuple (task_id, task) through the 'tasks_queue' Queue.
    A tuple (X, None) will stop the current worker from accepting new tasks.

    Parameters
    ----------
    worker_id: int
        Worker identifier
    tasks_queue: multiprocessing.Queue
        Queue where tasks are sent from main task processor to workers
    results_queue: multiprocessing.Queue
        Queue where results are sent from workers to main task processor
    processing_function: callable
        Function executed by worker each time a task is sent.
        It must have only one argument: the task itself.
    """
    proc = processing_class(*(proc_class_init_args or ()), **(proc_class_init_kwargs or {}))
    proc.worker_id = worker_id
    while True:
        task_id, task = tasks_queue.get()
        if task is None:
            break
        try:
            result = proc.process_task(task)
        except Exception as exc:
            result = {"error": exc}
            print_exc()
        results_queue.put((task_id, result))


# Possible improvements:
#  - submit() could automatically pick a worker
#  - standardize the tasks: dictionary with worker_id
#  - check that 'processing_class' has a 'process_task' method. Make it inherit from a base class ?


class TaskProcessor:

    queue_class = mp.Queue

    def __init__(self, processing_class, n_processes=2, worker_init_args=None, worker_init_kwargs=None):
        self.n_processes = n_processes
        self.task_queues = []
        self.results_queue = self.queue_class()
        self.workers = []
        self.futures = {}
        self._task_counter = 0
        self._workers_stopped = False
        self.processing_class = processing_class
        self._worker_init_args = worker_init_args or ()
        self._worker_init_kwargs = worker_init_kwargs or {}

    def start_workers(self):
        for wid in range(self.n_processes):
            tasks_queue = self.queue_class()
            p = mp.Process(
                target=worker_entrypoint,
                args=(tasks_queue, self.results_queue, self.processing_class),
                kwargs={
                    "worker_id": wid,
                    "proc_class_init_args": self._worker_init_args,
                    "proc_class_init_kwargs": self._worker_init_kwargs,
                },
            )
            p.start()
            self.task_queues.append(tasks_queue)
            self.workers.append(p)

        # start listener thread
        self.listening_thread = Thread(target=self._result_listener, daemon=True).start()

    def start_work(self): ...

    def stop_workers(self):
        if self._workers_stopped:
            return
        for q in self.task_queues:
            q.put((None, None))
        for p in self.workers:
            p.join()
        self._workers_stopped = True

    def _result_listener(self):
        while True:
            task_id, result = self.results_queue.get()
            if task_id not in self.futures:
                break
            self.futures[task_id].set_result(result)

    def submit(self, worker_id, task):
        fut = Future()
        task_id = self._task_counter
        self._task_counter += 1
        self.futures[task_id] = fut
        self.task_queues[worker_id].put((task_id, task))
        return fut


class FakeTaskProcessor(TaskProcessor):
    """
    A "fake" TaskProcessor that does not use multi-processing and will process tasks serially
    """

    queue_class = queue.Queue

    def start_workers(self):
        self.task_queues = [self.queue_class()]  # one single task queue for all workers
        self.workers = [None]

    def stop_workers(self):
        self._workers_stopped = True

    def start_work(self):
        task_queue = self.task_queues[0]
        proc = self.processing_class(*(self._worker_init_args or ()), **(self._worker_init_kwargs or {}))
        proc.worker_id = 0  # ?
        while task_queue.qsize() > 0:
            task_id, task = task_queue.get_nowait()
            if task is None:
                break
            try:
                result = proc.process_task(task)
            except Exception as exc:
                result = {"error": exc}
                print_exc()
            if task_id not in self.futures:
                break
            self.futures[task_id].set_result(result)
