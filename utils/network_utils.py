import psutil
import subprocess
import re
import _thread
from time import sleep, time
from urllib.request import urlopen
import helpers.data_helper as dh


class NetworkUtils:

    RTT = 1
    IP = None

    def __init__(self, rtt_freq):
        self.rtt_freq = rtt_freq
        _thread.start_new_thread(self.set_rtt, ("ping_thread", ))

    def get_rtt(self):
        return self.RTT

    def set_rtt(self, thread_name):
        while (True):
            print("pinging")
            start_time = time()
            ping_proc = subprocess.Popen("ping 157.253.236.113", stdout=subprocess.PIPE)
            ping_output = ping_proc.stdout.read().decode('utf-8')
            average_regex = r'Average = ([0-9]+)ms'
            new_rtt = re.search(average_regex, ping_output).group(1)
            if new_rtt:
                self.RTT = int(new_rtt)
            else:
                self.RTT = -1
            sleep(self.rtt_freq - ((time() - start_time)))

    def get_ip_addr(self):
        if(not self.IP):
            self.set_ip_addr()
        return self.IP

    def set_ip_addr(self):
        self.IP = urlopen('http://ip.42.pl/raw').read().decode("utf-8")

    def get_net_stats(self):
        stats = psutil.net_if_stats()
        for key, value in stats.items():
            stats[key] = dh.ntuple_to_dict(value)
        return stats

    def get_net_io_counters(self):
        return dh.ntuple_to_dict(psutil.net_io_counters())
