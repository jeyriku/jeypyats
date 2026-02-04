#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: xrd_interface_parser.py
# This file is a part of Netalps.fr
#
# Created: 2025/06/25 13:41:04
# Author: Jeremie Rouzet
#
# Last Modified: 27.01.2026 18:44:08
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Parser for retrieving interface status via Netconf using Cisco IOS XR YANG models.
'''

import logging
import xmltodict
import pprint
from genie.utils import Dq
from lxml import etree
from ...utils import BASE_RPC


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

parser = etree.XMLParser()
parser.set_element_class_lookup(
    etree.ElementDefaultClassLookup(element=etree.ElementBase)
)

def get_interface_status_xr(self):
    """
    Retrieve the status of a specified network interface via Netconf
    """
    xml_rpc = """
    <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-pfi-im-cmd-oper">
        <interface-xr>
            <interface>
                <interface-name/>
                <description/>
                <line-state/>
                <state/>
            </interface>
        </interface-xr>
    </interfaces>
    """
    filter_xml = f"""
      <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" type="subtree">
        {xml_rpc}
      </filter>
    """
    filter_element = etree.fromstring(filter_xml, parser)
    get_element = etree.Element("{urn:ietf:params:xml:ns:netconf:base:1.0}get")
    get_element.append(filter_element)
    logger.info(f"Envoi de la requête NETCONF:\n{etree.tostring(get_element, pretty_print=True).decode()}")
    reply = self.dispatch(get_element)
    logger.info(f"Réponse reçue: {reply.xml}")
    reply_dict = xmltodict.parse(reply.xml)
    if not reply.ok or not reply_dict.get("rpc-reply", {}).get("data"):
        return []
    logger.info(f"Full parsed RPC reply:\n{pprint.pformat(reply_dict, indent=2)}")
    # Navigate to the interface data
    data = reply_dict.get("rpc-reply", {}).get("data", {})
    interfaces_data = data.get("interfaces", {}).get("interface-xr", {}).get("interface", [])

    # Handle both single interface (dict) and multiple interfaces (list)
    if isinstance(interfaces_data, dict):
        interfaces = [interfaces_data]
    else:
        interfaces = interfaces_data

    logger.info(f"The interfaces data:\n{pprint.pformat(interfaces, indent=2)}")
    results = []
    for intf in interfaces:
        ifstate = intf.get("state")
        ifname = intf.get("interface-name")
        results.append({
            "interface-name": ifname,
            "state": ifstate
        })
    return results
