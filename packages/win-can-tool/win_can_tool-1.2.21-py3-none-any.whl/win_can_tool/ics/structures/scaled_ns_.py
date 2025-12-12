# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum



class scaled_ns_(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('nanoseconds_msb', ctypes.c_int16),
        ('nanoseconds_lsb', ctypes.c_int64),
        ('fractional_nanoseconds', ctypes.c_int16),
    ]


_scaled_ns = scaled_ns_

