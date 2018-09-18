import psutil


class RAMUtils:

    def get_ram_percent(self):
        return getattr(psutil.virtual_memory(), 'percent')
