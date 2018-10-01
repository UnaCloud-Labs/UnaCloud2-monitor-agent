import psutil
import helpers.data_helper as dh


class ProcessUtils:

    def __init__(self, pname="", port=0):
        self.pname = pname
        self.process = None
        if pname:
            self.process = self.find_process_by_name(pname)
        if port:
            self.process = self.find_process_by_port(port)

    def find_process_by_name(self, name):
        for p in psutil.process_iter(attrs=['name']):
            if name in p.info['name']:
                return p
        return None
    
    def find_process_by_port(self, port):
        for p in psutil.process_iter():
            if port in ProcessUtils.get_process_ports(p):
                return p
        return None
    
    def get_process_status(self):
        return self.process.status() if self.process else ''

    @staticmethod
    def count_processes_by_name(name):
        count = 0
        for p in psutil.process_iter(attrs=['name']):
            if name in p.info['name']:
                count = count + 1
        return count
    
    @staticmethod
    def get_process_ports(p):
        return [dh.ntuple_to_dict(dh.ntuple_to_dict(conn)["laddr"])["port"] for conn in p.connections()]
