#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""c2pcontrol - remote control of the CRONUS-2P optical parametric oscillator.

Copyright 2020-2025 Light Conversion
Contact: support@lightcon.com
"""
import json
import socket
from time import sleep
from urllib.error import URLError
from ..common._http_methods import HTTP_methods
from ..common._logging import init_logger


class C2PControl(HTTP_methods):
    """REST API interaction with CRONUS-2P REST Server."""

    silent = True
    connected = False
    logger = None
    type = 'cronus2p'

    def __init__(self, ip_address='127.0.0.1', port=35100, version='v0', wait_for_device=True):
        self.logger = init_logger('c2p', 'cronus_2p.log')

        # Set default socket timeout to 1 second. If the communication with the
        # CRONUS-2P has a latency even close to this remote control is not
        # going to work anyway.
        # Is no default is set then the timeout is governed by the OS network
        # stack and this seems to vary. In some cases connecting to the
        # CRONUS-2P takes 30 seconds to timeout, which is too long.

        socket.setdefaulttimeout(1)
        self.logger.info("Setting communication timeout to 1 second")

        self.url = 'http://{}:{}/{}/Cronus/'.format(
            ip_address, port, version)
        self.logger.info("Connecting to CRONUS-2P at {:s}:{:d}".format(
            ip_address, port))

        while True:
            try:
                status = self.get_status()
            except URLError as excp:
                if type(excp.reason) is TimeoutError:
                    self.logger.error("Timed out while trying to connect to CRONUS-2P")
                    if wait_for_device:
                        self.logger.info("Trying again in 3 seconds...")
                        sleep(3)
                    else:
                        break
                else:
                    self.logger.error("Error while trying to connect tot CRONUS-2P")
            except Exception as excp:
                self.logger.error("An unknown error has occurred. "
                                "Exception: {}".format(excp))

            if status and status.get('OK'):
                self.connected = True
                self.logger.info("Connection to CRONUS-2P established "
                                "at {}".format(self.url))
                break

    def __del__(self):
        self.logger.info("Stopping remote control")

    def get_status(self):
        return self._get('Status')

    def set_mode_run(self):
        self._put("ModeRun", '')

    def get_mode(self):
        return self._get("Mode")

    def get_pump_power(self):
        return float(self._get("PumpPower").get("Power"))*1E-3

    def _check_channel(self, channel=None):
        if channel is None:
            print("No channel specified")
            return False

        if channel < 1 or channel > 3:
            print("Channel must be 1 – 3")
            return False

        return True

    def _check_wavelength(self, channel=None, wavelength=None):
        rng = self.get_wavelength_range(channel)
        if wavelength < rng[0] or wavelength > rng[1]:
            print("Wavelenngth {:.1f} nm is out of range for Channel {:d} "
                  "({:.1f} - {:.1f})".format(
                        wavelength, channel, rng[0], rng[1]))
            return False
        return True

    def _check_gdd(self, channel=None, gdd=None):
        rng = self.get_current_gdd_range(channel)
        if gdd < rng[0] or gdd > rng[1]:
            print("GDD {:.1f} fs2 is out of range for Channel {:d} "
                  "({:.1f} - {:.1f})".format(gdd, channel, rng[0], rng[1]))
            return False
        return True

    def open_shutter(self, channel=None):
        if not self._check_channel(channel):
            return
        self._put("Ch{:d}".format(channel) + "/ShutterOpen", '')

    def close_shutter(self, channel=None):
        if not self._check_channel(channel):
            return
        self._put("Ch{:d}".format(channel) + "/ShutterClosed", '')

    def get_shutter_states(self):
        states = []
        for ch_id in [1,  2, 3]:
            states.append(self._get(f'Ch{ch_id}/Shutter').get('IsShutterOpen'))
                
        return states

    def get_wavelength(self, channel=None):
        if not self._check_channel(channel):
            return
        return float(self._get("Ch{:d}".format(channel) + "/Wavelength").get(
            "Wavelength"))

    def set_wavelength(self, channel=None, wavelength=None, verbose=True):
        if not self._check_channel(channel):
            return
        if not self._check_wavelength(channel, wavelength):
            return
        self._put("Ch{:d}".format(channel) + "/Wavelength",
                  json.dumps({'Wavelength': wavelength}))

    def get_wavelength_range(self, channel=None):
        if not self._check_channel(channel):
            return
        response = self._get("Ch{:d}".format(channel) + "/WavelengthRange")
        return [float(response.get('Min')), float(response.get('Max'))]

    def get_gdd(self, channel=None):
        if not self._check_channel(channel):
            return
        response = self._get("Ch{:d}".format(channel) + "/GDD")
        return float(response.get('GDD'))

    def set_gdd(self, channel=None, gdd=None):
        if not self._check_channel(channel):
            return
        if not self._check_gdd(channel, gdd):
            return
        self._put("Ch{:d}".format(channel) + "/GDD", json.dumps({'GDD': gdd}))

    def get_current_gdd_range(self, channel=None):
        if not self._check_channel(channel):
            return
        response = self._get("Ch{:d}".format(channel) + "/CurrentGDDRange")
        return [float(response.get('Min')), float(response.get('Max'))]

    def get_gdd_range(self, channel=None, wavelength=None):
        if not self._check_channel(channel):
            return
        if not self._check_wavelength(channel, wavelength):
            return
        response = self._report("Ch{:d}".format(channel) + "/GDDRange",
                                json.dumps({'Wavelength': wavelength}))
        return [float(response.get('Min')), float(response.get('Max'))]
