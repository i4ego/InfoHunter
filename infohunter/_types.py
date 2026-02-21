from . import modules

class os:
    def __init__(self):
        os = modules.platform.uname()
        self.fullname = f"{os.system} {os.release} ({os.version} {os.machine.upper()})"
        self.name = f"{os.system} {os.release}"
        self.l_name = os.system
        self.arch = os.machine
        self.platform = modules.sys.platform
    def __str__(self):
        return self.fullname
    
class signals:
    def __init__(self):
        self.raw_signals = list()
        for signum in modules.signal.valid_signals(): self.raw_signals.append(signum.value)
        self.signals = list()
        for signum in self.raw_signals: self.signals.append(modules.signal.strsignal(signum))
    def __str__(self):
        return ", ".join(self.signals)