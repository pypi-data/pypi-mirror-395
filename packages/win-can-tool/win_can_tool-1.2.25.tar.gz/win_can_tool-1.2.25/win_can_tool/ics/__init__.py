# Warning: This file is auto generated. Don't modify if you value your sanity!
try:
    import ics.__version
    __version__ = ics.__version.__version__
    __full_version__ = ics.__version.__full_version__
except Exception as ex:
    print(ex)


from ics.structures import *
from ics.structures.neo_device import NeoDevice, neo_device
from ics.hiddenimports import hidden_imports
try:
    from ics.py_neo_device_ex import PyNeoDeviceEx
except ModuleNotFoundError as ex:
    print(f"Warning: {ex}")

try:
    # Release environment
    #print("Release")
    from ics.ics import *
except Exception as ex:
    # Build environment
    #print("Debug", ex)
    from ics import *
