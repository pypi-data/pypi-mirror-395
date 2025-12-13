#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""c3pcontrol - remote control of the CRONUS-3P laser.

Copyright 2020-2024 Light Conversion
Contact: support@lightcon.com
"""
import os
import json
import time
import datetime
from enum import IntEnum
import numpy as np
from ..common._http_methods import HTTP_methods
from ..common._logging import init_logger
from ..wintopas._wintopas import WinTopas
from ..laser_clients._laser_clients import Carbide

SRV_DIR = "C:\Programs\WinTopas4\Resources\SelfHostedServer"

def list_dirs(path):
    dir_names = []
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_dir():
                dir_names.append(entry.name)

    return dir_names

class C3PState(IntEnum):
    """CRONUS-3P laser states."""
    UnknownState = -3
    Fail = -2
    SoftFail = -1
    Idle = 0
    Preparation = 1
    MovingMotorsToInitialPosition = 2
    AdjustingOutputBeam = 3
    Success = 4


class C3PControl_Base(HTTP_methods):
    """CRONUS-3P remote control interface class."""
    silent = True
    verbose = False
    connected = False
    logger = None
    type = 'cronus-3p'
    hw_ver = None  # c3pv1 or c3pv2, set and implemented elsewhere
    has_gdd_control = True

    # Wait and timer constants
    max_wait_to_start = 3  # Maximum time to wait to start output setting
    max_wait_output_set = 30  # Maximum time to wait in seconds to complete output setting including all steps
    max_wait_state_change = 1  # Maximum time to wait for a state to change
    status_poll_delay = 0.05  # Delay to throttle status poll frequency

    # Accuracy limits
    wavl_eps = 2  # Maximum allowed wavelength difference in nm
    gdd_eps = 10  # Maximum allowed GDD difference in fs2

    def __init__(
            self, ip_address=None, port=35120, dev_sn=None, version='v0', **kwargs):
        """Initialization."""
        self.logger = init_logger('c3p', 'cronus_3p.log')

        if dev_sn is None:
            server_list = [srv for srv in list_dirs(SRV_DIR) if srv != 'Master']
            if len(server_list) == 1:
                dev_sn = server_list[0]
                self.logger.info(f"Using SN '{dev_sn}' as it is the only one available")
            elif len(server_list) == 0:
                raise RuntimeError("No CRONUS-3P servers found")
            elif len(server_list) > 1:
                dev_sn = server_list[0]
                self.logger.warning(f"No device SN provided and multiple Topas4 servers detected. Using the first one SN '{dev_sn}'.")

        if ip_address is None:
            ip_address = '127.0.0.1'

        self.dev_sn = dev_sn
        self.ip_address = ip_address

        self.virtual = self.read_cfg("General.json", "IsDemo")
        
        if self.virtual:
           self.logger.info("This is a virtual device, some functions will not work")

        self.url = 'http://{}:{}/{}/{}/'.format(
            ip_address, port, dev_sn, version)
        self.logger.info("Connecting to CRONUS-3P device "
                         "SN {:s} at {:s}:{:d}".format(
                            dev_sn, ip_address, port))
        try:
            self.connected = self._open('Help/API').find('Beam') != -1
        except Exception as excpt:
            self.logger.error(
                "Could not connect to CRONUS-3P. Make sure IP address, REST "
                "port and device SN are correct, the host is reachable, and "
                "that Light Composer is running. Exception reason: %s", excpt)
            self.connected = False
            raise RuntimeError("Could not connect to CRONUS-3P")

        if self.connected:
            self.logger.info("CRONUS-3P control established at %s", self.url)

        self.tctrl = None
        self.with_topas_control = kwargs.get('with_topas_control')
        if not self.with_topas_control:
            if kwargs.get('with_attenuator_control'):
                self.with_topas_control = True
                self.logger.info("Attenuator control for this device requires "
                    "a connection to Topas4 REST server.")
                self.idl_attn_motor_id = kwargs.get('idl_attn_motor_id', 12)

        if self.with_topas_control:
            self.logger.info("Connecting to the Topas4 server of "
                                "CRONUS-3P...")
            try:
                self.tctrl = WinTopas(ip_address, dev_sn=dev_sn,
                                      port=kwargs.get('topas_port', 8000))
            except Exception as excpt:
                self.logger.error("Could not connect to Topas4 REST server. "
                                "Exception reason: ", excpt)
                raise RuntimeError("Could not connect to Topas4 REST server")

            if self.tctrl is not None and self.tctrl.connected:
                self.logger.info("Topas4 control established at "
                                 f"{self.tctrl.url}")
            else:
                self.logger.error("Could not connect to Topas4 REST server. An"
                      " incrrect port was likely specified. The default port "
                      "for the first Topas4 server is 8000, but in some cases"
                      "the server might be running at a higher port "
                      "(8000-8200).")
                raise RuntimeError("Could not connect to Topas4 REST server")

        self.with_carbide_control = kwargs.get('with_carbide_control')
        if self.with_carbide_control:
            if self.virtual:
                self.logger.info("CARBIDE REST service not available for virtual devices")
            else:
                carbide_ip_address = kwargs.get('carbide_ip_address', '10.1.251.1')
                try:
                    self.logger.info("Connecting to CARBIDE REST server...")
                    self.cbxctrl = Carbide(
                        ip_address=carbide_ip_address, port=20010,
                        with_register_access=True)
                except Exception as excpt:
                    self.logger.error("Could not connect to CARBIDE REST server")
                    self.cbxctrl = None

                if self.cbxctrl is not None:
                    self.logger.info("CARBIDE control established at "
                                    f"{self.cbxctrl.url}")

    def __del__(self):
        self.logger.info("Stopping remote CRONUS-3P control")

    def _put(self, command, data):
        """PUT wrapper that parses returned data.

        A valid PUT returns None, an error returns the error message.
        """
        result = super()._put(command, data)
        if result is not None and result.__class__ != int:
            if "Remote control is blocked by user" in result:
                raise RuntimeError("Remote control is blocked")
            else:
                raise RuntimeError(f"Error while sending a PUT request: {result}")

        return result

    def read_cfg(self, cfg_file, key):
        """Read device configuration files."""
        file_name = SRV_DIR + f"\{self.dev_sn}\Configuration\Settings\\" \
            + cfg_file
        return json.load(open(file_name, 'r'))[key]

    # === Helper ===
    def _set_and_track_state(self, wait_until_done=True, verbose=False, output_set_func=None, output_set_args=None):
        """Set output and track output setting status.

        Implements a common state tracker routine for wavelength and GDD
        setting.
        """
        # Mark the initial output setting state before a PUT request is issued
        initial_state = self.get_wavelength_setting_state()

        output_set_func(*output_set_args)

        if not wait_until_done:
            return True

        # Step 1: Wait until state starts to change
        if verbose:
            self.logger.info(f"Waiting for output setting to start...")

        t_start = time.time()
        while True:
            time.sleep(self.status_poll_delay)
            set_state = self.get_wavelength_setting_state()

            # Timeout if this takes too long
            if time.time() - t_start > self.max_wait_to_start:
                raise RuntimeError(f"Output setting did not start within the specified {self.max_wait_to_start:.0f} s timeout period")

            # Wait some more if the setting state has not changed.
            # NOTE: This is better than checking when the state is no longer
            # Success because this way it also works when the change starts
            # from a state other than success, e.g., a retry after a previous
            # failure
            if set_state == initial_state:
                continue

            if set_state == C3PState.Fail:
                raise RuntimeError("Failed to set output")

            if set_state != C3PState.Success:
                # Change started successfully, exit loop
                break

        # Step 2: Wait until state change either succeeds or fails
        if verbose:
            self.logger.info(f"Setting output...")
        set_state = self.get_wavelength_setting_state()
        while True:
            time.sleep(self.status_poll_delay)
            set_state = self.get_wavelength_setting_state()

            # Timeout if this takes too long
            if time.time() - t_start > self.max_wait_output_set:
                raise RuntimeError(f"Output setting was not completed within the allowed {self.max_wait_to_start:.0f} s")

            if verbose:
                self.logger.info(f"Set state: {set_state.name} ({set_state.value})")

            if set_state in [C3PState.Success, C3PState.Fail]:
                break

        # Step 3: Wait to check if the Success state holds for some time
        t_start = time.time()
        while True:
            time.sleep(self.status_poll_delay)
            set_state = self.get_wavelength_setting_state()

            if verbose:
                self.logger.info(f"Set state: {set_state.name} ({set_state.value})")

            if set_state not in [C3PState.Success, C3PState.Fail]:
                raise RuntimeError("Output setting state changed after reporting success")

            if time.time() - t_start > self.max_wait_state_change:
                if verbose:
                    self.logger.info(f"Output setting completed")
                break

        return True


    # === Status ===

    def get_status(self):
        """Get laser system status."""
        return self._get('Main/Status')

    def get_pump_laser_status(self):
        """Get pump laser status."""
        return self._get('PumpLaser/Status')

    def get_info(self):
        """Get laser info."""
        return self._get('Main/Info')

    def wavelength_setting_state_str_to_enum(self, state_str):
        """Convert wavelength setting state string to enum."""
        c3p_state_strings = [
            'UnknownState', 'Fail', 'SoftFail',
            'Idle', 'Preparation', 'MovingMotorsToInitialPosition',
            'AdjustingOutputBeam', 'Success']

        if state_str not in c3p_state_strings:
            self.logger.error(f"Unrecognized state string '{state_str}'")
            return C3PState.UnknownState
        else:
            return C3PState(c3p_state_strings.index(state_str) - 3)

    def get_wavelength_setting_state(self):
        """Get wavelength setting state."""
        return self.wavelength_setting_state_str_to_enum(
            self.get_status()['WavelengthSettingState'])

    def print_status(self):
        """Print status."""
        status = self.get_status()

        print('Wavelength: {:.0f} nm'.format(status['Wavelength']))
        print('GDD: {:.0f} fs^2'.format(status['GDD']))

        print('Wavelength set result: ' + status['WavelengthSettingState'])

        print('Beam tracking:')
        beam_tr = status['BeamPositions'][0]
        print('\tNear: power={:.3f}, x={:.3f}, y={:.3f}'.format(
            beam_tr['Intensity'], beam_tr['X'], beam_tr['Y']))
        beam_tr = status['BeamPositions'][1]
        print('\tFar : power={:.3f}, x={:.3f}, y={:.3f}'.format(
            beam_tr['Intensity'], beam_tr['X'], beam_tr['Y']))

    def is_motor_moving(self, index):
        """Check if motor is moving."""
        return self.tctrl._get(f'Motors/ActualPosition?id={index}') == \
            self.tctrl._get(f'Motors/TargetPosition?id={index}')

    # === Wavelength ===

    def get_wavelength(self):
        """Get wavelength in nm."""
        return self._get('Main/Status')['Wavelength']

    def set_wavelength(self, wavl, retry=True, num_retries=3, **kwargs):
        """Set wavelength in nm."""
        for attempt_ind in range(num_retries):
            try:
                return self._set_wavelength(wavl, **kwargs)
            except Exception as excpt:
                self.logger.error("Could not set wavelength. Reason: ", excpt)
                if retry:
                    self.logger.info("Trying again, attempt " \
                                     f"{attempt_ind+1}/{num_retries}")
                if attempt_ind == num_retries:
                    self.logger.error("Could not set wavelength after multiple"
                                      "retries")
                    raise excpt

    def _set_wavelength(
            self, wavl, gdd=None, skip_if_set=True, wait_until_done=False,
            with_beam_tracking=False, open_shutters=False, verbose=None):
        """Set wavelength with optional beam tracking."""
        if verbose is None:
            verbose = self.verbose

        if open_shutters:
            if verbose:
                self.logger.info('Opening shutters...')
            self.open_all_shutters()

        old_wavl = self.get_wavelength()

        if self.has_gdd_control and gdd is not None:
            old_gdd = self.get_gdd()

        if skip_if_set and np.abs((old_wavl - wavl)) < 1:
            if not self.has_gdd_control or gdd is None:
                self.logger.info("Wavelength already set")
                return True
            elif np.abs((old_gdd - gdd)) < 100:
                self.logger.info("Wavelength and GDD already set")
                return True

        if verbose:
            if self.has_gdd_control and gdd is not None:
                self.logger.info(f"Setting wavelength to {wavl:.0f} nm and GDD"
                      f" to {gdd:.0f} fs2...")
            else:
                self.logger.info(f"Setting wavelength to {wavl:.0f} nm...")

        timestamp = datetime.datetime.now()
        timestamp_str = timestamp.strftime('%Y-%m-%d_%H%M%S')

        gdd_setting_enabled = False
        skip_gdd_setting_outside_range = True
        if self.has_gdd_control and gdd is not None:
            if wavl < 1250 or wavl > 1800:
                gdd_setting_enabled = False
            else:
                gdd_range = self.get_gdd_range()
                if gdd >= gdd_range[0] and gdd <= gdd_range[1]:
                    gdd_setting_enabled = True
                elif skip_gdd_setting_outside_range:
                    gdd_setting_enabled = True
                    self.logger.info("Requested GDD is outside the available "
                                     "range, setting wavelength only")
                else:
                    gdd_setting_enabled = False

        output_set_func = self._put
        if gdd_setting_enabled:
            output_set_args = ['Main/WavelengthAndGDD', json.dumps({'Wavelength': float(wavl), 'GDD': float(gdd)})]
        else:
            output_set_args = ['Main/Wavelength', json.dumps({'Wavelength': float(wavl)})]

        status = self._set_and_track_state(wait_until_done=wait_until_done, verbose=verbose, output_set_func=output_set_func, output_set_args=output_set_args)

        if not status:
            return False

        set_state = self.get_wavelength_setting_state()

        if set_state == C3PState.Success:
            if abs(self.get_wavelength() - wavl) > self.wavl_eps:
                self.logger.info("OK")
            else:
                self.logger.error(f"Wavelength set reported success but the actual wavelength {self.get_wavelength()} nm is incorrect")
                return False
        elif set_state == C3PState.Fail:
            self.logger.error("Failed to set wavelength")
            return False
        else:
            self.logger.error("Unknown laser state encountered")
            return False
        return True


    def wait_until_wavelength_set(self):
        """Wait until wavelength setting procedure is completed."""
        while self.get_wavelength_setting_state() != 'Success':
            time.sleep(0.05)

    # === GDD ===

    def get_gdd(self):
        """Get GDD in fs^2."""
        # return self._get('GDD')['GDD']
        return self._get('Main/Status').get('GDD')

    def set_gdd(
            self, gdd, skip_if_set=True, wait_until_done=False,
            open_shutters=False, verbose=None):
        """Set GDD."""
        if verbose is None:
            verbose = self.verbose

        if not self.has_gdd_control:
            return False

        if open_shutters:
            if verbose:
                self.logger.info("Opening shutters...")
            self.open_all_shutters()

        old_gdd = self.get_gdd()

        if skip_if_set and np.abs((old_gdd - gdd)) < 10:
            self.logger.info("GDD already set")
            return True

        if verbose:
            self.logger.info(f"Setting GDD to {gdd:.0f} fs^2...")

        timestamp = datetime.datetime.now()
        timestamp_str = timestamp.strftime('%Y-%m-%d_%H%M%S')

        output_set_func = self._put
        output_set_args = ['Main/GDD', json.dumps({'GDD': float(gdd)})]

        if not self._set_and_track_state(wait_until_done=wait_until_done, verbose=verbose, output_set_func=output_set_func, output_set_args=output_set_args):
            return False

        set_state = self.get_wavelength_setting_state()
        final_gdd = self.get_gdd()

        if set_state == C3PState.Success:
            if abs(final_gdd - gdd) < self.gdd_eps:
                self.logger.info("OK")
            else:
                self.logger.error(f"GDD set reported success but the actual GDD {final_gdd} fs2 differs from the requested {gdd} fs2")
                return False
        elif set_state == C3PState.Fail:
            self.logger.error("Failed to set gdd")
            return False
        else:
            self.logger.error(f"Unexpected laser state {set_state.name} ({set_state.value}) encountered")
            return False

        return True


    def get_gdd_range(self, wavl=None):
        """Get GDD range in fs^2."""
        if wavl is None:
            response = self._get('Main/CurrentGDDRange')
            return [response.get('Min'), response.get('Max')]
        else:
            response = self._post('Main/GDDRange', {'Interaction': 'IDL',
                                                    'Wavelength': float(wavl)})
            return [response.get('Min'), response.get('Max')]

    # === Beam steering ===

    def has_beam_steering(self):
        """Check whether laser system has beam steering."""
        return self.get_info().get('HasOutputBeamStabilization', False)

    def is_beam_steering_active(self):
        """Check whether beam steering is active."""
        return self.get_status()['IsBeamSteeringActive']

    def get_beam_steering_pos(self):
        """Get the position of beam steering motors."""
        return self.get_status().get('BeamMirrorActualPositions')

    def get_beam_position(self):
        """Get beam position."""
        return self.get_status().get('BeamPositions')

    def get_beam_position_total(self):
        """Get beam position total signal."""
        status = self.get_status()
        qd1_ampl = status['BeamPositions'][0]['Intensity']
        qd2_ampl = status['BeamPositions'][1]['Intensity']

        return [qd1_ampl, qd2_ampl]

    def set_beam_pos(self, mirror_id=1, xpos=0, ypos=0, wait_until_done=False,
                     extra_wait_time=0.05):
        """Move beam steering mirror."""
        self._put('Beam/MoveBeam/{:d}'.format(mirror_id), json.dumps(
                  {'X': float(xpos), 'Y': float(ypos)}))

        if wait_until_done:
            self.logger.info("Waiting for mirror to move...")
            t_start = time.time()
            while True:
                if time.time() - t_start > 5:
                    self.logger.warning("Mirror move taking longer than 5 s, "
                                        "reissuing move command...")
                    self._put('Beam/MoveBeam/{:d}'.format(mirror_id),
                              json.dumps({'X': float(xpos), 'Y': float(ypos)}))
                    t_start = time.time()

                pos = self.get_beam_steering_pos()[mirror_id-1]
                if np.abs((pos['X'] - xpos)) < 0.01 \
                        and np.abs((pos['Y'] - ypos)) < 0.01:
                    break
                time.sleep(extra_wait_time)
            self.logger.info("Mirror move completed")

    def center_beam(self, wait_until_done=True):
        """Activate beam steering procedure to center the beam."""
        if wait_until_done:
            self.logger.info("Initiating beam steering...")
        else:
            self.logger.info("Beam steering initiated (no wait)")

        self._put('CenterBeam', '')

        if wait_until_done:
            while not self.is_beam_steering_active():
                time.sleep(0.01)

            while self.is_beam_steering_active():
                time.sleep(0.01)

            self.logger.info("Beam steering completed")


class C3Pv1Control(C3PControl_Base):
    def __init__(self, ip_address, **kwargs):
        self.hw_ver = 'c3pv1'
        super().__init__(ip_address, **kwargs)

    def print_status(self):
        """Print status for C3Pv1 systems."""
        super().print_status()
        status = self.get_status()

        print('Shutter: ' + 'Open' if status['IsPrimaryShutterOpen'] else
            'False')

    def is_output_shutter_open(self):
        return self.get_status()['IsPrimaryShutterOpen']

    def open_all_shutters(self, wait_to_stabilize=True, verbose=None,
                          max_wait=3):
        """Open all shutters."""
        if verbose is None:
            verbose = self.verbose

        if verbose:
            self.logger.info("Opening shutters...")

        ret_val = self._put('Main/OpenShutters', '')
        t_start = time.time()

        time.sleep(1)

        while not self.get_status()['Shutters']['IsShutterOpen']:
            if time.time() - t_start > max_wait:
                raise RuntimeError("Could not open shutters in the allocated "
                                   "maximum time ({:d} seconds)".format(
                                       max_wait))
            time.sleep(0.1)

        if wait_to_stabilize:
            if verbose:
                self.logger.info("Waiting for system to stabilize...")
            time.sleep(2)

        return ret_val

    def close_all_shutters(self, wait_to_stabilize=False, verbose=None):
        """Close all shutters."""
        if verbose is None:
            verbose = self.verbose

        if verbose:
            self.logger.info("Closing shutters...")

        ret_val = self._put('Main/CloseShutters', '')

        if wait_to_stabilize:
            if verbose:
                self.logger.info("Waiting for system to stabilize...")
            time.sleep(2)

        return ret_val

class C3Pv2Control(C3PControl_Base):
    def __init__(self, **kwargs):
        self.hw_ver = 'c3pv2'
        super().__init__(**kwargs)

        # Determine analog input adu to Volts factor
        try:
            self.ain_adu_per_volt = self.read_cfg(
                "LightComposer\Channels\IDL\ExternalAttenuatorControl.json",
                "InputAduPerVolt")
        except Exception as excpt:
            # TODO: This will fail for Light Composer <v3 because there is no 'Channels'
            # folder there yet. Might be good to scan the entire server
            # configuration folder to look for the file, or just use the
            # default.
            self.ain_adu_per_volt = 2625
            self.logger.warning("Could not determine adu to Volts from " \
                                "configuration, using default value " \
                                f"{self.ain_adu_per_volt:.1f}.")
            # raise

    def print_status(self):
        """Print status."""
        super().print_status()
        status = self.get_status()

        for shutter in status['Shutters']['Shutters']:
            print(f"Shuter '{shutter['Name']}' is {shutter['IsShutterOpen']}")

    def check_if_beam_is_ready(self):
        """Check if laser is ready for beam output."""
        # Make sure laser is ready
        status = self.get_status()
        if not status['IsPumpLaserReady']:
            raise RuntimeError("CRONUS-3P pump laser is not ready")
        if not status['IsWavelengthSet']:
            raise RuntimeError("CRONUS-3P wavelength is not set")

        return True

    # === Attenuator ===
    def get_attenuator_pos(self):
        """Get IDL channel attenuator motor position in steps."""
        if not self.check_attenuator():
            self.logger.error("Cannot get attenuator motor position.")
        else:
            return self.tctrl.get_motor_pos(self.idl_attn_motor_id)

    def set_attenuator_pos(self, pos, wait_until_done=False):
        """Set IDL channel attenuator motor position in steps."""
        if not self.check_attenuator():
            self.logger.error("Cannot get attenuator motor position.")
        else:
            self.tctrl.set_motor_pos(self.idl_attn_motor_id, pos)

            if wait_until_done:
                while True:
                    actual = self.tctrl.get_motor_pos(self.idl_attn_motor_id)
                    if np.abs((pos - actual)) < 10:
                        break
                    time.sleep(0.05)

    def check_attenuator(self):
        """Check whether IDL channel attenuator can be controlled."""
        if not self.tctrl:
            self.logger.error("Attenuator control requires Topas4 REST")
            return False

        if not self.idl_attn_motor_id:
            self.logger.error("IDL attenuator motor ID not defined")
            return False

        if not self.virtual and not self.get_status().get('IsPumpLaserReady'):
            self.logger.error("Pump laser is not started")
            return False

        return True

    def attn_pwr_target_to_steps(self, target, min_pos=0, max_pos=5200):
        """Convert attenuator target transmission to motor steps.

        Conversion assumes Malus law and that the provided max_pos and min_pos
        values are correct.
        """
        period = max_pos - min_pos
        attn_pos = 4*period/(2*np.pi) * (np.arcsin(np.sqrt(target))) + min_pos
        attn_pos = int(np.round(attn_pos))
        return attn_pos

    def attn_ain_to_pwr_target(self, ain, max_ain=5):
        """Convert analog input to power target transmission.

        Conversion just applies linear mapping from [0, max_ain] to [0, 1.0].
        """
        return np.nanmax([np.nanmin([ain/max_ain, 1.0]), 0.0])

    # === Shutters ===

    def is_output_shutter_open(self):
        """Check if the output shutter of the main tunable channel is open."""
        for shutter in self.get_status()['Shutters']['Shutters']:
            if shutter['Name'] == 'OPA':
                return shutter['IsShutterOpen']

        self.logger.error("Could not find 'OPA' output shutter")
        return False


    def open_all_shutters(self, wait_to_stabilize=True, verbose=None,
                          max_wait=3):
        """Open all shutters."""
        if verbose is None:
            verbose = self.verbose

        if verbose:
            self.logger.info("Opening shutters...")

        ret_val = self._put('Main/OpenShutters', '')
        t_start = time.time()

        time.sleep(1)

        while not self.get_status()['Shutters']['IsShutterOpen']:
            if time.time() - t_start > max_wait:
                raise RuntimeError("Could not open shutters in the allocated "
                                   "maximum time ({:d} seconds)".format(
                                       max_wait))
            time.sleep(0.1)

        if wait_to_stabilize:
            if verbose:
                self.logger.info("Waiting for system to stabilize...")
            time.sleep(2)

        return ret_val

    def close_all_shutters(self, wait_to_stabilize=False, verbose=None):
        """Close all shutters."""
        if verbose is None:
            verbose = self.verbose

        if verbose:
            self.logger.info("Closing shutters...")

        ret_val = self._put('Main/CloseShutters', '')

        if wait_to_stabilize:
            if verbose:
                self.logger.info("Waiting for system to stabilize...")
            time.sleep(2)

        return ret_val

    # === Analog input ===

    def _get_ain_adu(self):
        if not self.with_carbide_control:
            raise RuntimeError("AIN read requires CARBIDE control")
        if not self.with_topas_control:
            raise RuntimeError("AIN read requires Topas control")
        if self.virtual:
            return 12345
        else:
            return self.cbxctrl.get_register('0x03000700')

    def get_ain_volts(self):
        return self._get_ain_adu()/self.ain_adu_per_volt

class C3PControl(C3Pv2Control):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
