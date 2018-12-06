import psutil
import helpers.data_helper as dh


class RAMUtils:

    def get_ram_percent(self, total=False):
        if total:
            return dh.ntuple_to_dict(psutil.virtual_memory())["total"]
        else:
            return {k: dh.ntuple_to_dict(psutil.virtual_memory())[k] for k in ('used', 'free', 'percent')}

    def get_swap_memory(self, total=False):
        if total:
            return dh.ntuple_to_dict(psutil.swap_memory())["total"]
        else:
            return {k: dh.ntuple_to_dict(psutil.swap_memory())[k] for k in ('used', 'free', 'percent', 'sin', 'sout')}
