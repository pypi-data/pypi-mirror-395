#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# Harpia REST API Interface
#--------------------------------------------------------------------------
# Copyright (c) 2018 Light Conversion (UAB MGF "Šviesos konversija")
# All rights reserved.
# www.lightcon.com
#==========================================================================

from ..common import HTTP_methods

class CameraApp(HTTP_methods):
    """REST client of Camera App application"""
    silent = True
    connected = False
            
    def __init__ (self, ip_address, port=20080, version='v1'):
        self.url = 'http://{}:{}/{}/'.format(ip_address, port, version)
        if version == '':
            self.url = 'http://{}:{}/'.format(ip_address, port)
            
        self.connected = self._get('/') != {}
        if self.connected:
            print ('Camera App Service initialized at', self.url)

    #==============================================================================
    # /Basic
    #==============================================================================

    def get_beam_parameters(self):
        '''Returns beam parameters if beam profiler is enabled'''
        return self._get('/BeamProfiler/BeamParameters')
    
    def enable_beam_profiler(self):
        '''Enables beam profiler'''
        self._put('/BeamProfiler/IsEnabled', '1')

    def disable_beam_profiler(self):
        '''Disables beam profiler'''
        self._put('/BeamProfiler/IsEnabled', '0')
        
    def get_beam_profiler_status(self):
        '''Returns whether beam profiler is enabled'''
        return self._get('/BeamProfiler/IsEnabled')
    
    def set_beam_profiler_mode(self, mode=['ISO','GAUSS'][0]):
        '''Sets beam profiler mode (ISO or GAUSSIAN)'''
        self._put('/BeamProfiler/Mode', mode)
        
    def get_beam_profiler_mode(self):
        '''Gets beam profiler mode (ISO or GAUSSIAN)'''
        return self._get('/BeamProfiler/Mode')
    
    def get_frame_id(self):
        '''Gets ID of the last frame'''
        return self._get('/Camera/FrameID')
        
    def get_camera_alldata(self):
        '''Gets all camera data'''
        return self._get('/Camera/AllData')            
    
    def get_camera_histogram(self):
        '''Gets histogram of the last frame'''
        return self._get('/Camera/Histogram')
    
    def get_camera_exposure(self):
        '''Get camera exposure'''
        return self._get('/Camera/Exposure')
    
    def set_camera_exposure(self, exposure_in_ms):
        '''Sets camera exposure in ms'''
        self._put('/Camera/Exposure', str(exposure_in_ms))
        
    def get_camera_serial_number(self):
        '''Gets serial number of the camera used'''
        return self._get('/Camera/SerialNumber')
    
    def get_camera_background(self):
        '''Gets background value, used for beam profiler'''
        return self._get('/Camera/Background')
    
    def set_camera_averaging(self, averaging):
        '''Enables/disables averaging'''
        self._put('/Camera/Averaging', str(averaging))
        
    def get_camera_averaging(self):
        '''Gets status of averaging'''
        return self._get('/Camera/Averaging')
    
    def set_camera_gain(self, gain):
        '''Sets camera gain value'''
        self._put('/Camera/Gain', str(gain))
        
    def get_camera_gain(self):
        '''Gets camera gain value'''
        return self._get('/Camera/Gain')
    
    def get_camera_pixel_size(self):
        '''Returns size of camera pixel in um'''
        return self._get('/Camera/PixelSize')
    
    def get_camera_sensor_information(self):
        '''Returns camera sensor information'''
        return self._get('/Camera/SensorInformation')