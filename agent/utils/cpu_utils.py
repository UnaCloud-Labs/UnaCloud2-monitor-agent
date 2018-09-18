import psutil


class CPUUtils:

    def get_cpu_percent(self):
        return psutil.cpu_percent()

    def get_percpu_peruser_percent(self):
        return dict(psutil.cpu_times_percent()._asdict())
