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

class EthMotorBoardLepreCanProvider(LepreCanProvider):
    def __init__(self, emb):
        supplier = EthMotorBoardLepreCanSupplier(emb)
        LepreCanProvider.__init__(self, supplier)

class EthMotorBoardLepreCanSupplier:
    def __init__(self, emb):
        self.emb = emb

    def send(self, base_id, data):
        msb = (int.from_bytes(data, 'big') & 0xffffffff00000000) >> 32
        lsb = int.from_bytes(data, 'big') & 0xffffffff
        message = "CAN_TRANSMIT {:} {:} {:}\r\n".format(base_id,  msb, lsb)
        # print ('>', base_id, data)
        self.received = self.emb.send(message)

    def receive(self):
        if (self.received):
            recv_array = [int(item) for item in self.received.split(' ')]
            base_id = recv_array[0]
            msb = recv_array[1]
            lsb = recv_array[2]
            bytes_array = [(msb >> 24) & 0xff,
                           (msb >> 16) & 0xff,
                           (msb >>  8) & 0xff,
                           (msb >>  0) & 0xff,
                           (lsb >> 24) & 0xff,
                           (lsb >> 16) & 0xff,
                           (lsb >>  8) & 0xff,
                           (lsb >>  0) & 0xff
                           ]
            # print('<', base_id, bytes_array)
            return bytes_array
