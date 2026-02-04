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
# Last Modified: 27.01.2026 18:51:29
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

import xmltodict
from genie.utils import Dq
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ...utils import sanitize_xml
from ...utils import BASE_RPC


class ParsersMixin:
    """Mixin class containing parsing methods for IOS-XE devices"""

    def get_l2vpn_bridge_domain_brief(self):
        """
        Retrieve L2VPN bridge domain brief information via NETCONF.

        Returns:
            dict: Dictionary containing bridge domain information
        """
        xml_rpc = """
        <l2vpnv2 xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-l2vpn-oper">
          <nodes>
            <node>
              <node-id>0/RP0/CPU0</node-id>
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

        rpc_msg = BASE_RPC.format(xml_rpc=xml_rpc)
        rpc_msg = sanitize_xml(rpc_msg)

        reply = self.request(msg=rpc_msg, return_obj=True)

        if not reply.ok:
            return {}

        # Parse the XML response
        reply_dict = xmltodict.parse(reply.xml)

        # Extract bridge domain information
        result = {}
        rpc_reply = reply_dict.get("rpc-reply")
        if not rpc_reply:
            return result
        data = rpc_reply.get("data")
        if data is None or not isinstance(data, dict):
            return result
        l2vpn_data = data.get("l2vpnv2", {}).get("nodes", {}).get("node", {}).get("bridge-domains") or {}
        l2vpn_data = l2vpn_data.get("bridge-domain", []) if isinstance(l2vpn_data, dict) else []

        # Handle case where bridge-domains might be None or missing
        if l2vpn_data is None:
            bridge_domains = []
        elif isinstance(l2vpn_data, list):
            bridge_domains = l2vpn_data
        else:
            # Single bridge domain
            bridge_domains = [l2vpn_data]

        for bd in bridge_domains:
            if isinstance(bd, dict):
                bd_name = bd.get("bridge-domain-name")
                bd_info = bd.get("bridge-domain-info", {})
                bd_state = bd_info.get("bridge-state")

                if bd_name and bd_state:
                    result[bd_name] = {"state": bd_state}

        return result
