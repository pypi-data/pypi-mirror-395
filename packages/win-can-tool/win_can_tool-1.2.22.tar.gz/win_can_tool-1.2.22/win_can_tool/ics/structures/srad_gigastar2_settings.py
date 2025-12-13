# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum

from ics.structures.can_settings import *
from ics.structures.canfd_settings import *
from ics.structures.disk_settings import *
from ics.structures.ethernet10_t1_s_settings import *
from ics.structures.ethernet10_t1_s_settings_ext import *
from ics.structures.ethernet_settings2 import *
from ics.structures.iso9141_keyword2000_settings import *
from ics.structures.lin_settings import *
from ics.structures.logger_settings import *
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



class srad_gigastar2_settings(ctypes.Structure):
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
        ('can3', CAN_SETTINGS),
        ('canfd3', CANFD_SETTINGS),
        ('can4', CAN_SETTINGS),
        ('canfd4', CANFD_SETTINGS),
        ('iso9141_kwp_settings_1', ISO9141_KEYWORD2000_SETTINGS),
        ('iso_parity_1', ctypes.c_uint16),
        ('iso_msg_termination_1', ctypes.c_uint16),
        ('iso9141_kwp_settings_2', ISO9141_KEYWORD2000_SETTINGS),
        ('iso_parity_2', ctypes.c_uint16),
        ('iso_msg_termination_2', ctypes.c_uint16),
        ('iso9141_kwp_settings_3', ISO9141_KEYWORD2000_SETTINGS),
        ('iso_parity_3', ctypes.c_uint16),
        ('iso_msg_termination_3', ctypes.c_uint16),
        ('iso9141_kwp_settings_4', ISO9141_KEYWORD2000_SETTINGS),
        ('iso_parity_4', ctypes.c_uint16),
        ('iso_msg_termination_4', ctypes.c_uint16),
        ('iso9141_kwp_settings_5', ISO9141_KEYWORD2000_SETTINGS),
        ('iso_parity_5', ctypes.c_uint16),
        ('iso_msg_termination_5', ctypes.c_uint16),
        ('iso9141_kwp_settings_6', ISO9141_KEYWORD2000_SETTINGS),
        ('iso_parity_6', ctypes.c_uint16),
        ('iso_msg_termination_6', ctypes.c_uint16),
        ('iso9141_kwp_settings_7', ISO9141_KEYWORD2000_SETTINGS),
        ('iso_parity_7', ctypes.c_uint16),
        ('iso_msg_termination_7', ctypes.c_uint16),
        ('iso9141_kwp_settings_8', ISO9141_KEYWORD2000_SETTINGS),
        ('iso_parity_8', ctypes.c_uint16),
        ('iso_msg_termination_8', ctypes.c_uint16),
        ('iso9141_kwp_settings_9', ISO9141_KEYWORD2000_SETTINGS),
        ('iso_parity_9', ctypes.c_uint16),
        ('iso_msg_termination_9', ctypes.c_uint16),
        ('iso9141_kwp_settings_10', ISO9141_KEYWORD2000_SETTINGS),
        ('iso_parity_10', ctypes.c_uint16),
        ('iso_msg_termination_10', ctypes.c_uint16),
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
        ('disk', DISK_SETTINGS),
        ('logger', LOGGER_SETTINGS),
        ('lin1', LIN_SETTINGS),
        ('lin2', LIN_SETTINGS),
        ('lin3', LIN_SETTINGS),
        ('lin4', LIN_SETTINGS),
        ('lin5', LIN_SETTINGS),
        ('lin6', LIN_SETTINGS),
        ('lin7', LIN_SETTINGS),
        ('lin8', LIN_SETTINGS),
        ('lin9', LIN_SETTINGS),
        ('lin10', LIN_SETTINGS),
        ('ethernet1', ETHERNET_SETTINGS2),
        ('ethernet2', ETHERNET_SETTINGS2),
        ('opEthGen', OP_ETH_GENERAL_SETTINGS),
        ('ethT1', ETHERNET_SETTINGS2),
        ('opEth1', OP_ETH_SETTINGS),
        ('ethT12', ETHERNET_SETTINGS2),
        ('opEth2', OP_ETH_SETTINGS),
        ('ethT1s1', ETHERNET_SETTINGS2),
        ('t1s1', ETHERNET10T1S_SETTINGS),
        ('t1s1Ext', ETHERNET10T1S_SETTINGS_EXT),
        ('ethT1s2', ETHERNET_SETTINGS2),
        ('t1s2', ETHERNET10T1S_SETTINGS),
        ('t1s2Ext', ETHERNET10T1S_SETTINGS_EXT),
        ('ethT1s3', ETHERNET_SETTINGS2),
        ('t1s3', ETHERNET10T1S_SETTINGS),
        ('t1s3Ext', ETHERNET10T1S_SETTINGS_EXT),
        ('ethT1s4', ETHERNET_SETTINGS2),
        ('t1s4', ETHERNET10T1S_SETTINGS),
        ('t1s4Ext', ETHERNET10T1S_SETTINGS_EXT),
        ('ethT1s5', ETHERNET_SETTINGS2),
        ('t1s5', ETHERNET10T1S_SETTINGS),
        ('t1s5Ext', ETHERNET10T1S_SETTINGS_EXT),
        ('ethT1s6', ETHERNET_SETTINGS2),
        ('t1s6', ETHERNET10T1S_SETTINGS),
        ('t1s6Ext', ETHERNET10T1S_SETTINGS_EXT),
        ('ethT1s7', ETHERNET_SETTINGS2),
        ('t1s7', ETHERNET10T1S_SETTINGS),
        ('t1s7Ext', ETHERNET10T1S_SETTINGS_EXT),
        ('ethT1s8', ETHERNET_SETTINGS2),
        ('t1s8', ETHERNET10T1S_SETTINGS),
        ('t1s8Ext', ETHERNET10T1S_SETTINGS_EXT),
    ]


_SRADGigaStar2Settings = srad_gigastar2_settings
SRADGigastar2Settings = srad_gigastar2_settings

