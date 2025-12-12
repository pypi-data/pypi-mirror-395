# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum



class ethernet10_t1_s_settings_ext(ctypes.Structure):
    _pack_ = 2
    _fields_ = [
        ('enable_multi_id', ctypes.c_uint8),
        ('multi_id', ctypes.c_uint8 * 7),
        ('rsvd', ctypes.c_uint8 * 8),
    ]


ETHERNET10T1S_SETTINGS_EXT_t = ethernet10_t1_s_settings_ext
ETHERNET10T1S_SETTINGS_EXT = ethernet10_t1_s_settings_ext

