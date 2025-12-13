# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum

from ics.structures.can_settings import *
from ics.structures.canfd_settings import *
from ics.structures.ethernet10_t1_s_settings import *
from ics.structures.ethernet10_t1_s_settings_ext import *
from ics.structures.ethernet_settings2 import *
from ics.structures.iso9141_keyword2000_settings import *
from ics.structures.lin_settings import *
from ics.structures.op_eth_general_settings import *
from ics.structures.op_eth_settings import *
from ics.structures.rad_reporting_settings import *
from ics.structures.s_text_api_settings import *
from ics.structures.srad_gptp_settings_s import *
from ics.structures.timesync_icshardware_settings import *


class flags(ctypes.Structure):
    _pack_ = 2
    _fields_ = [
        ('hwComLatencyTestEn', ctypes.c_uint16, 1),
        ('disableUsbCheckOnBoot', ctypes.c_uint16, 1),
        ('reserved', ctypes.c_uint16, 14),
    ]



class srad_comet3_settings(ctypes.Structure):
    _pack_ = 2
    _fields_ = [
        ('ecu_id', ctypes.c_uint32),
        ('perf_en', ctypes.c_uint16),
        ('flags', flags),
        ('network_enabled_on_boot', ctypes.c_uint16),
        ('can1', CAN_SETTINGS),
        ('canfd1', CANFD_SETTINGS),
        ('can2', CAN_SETTINGS),
        ('canfd2', CANFD_SETTINGS),
        ('iso9141_kwp_settings_1', ISO9141_KEYWORD2000_SETTINGS),
        ('iso_parity_1', ctypes.c_uint16),
        ('iso_msg_termination_1', ctypes.c_uint16),
        ('network_enables', ctypes.c_uint64),
        ('network_enables_2', ctypes.c_uint64),
        ('termination_enables', ctypes.c_uint64),
        ('timeSyncSettings', TIMESYNC_ICSHARDWARE_SETTINGS),
        ('reporting', RAD_REPORTING_SETTINGS),
        ('iso15765_separation_time_offset', ctypes.c_int16),
        ('pwr_man_timeout', ctypes.c_uint32),
        ('pwr_man_enable', ctypes.c_uint16),
        ('gPTP', RAD_GPTP_SETTINGS),
        ('text_api', STextAPISettings),
        ('ethernet', ETHERNET_SETTINGS2),
        ('opEthGen', OP_ETH_GENERAL_SETTINGS),
        ('ethT1', ETHERNET_SETTINGS2),
        ('opEth1', OP_ETH_SETTINGS),
        ('ethT1s1', ETHERNET_SETTINGS2),
        ('t1s1', ETHERNET10T1S_SETTINGS),
        ('ethT1s2', ETHERNET_SETTINGS2),
        ('t1s2', ETHERNET10T1S_SETTINGS),
        ('ethT1s3', ETHERNET_SETTINGS2),
        ('t1s3', ETHERNET10T1S_SETTINGS),
        ('ethT1s4', ETHERNET_SETTINGS2),
        ('t1s4', ETHERNET10T1S_SETTINGS),
        ('ethT1s5', ETHERNET_SETTINGS2),
        ('t1s5', ETHERNET10T1S_SETTINGS),
        ('ethT1s6', ETHERNET_SETTINGS2),
        ('t1s6', ETHERNET10T1S_SETTINGS),
        ('lin1', LIN_SETTINGS),
        ('t1s1Ext', ETHERNET10T1S_SETTINGS_EXT),
        ('t1s2Ext', ETHERNET10T1S_SETTINGS_EXT),
        ('t1s3Ext', ETHERNET10T1S_SETTINGS_EXT),
        ('t1s4Ext', ETHERNET10T1S_SETTINGS_EXT),
        ('t1s5Ext', ETHERNET10T1S_SETTINGS_EXT),
        ('t1s6Ext', ETHERNET10T1S_SETTINGS_EXT),
    ]


_SRADComet3Settings = srad_comet3_settings
SRADComet3Settings = srad_comet3_settings

