#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""power_meter - remote control API of Light Conversion PowerMeter devices.

Copyright 2019-2024 Light Conversion
Contact: support@lightcon.com
"""
import json
import time
from lightcon.common import HTTP_methods, UdpLocator
from lightcon.common._logging import init_logger


class PowerMeter(HTTP_methods):
    """PowerMeter remote control interface class."""
    silent = True
    connected = False
    logger = None
    serialNumber = None

    def __init__(
            self, ip_address=None, port=52568, dev_sn=None, version='v2',
            **kwargs):
        """Initialization."""
        self.logger = init_logger('powermeter', 'powermeter.log')

        if ip_address is None:
            # Locate a PowerMeter service on the network by using UDP multicast
            # based on the serial number of the connected meter head.
            locator = UdpLocator()
            print("Looking for PowerMeter devices on the network...")
            devices = locator.locate('Remote PowerMeter v2')
            if len(devices) > 0:
                print("Found {:} devices".format(len(devices)))
            else:
                self.logger.error("No devices found")
                return None

            device_info = next((entry for entry in devices \
                                if entry['SerialNumber'] == self.serialNumber),
                                None)

            if device_info is None:
                print("PowerMeter SN {:} not found".format(self.serialNumber))
                raise RuntimeError
            else:
                print("PowerMeter SN {:} located".format(self.serialNumber))
                ip_address = device_info['IpAddress']
                port = device_info['RestPort']

        self.url = 'http://{}:{}/{}/'.format(ip_address, port, version)
        self.logger.info("Connecting to PowerMeter SN {:} at {:}:{:}".format(
                            dev_sn, ip_address, port))
        try:
            self.connected = self._open('Info') != -1
        except Exception as excpt:
            self.logger.error(
                "Could not connect to PowerMeter. Make sure the device is "
                " powered up, connected to the host computer, the IP address "
                " and the REST port are correct, the host is reachable, and "
                "that PowerMeter is running. Exception reason: %s", excpt)
            self.connected = False

        if self.connected:
            self.logger.info("PowerMeter control established at %s", self.url)

    def __del__(self):
        self.logger.info("Stopping remote PowerMeter control")

    # === get_power ===
    def get_power(self, num_samples=1, sample_delay=0):
        """Get power meter readings."""
        val_arr = []
        for ind in range(num_samples):
            data = json.loads(self._get('/PowerData').content.decode('UTF8'))
            val_arr.append(data['measuredValue'])
            time.sleep(sample_delay)

        return val_arr
