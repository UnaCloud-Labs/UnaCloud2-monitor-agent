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
STATS_LIST = []


def get_process_stats():
    stats = PROCESS.as_dict(ATTRS)
    for att in DICT_ATTRS:
        stats[att] = dict(stats[att]._asdict())
    threads = []
    for thread in stats["threads"]:
        threads.append(dict(thread._asdict()))
    stats["threads"] = threads
    STATS_LIST.append(stats)
    return stats

def report():
    avg_memory_file = open("reports/avg_memory.csv", "a")
    avg_cpu_file = open("reports/avg_cpu.csv", "a")
    memory_file = open("reports/memory.csv", "a")
    cpu_file = open("reports/cpu.csv", "a")

    memory_percent_list = [stat["memory_percent"] for stat in STATS_LIST]
    cpu_percent_list = [stat["cpu_percent"] for stat in STATS_LIST]   
    avg_memory_percent = average(memory_percent_list)
    avg_cpu_percent = average(cpu_percent_list)

    avg_memory_file.write(avg_memory_percent)
    avg_cpu_file.write(avg_cpu_percent)
    memory_file.write(str.join(memory_percent_list, ","))
    cpu_file.write(str.join(cpu_percent_list, ","))

def average(l):
    return sum(l) / len(l)
