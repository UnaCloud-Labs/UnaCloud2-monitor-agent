import psutil


class DiskUtils:

    def get_disk_percent(self):
        return getattr(psutil.disk_usage('/'), 'percent')
