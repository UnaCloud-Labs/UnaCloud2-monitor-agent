import datetime


def ntuple_to_dict(ntuple):
    return dict(ntuple._asdict())

def format_time():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def sort_process_cpu(process):
    return process["cpu_percent"]

def sort_process_ram(process):
    return process["memory_percent"]
