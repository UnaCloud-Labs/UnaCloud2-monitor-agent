import psutil


class RAMUtils:

    def get_ram_percent(self):
        return dict(psutil.virtual_memory()._asdict())

    def get_swap_memory(self):
        return dict(psutil.swap_memory()._asdict())
