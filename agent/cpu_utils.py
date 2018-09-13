import psutil


class CPUUtils:

    def get_cpu_percent(self):
        return psutil.cpu_percent()