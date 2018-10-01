import psutil
import helpers.data_helper as dh


class RAMUtils:

    def get_ram_percent(self):
        return dh.ntuple_to_dict(psutil.virtual_memory())

    def get_swap_memory(self):
        return dh.ntuple_to_dict(psutil.swap_memory())
