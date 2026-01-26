#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: main.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/24 13:41:04
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 13:41:04
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

from tests.connectivity_test import ConnectivityTest

if __name__ == "__main__":
    file_yaml = "sw_tb_v1.0.yaml"
    test = ConnectivityTest(file_yaml)
    test.check_connectivity()