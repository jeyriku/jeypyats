#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: netconf_connector.py
# This file is a part of Netalps.fr
#
# Created: 2025/06/25 13:41:04
# Author: Jeremie Rouzet
#
# Last Modified: 29.01.2026 23:42:07
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Utility module for establishing NETCONF connections using ncclient
This module provides a function to connect to a NETCONF-enabled device.
It uses the ncclient library to manage the connection.
It handles connection errors and logs them appropriately.
'''

import logging
from ncclient import manager
from pyats.connections import BaseConnection


def connect_netconf(host, port, username, password, device_params=None):
    try:
        return manager.connect(
            host=str(host),
            port=port,
            username=username,
            password=password,
            hostkey_verify=False,
            allow_agent=False,
            look_for_keys=False,
            timeout=30
        )
    except Exception as e:
        logging.error(f"Failed to connect to {host}: {e}")
        return None

class NetconfConnectorConnection(BaseConnection):
    """Custom NETCONF connection class using ncclient directly."""

    def __init__(self, device=None, alias=None, via=None, **kwargs):
        if device is not None:
            self.device = device
        if alias is not None:
            self.alias = alias
        self._connection_info = kwargs
        self.nc = None
        self._connected = False
        if device is not None or alias is not None:
            super().__init__(device=device, alias=alias, via=via)

    @property
    def connected(self):
        return self._connected
    def connect(self):
        import os
        user = os.getenv('PYATS_USER')
        password = os.getenv('PYATS_PASSWORD')
        if not user or not password:
            raise Exception("PYATS_USER and PYATS_PASSWORD environment variables must be set")
        ip = self.connection_info['ip']
        port = self.connection_info['port']
        self.nc = connect_netconf(ip, port, user, password)
        if not self.nc:
            raise Exception("Failed to connect to NETCONF")
        self._connected = True
        # Set device.nc for easy access
        if hasattr(self, 'device') and self.device:
            self.device.nc = self.nc
            self.device.netconf_get = lambda filter=None: self.nc.get(filter=filter) if filter else None

    def disconnect(self):
        if self.nc:
            self.nc.close()
            self.nc = None
        self._connected = False
