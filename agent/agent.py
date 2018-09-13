from time import time, sleep

from agent.cpu_utils import CPUUtils
from agent.network_utils import NetworkUtils


network_utils = NetworkUtils()
cpu_utils = CPUUtils()


def main():
    while True:
        start_time = time()
        print(get_system_info())
        sleep(1 - ((time() - start_time) % 1))


def get_system_info():
    return {
        "ip": network_utils.get_ip_addr(),
        "cpu": cpu_utils.get_cpu_percent()
    }


if __name__ == "__main__":
    main()
