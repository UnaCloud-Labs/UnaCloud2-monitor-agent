import psutil
from urllib.request import urlopen
import helpers.data_helper as dh


class NetworkUtils:

    def get_ip_addr(self):
        return urlopen('http://ip.42.pl/raw').read().decode("utf-8")

    def get_net_stats(self):
        stats = psutil.net_if_stats()
        for key, value in stats.items():
            stats[key] = dh.ntuple_to_dict(value)
        return stats

    def get_net_io_counters(self):
        return dh.ntuple_to_dict(psutil.net_io_counters())
