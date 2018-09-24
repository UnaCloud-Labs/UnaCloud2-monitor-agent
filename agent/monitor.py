import psutil

PROCESS = psutil.Process()
ATTRS = ["cpu_times",
         "num_threads",
         "num_ctx_switches",
         "create_time",
         "num_handles",
         "status",
         "io_counters",
         "memory_info",
         "memory_full_info",
         "threads",
         "memory_percent",
         "cpu_percent",
         "ppid"]
DICT_ATTRS = [
    "cpu_times",
    "num_ctx_switches",
    "io_counters",
    "memory_info",
    "memory_full_info"
]


def get_process_stats():
    stats = PROCESS.as_dict(ATTRS)
    for att in DICT_ATTRS:
        stats[att] = dict(stats[att]._asdict())
    threads = []
    for thread in stats["threads"]:
        threads.append(dict(thread._asdict()))
    stats["threads"] = threads
    return stats

