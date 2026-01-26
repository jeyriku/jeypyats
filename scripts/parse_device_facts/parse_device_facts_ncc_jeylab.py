#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: parse_device_version.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/28 11:19:12
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/28 11:19:12
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

# New module! Now using Genie!
from genie import testbed
import xmltodict
from lxml import etree

# Step 0: load the testbed
testbed = testbed.load('./sw_tb_ncc_v1.0_clab.yaml')

# Step 1: testbed is a dictionary. Extract the device core-nw
device = testbed.devices["jeylab-iosxrd-cr-01"]
print()
print(device)

# Step 2: Connect to the device using Netconf
device.connect(via='netconf', log_stdout=True, connection_timeout=10)

# Step 3: If connection succeeds display the following message
if device.netconf.connected:
    print()
    print("NETCONF connection established")
    print()

# Step 4: Display target devices Netconf capabilities
if device.netconf.connected:
    print("Server Capabilities:")
    print("\n".join(device.netconf.server_capabilities))

# Step 5: saving the `show l2vpn bridge-domain brief` output in a variable
rpc_request = """
<l2vpnv2 xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-l2vpn-oper">
    <nodes>
        <node>
            <bridge-domains>
                <bridge-domain>
                    <bridge-domain-info>
                        <bridge-state/>
                    </bridge-domain-info>
                </bridge-domain>
            </bridge-domains>
        </node>
    </nodes>
</l2vpnv2>
"""
# Step 6: Send the RPC request to the device and get the reply
reply_xml = device.netconf.get(('subtree', rpc_request))
print()
print("Type of reply_xml:", type(reply_xml))
print()
print("Content of reply_xml:\n\n", reply_xml)
print()

# Step 7: Use the data_xml attribute to get the XML content
reply_xml_content = reply_xml.data_xml
print("Content of reply_xml.data_xml:\n\n", reply_xml_content)

# Step 8: Parse the XML content into a Python dictionary
if reply_xml_content:
    reply = xmltodict.parse(reply_xml_content)
    print(reply)
else:
    print("Failed to get a valid XML response")
print()
# Step 9: Check if the original XML request is well-formed
try:
    etree.fromstring(rpc_request.encode('utf-8'))
    print("✅ XML is well-formed!")
except etree.XMLSyntaxError as e:
    print("❌ XML Syntax Error:", e)
print()
# Step 10: disconnect from the device
device.disconnect()

'''
The provided code snippet is part of a Python script that interacts with a network device using the NETCONF protocol to retrieve information about Layer 2 VPN (L2VPN) bridge domains. 

The script constructs an XML RPC request to query the device for bridge domain information.

First, an XML string `rpc_request` is defined, which specifies the structure of the request. 

This XML string includes the namespace for Cisco IOS XR L2VPN operational data and requests information about bridge domains within the device.

The script then sends this RPC request to the device using the `device.netconf.get` method, which retrieves the response from the device. 

The response is stored in the `reply_xml` variable. The script prints the type and content of `reply_xml` to the console for verification.

Next, the script extracts the actual XML content from the `reply_xml` object using the `data_xml` attribute and stores it in the `reply_xml_content` variable. 

It prints the content of `reply_xml_content` to the console.

If `reply_xml_content` is not empty, the script parses the XML content into a Python dictionary using the `xmltodict.parse` method and prints the resulting dictionary. 

If the content is empty, it prints an error message indicating that a valid XML response was not received.

The script then checks if the original `rpc_request` XML string is well-formed by attempting to parse it using `etree.fromstring`. 

If the XML is well-formed, it prints a success message; otherwise, it catches the `XMLSyntaxError` exception and prints an error message with details about the syntax error.

Finally, the script disconnects from the device using the `device.disconnect` method, ensuring that the connection is properly closed.

'''