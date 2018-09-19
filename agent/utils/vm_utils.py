import virtualbox


class VMUtils:

    VBOX = virtualbox.VirtualBox()

    def get_vms(self):
        return [vm.name for vm in self.VBOX.machines]
