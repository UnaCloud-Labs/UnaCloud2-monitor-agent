import psutil


class ProcessUtils:

    def __init__(self, pname):
        self.pname = pname
        self.process = self.find_process_by_name(pname)

    def find_process_by_name(self, name):
        for p in psutil.process_iter(attrs=['name']):
            if p.info['name'] == name:
                return p
        return None

    def get_process_status(self):
        return self.process.status()

    