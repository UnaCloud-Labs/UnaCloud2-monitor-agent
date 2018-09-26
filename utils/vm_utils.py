import subprocess

class VMUtils:
    
    #  TODO - Check hardcoded value
    VBOXMANAGE = "C:/Program Files/Oracle/VirtualBox/VBoxManage"

    def get_vms(self, running=True):
        result = subprocess.check_output([self.VBOXMANAGE, 
                                          "list",
                                          "runningvms" if running else "vms"]
                                        ).decode().strip()
        if result:
            return len(result.split("\r\n"))
        else:
            return 0
