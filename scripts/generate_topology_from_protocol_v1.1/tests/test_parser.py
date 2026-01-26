#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: test_parser.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/24 14:44:14
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 14:44:14
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

from utils.parser import parse_neighbors

def test_parse_neighbors():
    output = """
    Device ID       Local Intf      Port ID
    Switch1         Gi1/0/1         Gi1/0/2
    Router1         Gi1/0/2         Gi0/1
    """
    expected = [
        {"device": "Switch1", "interface": "Gi1/0/1"},
        {"device": "Router1", "interface": "Gi1/0/2"},
    ]
    assert parse_neighbors(output) == expected
