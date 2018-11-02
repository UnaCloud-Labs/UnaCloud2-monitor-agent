import psutil
import subprocess
import re
import _thread
from time import sleep, time
from urllib.request import urlopen
import helpers.data_helper as dh


class NetworkUtils:

    RTT = 1

    def __init__(self, rtt_freq):
        self.rtt_freq = rtt_freq
        _thread.start_new_thread(self.set_rtt, ("ping_thread", ))

    def get_rtt(self):
        return self.RTT

    def set_rtt(self, thread_name):
        while (True):
            start_time = time()
            ping_proc = subprocess.Popen("ping 157.253.236.113", stdout=subprocess.PIPE)
            ping_output = ping_proc.stdout.read().decode('utf-8')
            average_regex = r'Average = ([0-9]+)ms'
            self.RTT = re.search(average_regex, ping_output).group(1)
            sleep(self.rtt_freq - ((time() - start_time)))

    def get_ip_addr(self):
        return urlopen('http://ip.42.pl/raw').read().decode("utf-8")

    def get_net_stats(self):
        stats = psutil.net_if_stats()
        for key, value in stats.items():
            stats[key] = dh.ntuple_to_dict(value)
        return stats

    def get_net_io_counters(self):
        return dh.ntuple_to_dict(psutil.net_io_counters())
