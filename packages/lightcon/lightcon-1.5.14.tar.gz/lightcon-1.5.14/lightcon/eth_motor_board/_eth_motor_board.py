# -*- coding: utf-8 -*-
"""lightcon - a Python library for controlling Light Conversion devices.

API for controlling Ethernet-connected motor boards (EthMotorBoard).

A working IPv4 connection to the EthMotorBoard is needed to control it.
EthMotorBoards get assigned either a fixed IP address in the
10.1.1.x space or an auto-generated one in the 10.x.x.x at the factory. You
will need an Ethernet adapter with a static IP address in the 10.x.x.x space to
connected to the EthMotorBoard. The use of a dedicated Ethernet adapter is
recomended.

If you do not know the IP address of the EthMotorBoard you want to control you
can use the "Manage Eth motor boards" feature in WinTopas4. You can also use
the UDP locator feature included in this library.

Copyright 2019-2025 Light Conversion
Contact: support@lightcon.com
"""
import socket
import time
import string

from ..common._leprecan_provider import LepreCanProvider
from ..common._udp_locator import UdpLocator
from ._eth_motor_board_leprecan_provider import EthMotorBoardLepreCanProvider


class EthMotorBoard(LepreCanProvider):
    """Class to control EthMotorBoards."""

    BUFFER_SIZE = 1024
    sock = None
    connected = False
    name = None
    timeout = 100
    fv = None
    ip_address = None
    verbose = False
    max_position = 2**21-1

    info_dict = {
        'Acc': 'ACC', 'Dec': 'DEC', 'FnSlpAcc': 'FN_SLP_ACC',
        'FnSlpDec': 'FN_SLP_DEC', 'IntSpeed': 'INT_SPEED',
        'KTherm': 'K_THERM', 'KvalAcc': 'KVAL_ACC', 'KvalDec': 'KVAL_DEC',
        'KvalHold': 'KVAL_HOLD', 'KvalRun': 'KVAL_RUN',
        'MaxSpeed': 'MAX_SPEED', 'MinSpeed': 'MIN_SPEED',
        'OcdTh': 'OCD_TH', 'StSlp': 'ST_SLP', 'StallTh': 'STALL_TH',
        'AlarmEn': 'ALARM_EN', 'Config': 'CONFIG', 'FsSpeed': 'FS_SPD',
        'MotorName': 'MOTOR_NAME',
        'StepMode': 'STEP_MODE', 'LsEnable': 'LS_ENABLE',
        'LsInvert': 'LS_INVERT', 'LsSwap': 'LS_SWAP'}

    reg_dict = {'HardHiZ': ('HIZ {:} HARD', 0x00A8),
                'AbsPos': ('', 0x0001),
                'Stop': ('', 0x00B8),
                'GoTo': ('', 0x0060),
                'RunForward': ('RUN {:} 0', 0x0051),
                'RunReverse': ('RUN {:} 1', 0x0050),
                'Acc': ('ACC', 0x0005),
                'Dec': ('DEC', 0x0006),
                'FnSlpAcc': ('FN_SLP_ACC', 0x000F),
                'FnSlpDec': ('FN_SLP_DEC', 0x0010),
                'IntSpeed': ('INT_SPEED', 0x000D),
                'KTherm': ('K_THERM', 0x0011),
                'KvalAcc': ('KVAL_ACC', 0x000B),
                'KvalDec': ('KVAL_DEC', 0x000C),
                'KvalHold': ('KVAL_HOLD', 0x0009),
                'KvalRun': ('KVAL_RUN', 0x000A),
                'MaxSpeed': ('MAX_SPEED', 0x0007),
                'MinSpeed': ('MIN_SPEED', 0x0008),
                'OcdTh': ('OCD_TH', 0x0013),
                'StSlp': ('ST_SLP', 0x000E),
                'StallTh': ('STALL_TH', 0x0014),
                'StepMode': ('STEP_MODE', 0x0016),
                'LSStatus': ('', 0x0100),
                'LSEnable': ('', 0x0103)}

    status_registers = [
        (0x01, 0x01, 'HiZ'), (0x02, 0x0, 'BUSY'), (0x04, 0x04, 'SW_F'),
        (0x08, 0x08, 'SW_ENV'), (0x60, 0x00, 'Stopped'),
        (0x60, 0x20, 'Acceleration'), (0x60, 0x40, 'Deceleration'),
        (0x60, 0x60, 'Constant speed'), (0x80, 0x80, 'NOTPERF_CMD'),
        (0x100, 0x100, 'WRONG_CMD'), (0x200, 0x0, 'OVLO'),
        (0x400, 0x0, 'TH_WRN'), (0x800, 0x0, 'TH_SD'), (0x1000, 0x0, 'OCD'),
        (0x2000, 0x0, 'STEP_LOSS_A'), (0x4000, 0x0, 'STEP_LOSS_B'),
        (0x8000, 0x8000, 'SCK_MOD')]

    ls_registers = [
        (0x01, 0x01, 'Left LS reached'), (0x02, 0x02, 'Right LS reached')]

    def __init__(self, ip_address=None, **kwargs):
        """Create an EthMotorBoard control instance."""

        if ip_address is None:
            loc = UdpLocator()
            devices = loc.locate('EthMotorBoard', **kwargs)

            if not devices:
                raise RuntimeError("No EthMotorBoard devices found.")

            if len(devices) > 1:
                print("A total of {:} EthMotorBoard devices were found, using "
                      "the first one".format(len(devices)))

            ip_address = devices[0].get('IpAddress')

        if ip_address is None:
            raise RuntimeError("No EthMotorBoard devices found")

        self.ip_address = ip_address

        self.name = self.send('GET BOARD_NAME')
        self.fv = self.send('FIRMWARE_VERSION')

        self.connected = self.fv is not None

        if self.connected:
            print("Successfully connected to EthMotorBoard {:} at address {:},"
                  " firmware version: {:}".format(
                    self.name, self.ip_address, self.fv))

            self.can = EthMotorBoardLepreCanProvider(self)

        else:
            raise RuntimeError(
                "Motor board not found at {:}".format(self.ip_address))

    def get_stage_param(self, stage_name=None):
        """Get stage parameters."""
        from lightcon.common import stage_parameters

        if stage_name is None:
            print("Stage name not specified")
            return False

        stage_cfg = stage_parameters.get(stage_name) \
            or stage_parameters.get(stage_name.replace('.json', '')) \
            or stage_parameters.get(stage_name + '.json')

        if not stage_cfg:
            print("Stage configuration not found")
            return False

        return stage_cfg

    def setup_stage(self, motor_index, stage_name=None, **kwargs):
        """Set stage parameters.

        Stage parameters are parsed from the stage_parameters.py file. The
        stage entry must include a MotorName with is then used in setup_motor
        to parse motor parameters. Stage parameters override motor parameters.
        """
        stage_cfg = self.get_stage_param(stage_name)

        motor_name = stage_cfg.get('motor_name') or stage_cfg.get('MotorName')
        if not motor_name:
            print("Stage has no motor defined")
            return False

        return self.setup_motor(motor_index=motor_index, cfg_name=motor_name,
                                extra_par=stage_cfg, **kwargs)

    def setup_motor(self, motor_index, cfg_name, extra_par=None, **kwargs):
        """Set motor parameters.

        This is a wrapper function to parse the motor parameters from the
        motor_parameters.py file. The actual set commands are in
        setup_motor_dict.
        """
        from lightcon.common import motor_parameters

        if cfg_name is None:
            print("Configuration file not specified for motor ", motor_index)
            return False

        motor_name = cfg_name.replace('.json', '')
        motor_name_with_ext = motor_name + '.json'

        motor_cfg = motor_parameters.get(cfg_name) \
            or motor_parameters.get(motor_name) \
            or motor_parameters.get(motor_name_with_ext)

        if not motor_cfg:
            print("Motor configuration not found")
            return False

        if extra_par:
            for key in extra_par.keys():
                motor_cfg[key] = extra_par[key]

        return self.setup_motor_dict(motor_index=motor_index,
                                     motor_cfg=motor_cfg, **kwargs)

    def get_motor_config(self, motor_index):
        """Get all motor parameters."""
        motor_cfg = {}
        for key in self.info_dict.keys():
            message = 'GET {:} {:}'.format(
                self.info_dict[key], motor_index)
            response = self.send(message)
            motor_cfg[key] = response

        return motor_cfg

    def setup_motor_dict(
            self, motor_index, motor_cfg, **kwrags):
        """Setup motor parameters from a preformatted dict."""

        motor_name = motor_cfg.get('MotorName', '')
        print("Configuring motor {:} on port {:d}".format(motor_name,
                                                          motor_index))

        self.send('HIZ {:} HARD'.format(1 << motor_index))
        time.sleep(1)

        for key in motor_cfg.keys():
            if self.info_dict.get(key):
                message = 'SET {:} {:} {:}'.format(
                    self.info_dict[key], motor_index, motor_cfg[key])
                response = self.send(message)
                if self.verbose:
                    print(response, 'from', message)

        return True

    def send(self, message, args=None):
        """Send a command to the board and get a response.

        TODO: This should probably be called a querry.
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout/1000)
            self.sock.connect((self.ip_address, 80))

            if args is None:
                self.sock.send((str(message)+'\r\n').encode('UTF-8'))
            else:
                self.sock.send((
                    str(message) + ' '
                    + ' '.join([str(arg) for arg in args])
                    + '\r\n').encode('UTF-8'))

            data = self.sock.recv(self.BUFFER_SIZE)
            self.sock.close()
            return data[:-2].decode()
        except socket.timeout:
            return None

    def get_status(self, motor_index):
        """Get board status."""
        status = int(self.send('GET STATUS', [motor_index]))
        ls_result = self.send('GET LIMIT_SWITCH', [motor_index])
        ls_status = eval(ls_result)['Logical']
        return [stat for mask, val, stat in self.status_registers
                if status & mask == val] \
            + [stat for mask, val, stat in self.ls_registers
                if ls_status & mask == val]

    def stop_motor(self, motor_index):
        """Stop motor."""
        status = self.send('STOP {:} HARD'.format(1 << motor_index))
        return status

    def wait_until_stopped(self, motor_index):
        """Wait until motor stops."""
        stopped = False
        if self.verbose:
            print("Waiting for the stage to stop...")

        while not stopped:
            status = self.get_status(motor_index)

            if self.verbose:
                print("Status: ", self.get_status(motor_index))
                print("Speed: ", self.get_speed(motor_index))

            stopped = 'Stopped' in status
            if stopped:
                continue

            time.sleep(0.05)

    def wait_until_stopped_ext(self, motor_index,
                               ls_safety_stop=False, measure_speed=False):
        """Wait until motor stops.

        This is an extended version of wait_until_stopped() used for testing
        and debuging.
        """
        stopped = False
        if self.verbose:
            print("Waiting for the stage to stop...")

        speed_poll_intveral = 1
        pos_ref = None
        t_ref = None

        t_last_ls_trip = None

        if self.verbose:
            print("Max speed: ", self.get_max_speed(motor_index))

        while not stopped:
            t_now = time.time()
            if measure_speed:
                if not t_ref:
                    t_ref = t_now
                    pos_ref = self.get_abs_pos(motor_index)
                if t_now - t_ref > speed_poll_intveral:
                    pos_now = self.get_abs_pos(motor_index)
                    print("Speed: {:.0f} steps/s".format(
                        (pos_now - pos_ref)/(t_now - t_ref)))
                    t_ref = t_now
                    pos_ref = pos_now

            status = self.get_status(motor_index)

            if self.verbose:
                print("Status: ", self.get_status(motor_index))
                print("Speed: ", self.get_speed(motor_index))

            stopped = 'Stopped' in status
            if stopped:
                continue

            if ls_safety_stop \
                    and ('Left LS reached' in status
                         or 'Right LS reached' in status):
                if not t_last_ls_trip:
                    t_last_ls_trip = t_now

                if t_now - t_last_ls_trip > 2:
                    self.stop_motor(motor_index)
                    raise RuntimeError(
                        "Stage limit switches are likely swapped.")
            time.sleep(0.05)

    def get_abs_pos(self, motor_index):
        """Get absolute position in steps."""
        return int(self.send('GET ABS_POS ' + str(motor_index)))

    def move_rel(self, motor_index, move_dir=0, pos_delta=0):
        """Move motor a given distance from the current position."""
        ret_code = self.send('MOVE {:d} {:d} {:d}'.format(
            motor_index, move_dir, pos_delta))

        self.check_error(ret_code)

    def move_abs(self, motor_index, abs_pos=0):
        """Move motor to an absolute position."""
        ret_code = self.send('GOTO {:d} {:d}'.format(motor_index, abs_pos))
        self.check_error(ret_code)

    def run_stage(self, motor_index, move_dir=0, speed=10000):
        """Run stage continuously.

        Run the stage continuously in the given direction until stopped or a
        limit switch is activated.
        """
        ret_code = self.send('RUN {:d} {:d} {:d}'.format(
            motor_index, move_dir, speed))

        return self.check_error(ret_code)

    def get_max_speed(self, motor_index):
        """Get maximum speed."""
        return int(self.send('GET MAX_SPEED ' + str(motor_index)))

    def get_speed(self, motor_index):
        """Get current speed."""
        return int(self.send('GET SPEED ' + str(motor_index)))

    def set_max_speed(self, motor_index, speed=100):
        """Set maximum speed."""
        if speed < 0:
            raise ValueError("Speed has to be positive")
        if speed > 1024:
            raise ValueError("Speed has to be less than 1024")

        ret_code = self.send('SET MAX_SPEED {:d} {:d}'.format(
            motor_index, speed))
        self.check_error(ret_code)

    def check_error(self, ret_code):
        """Check the return value.

        'ERR0' means that everything is fine. 'ERR4' means that a limit switch
        has been reached. These two codes can be ignored in most cases.
        Anything else indicates an error.
        """
        ret_code = strip_whitespace(ret_code)

        if ret_code not in ['ERR0', 'ERR4']:
            print("Error: " + ret_code)

    def reset_motor(self, motor_index, move_dir=0, speed=10000):
        """Reset motor and set current position to 0.

        Move motor in the given direction until a limit switch has been
        reached and set the current position there to 0.
        """
        ret_code = self.send('RUN {:d} {:d} {:d}'.format(
            motor_index, move_dir, speed))

        self.check_error(ret_code)

        self.wait_until_stopped(motor_index)

        pos = self.get_abs_pos(motor_index)

        ret_code = self.send('RESET_POS {:d}'.format(motor_index))
        self.check_error(ret_code)

        return {'abs_pos_at_reset': pos}


# === Helper functions ===
def strip_whitespace(s):
    return s.translate(str.maketrans('', '', string.whitespace))
