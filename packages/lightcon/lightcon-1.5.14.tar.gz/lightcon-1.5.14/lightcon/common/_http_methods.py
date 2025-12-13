#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""lightcon - a Python library for controlling Light Conversion devices.

HTTP methods class, which implements REST communication.

Copyright 2020-2024 Light Conversion
Contact: support@lightcon.com
"""
import json
import urllib
import urllib.error
import urllib.request
import urllib.parse
import time
import http


def print_timer(cmd, time_from):
    """Print elapsed time for command in ms."""
    print(cmd + " : {:.3f} ms".format((time.perf_counter() - time_from)*1E3))


class HTTP_methods:
    """Base class for REST clients"""
    url = None
    silent = True
    retry_on_incomplete_read = True
    print_full_http_response_on_failure = True

    def _open(self, page_url):
        return urllib.request.urlopen(self.url+page_url).read().decode('utf-8')

    def _get(self, command):
        time_init = time.perf_counter()
        cont = True

        while cont:
            try:
                data = json.loads(urllib.request.urlopen(
                    self.url+command).read().decode('utf-8'))
                cont = False
            except urllib.error.HTTPError as e:
                error_string = e.read().decode('utf-8', 'ignore')
                print(error_string)
                return error_string
            except http.client.IncompleteRead:
                cont = True and self.retry_on_incomplete_read
                if not self.silent:
                    print('Incomplete read')

        if not self.silent:
            print_timer(command, time_init)
        return data

    def _put(self, command, data):
        time_init = time.perf_counter()
        try:
            post_url = urllib.request.Request(
                url=self.url+command, data=data.encode('utf-8'), method='PUT')

            post_url.add_header('Content-Type', 'application/json')

            with urllib.request.urlopen(post_url) as f:
                pass
            if not self.silent:
                print_timer(command, time_init)
            return f.status
        except urllib.error.HTTPError as e:
            print("Exception while PUT to {:} with data {:}".format(post_url.full_url, data))
            error_string = e.read().decode('utf-8', 'ignore')
            if self.print_full_http_response_on_failure:
                print(error_string)
            return error_string

    def _post(self, command, details={}):
        time_init = time.perf_counter()
        try:
            post_details = urllib.parse.urlencode(details).encode('UTF-8')

            post_url = urllib.request.Request(self.url+command, post_details)

            res = urllib.request.urlopen(post_url).read().decode('utf-8', 'ignore')
        except urllib.error.HTTPError as e:
            error_string = e.read().decode('utf-8', 'ignore')
            print(error_string)
            return error_string

        if not self.silent:
            print(command + " : {:.3f} ms".format((time.perf_counter()-time_init)*1000))
        return res

    def _report(self, command, data={}):
        time_init = time.perf_counter()
        try:
            req = urllib.request.Request(
                url=self.url+command, data=data.encode('utf-8'),
                method='REPORT')

            req.add_header('Content-Type', 'application/json')

            res = json.loads(
                urllib.request.urlopen(req).read().decode('utf-8', 'ignore'))
        except urllib.error.HTTPError as e:
            error_string = e.read().decode('utf-8', 'ignore')
            print(error_string)
            return error_string

        if not self.silent:
            print_timer(command, time_init)
        return res
