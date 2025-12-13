#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# 
#--------------------------------------------------------------------------
# Copyright (c) 2022 Light Conversion, UAB
# All rights reserved.
# www.lightcon.com
#==========================================================================
import struct

def float_to_hex(f):
    return int(struct.unpack('<I', struct.pack('<f', f))[0])

def hex_to_float(f):
    return float(struct.unpack('<f', struct.pack('<I', f))[0])

def int_to_float(i):
    return float(struct.unpack('<f', struct.pack('<I', i))[0])

def bytes_array_to_int (data):
    result = 0
 
    for i, val in enumerate(data):
        result = result + (val << (i * 8))
                                 
    return result

def bytes_array_to_float (data):
    i = bytes_array_to_int(data)
    return int_to_float(i)