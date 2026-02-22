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
    def __init__(self,name: str, terminal: str | None = None, host: str | None = None, started: float | None = None): self.name = name; self.terminal = terminal; self.host = host; self.started = started
class users:
    def __init__(self):
        self.current: user = user(modules.getpass.getuser())
        self.active: list[user] = list()
        for usr in modules.psutil.users(): self.active.append(user(usr.name, usr.terminal, usr.host, usr.started))
        self.all: list[user] = list()
        for usr in modules.os.listdir(modules.pathlib.Path.home()/".."): self.all.append(user(usr))
    def __str__(self): return str(self.current)

class cpufreq:
    def __init__(self, current: float, min: float, max: float): self.current = current; self.min = min; self.max = max
class cpucount:
    def __init__(self, logical, physical): self.logical = logical; self.physical = physical
class cpu:
    def __init__(self):
        self.cpu = modules.platform.processor()
        freq = modules.psutil.cpu_freq()
        self.freq = cpufreq(freq.current, freq.min, freq.max)
        self.count = cpucount(modules.psutil.cpu_count(True), modules.psutil.cpu_count(False))
        self.boot_time = modules.psutil.boot_time()
        self.update()
    def update(self):
        self.percent = modules.psutil.cpu_percent()
        self.freq.current = modules.psutil.cpu_freq().current
        return self.percent
    def __str__(self):
        return f"{self.cpu} ({self.percent}% used)"

class ram:
    def __init__(self):
        self.update()
    def update(self):
        mem = modules.psutil.virtual_memory()
        self.total = mem.total
        self.avaliable = mem.available
        self.used = mem.used
        self.percent = mem.percent
        return self.percent
    def __str__(self):
        return f"{self.percent}% used"

class singlegpu:
    def __init__(self, name, id, uuid, load, memory: tuple[float, float, float]):
        self.name = name, self.id = id, self.uuid = uuid, self.load = load; memory_total = memory[0]; memory_used = memory[1]; memory_free = memory[2]
    def __str__(self):
        return self.name
class gpu:
    def __init__(self):
        self.gpus = list()
        self.update()
    def update(self):
        self.gpus.clear()
        gpus: list[modules.GPUtil.GPU] = modules.GPUtil.getGPUs()
        for gpu in gpus:
            self.gpus.append(singlegpu(gpu.name, gpu.id, gpu.uuid, gpu.load, (gpu.memoryTotal, gpu.memoryUsed, gpu.memoryFree)))
    def __str__(self):
        return "GPUs: "+(", ".join(str(self.gpus)))
    
class disk: 
    def __init__(self, device, mount, fs, size: tuple[float, float, float], percent):
        self.device = device; self.mount = mount; self.fs = fs; self.sizeTotal = size[0]; self.sizeUsed = size[1]; self.sizeFree = size[2]; self.percent = percent
    def __str__(self):
        return f"{self.device} ({self.mount})"
class disks:
    def __init__(self):
        self.disks: list[disk] = list()
        self.update()
    def update(self):
        disks = modules.psutil.disk_partitions(False)
        self.disks.clear()
        for iter_disk in disks:
            size = modules.psutil.disk_usage(iter_disk.device)
            self.disks.append(disk(iter_disk.device, iter_disk.mountpoint, iter_disk.fstype, (size.total, size.used, size.free), size.percent))

class network:
    def __init__(self):
        self.mac = modules.getnode()
        self.update()
    def update(self):
        self.host = modules.socket.gethostname()
        self.localIP = modules.socket.gethostbyname(self.host)
        try: ipinfo = modules.json.loads(modules.requests.get("http://ipinfo.io/json").text)
        except modules.requests.exceptions.ConnectionError: self.ipinfo = None
        self.publicIP = None; self.country = None; self.region = None; self.city = None; self.postalcode = None; self.timezone = None
        if not ipinfo is None:
            self.publicIP = ipinfo["ip"]
            self.country = ipinfo["country"]
            self.region = ipinfo["region"]
            self.city = ipinfo["city"]
            self.postalcode = ipinfo["postal"]
            self.timezone = ipinfo["timezone"]
    def __str__(self):
        return f"Host: {self.host}; Local IP: {self.localIP}; {self.publicIP if not self.publicIP is None else ""}"

class battery: 
    def __init__(self, percent, plugged, secsleft):
        self.percent = percent; self.plugged = plugged; self.secsleft = secsleft
    def __str__(self):
        return f"{self.percent}%; {"Battery is charging" if self.plugged else "Battery is not charging"}; Seconds to discharge: {self.secsleft}"
class sensors: 
    def __init__(self):
        self.update()
    def update(self):
        s_battery = modules.psutil.sensors_battery()
        self.battery = battery(s_battery.percent, s_battery.power_plugged, s_battery.secsleft)