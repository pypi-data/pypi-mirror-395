# ruff: noqa
import numpy as np
from os import path
from datetime import datetime
from ..utils import check_supported, convert_str_to_tuple
from .utils import parse_params_values
from .cli_configs import ShowReconstructionTimingsConfig

try:
    import matplotlib.pyplot as plt

    __have_matplotlib__ = True
except ImportError:
    __have_matplotlib__ = False

steps_to_measure = [
    "Reading data",
    "Applying flat-field",
    "Applying double flat-field",
    "Applying CCD corrections",
    "Rotating projections",
    "Performing phase retrieval",
    "Performing unsharp mask",
    "Taking logarithm",
    "Applying radios movements",
    "Normalizing sinograms",
    "Building sinograms",  # deprecated
    "Removing rings on sinograms",
    "Reconstruction",
    "Computing histogram",
    "Saving data",
]


def extract_timings_from_volume_reconstruction_lines(lines, separator=" - "):
    def extract_timestamp(line):
        timestamp = line.split(separator)[0]
        return datetime.strptime(timestamp, "%d-%m-%Y %H:%M:%S")

    def extract_current_step(line):
        return line.split(separator)[-1]

    current_step = extract_current_step(lines[0])
    t1 = extract_timestamp(lines[0])

    res = {}
    for line in lines[1:]:
        line = line.strip()
        if len(line.split(separator)) == 1:
            continue
        timestamp = line.strip().split(separator)[0]
        t2 = datetime.strptime(timestamp, "%d-%m-%Y %H:%M:%S")

        res.setdefault(current_step, [])
        res[current_step].append((t2 - t1).seconds)

        t1 = t2
        current_step = extract_current_step(line)

    return res


def parse_logfile(fname, separator=" - "):
    """
    Returns
    -------
    timings: list of dict
        List of dictionaries: one dict per reconstruction in the log file.
        For each dict, the key is the pipeline step name, and the value is the list of timings for the different chunks.
    """
    with open(fname, "r") as f:
        lines = f.readlines()

    start_text = "Going to reconstruct slices"
    end_text = "Merging reconstructions to"

    start_line = None
    rec_log_bounds = []
    for i, line in enumerate(lines):
        if start_text in line:
            start_line = i
        if end_text in line:
            if start_line is None:
                raise ValueError("Could not find reconstruction start string indicator")
            rec_log_bounds.append((start_line, i))
            rec_file_basename = path.basename(line.split(end_text)[-1])

    results = []
    for bounds in rec_log_bounds:
        start, end = bounds
        timings = {}
        res = extract_timings_from_volume_reconstruction_lines(lines[start:end], separator=separator)
        for step in steps_to_measure:
            if step in res:
                timings[step] = res[step]
        results.append(timings)
    return results


def display_timings_pie(timings, reduce_function=None, cutoffs=None):
    reduce_function = reduce_function or np.median
    cutoffs = cutoffs or (0, np.inf)

    def _format_pie_text(pct, allvals):
        # https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html
        absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d} s)"

    for run in timings:
        fig = plt.figure()
        pie_labels = []
        pie_sizes = []
        for step_name, step_timings in run.items():
            t = reduce_function(step_timings)
            if t > cutoffs[0] and t < cutoffs[1]:
                # pie_labels.append(step_name)
                pie_labels.append(step_name + "\n(%d s)" % t)
                pie_sizes.append(t)
        ax = fig.subplots()
        # ax.pie(pie_sizes, labels=pie_labels, autopct=lambda pct: _format_pie_text(pct, pie_sizes)) # autopct='%1.1f%%')
        ax.pie(pie_sizes, labels=pie_labels, autopct="%1.1f%%")

        fig.show()
    input("Press any key to continue")


def parse_reclog_cli():
    args = parse_params_values(
        ShowReconstructionTimingsConfig, parser_description="Display reconstruction performances from a log file"
    )
    if not (__have_matplotlib__):
        print("Need matplotlib to use this utility")
        exit(1)

    display_functions = {
        "pie": display_timings_pie,
    }

    logfile = args["logfile"]
    cutoff = args["cutoff"]
    display_type = args["type"]

    check_supported(display_type, display_functions.keys(), "Graphics display type")
    if cutoff is not None:
        cutoff = list(map(float, convert_str_to_tuple(cutoff)))

    timings = parse_logfile(logfile)
    display_functions[display_type](timings, cutoffs=cutoff)

    return 0


if __name__ == "__main__":
    parse_reclog_cli()
    exit(0)
