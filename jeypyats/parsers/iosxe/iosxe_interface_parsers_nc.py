#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 23.01.2026 22:58:12
# Author: Jeremie Rouzet
#
# Last Modified: 28.01.2026 16:33:57
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Pyats IOS XE Interface parsers using Netconf
This module contains parsers to retrieve interface status from IOS XE devices via Netconf.
It includes functions to get interface status using both OpenConfig and Cisco IOS XE YANG models.
The parsers utilize XML filters to query the device and parse the XML responses into structured data.
Each function is designed to handle specific YANG models and return relevant information in a user-friendly format.
The module leverages the Genie and lxml libraries for XML parsing and data extraction.
'''
import logging
import xmltodict
from genie.utils import Dq
from lxml import etree
from ...utils import BASE_RPC
from packaging import version
import json



logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

parser = etree.XMLParser()
parser.set_element_class_lookup(
    etree.ElementDefaultClassLookup(element=etree.ElementBase)
)

class IOSXEInterfacesParsersMixin:
    """ Parsers for IOS XE Interfaces using Netconf """

    def get_interfaces_status_openconfig(self, interface_name=None):
        """ Get interface status using OpenConfig YANG model

            Args:
                interface_name (str, optional): Specific interface name to query. If None, all interfaces are queried.

            Returns:
                dict: Parsed interface status information.
        """
        logger.info("Retrieving interface status using OpenConfig model")
        filter = """
            <filter>
                <interfaces xmlns="http://openconfig.net/yang/interfaces">
                    <interface>
                        {interface_name}
                    </interface>
                </interfaces>
            </filter>
        """.format(
            interface_name=f"<name>{interface_name}</name>" if interface_name else ""
        )

        response = self.netconf_get(filter=filter)
        xml_data = etree.fromstring(response.xml, parser)

        interfaces_data = xmltodict.parse(etree.tostring(xml_data))['rpc-reply']['data']['interfaces']['interface']
        if not isinstance(interfaces_data, list):
            interfaces_data = [interfaces_data]

        result = {}
        for intf in interfaces_data:
            name = intf['name']
            oper_status = intf.get('state', {}).get('oper-status', 'unknown')
            admin_status = intf.get('state', {}).get('admin-status', 'unknown')
            result[name] = {
                'oper_status': oper_status,
                'admin_status': admin_status
            }

        logger.info("Interface status retrieved successfully")
        return result

    def get_interfaces_cellular_status(self, interface_name=None):
        """ Get cellular interface status using Cisco IOS XE YANG model

            Args:
                interface_name (str, optional): Specific cellular interface name to query. If None, all cellular interfaces are queried.

            Returns:
                dict: Parsed cellular interface status information.
        """
        logger.info("Retrieving cellular interface status using Cisco IOS XE model")
        filter = """
            <filter>
                <interfaces-state xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
                    <interface>
                        {interface_name}
                    </interface>
                </interfaces-state>
            </filter>
        """.format(
            interface_name=f"<name>{interface_name}</name>" if interface_name else ""
        )

        response = self.netconf_get(filter=filter)
        xml_data = etree.fromstring(response.xml, parser)

        interfaces_data = xmltodict.parse(etree.tostring(xml_data))['rpc-reply']['data']['interfaces-state']['interface']
        if not isinstance(interfaces_data, list):
            interfaces_data = [interfaces_data]

        result = {}
        for intf in interfaces_data:
            name = intf['name']
            if 'Cellular' in name:
                oper_status = intf.get('oper-status', 'unknown')
                admin_status = intf.get('admin-status', 'unknown')
                result[name] = {
                    'oper_status': oper_status,
                    'admin_status': admin_status
                }

        logger.info("Cellular interface status retrieved successfully")
        return result

    def get_interface_status(self, interface):
        """ Get status of a specific interface

            Args:
                interface (str): Interface name to query.

            Returns:
                dict: Parsed interface status information.
        """
        logger.info(f"Retrieving status for interface {interface}")
        filter_xml = """
            <filter>
                <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                </interfaces-state>
            </filter>
        """

        response = self.netconf_get(filter=filter_xml)
        # Remove XML declaration if present
        xml_content = response.xml
        if xml_content.startswith('<?xml'):
            xml_content = xml_content.split('?>', 1)[1].strip()
        xml_data = etree.fromstring(xml_content.encode('utf-8'), parser)

        data_dict = xmltodict.parse(etree.tostring(xml_data))
        if 'rpc-reply' not in data_dict or 'data' not in data_dict['rpc-reply'] or data_dict['rpc-reply']['data'] is None:
            return {'oper_status': 'unknown', 'admin_status': 'unknown'}

        interfaces_state = data_dict['rpc-reply']['data'].get('interfaces-state', {})
        interfaces = interfaces_state.get('interface', [])

        # Handle single interface (dict) or multiple (list)
        if isinstance(interfaces, dict):
            interfaces = [interfaces]

        logger.info(f"DEBUG: interfaces found: {json.dumps(interfaces, indent=2)}")

        for intf in interfaces:
            if intf.get('name') == interface:
                oper_status = intf.get('oper-status', 'unknown')
                admin_status = intf.get('admin-status', 'unknown')
                result = {
                    'oper_status': oper_status,
                    'admin_status': admin_status
                }
                logger.info(f"Interface {interface} status retrieved successfully")
                return result

        # Interface not found
        return {'oper_status': 'unknown', 'admin_status': 'unknown'}

    @classmethod
    def bind_to_device(cls, device):
        setattr(device, 'get_interface_status', cls.get_interface_status.__get__(device, type(device)))
