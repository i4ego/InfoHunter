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

class user:
    def __init__(self,name: str, terminal: str | None = None, host: str | None = None, started: float | None = None): 
        self.name = name; self.terminal = terminal; self.host = host; self.started = started
    def __str__(self): return self.name
class users:
    def __init__(self):
        self.current: user = user(modules.getpass.getuser())
        self.active: list[user] = list()
        for usr in modules.psutil.users(): self.active.append(user(usr.name, usr.terminal, usr.host, usr.started))
        self.all: list[user] = list()
        for usr in modules.os.listdir(modules.pathlib.Path.home()/".."): self.all.append(user(usr))
    def __str__(self): return str(self.current)