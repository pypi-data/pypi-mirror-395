# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum

from ics.structures.port_identity import *


class parent_ds_(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('parent_port_identity', port_identity),
        ('cumulative_rate_ratio', ctypes.c_int32),
        ('grandmaster_identity', ctypes.c_uint64),
        ('gm_clock_quality_clock_class', ctypes.c_uint8),
        ('gm_clock_quality_clock_accuracy', ctypes.c_uint8),
        ('gm_clock_quality_offset_scaled_log_variance', ctypes.c_uint16),
        ('gm_priority1', ctypes.c_uint8),
        ('gm_priority2', ctypes.c_uint8),
    ]


_parent_ds = parent_ds_

