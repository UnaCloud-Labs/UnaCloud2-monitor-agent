import psutil
import helpers.data_helper as dh


class DiskUtils:

    def get_disk_partitions(self):
        return [dh.ntuple_to_dict(partition) for partition in psutil.disk_partitions(all=True)]

    def get_disk_percent(self, total=False):
        if total:
            return dh.ntuple_to_dict(psutil.disk_usage('/'))["total"]
        else:
            return {k: dh.ntuple_to_dict(psutil.disk_usage('/'))[k] for k in ('used', 'free', 'percent')}
