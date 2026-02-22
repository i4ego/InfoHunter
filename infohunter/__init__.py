from . import modules
from . import _types 

def scan(types: list[modules.typing.Literal["os", "signals", "users", "cpu", "ram", "gpu", "disks", "network", "sensors"]]):
    scanresults = list()
    for scantype in types:
        if scantype=="os":scanresults.append(_types.os());           continue
        if scantype=="signals":scanresults.append(_types.signals()); continue
        if scantype=="users":scanresults.append(_types.users());     continue
        if scantype=="cpu":scanresults.append(_types.cpu());         continue
        if scantype=="ram":scanresults.append(_types.ram());         continue
        if scantype=="gpu":scanresults.append(_types.gpu());         continue
        if scantype=="disks":scanresults.append(_types.disks());     continue
        if scantype=="network":scanresults.append(_types.network()); continue
        if scantype=="sensors":scanresults.append(_types.sensors()); continue
    return scanresults