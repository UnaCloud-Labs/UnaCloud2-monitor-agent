import subprocess

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

    def get_vbox_processes(self):
        processes = subprocess.check_output(["tasklist"]).decode().strip().split("\r\n")
        return len(processes)