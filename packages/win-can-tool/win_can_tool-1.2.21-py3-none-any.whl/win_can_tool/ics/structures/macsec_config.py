# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum

from ics.structures.mac_sec_flags_t import *
from ics.structures.mac_sec_map_t import *
from ics.structures.mac_sec_rule_t import *
from ics.structures.mac_sec_sa_t import *
from ics.structures.mac_sec_sc_t import *
from ics.structures.mac_sec_sec_y_t import *


class macsec_config(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('flags', MACSecFlags_t),
        ('rule', MACSecRule_t * 2),
        ('map', MACSecMap_t * 2),
        ('secy', MACSecSecY_t * 2),
        ('sc', MACSecSc_t * 2),
        ('sa', MACSecSa_t * 4),
    ]


MACSEC_CONFIG_t = macsec_config
MACSEC_CONFIG = macsec_config

