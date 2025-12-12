# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum

from ics.structures.scaled_ns_ import *


class current_ds_(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('steps_removed', ctypes.c_uint16),
        ('offset_from_master', ctypes.c_int64),
        ('last_gm_phase_change', scaled_ns_),
        ('last_gm_freq_change', ctypes.c_double),
        ('gm_time_base_indicator', ctypes.c_uint16),
        ('gm_change_count', ctypes.c_uint32),
        ('time_of_last_gm_change_event', ctypes.c_uint32),
        ('time_of_last_gm_phase_change_event', ctypes.c_uint32),
        ('time_of_last_gm_freq_change_event', ctypes.c_uint32),
    ]


_current_ds = current_ds_

