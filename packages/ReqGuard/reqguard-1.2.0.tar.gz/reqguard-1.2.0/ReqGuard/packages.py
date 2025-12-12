import sys

from .compat import chardet

for package in ("urllib3", "idna"):
    locals()[package] = __import__(package)
    for mod in list(sys.modules):
        if mod == package or mod.startswith("{0}.".format(package)):
            sys.modules["requests.packages.{0}".format(mod)] = sys.modules[mod]

if chardet is not None:
    target = chardet.__name__
    for mod in list(sys.modules):
        if mod == target or mod.startswith("{0}.".format(target)):
            imported_mod = sys.modules[mod]
            sys.modules["requests.packages.{0}".format(mod)] = imported_mod
            mod = mod.replace(target, "chardet")
            sys.modules["requests.packages.{0}".format(mod)] = imported_mod
