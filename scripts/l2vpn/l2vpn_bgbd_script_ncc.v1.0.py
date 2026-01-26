#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: third_script_v1.0.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/28 11:14:20
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/28 11:14:20
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

# New module! Now using Genie!
from genie import testbed
import json
import yaml

# Step 0: load the testbed
testbed = testbed.load('./sw_tb_v1.0_ncc.yaml')

# Step 1: testbed is a dictionary. Extract the device clab-jeylab_v0.1-jeylab-iosxrd-cr-01
device = testbed.devices["jeylab-iosxrd-cr-01"]

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
