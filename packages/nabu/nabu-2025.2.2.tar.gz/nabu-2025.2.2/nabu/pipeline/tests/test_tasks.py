import os
from time import sleep
import pytest
import numpy as np
from nabu.pipeline.tasks import TaskProcessor, FakeTaskProcessor

task_processor_class = [TaskProcessor, FakeTaskProcessor]


@pytest.mark.parametrize("task_processor_class", task_processor_class)
def test_task_processor_simple(task_processor_class):
    class DummyTask:
        def __init__(self): ...

        def process_task(self, task):
            result = {
                "task_id": task["task_id"],
                "result": task["expected_result"],
            }
            return result

    task_processor = task_processor_class(DummyTask, n_processes=1)
    task_processor.start_workers()
    tasks = [{"task_id": i, "expected_result": i + 10} for i in range(5)]
    futures = []
    for task in tasks:
        future_result = task_processor.submit(0, task)
        futures.append(future_result)
    task_processor.start_work()  # not needed for TaskProcessor, but needed for FakeTaskProcessor

    # Optional: wait for results (here processing is "instant")
    for future in futures:
        result = future.result()  # blocking call
        i = result["task_id"]
        assert result["result"] == tasks[i]["expected_result"]

    task_processor.stop_workers()


@pytest.mark.parametrize("task_processor_class", task_processor_class)
def test_task_processor_callback(task_processor_class):
    class MyProcessingClass:
        def __init__(self, a):
            self.a = a
            self.previous_task = None

        def process_task(self, task):
            print(f"[{os.getpid()}] Got task: {task} (previous was: {self.previous_task})")
            sleep(0.5)
            result = f"{os.getpid()} did {task}"
            self.previous_task = task
            return result

    tp = task_processor_class(MyProcessingClass, n_processes=2, worker_init_args={"a": 1})
    tp.start_workers()

    # Submit tasks
    futures = []
    for idx, t in enumerate([f"task_{i}" for i in range(6)]):
        wid = idx % len(tp.workers)  # even/odd distribution
        fut = tp.submit(wid, t)
        fut.add_done_callback(lambda f: print(f"Callback: {f.result()}"))
        futures.append(fut)
    print("submitted")
    tp.start_work()  # not needed for TaskProcessor, but needed for FakeTaskProcessor

    # Wait for all results
    results = [f.result() for f in futures]
    print("Final results:", results)

    tp.stop_workers()


@pytest.mark.parametrize("task_processor_class", task_processor_class)
def test_with_worker_failure(task_processor_class):
    class DummyProcessing:
        def __init__(self, sleep_time):
            self.s = sleep_time

        def process_task(self, task):
            sleep(self.s)
            if task.get("fail", False):
                raise ValueError("kaboom")
            i = task.get("task_id", 1)
            return {"result": i + 10}

    tp = task_processor_class(DummyProcessing, n_processes=2, worker_init_args=(0.1,))
    tp.start_workers()

    try:
        tasks = [{"task_id": i, "fail": bool(np.random.randint(0, high=2))} for i in range(10)]
        futures = {}
        # Submit tasks, distribute evenly among workers
        for i, task in enumerate(tasks):
            w_id = i % len(tp.workers)
            f = tp.submit(w_id, task)
            futures[task["task_id"]] = f

        tp.start_work()  # not needed for TaskProcessor, but needed for FakeTaskProcessor

        # Wait for completion of all tasks
        while not (all(f.done() for f in futures.values())):
            sleep(0.5)

        # Inspect results
        for task_id, future in futures.items():
            # in principle blocking call, but since done() is True, this will return instantly
            # Also, this would hang forever if there was no failure handling mechanism
            result = future.result()
            task_failed = result.get("error", None)
            if tasks[task_id]["fail"]:
                assert task_failed is not None
            else:
                assert task_failed is None
                assert result["result"] == task_id + 10
    finally:
        tp.stop_workers()
