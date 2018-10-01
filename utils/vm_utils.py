import subprocess
from utils.process_utils import ProcessUtils

class VMUtils:
    
    #  TODO - Check hardcoded value
    VBOXMANAGE = "C:/Program Files/Oracle/VirtualBox/VBoxManage"

    # TODO - Check process name
    VBOX_PROCESS = "VBoxHeadless.exe"

    def get_vms(self, running=True):
        result = subprocess.check_output([self.VBOXMANAGE, 
                                          "list",
                                          "runningvms" if running else "vms"]
                                        ).decode().strip()
        if result:
            return len(result.split("\r\n"))
        else:
            return 0

    def get_vbox_status(self):
        for p in ProcessUtils.get_processes_by_name(self.VBOX_PROCESS):
            if p.status() != "running":
                return 0
        return 1
