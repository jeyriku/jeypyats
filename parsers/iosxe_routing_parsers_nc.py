#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 23.01.2026 22:58:12
# Author: Jeremie Rouzet
#
# Last Modified: 26.01.2026 13:55:16
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Pyats IOS XE Routing parsers using Netconf
This module contains parsers to retrieve routing information from Cisco IOS XE devices via Netconf.
It includes functions to get routing table entries, OSPF routes, and BGP routes.
The parsers utilize XML filters to query the device and parse the XML responses into structured data.
Each function is designed to handle specific routing protocols and return relevant information in a user-friendly format.
The module leverages the Genie and lxml libraries for XML parsing and data extraction.
'''
import logging
import xmltodict
from genie.utils import Dq
from lxml import etree
from utils.rpc_msgs import BASE_RPC
from packaging import version



logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

parser = etree.XMLParser()
parser.set_element_class_lookup(
    etree.ElementDefaultClassLookup(element=etree.ElementBase)
)

class IOSXERoutingParsersMixin:
    '''
    Collection of RPCs for parsing routing information on IOS-XE devices
    '''
    def get_routing_table(self, vrf='default'):
        '''
        Get routing table entries for a specified VRF
        Args:
            vrf (str): VRF name (default is 'default')
        Returns:
            dict: Parsed routing table entries
        Similar cli command:
            show ip route vrf {vrf}
        '''
        rpc = BASE_RPC + f'''
            <get-routing-table xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
                <vrf-name>{vrf}</vrf-name>
            </get-routing-table>
        '''
        response = self.netconf_get(rpc)
        xml_response = etree.fromstring(response.xml, parser=parser)
        xml_str = etree.tostring(xml_response, encoding='utf-8').decode('utf-8')
        data_dict = xmltodict.parse(xml_str)
        dq = Dq(data_dict)

        routing_entries = dq.get_values('rt-entry', default=[])
        parsed_entries = []

        for entry in routing_entries:
            parsed_entry = {
                'prefix': entry.get('prefix'),
                'protocol': entry.get('protocol-name'),
                'next_hop': entry.get('nh', {}).get('address'),
                'metric': entry.get('metric'),
                'interface': entry.get('interface-name'),
            }
            parsed_entries.append(parsed_entry)

        return parsed_entries

    def get_ospf_routes(self, vrf='default'):
        '''
        Get OSPF routes for a specified VRF
        Args:
            vrf (str): VRF name (default is 'default')
        Returns:
            dict: Parsed OSPF routes
        Similar cli command:
            show ip ospf route vrf {vrf}
        '''
        rpc = BASE_RPC + f'''
            <get-ospf-routes xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
                <vrf-name>{vrf}</vrf-name>
            </get-ospf-routes>
        '''
        response = self.netconf_get(rpc)
        xml_response = etree.fromstring(response.xml, parser=parser)
        xml_str = etree.tostring(xml_response, encoding='utf-8').decode('utf-8')
        data_dict = xmltodict.parse(xml_str)
        dq = Dq(data_dict)

        ospf_routes = dq.get_values('ospf-route', default=[])
        parsed_routes = []

        for route in ospf_routes:
            parsed_route = {
                'prefix': route.get('prefix'),
                'area': route.get('area-id'),
                'next_hop': route.get('next-hop'),
                'metric': route.get('metric'),
            }
            parsed_routes.append(parsed_route)

        return parsed_routes

    def get_bgp_routes(self, vrf='default'):
        '''
        Get BGP routes for a specified VRF
        Args:
            vrf (str): VRF name (default is 'default')
        Returns:
            dict: Parsed BGP routes
        Similar cli command:
            show ip bgp vrf {vrf}
        '''
        rpc = BASE_RPC + f'''
            <get-bgp-routes xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
                <vrf-name>{vrf}</vrf-name>
            </get-bgp-routes>
        '''
        response = self.netconf_get(rpc)
        xml_response = etree.fromstring(response.xml, parser=parser)
        xml_str = etree.tostring(xml_response, encoding='utf-8').decode('utf-8')
        data_dict = xmltodict.parse(xml_str)
        dq = Dq(data_dict)

        bgp_routes = dq.get_values('bgp-route', default=[])
        parsed_routes = []

        for route in bgp_routes:
            parsed_route = {
                'prefix': route.get('prefix'),
                'next_hop': route.get('next-hop'),
                'as_path': route.get('as-path'),
                'local_pref': route.get('local-pref'),
            }
            parsed_routes.append(parsed_route)

        return parsed_routes

    def get_routing_table_global(self):
        '''
        Get global routing table entries
        Returns:
            dict: Parsed global routing table entries
        Similar cli command:
            show ip route
        '''
        rpc = BASE_RPC + '''
            <get-routing-table xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
                <vrf-name>default</vrf-name>
            </get-routing-table>
        '''
        response = self.netconf_get(rpc)
        xml_response = etree.fromstring(response.xml, parser=parser)
        xml_str = etree.tostring(xml_response, encoding='utf-8').decode('utf-8')
        data_dict = xmltodict.parse(xml_str)
        dq = Dq(data_dict)

        routing_entries = dq.get_values('rt-entry', default=[])
        parsed_entries = []

        for entry in routing_entries:
            parsed_entry = {
                'prefix': entry.get('prefix'),
                'protocol': entry.get('protocol-name'),
                'next_hop': entry.get('nh', {}).get('address'),
                'metric': entry.get('metric'),
                'interface': entry.get('interface-name'),
            }
            parsed_entries.append(parsed_entry)

        return parsed_entries
