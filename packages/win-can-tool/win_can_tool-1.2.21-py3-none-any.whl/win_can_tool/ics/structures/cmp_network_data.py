# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum



class Nameless43713(ctypes.Structure):
    _pack_ = 2
    _fields_ = [
        ('network_enables', ctypes.c_uint16),
        ('network_enables_2', ctypes.c_uint16),
        ('network_enables_3', ctypes.c_uint16),
        ('network_enables_4', ctypes.c_uint16),
    ]



class network_enables(ctypes.Union):
    _pack_ = 2
    _anonymous_  = ('Nameless43713',)
    _fields_ = [
        ('word', ctypes.c_uint64),
        ('Nameless43713', Nameless43713),
    ]



class cmp_network_data(ctypes.Structure):
    _pack_ = 2
    _fields_ = [
        ('bStreamEnabled', ctypes.c_uint8, 1),
        ('EthModule', ctypes.c_uint8, 2),
        ('bControlEnabled', ctypes.c_uint8, 1),
        ('spare', ctypes.c_uint8, 4),
        ('streamId', ctypes.c_uint8),
        ('dstMac', ctypes.c_uint8 * 6),
        ('network_enables', network_enables),
        ('network_enables_2', ctypes.c_uint64),
    ]


CMP_NETWORK_DATA = cmp_network_data

