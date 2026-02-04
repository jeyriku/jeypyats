#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: __init__.py
# This file is a part of Netalps.fr
#
# Created: 2025/06/25 13:41:04
# Author: Jeremie Rouzet
#
# Last Modified: 27.01.2026 18:31:20
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

from .utils import *
from .rpc_msgs import BASE_RPC, BASE_RPC_RPC, RPC_OK_MSG, RPC_EMPTY_MSG
from .netconf_connector import connect_netconf
