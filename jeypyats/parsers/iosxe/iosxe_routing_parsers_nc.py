#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 23.01.2026 22:58:12
# Author: Jeremie Rouzet
#
# Last Modified: 27.01.2026 20:09:16
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
from ...utils import BASE_RPC
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
        rpc = f'''
            <get-routing-table xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
                <vrf-name>{vrf}</vrf-name>
            </get-routing-table>
        '''
        response = self.netconf_get(rpc)
        xml_data = etree.fromstring(response.xml, parser)
        data_dict = xmltodict.parse(etree.tostring(xml_data))

        # Navigate to routing table entries
        rpc_reply = data_dict.get("rpc-reply", {})
        routing_table = rpc_reply.get("routing-table", {})
        rt_entries = routing_table.get("rt-entry", [])

        # Handle both single entry (dict) and multiple entries (list)
        if isinstance(rt_entries, dict):
            routing_entries = [rt_entries]
        else:
            routing_entries = rt_entries

        parsed_entries = []

        for entry in routing_entries:
            parsed_entry = {
                'prefix': entry.get('destination'),
                'protocol': entry.get('protocol'),
                'next_hop': entry.get('gateway'),
                'metric': entry.get('metric'),
                'interface': entry.get('interface'),
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
        rpc = f'''
            <get-ospf-routes xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
                <vrf-name>{vrf}</vrf-name>
            </get-ospf-routes>
        '''
        response = self.netconf_get(rpc)
        xml_data = etree.fromstring(response.xml, parser)
        data_dict = xmltodict.parse(etree.tostring(xml_data))
        # Navigate to OSPF routes
        ospf_routes_data = data_dict.get("ospf-routes", {})
        ospf_route_entries = ospf_routes_data.get("ospf-route", [])

        # Handle both single route (dict) and multiple routes (list)
        if isinstance(ospf_route_entries, dict):
            ospf_routes = [ospf_route_entries]
        else:
            ospf_routes = ospf_route_entries

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
        rpc = f'''
            <get-bgp-routes xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
                <vrf-name>{vrf}</vrf-name>
            </get-bgp-routes>
        '''
        response = self.netconf_get(rpc)
        xml_data = etree.fromstring(response.xml, parser)
        data_dict = xmltodict.parse(etree.tostring(xml_data))
        # Navigate to BGP routes
        bgp_routes_data = data_dict.get("bgp-routes", {})
        bgp_route_entries = bgp_routes_data.get("bgp-route", [])

        # Handle both single route (dict) and multiple routes (list)
        if isinstance(bgp_route_entries, dict):
            bgp_routes = [bgp_route_entries]
        else:
            bgp_routes = bgp_route_entries

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
        rpc = '''
            <get-routing-table xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
                <vrf-name>default</vrf-name>
            </get-routing-table>
        '''
        response = self.netconf_get(rpc)
        xml_data = etree.fromstring(response.xml, parser)
        data_dict = xmltodict.parse(etree.tostring(xml_data))

        # Navigate to routing table entries
        rpc_reply = data_dict.get("rpc-reply", {})
        routing_table = rpc_reply.get("routing-table", {})
        rt_entries = routing_table.get("rt-entry", [])

        # Handle both single entry (dict) and multiple entries (list)
        if isinstance(rt_entries, dict):
            routing_entries = [rt_entries]
        else:
            routing_entries = rt_entries

        parsed_entries = []

        for entry in routing_entries:
            parsed_entry = {
                'prefix': entry.get('destination'),
                'protocol': entry.get('protocol'),
                'next_hop': entry.get('gateway'),
                'metric': entry.get('metric'),
                'interface': entry.get('interface'),
            }
            parsed_entries.append(parsed_entry)

        return parsed_entries

    def get_routing_table_default_routes(self):
        '''
        Get default route entries from the global routing table
        Returns:
            list: List of default route entries
        Similar cli command:
            show ip route 0.0.0.0 0.0.0.0
        '''
        filter_xml = '''
            <filter>
                <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
                </routing-state>
            </filter>
        '''
        response = self.netconf_get(filter=filter_xml)
        print(f"DEBUG routing: raw response.xml = {response.xml}")  # Debug raw response
        # Remove XML declaration if present
        xml_content = response.xml
        if xml_content.startswith('<?xml'):
            xml_content = xml_content.split('?>', 1)[1].strip()
        xml_data = etree.fromstring(xml_content.encode('utf-8'), parser)
        data_dict = xmltodict.parse(etree.tostring(xml_data))
        print(f"DEBUG routing: data_dict = {data_dict}")  # Debug print

        # Fix interface for default route if None
        routing_state = data_dict.get('rpc-reply', {}).get('data', {}).get('routing-state', {})
        routing_instances = routing_state.get('routing-instance', [])
        if isinstance(routing_instances, list):
            for ri in routing_instances:
                if ri.get('name') == 'default':
                    ribs = ri.get('ribs', {}).get('rib', [])
                    if isinstance(ribs, list):
                        for rib in ribs:
                            if rib.get('name') == 'ipv4-default':
                                routes = rib.get('routes', {}).get('route', [])
                                if isinstance(routes, list):
                                    for route in routes:
                                        if route.get('destination-prefix') == '0.0.0.0/0':
                                            next_hop = route.get('next-hop', {})
                                            if next_hop.get('outgoing-interface') is None:
                                                next_hop_addr = next_hop.get('next-hop-address')
                                                if next_hop_addr:
                                                    # Assume /24 network
                                                    network = '.'.join(next_hop_addr.split('.')[:3]) + '.0/24'
                                                    # Find the route for this network
                                                    for r in routes:
                                                        if r.get('destination-prefix') == network:
                                                            intf = r.get('next-hop', {}).get('outgoing-interface')
                                                            if intf:
                                                                next_hop['outgoing-interface'] = intf
                                                            break

        # Navigate to routing table entries
        try:
            rpc_reply = data_dict.get("rpc-reply", {})
            data = rpc_reply.get("data", {})
            routing_state = data.get("routing-state", {})
            routing_instances = routing_state.get("routing-instance", [])

            # Find the default routing instance
            routing_instance = None
            if isinstance(routing_instances, list):
                for ri in routing_instances:
                    if ri.get("name") == "default":
                        routing_instance = ri
                        break
            elif isinstance(routing_instances, dict):
                if routing_instances.get("name") == "default":
                    routing_instance = routing_instances

            if routing_instance is None:
                return []

            ribs = routing_instance.get("ribs", {})
            rib_list = ribs.get("rib", [])

            # Find the ipv4-default rib
            rib = None
            if isinstance(rib_list, list):
                for r in rib_list:
                    if r.get("name") == "ipv4-default":
                        rib = r
                        break
            elif isinstance(rib_list, dict):
                if rib_list.get("name") == "ipv4-default":
                    rib = rib_list

            if rib is None:
                return []

            routes = rib.get("routes", {})
            route_entries = routes.get("route", [])

            # Handle both single entry (dict) and multiple entries (list)
            if isinstance(route_entries, dict):
                routing_entries = [route_entries]
            else:
                routing_entries = route_entries

            parsed_entries = []

            for entry in routing_entries:
                if entry.get('destination-prefix') == '0.0.0.0/0':
                    next_hop = entry.get('next-hop', {})
                    parsed_entry = {
                        'prefix': entry.get('destination-prefix'),
                        'protocol': entry.get('source-protocol'),
                        'next_hop': next_hop.get('next-hop-address') if next_hop else None,
                        'metric': entry.get('metric'),
                        'interface': next_hop.get('outgoing-interface') if next_hop else None,
                    }
                    parsed_entries.append(parsed_entry)

            return parsed_entries
        except (KeyError, TypeError):
            # If the expected structure is not found, return empty list
            return []

    def get_routing_table_default_routes(self):
        """
        Retrieve default routes via NETCONF by getting all routes and filtering for 0.0.0.0/0.
        Returns list of dicts with prefix, protocol, next_hop, metric, interface
        """
        try:
            all_routes = self.get_routing_table(vrf='default')
            logger.debug(f"All routes: {all_routes}")
            default_routes = [route for route in all_routes if route.get('prefix') == '0.0.0.0/0']
            logger.info(f"Default routes found: {default_routes}")
            return default_routes
        except Exception as e:
            logger.error(f"Failed to retrieve default routes via NETCONF: {e}")
            return []

    @classmethod
    def bind_to_device(cls, device):
        setattr(device, 'get_routing_table_default_routes', cls.get_routing_table_default_routes.__get__(device, type(device)))
