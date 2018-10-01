import psutil
import helpers.data_helper as dh


class DiskUtils:

    def get_disk_percent(self):
        return dh.ntuple_to_dict(psutil.disk_usage('/'))
