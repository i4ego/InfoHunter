from . import modules

class os:
    def __init__(self, os: modules.platform.uname_result):
        self.fullname = f"{os.system} {os.release} ({os.version} {os.machine.upper()})"
        self.name = f"{os.system} {os.release}"
        self.l_name = os.system
        self.arch = os.machine
        self.platform = modules.sys.platform
    def __str__(self):
        return self.fullname