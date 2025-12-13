# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum



class cmp_global_data(ctypes.Structure):
    _pack_ = 2
    _fields_ = [
        ('cmp_enabled', ctypes.c_uint8, 1),
        ('sparebits', ctypes.c_uint8, 7),
        ('spare', ctypes.c_uint8),
        ('cmp_device_id', ctypes.c_uint16),
    ]


CMP_GLOBAL_DATA = cmp_global_data

