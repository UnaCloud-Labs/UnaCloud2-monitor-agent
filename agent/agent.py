from time import time, sleep

from utils.cpu_utils import CPUUtils
from utils.network_utils import NetworkUtils
from utils.ram_utils import RAMUtils
from utils.disk_utils import DiskUtils
from utils.vm_utils import VMUtils

import db_helper


network_utils = NetworkUtils()
cpu_utils = CPUUtils()
ram_utils = RAMUtils()
disk_utils = DiskUtils()
vm_utils = VMUtils()


def main():
    while True:
        start_time = time()
        print(db_helper.post(get_system_info()))
        sleep(1 - ((time() - start_time) % 1))


def get_system_info():
    return {
        "timestamp": time(),
        "ip": network_utils.get_ip_addr(),
        "ram": ram_utils.get_ram_percent(),
        "swap": ram_utils.get_swap_memory(),
        "disk": disk_utils.get_disk_percent(),
        "cpu": cpu_utils.get_cpu_percent(),
        "cpu_details": cpu_utils.get_percpu_peruser_percent(),
        "net_stats": network_utils.get_net_stats(),
        "net_io_counters": network_utils.get_net_io_counters()
    }


if __name__ == "__main__":
    main()
