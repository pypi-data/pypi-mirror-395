from collections.abc import Callable
from contextlib import contextmanager
import csv
from dataclasses import dataclass
from pathlib import Path
import platform
from threading import Event, Thread

import numpy
import psutil
from terminaltables import AsciiTable

DEFAULT_SAMPLING_FREQ = 10  # Hz


@dataclass
class TrackerConf:
    output_dir: str = "."
    output_name: str = "report.csv"
    register: Callable | None = None
    complete: Callable = lambda: None


@dataclass
class TrackerProbe:
    data: dict = None


@contextmanager
def resource_tracking(
    frequency: int = DEFAULT_SAMPLING_FREQ,
    show: bool = False,
    csv_report: bool = False,
    probe: TrackerProbe | None = None,
    conf: TrackerConf | None = None,
    show_pids: bool = False,
    mask_parent: bool = True,
) -> None:
    assert frequency <= 10, "Highest confirmed frequency is 10Hz."

    tracker_conf = conf or TrackerConf()

    if csv_report or show:
        metric_names = [
            "cpu%",
            "rss",
            "vms",
        ]
        if "linux" in platform.system().lower():
            metric_names.extend(["text", "data"])
        metrics = {}

        def track(metrics, stop_event):
            process = psutil.Process()
            total_mem = psutil.virtual_memory().total
            watched = {process}
            while not stop_event.wait(timeout=1e-8):
                # Update the process list
                watched |= set(process.children(recursive=True))
                for proc in watched:
                    try:
                        # Entry orders follow `metric_names`
                        mem = proc.memory_info()
                        data = [
                            proc.cpu_percent(interval=1.0 / frequency),
                            mem.rss / total_mem * 100,
                            mem.vms / total_mem * 100,
                        ]
                        if "linux" in platform.system().lower():
                            data.append(mem.text / total_mem * 100)
                            data.append(mem.data / total_mem * 100)
                        metrics[proc.pid]["data"].append(data)
                        # "gpu", Unfortunately unlikely https://github.com/giampaolo/psutil/issues/526
                    except psutil.NoSuchProcess:
                        # Child ended or crashed, so we do not need to track.
                        # We assume the client manages its child processes state.
                        continue
                    except KeyError:  # noqa: E722
                        # We have to ignore the first CPU record and keep 0.1s before
                        # a second call to get a valid value.
                        # https://psutil.readthedocs.io/en/latest/#psutil.Process.cpu_percent
                        # The first record is set to 0.0 and affects statistics.
                        (proc.cpu_percent(interval=1.0 / frequency),)
                        metrics[proc.pid] = {
                            "name": proc.name().lower(),
                            "data": [],
                        }

        stop_request = Event()
        stop_request.clear()
        loop = Thread(
            target=track,
            args=(
                metrics,
                stop_request,
            ),
        )
        try:
            loop.start()
            yield tracker_conf
        finally:
            stop_request.set()
            loop.join()

        if probe:
            probe.data = metrics

        if show:
            try:
                stats = [
                    [
                        "Process",
                        "CPU%",
                        "",
                        "",
                        "",
                        "",
                        "RSS%",
                        "VMS%",
                    ],
                    [
                        "",
                        "min",
                        "median",
                        "mean",
                        "std",
                        "max",
                        "max",
                        "max",
                    ],
                ]
                if show_pids:
                    stats[0].insert(1, "PID")
                    stats[1].insert(1, "")
                if "linux" in platform.system().lower():
                    stats[0].extend(["TRS%", "DRS%"])
                    stats[1].extend(["text", "data"])
                parent = psutil.Process().pid
                for child, info in metrics.items():
                    if len(info["data"]) > 0:
                        ndata = numpy.array(info["data"])
                        if child == parent and mask_parent:
                            continue
                        cpu = ndata[:, metric_names.index("cpu%")]
                        point = [
                            info["name"],
                            f"{cpu.min():.2f}",
                            f"{numpy.median(cpu):.2f}",
                            f"{cpu.mean():.2f}",
                            f"{cpu.std():.2f}",
                            f"{cpu.max():.2f}",
                            f"{ndata[:, metric_names.index('rss')].max():.2f}",
                            f"{ndata[:, metric_names.index('vms')].max():.2f}",
                        ]
                        if "linux" in platform.system().lower():
                            point.extend(
                                [
                                    f"{ndata[:, metric_names.index('text')].max():.2f}",
                                    f"{ndata[:, metric_names.index('data')].max():.2f}",
                                ]
                            )
                        if show_pids:
                            point.insert(1, str(child))
                        stats.append(point)

                table_instance = AsciiTable(stats, "Runtime statistics")
                print(table_instance.table)
            except:  # noqa: E722
                # TODO Silent errors and loss of report for now
                pass

        if csv_report:
            parent = psutil.Process().pid
            for child, info in metrics.items():
                if len(info["data"]) > 0:
                    if child == parent and mask_parent:
                        continue
                    for metric in metric_names:
                        if "cpu" in metric.lower():
                            mem_met = ""
                        else:
                            mem_met = "mem_"
                        save_path = str(
                            Path(tracker_conf.output_dir)
                            / f"{info['name']}_{mem_met}{metric.replace('%', '')}_{tracker_conf.output_name}"
                        )
                        with open(
                            save_path,
                            "w",
                        ) as f:
                            writer = csv.writer(f)
                            writer.writerow(["offset", metric])
                            for idx, row in enumerate(info["data"]):
                                writer.writerow(
                                    [str(idx), f"{row[metric_names.index(metric)]:.2f}"]
                                )
                        if tracker_conf.register:
                            tracker_conf.register(save_path)
    else:
        yield tracker_conf

    # Ensure that any completion callback is run last, to address all scenarios.
    #   Note: This is internal, and defaults to noop. Most uses will call
    #   the stop function of a Run object.
    tracker_conf.complete()
