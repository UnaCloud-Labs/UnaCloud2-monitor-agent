import argparse
import sys
from time import sleep, time

import helpers.db_helper as db
import helpers.data_helper as dh
from utils.cpu_utils import CPUUtils
from utils.disk_utils import DiskUtils
from utils.energy_utils import EnergyUtils
from utils.network_utils import NetworkUtils
from utils.ram_utils import RAMUtils
from utils.vm_utils import VMUtils
from utils.process_utils import ProcessUtils
from utils.user_utils import UserUtils

CURR_VERSION = "4.2"

FREQUENCY = 1
INFINITE = True
DURATION = 0
UNACLOUD_PORT = 10027
RTT_FREQUENCY = 10
PG_DURATION = 10

RAM_THRESHOLD = 75
CPU_THRESHOLD = 75
DISK_THRESHOLD = 75
NUM_PROCESSES = 5

properties = None
cpu_utils = None
ram_utils = None
disk_utils = None
vm_utils = None
vbox_process = None
unacloud_process = None
network_utils = None
energy_utils = None
user_utils = None


def parse_arguments():
    global unacloud_process
    parser = argparse.ArgumentParser(description="Monitor the machine's resources")
    parser.add_argument('-f', '--frequency', type=int,
                        help='Frequency (in seconds) with which the agent will send system information')
    parser.add_argument('-d', '--duration', type=int,
                        help='Duration (in seconds) for which the problem will run')
    parser.add_argument('-pp', '--pport', type=int,
                        help='Port in which the UnaCloud process is running')
    parser.add_argument('-ramth', '--ramthreshold', type=int,
                        help="If the RAM of a reading surpasses this value, information about most RAM intensive processes will be sent")
    parser.add_argument('-cputh', '--cputhreshold', type=int,
                        help="If the CPU of a reading surpasses this value, information about most CPU intensive processes will be sent")
    parser.add_argument('-diskth', '--diskthreshold', type=int,
                        help="If the disk of a reading surpasses this value, information about most disk intensive processes will be sent")
    parser.add_argument('-n', '--numprocesses', type=int,
                        help="Number of top processes to be sent when a resource surpasses the threshold")
    parser.add_argument('-rtt', '--rttfrequency', type=int,
                        help="Frequency (in seconds) with which the agent will measure the RTT")
    parser.add_argument('-pg', '--pgduration', type=int,
                        help="Duration (in seconds) with which the agent will measure power consumption")
    parser.add_argument('--version', action='store_true',
                        help="Print the version of the agent")
    args = parser.parse_args()

    if args.frequency:
        global FREQUENCY
        FREQUENCY = args.frequency

    if args.duration:
        global DURATION, INFINITE
        DURATION = args.duration
        INFINITE = False

    if args.pport:
        global UNACLOUD_PORT
        UNACLOUD_PORT = args.pport

    if args.ramthreshold:
        global RAM_THRESHOLD
        RAM_THRESHOLD = args.ramthreshold

    if args.diskthreshold:
        global DISK_THRESHOLD
        DISK_THRESHOLD = args.cputhreshold

    if args.cputhreshold:
        global CPU_THRESHOLD
        CPU_THRESHOLD = args.cputhreshold

    if args.numprocesses:
        global NUM_PROCESSES
        NUM_PROCESSES = args.numprocesses

    if args.rttfrequency:
        global RTT_FREQUENCY
        RTT_FREQUENCY = args.rttfrequency

    if args.pgduration:
        global PG_DURATION
        PG_DURATION = args.pgduration

    return args.version


def initialize_utils():
    global cpu_utils, ram_utils, disk_utils, vm_utils, vbox_process, unacloud_process, network_utils, energy_utils, user_utils, properties
    properties = dh.get_local_properties()
    cpu_utils = CPUUtils()
    ram_utils = RAMUtils()
    disk_utils = DiskUtils()
    vm_utils = VMUtils()
    vbox_process = ProcessUtils(VMUtils.VBOX_PROCESS)
    unacloud_process = ProcessUtils(port=UNACLOUD_PORT)
    network_utils = NetworkUtils(RTT_FREQUENCY)
    energy_utils = EnergyUtils(properties['pg_path'], properties['pg_exe'], PG_DURATION)
    user_utils = UserUtils()


def main():
    only_print_version = parse_arguments()
    if only_print_version:
        print_version()
    else:
        run()


def run():
    initialize_utils()

    response = db.post(db.initial_info, get_initial_info())
    handle_response(response)

    curr_duration = DURATION
    while (curr_duration > 0) or INFINITE:
        start_time = time()
        response = db.post(db.metric, get_system_info())
        handle_response(response)
        if not INFINITE:
            curr_duration = curr_duration - FREQUENCY
        sleep_duration = FREQUENCY - ((time() - start_time) % FREQUENCY)
        if sleep_duration > 0:
            sleep(sleep_duration)


def get_system_info():
    info = {
		"timestamp": dh.format_time(),
        "ip": network_utils.get_ip_addr(),
        "ram": ram_utils.get_ram_percent(),
        "swap": ram_utils.get_swap_memory(),
        "disk": disk_utils.get_disk_percent(),
        "unacloud_disk": disk_utils.get_disk_percent(partition=properties['partition']),
        "cpu": cpu_utils.get_cpu_percent(),
        "cpu_details": cpu_utils.get_percpu_peruser_percent(),
        "net_io_counters": network_utils.get_net_io_counters(),
        "vms": vm_utils.get_vms(running=False),
        "running_vms": vm_utils.get_vms(),
        "virtualbox_status": vm_utils.get_vbox_status(),
        "vbox_process_count": ProcessUtils.count_processes_by_name(VMUtils.VBOX_PROCESS),
        "unacloud_status": 1 if unacloud_process.get_process_status() == "running" else 0,
        "rtt": network_utils.get_rtt(),
        "energy": energy_utils.get_power_consumption(),
        "user_logged": user_utils.get_users_logged()
    }
    for critical_resource in resources_above_threshold(info):
        db.post(db.processes, critical_resource)
    return info


def get_initial_info():
    return {
        "timestamp": dh.format_time(),
        "ip": network_utils.get_ip_addr(),
        "cpu_count": cpu_utils.get_cpu_count(),
        "disk_partitions": disk_utils.get_disk_partitions(),
        "total_ram": ram_utils.get_ram_percent(total=True),
        "total_swap": ram_utils.get_swap_memory(total=True),
        "total_disk": disk_utils.get_disk_percent(total=True),
        "total_unacloud_disk": disk_utils.get_disk_percent(total=True, partition=properties['partition'])
    }



def get_processes_info(critical_resource):
    return {
        "ip": network_utils.get_ip_addr(),
        "critical_resource": critical_resource,
        "processes": ProcessUtils.get_top_processes(NUM_PROCESSES, resource=critical_resource)
    }


def get_offline_data():
    return {
        "ip": network_utils.get_ip_addr(),
        "timeOffline": network_utils.get_offline_counter() * FREQUENCY
    }


def resources_above_threshold(info):
    critical_resources = []
    if info["ram"]["percent"] > RAM_THRESHOLD:
        critical_resources.append("ram")
    if info["cpu"] > CPU_THRESHOLD:
        critical_resources.append("cpu")
    if info["disk"]["percent"] > DISK_THRESHOLD:
        critical_resources.append("disk")
    return critical_resources


def handle_response(response):
    status_code = response.status_code
    if status_code != 200:
        network_utils.went_offline()
    else:
        if network_utils.is_offline():
            db.post(db.offline, get_offline_data())
        network_utils.went_online()


def print_version():
    print(CURR_VERSION)


if __name__ == "__main__":
    main()
