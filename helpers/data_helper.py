import datetime


def ntuple_to_dict(ntuple):
    return dict(ntuple._asdict())

def format_time():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def sort_process_cpu(process):
    return process["cpu_percent"]

def sort_process_ram(process):
    return process["memory_percent"]

def get_local_properties():
    properties = {}
    try:
        local_properties = open('local.properties', 'r')
        lines = local_properties.readlines()
        for line in lines:
            if line.startswith("DATA_PATH"):
                properties["partition"] = line.split('=')[1].replace("\\:", ":").replace("\\", "/").strip()
            if line.startswith("PG_POWER_PATH"):
                properties["pg_path"] = line.split('=')[1].replace("\\\\", "/").strip()
            if line.startswith("PG_EXE_NAME"):
                properties["pg_exe"] = line.split('=')[1].replace("\\\\", "/").strip()
        return properties
    except (IOError, ValueError):
        return {
            'partition': 'C://',
            'pg_path': 'C:/Program Files/Intel/Power Gadget 3.0/',
            'pg_exe': 'PowerLog3.0.exe'
        }
