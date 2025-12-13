#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""remote_spectrometer - remote control API of Light Conversion spectraLight devices.

Copyright 2019-2024 Light Conversion
Contact: support@lightcon.com
"""
from lightcon.common import HTTP_methods

class RemoteSpectrometer(HTTP_methods):
    silent = True
    connected = False
            
    def __init__ (self, ip_address, port=54368, version='V2'):
        self.url = 'http://{}:{}/{}/'.format(ip_address, port, version)
        if version == '':
            self.url = 'http://{}:{}/'.format(ip_address, port)
            
        self.connected = self._get('/Info') != {}
        if self.connected:
            print ('Remote spectrometer initialized at', self.url)
            
    def get_info (self):
        return self._get('/Info')
    
    def get_raw_spectrum (self):
        return self._get('/RawSpectrum')
    
    def get_counts_spectrum (self):
        return self._get('/CountsSpectrum')
    
    def get_power_spectrum (self):
        return self._get('/PowerSpectrum')
    
    def get_integration_time (self):
        return self._get('/IntegrationTimeUs')
    
    def set_integration_time(self, integration_time_us):
        self._put('/IntegrationTimeUs', str(integration_time_us))
    