import psutil


class DiskUtils:

    def get_disk_percent(self):
        return dict(psutil.disk_usage('/')._asdict())
