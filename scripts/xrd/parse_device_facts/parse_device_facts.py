#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: parse_device_version.py
# This file is a part of Netalps.fr
#
# Created: 2025/01/28 11:19:12
# Author: Jeremie Rouzet
#
# Last Modified: 27.01.2026 19:42:45
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################

# New module! Now using Genie!
from genie import testbed
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Parse Device Facts Script')
    parser.add_argument('--testbed',
                       default='../testbed/xrd/xrd_sw_tb_v1.0.yaml',
                       help='Path to the testbed YAML file')
    args = parser.parse_args()

    # Step 0: load the testbed
    testbed_file = args.testbed
    if not os.path.exists(testbed_file):
        print(f"Error: Testbed file {testbed_file} not found")
        return

    testbed = testbed.load(testbed_file)

    # Step 1: testbed is a dictionary. Extract the device iosxr1
    device = testbed.devices["ipt-bei922-g-cme-01"]

    # Step 2: Connect to the device
    device.connect(init_exec_commands=[], init_config_commands=[], log_stdout=False)

    # Step 3: saving the `show ip interface brief` output in a variable
    show_interface = device.parse('show ip interface brief')

    # Step 4: saving the `show ip interface brief` output in a variable
    show_version = device.parse('show version')

    # Step 5: iterating through the parsed output. Extracting interface name and IP
    for interface, details in show_interface['interface'].items():
        print(f"{interface} -- {details['ip_address']}")

    # Step 6: iterating through the parsed output. Extracting software version
    print()
    print(f"Operating System: {show_version['operating_system']}")
    print(f"Software Version: {show_version['software_version']}")
    print()
    #or
    print()
    print(f"Operating System: {show_version['operating_system']}\nSoftware Version: {show_version['software_version']}")
    print()
    # Step 7: disconnect from the device
    device.disconnect()

if __name__ == "__main__":
    main()
