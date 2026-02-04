#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: third_script_v1.0.py
# This file is a part of Netalps.fr
#
# Created: 2025/01/28 11:14:20
# Author: Jeremie Rouzet
#
# Last Modified: 27.01.2026 19:39:40
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################

# New module! Now using Genie!
from genie import testbed
import json
import yaml
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='L2VPN Bridge Domain Brief NCC Script')
    parser.add_argument('--testbed',
                       default='../testbed/xrd/xrd_sw_tb_v1.0_ncc.yaml',
                       help='Path to the testbed YAML file')
    args = parser.parse_args()

    # Step 0: load the testbed
    testbed_file = args.testbed
    if not os.path.exists(testbed_file):
        print(f"Error: Testbed file {testbed_file} not found")
        return

testbed_obj = testbed.load(testbed_file)

    # Step 1: testbed is a dictionary. Extract the device clab-jeylab_v0.1-jeylab-iosxrd-cr-01
    device = testbed_obj.devices["jeylab-iosxrd-cr-01"]

    # Step 2: Connect to the device
    device.connect(log_stdout=True, connection_timeout=30)

    # Step 3: saving the `show l2vpn bridge-domain brief` output in a variable
    show_l2vpn_bd_brief = device.parse("""
<?xml version="1.0" encoding="UTF-8"?>
<rpc message-id="103" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <get>
    <filter type="subtree">
      <l2vpn xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-l2vpn-oper">
        <database>
          <bridge-domains/>
        </database>
      </l2vpn>
    </filter>
  </get>
</rpc>
""")
    print(show_l2vpn_bd_brief)

    # Step 5: disconnect from the device
    device.disconnect()


if __name__ == "__main__":
    main()
