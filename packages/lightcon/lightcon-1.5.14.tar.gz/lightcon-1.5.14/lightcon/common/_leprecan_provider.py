#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# 
#--------------------------------------------------------------------------
# Copyright (c) 2022 Light Conversion, UAB
# All rights reserved.
# www.lightcon.com
#==========================================================================
import numpy
from enum import Enum, IntEnum
import time
import struct
from lightcon.common._converters import int_to_float, bytes_array_to_int, float_to_hex, bytes_array_to_float

from collections import deque
from threading import Lock        

class LepreCanProvider:    
    mutex = Lock()
    
    def __init__ (self, leprecan_supplier):
        self.leprecan_supplier = leprecan_supplier
    
    def GetRegister(self, baseId, register, index, flags=0x00):
        can_id = self.GenerateMessageId(baseId, FrameType.GetRegisterCommandFrame)
        
        data = self.GenerateDataFrame(frameType = FrameType.GetRegisterCommandFrame, 
                                  registerAddress = register,
                                  index = index or 0x00, 
                                  flags = 0x00, 
                                  data4bytes=0x00000000)
        
        self.mutex.acquire()
        self.leprecan_supplier.send(can_id, data)
        recv = self.leprecan_supplier.receive()
        self.mutex.release()
        
        return (recv[3], recv[4:])
    
    def SetRegister(self, baseId, register, index, data4bytes, flags=0x00):
        can_id = self.GenerateMessageId(baseId, FrameType.SetRegisterCommandFrame)
        
        data = self.GenerateDataFrame(frameType = FrameType.SetRegisterCommandFrame, 
                                  registerAddress = register,
                                  index = index or 0x00, 
                                  flags = 0x00, 
                                  data4bytes=data4bytes)
        
        self.mutex.acquire()
        self.leprecan_supplier.send(can_id, data)
        recv = self.leprecan_supplier.receive()
        self.mutex.release()
                
        return (recv[3], recv[4:])
        
    def SetRegisterAsync(self, baseId, register, index, data4bytes, flags=0x00):
        can_id = self.GenerateMessageId(baseId, FrameType.SetRegisterCommandFrame)
        
        data = self.GenerateDataFrame(frameType = FrameType.SetRegisterCommandFrame, 
                                  registerAddress = register,
                                  index = index or 0x00, 
                                  flags = 0x00, 
                                  data4bytes=data4bytes)
             
        self.mutex.acquire()
        self.leprecan_supplier.send(can_id, data)
        self.mutex.release()
                
        return (0, 0)
    
    def IterateCrc8Byte(self, seed, newByte):
        data = numpy.uint8(seed ^ newByte);
        for i in range(8):
            if ((data & 0x80) != 0):
                data <<= 1;
                data ^= 0x07;
            else:
                data <<= 1;    
        return numpy.uint8(data);
    
    def PrepareFrame(self, data):
        indexes = [0, 1, 2, 4, 5, 6, 7]
        
        crc = self.IterateCrc8Byte (0xff, data[0]);    
        
        for index in indexes[1:]:
            crc = self.IterateCrc8Byte (crc, data[index])
            
        data[3] = crc;
        return data
        
    def GetDataString (self, data):
        return ' '.join(["{0:#0{1}x}".format(cell,4)[2:] for cell in data])
        
    def GenerateMessageId (self, baseId, frameType):
        return baseId + frameType.value
    
    def GenerateDataFrame (self, frameType, registerAddress, index, flags=0x00, data4bytes=0x00000000):
        data = [0] * 8
                   
        
        if (frameType == FrameType.GetRegisterCommandFrame):
            data = self.PrepareFrame([
                    registerAddress & 0x00ff,
                    (registerAddress & 0xff00) >> 8,
                    index,
                    0x00, # will be replaced by crc
                    data4bytes & 0x000000ff,
                    (data4bytes & 0x0000ff00) >> 8,
                    (data4bytes & 0x00ff0000) >> 16,
                    (data4bytes & 0xff000000) >> 24
                    ]);     
        
        if (frameType == FrameType.SetRegisterCommandFrame):
            data = self.PrepareFrame([
                    registerAddress & 0x00ff,
                    (registerAddress & 0xff00) >> 8,
                    index,
                    0x00, # will be replaced by crc
                    data4bytes & 0x000000ff,
                    (data4bytes & 0x0000ff00) >> 8,
                    (data4bytes & 0x00ff0000) >> 16,
                    (data4bytes & 0xff000000) >> 24
                    ]);   
        return data
        
class FrameType(IntEnum):
    BroadcastFrame = 0
    SetRegisterResponseFrame = 1
    GetRegisterResponseFrame = 2
    OutgoingIfuFrame = 3
    SetRegisterCommandFrame = 5
    GetRegisterCommandFrame = 6
    IncomingRawFrame = 7
    Invalid = 255
    
class ResponseStatus(IntEnum) :
    Success =                   0x00,
    UnsupportedCommand =        0x01,
    InvalidRegisterAddress =    0x02,
    InvalidIndex =              0x03,
    TypeError =                 0x04,
    DecryptionFailed =          0x05,
    InsufficientAccessLevel =   0x08,
    UnknownError2 =              0xef,
    UnknownError =              0xff
