# -*- coding: utf-8 -*-
"""lightcon - a Python library for controlling Light Conversion devices.

UDP locator class, which allows Light Conversion devices to be located on the
local area network without knowing their IP addresses.

Copyright 2020-2022 Light Conversion
Contact: support@lightcon.com
"""
import json
import socket

__doctest_skip__ = ['*']

class UdpLocator:
    """UDP locator class."""

    def locate(self, identifier='ALL', ipv4_only=True, verbose=False,
               one_response_enough=False, **kwargs):
        """Locates Light Conversion LAN devices using UDP multicasts. All host IP 
        interfaces are used as well as localhost which is needed when probing
        servers running on the same machine as this program.

        Other devices may or may not be supported.

        Examples:
            >>> from from lightcon.common import UdpLocator # doctest: +SKIP
            >>> udp_locator = UdpLocator() # doctest: +SKIP
            >>> devices = udp_locator.locate('ALL') # doctest: +SKIP

        Args:
            identifier (str): default: 'ALL'
                The identifier is used to limit the scope of devices that are
                supposed to respond to the multicast. All devices must respond to
                'ALL'. Some devices have device-specific identifiers.
            ipv4_only (bool): default: True
                If true, skip interfacing having IPv6 addresses.
            verbose : boolean, default: True
                If true, provide more information. Useful for troubleshooting.
            one_response_enough : boolean, default: True
                If true, stop scanning interfaces after the first valid response is
                received. Useful when working locally with just a single device.              
        Returns:
            A list of found devices information

        """
        if verbose:
            print("Running UDP locator for identifier {:}".format(identifier))

        host_addr_arr = []

        for addr_info in socket.getaddrinfo(socket.gethostname(), None):
            if ipv4_only and addr_info[0] != socket.AddressFamily.AF_INET:
                continue
            host_addr_arr.append(addr_info[4][0])

        host_addr_arr.append('127.0.0.1')

        if verbose:
            print("Host address list: {:}".format(host_addr_arr))

        unique_devices = []
        unique_guid = set()
        for host_addr in host_addr_arr:
            if verbose:
                print("Trying from host address {:}...".format(host_addr))

            # Create a UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            message = (identifier + '?').encode('UTF-8')

            # Send data both to multicast address and to localhost
            # localhost is for cases when server and client applications are
            # running on the same PC, and PC might be not connected to the
            # network

            if host_addr.split('.')[0] != '127':
                sock.bind((host_addr, 0))
                sock.sendto(message, ('239.0.0.181', 7415))
            else:
                # Works as loopback broadcast for reused sockets
                sock.sendto(message, ('127.255.255.255', 7415))

            devices = []
            while True:
                sock.settimeout(2.0)
                try:
                    data, sender = sock.recvfrom(4096)
                except socket.timeout:
                    break
                except Exception:
                    print("An exception occurred during socket operation")
                    break

                try:
                    description = json.loads(data.decode('UTF8'))
                    description['IpAddress'] = sender[0]

                    if 'SenderGuid' in description.keys():
                        description['SenderGUID'] = description['SenderGuid']
                        del description['SenderGuid']

                    if 'SenderGUID' in description.keys():
                        devices.append(description)

                except json.decoder.JSONDecodeError:
                    print('bad data received by locator')

            sock.close()

            if verbose:
                print("Number of responses: {:}".format(len(devices)))

            # Multiple answers from the same device are possible and certain if
            # the server is located on the same PC. Store sender GUIDs to keep
            # track of responding devices that are unique.
            for obj in devices:
                if obj['SenderGUID'] in unique_guid:
                    continue

                unique_guid.add(obj['SenderGUID'])
                unique_devices.append(obj)

            if verbose:
                print("Total number of devices: {:}".format(
                    len(unique_devices)))

            if one_response_enough and len(unique_devices) > 0:
                if verbose:
                    print("One response is considered enough, skipping the "
                          "remaining interfaces.")
                break

        return unique_devices


if __name__ == '__main__':
    loc = UdpLocator()
    devs = loc.locate('ALL')
