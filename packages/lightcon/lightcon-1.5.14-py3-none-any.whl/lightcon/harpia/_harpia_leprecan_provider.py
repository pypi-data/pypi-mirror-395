#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# 
#--------------------------------------------------------------------------
# Copyright (c) 2022 Light Conversion, UAB
# All rights reserved.
# www.lightcon.com
#==========================================================================
import numpy as np
from lightcon.common._leprecan_provider import LepreCanProvider, FrameType
from lightcon.common._converters import int_to_float, bytes_array_to_int, float_to_hex, bytes_array_to_float

class HarpiaLepreCanProvider(LepreCanProvider):
    def __init__(self, harpia):
        supplier = HarpiaLepreCanSuplier(harpia)
        LepreCanProvider.__init__(self, supplier)

class HarpiaLepreCanSuplier:
    harpia = None
    received_bytes = []

    def __init__ (self, _harpia):
        self.harpia = _harpia

    def send(self, can_id, data8bytes):
        frame_type = can_id % 8
        base_id = can_id - frame_type
        bytes_string = ''.join(['{0:0{1}x}'.format(b,2) for b in data8bytes])

        if frame_type == int(FrameType.GetRegisterCommandFrame):
            self.get_register(base_id, bytes_string)

        if frame_type == int(FrameType.SetRegisterCommandFrame):
            self.set_register(base_id, bytes_string)

    def receive(self):
        return self.received_bytes
        
    def set_register(self, base_id, data8bytes):
        response = self.harpia._get('Advanced/SetCanRegister/{:}/{:}'.format(base_id, data8bytes))
        self.handle_response(response)
        return response
        
    def get_register(self, base_id, data8bytes):
        response = self.harpia._get('Advanced/GetCanRegister/{:}/{:}'.format(base_id, data8bytes))
        self.handle_response(response)
        return response

    def handle_response(self, response):
        self.received_bytes = self.parse_bytes_from_response(response)

    def parse_bytes_from_response(self, response):
        data8bytes = [int('0x'+response[i:i+2], 16) for i in np.arange(0, len(response),2)]
        return data8bytes
    
    def bytes_to_string(self, bytes):
        return ''.join([s])

