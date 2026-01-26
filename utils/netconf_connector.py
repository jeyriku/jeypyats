#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: netconf_connector.py
# This file is a part of Netalps.fr
#
# Created: 2025/06/25 13:41:04
# Author: Jeremie Rouzet
#
# Last Modified: 26.01.2026 13:58:38
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


def connect_netconf(host, port, username, password, device_params=None):
    try:
        return manager.connect(
            host=host,
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
