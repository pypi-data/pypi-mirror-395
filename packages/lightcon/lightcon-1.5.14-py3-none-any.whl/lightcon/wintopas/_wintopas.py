# -*- coding: utf-8 -*-
"""topascontrol - remote control of Topas4-based optical parametric amplifiers.

Copyright 2020-2024 Light Conversion
Contact: support@lightcon.com
"""
import json
from ..common import HTTP_methods
from ..common._logging import init_logger

class WinTopas(HTTP_methods):
    """REST API interaction with Topas Server."""
    silent = True
    connected = False
    type = 'topas'

    def __init__(
            self, ip_address, port=8000, dev_sn=None, version='v0', **kwargs):
        """Initialization."""
        self.logger = init_logger('topas', 'topas.log')
        self.url = 'http://{}:{}/{}/{}/PublicAPI/'.format(
            ip_address, port, dev_sn, version)
        self.logger.info("Connecting to TOPAS device SN {:s} at {:s}:{:d}".format(
            dev_sn, ip_address, port))
        try:
            self.connected = self._open('Motors/help').find('AllProperties') != -1
        except Exception as excpt:
            self.logger.error(
                "Could not connect to Topas server. Make sure the IP address, "
                "the REST port and the device SN are correct, the host is "
                "reachable, and that the Topas4 server is running with  admin "
                "privileges. Exception reason: %s", excpt)
            self.connected = False

        if self.connected:
            self.logger.info("Topas control at %s established", self.url)

    def __del__(self):
        self.logger.info("Stopping remote Topas control")

    def set_motor_pos(self, index, pos, verbose=False, **kwargs):
        self.set_motor_target_pos(index, pos, **kwargs)

    def set_motor_target_pos(self, index, pos, verbose=False, **kwargs):
        if verbose:
            print("Setting motor {:d} to position {:.3f}".format(index, pos))

        self._put('Motors/TargetPosition?id={:d}'.format(index), str(pos), **kwargs)

    def get_motor_pos(self, index, **kwargs):
        return self.get_motor_actual_pos(index, **kwargs)

    def get_motor_actual_pos(self, index, **kwargs):
        return self._get('Motors/ActualPosition?id={:d}'.format(index), **kwargs)

    def get_motor_target_pos(self, index, **kwargs):
        return self._get('Motors/TargetPosition?id={:d}'.format(index), **kwargs)

    def get_wavelength(self):
        """Get wavelength in nm."""
        return self._get('Optical/WavelengthControl/Output/Wavelength')

    def set_wavelength(self, wavl, **kwargs):
        """Set wavelength in nm."""
        # return self._put(
        #     'Optical/WavelengthControl/SetWavelengthUsingAnyInteraction',
        #     json.dumps(float(wavl)))
        return self._put(
            'Optical/WavelengthControl/SetWavelength',
            json.dumps({"Interaction": "SIG", "Wavelength": float(wavl), "IgnoreSeparation": True}))

    def open_all_shutters(self, **kwargs):
        return self._put('/ShutterInterlock/OpenCloseShutter',  json.dumps('true'))

    def close_all_shutters(self, **kwargs):
        return self._put('/ShutterInterlock/OpenCloseShutter',  json.dumps('false'))

    def get_optical_system_data(self):
        return self._get(r'/Optical/WavelengthControl/OpticalSystemData')

    def get_output(self):
        return self._get(r'/Optical/WavelengthControl/Output')

    def finish_user_action(self):
        self._put(r'/Optical/WavelengthControl/FinishWavelengthSettingAfterUserActions', r'{"RestoreShutter" :false}')
