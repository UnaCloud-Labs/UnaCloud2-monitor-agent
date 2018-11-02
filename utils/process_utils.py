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
    def get_processes_info():
        processes_info = []
        for p in psutil.process_iter():
            try:
                pInfo = p.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent'])
                processes_info.append(pInfo)
            except psutil.NoSuchProcess:
                pass
        return processes_info

    @staticmethod
    def get_top_processes(amount, resource="cpu"):
        processes = ProcessUtils.get_processes_info()
        if resource == "cpu":
            processes.sort(key=dh.sort_process_cpu)
        if resource == "ram":
            processes.sort(key=dh.sort_process_ram)
        if amount >= len(processes):
            return processes
        else:
            return processes[0:amount]

    @staticmethod
    def count_processes_by_name(name):
        return len(ProcessUtils.get_processes_by_name(name))

    @staticmethod
    def get_processes_by_name(name):
        processes = []
        for p in psutil.process_iter(attrs=['name']):
            if name in p.info['name']:
                processes.append(p)
        return processes
    
    @staticmethod
    def get_process_ports(p):
        return [dh.ntuple_to_dict(dh.ntuple_to_dict(conn)["laddr"])["port"] for conn in p.connections()]
