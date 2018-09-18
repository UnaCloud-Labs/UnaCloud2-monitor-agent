from time import time, sleep

from utils.cpu_utils import CPUUtils
from utils.network_utils import NetworkUtils
from utils.ram_utils import RAMUtils
from utils.disk_utils import DiskUtils

network_utils = NetworkUtils()
cpu_utils = CPUUtils()
ram_utils = RAMUtils()
disk_utils = DiskUtils()


def main():
    while True:
        start_time = time()
        print(get_system_info())
        sleep(1 - ((time() - start_time) % 1))


def get_system_info():
    return {
        "timestamp": time(),
        "ip": network_utils.get_ip_addr(),
        "ram": ram_utils.get_ram_percent(),
        "disk": disk_utils.get_disk_percent(),
        "cpu": cpu_utils.get_cpu_percent(),
        "cpu_details": cpu_utils.get_percpu_peruser_percent()
    }


if __name__ == "__main__":
    main()
