#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: rpc_msgs.py
# This file is a part of Netalps.fr
#
# Created: 2025/06/25 13:41:04
# Author: Jeremie Rouzet
#
# Last Modified: 26.01.2026 13:59:23
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Predefined RPC message templates for NETCONF operations
This module contains XML templates for common NETCONF RPC messages,
including OK responses, empty data responses, and a base RPC structure.
These templates can be used to construct or validate NETCONF messages.
It helps standardize the format of RPC messages used in NETCONF communications.
It is useful for developers working with NETCONF-enabled devices.
'''

RPC_OK_MSG = """
<rpc-reply xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:a29a7ad2-4c0c-4508-a9d7-6f1206ef346f">
 <ok/>
</rpc-reply>"""

RPC_EMPTY_MSG = """
<rpc-reply xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:d4eeac17-67ba-4358-8f08-c82fafe3ea37">
 <data/>
</rpc-reply>
"""

BASE_RPC = """
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <get>
    <filter>
    {xml_rpc}
    </filter>
  </get>
</rpc>
"""
