# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum



class Nameless11656(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('index', ctypes.c_uint8),
        ('sak', ctypes.c_uint8 * 32),
        ('hashKey', ctypes.c_uint8 * 16),
        ('salt', ctypes.c_uint8 * 12),
        ('ssci', ctypes.c_uint32),
        ('AN', ctypes.c_uint8),
        ('nextPN', ctypes.c_uint64),
        ('rsvd', ctypes.c_uint8 * 5),
        ('enable', ctypes.c_uint8),
    ]



class mac_sec_sa_t(ctypes.Union):
    _pack_ = 1
    _anonymous_  = ('Nameless11656',)
    _fields_ = [
        ('Nameless11656', Nameless11656),
        ('byte', ctypes.c_uint8 * 80),
    ]


_MACSecSa = mac_sec_sa_t
MACSecSa_t = mac_sec_sa_t

