import psutil
import helpers.data_helper as dh


class CPUUtils:

    def get_cpu_count(self):
        return psutil.cpu_count()

    def get_cpu_percent(self):
        return psutil.cpu_percent()

    def get_cpu_stats(self):
        return psutil.cpu_stats()

    def get_percpu_peruser_percent(self):
        return dh.ntuple_to_dict(psutil.cpu_times_percent())
