# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum

from ics.structures.ethernet10_t1_s_settings import *
from ics.structures.ethernet10_t1_s_settings_ext import *
from ics.structures.ethernet_settings2 import *
from ics.structures.op_eth_general_settings import *
from ics.structures.rad_reporting_settings import *
from ics.structures.srad_gptp_settings_s import *


class flags(ctypes.Structure):
    _pack_ = 2
    _fields_ = [
        ('hwComLatencyTestEn', ctypes.c_uint16, 1),
        ('disableUsbCheckOnBoot', ctypes.c_uint16, 1),
        ('reserved', ctypes.c_uint16, 14),
    ]



class srad_moon_t1_s_settings(ctypes.Structure):
    _pack_ = 2
    _fields_ = [
        ('perf_en', ctypes.c_uint16),
        ('flags', flags),
        ('network_enabled_on_boot', ctypes.c_uint16),
        ('network_enables', ctypes.c_uint64),
        ('network_enables_2', ctypes.c_uint64),
        ('reporting', RAD_REPORTING_SETTINGS),
        ('pwr_man_timeout', ctypes.c_uint32),
        ('pwr_man_enable', ctypes.c_uint16),
        ('ethernet', ETHERNET_SETTINGS2),
        ('opEthGen', OP_ETH_GENERAL_SETTINGS),
        ('ethT1s', ETHERNET_SETTINGS2),
        ('t1s', ETHERNET10T1S_SETTINGS),
        ('t1sExt', ETHERNET10T1S_SETTINGS_EXT),
        ('gPTP', RAD_GPTP_SETTINGS),
    ]


_SRADMoonT1SSettings = srad_moon_t1_s_settings
SRADMoonT1SSettings = srad_moon_t1_s_settings

