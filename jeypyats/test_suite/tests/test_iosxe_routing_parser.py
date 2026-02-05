#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: test_iosxe_routing_parser.py
# This file is a part of Netalps.fr
#
# Created: 27.01.2026 18:45:00
# Author: GitHub Copilot
#
# Last Modified: 27.01.2026 18:42:29
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

import unittest
from unittest.mock import MagicMock, patch
from jeypyats.parsers.iosxe.iosxe_routing_parsers_nc import IOSXERoutingParsersMixin


class TestIOSXERoutingParser(unittest.TestCase):
    """Unit tests for IOS-XE routing parsers"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_device = MagicMock()

    @patch('jeypyats.parsers.iosxe.iosxe_routing_parsers_nc.logger')
    def test_get_routing_table_success(self, mock_logger):
        """Test successful routing table retrieval"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <routing-table xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
                <rt-entry>
                    <destination>0.0.0.0/0</destination>
                    <gateway>192.168.1.1</gateway>
                    <interface>GigabitEthernet0/0</interface>
                    <protocol>static</protocol>
                </rt-entry>
                <rt-entry>
                    <destination>192.168.1.0/24</destination>
                    <gateway>directly connected</gateway>
                    <interface>GigabitEthernet0/0</interface>
                    <protocol>connected</protocol>
                </rt-entry>
            </routing-table>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXERoutingParsersMixin.get_routing_table(self.mock_device, 'default')

        # Verify the call was made
        self.mock_device.netconf_get.assert_called_once()
        self.assertIsInstance(result, list)

    @patch('jeypyats.parsers.iosxe.iosxe_routing_parsers_nc.logger')
    def test_get_routing_table_custom_vrf(self, mock_logger):
        """Test routing table retrieval with custom VRF"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <routing-table xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
                <rt-entry>
                    <destination>10.0.0.0/8</destination>
                    <gateway>192.168.2.1</gateway>
                    <interface>GigabitEthernet0/1</interface>
                    <protocol>ospf</protocol>
                </rt-entry>
            </routing-table>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXERoutingParsersMixin.get_routing_table(self.mock_device, 'CUSTOM_VRF')

        # Verify the call was made with correct VRF
        self.mock_device.netconf_get.assert_called_once()
        call_args = self.mock_device.netconf_get.call_args[0][0]
        self.assertIn('<vrf-name>CUSTOM_VRF</vrf-name>', call_args)
        self.assertIsInstance(result, list)

    @patch('jeypyats.parsers.iosxe.iosxe_routing_parsers_nc.logger')
    def test_get_routing_table_global_success(self, mock_logger):
        """Test successful global routing table retrieval"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <routing-table xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
                <rt-entry>
                    <destination>192.168.1.0/24</destination>
                    <gateway>directly connected</gateway>
                    <interface>GigabitEthernet0/0</interface>
                    <protocol>connected</protocol>
                </rt-entry>
                <rt-entry>
                    <destination>172.16.0.0/16</destination>
                    <gateway>192.168.1.254</gateway>
                    <interface>GigabitEthernet0/0</interface>
                    <protocol>static</protocol>
                </rt-entry>
            </routing-table>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXERoutingParsersMixin.get_routing_table_global(self.mock_device)

        # Verify the call was made and result is a list
        self.mock_device.netconf_get.assert_called_once()
        self.assertIsInstance(result, list)
        # Should parse the routing entries
        self.assertGreater(len(result), 0)

    @patch('jeypyats.parsers.iosxe.iosxe_routing_parsers_nc.logger')
    def test_get_ospf_routes_success(self, mock_logger):
        """Test successful OSPF routes retrieval"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <ospf-routes xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf-oper">
                <route>
                    <destination>10.0.0.0/8</destination>
                    <next-hop>192.168.1.2</next-hop>
                    <interface>GigabitEthernet0/0</interface>
                    <metric>10</metric>
                </route>
                <route>
                    <destination>10.1.0.0/16</destination>
                    <next-hop>192.168.1.3</next-hop>
                    <interface>GigabitEthernet0/1</interface>
                    <metric>15</metric>
                </route>
            </ospf-routes>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXERoutingParsersMixin.get_ospf_routes(self.mock_device, 'default')

        self.mock_device.netconf_get.assert_called_once()
        self.assertIsInstance(result, list)

    @patch('jeypyats.parsers.iosxe.iosxe_routing_parsers_nc.logger')
    def test_get_bgp_routes_success(self, mock_logger):
        """Test successful BGP routes retrieval"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <bgp-routes xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-bgp-oper">
                <route>
                    <prefix>172.16.0.0/16</prefix>
                    <as-path>65001</as-path>
                    <next-hop>192.168.1.1</next-hop>
                    <metric>100</metric>
                </route>
                <route>
                    <prefix>192.168.0.0/16</prefix>
                    <as-path>65002 65001</as-path>
                    <next-hop>192.168.1.2</next-hop>
                    <metric>150</metric>
                </route>
            </bgp-routes>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXERoutingParsersMixin.get_bgp_routes(self.mock_device, 'default')

        self.mock_device.netconf_get.assert_called_once()
        self.assertIsInstance(result, list)

    @patch('jeypyats.parsers.iosxe.iosxe_routing_parsers_nc.logger')
    def test_get_routing_table_default_routes_success(self, mock_logger):
        """Test successful retrieval of default routes using IETF routing"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
                    <routing-instance>
                        <name>default</name>
                        <ribs>
                            <rib>
                                <name>ipv4-default</name>
                                <routes>
                                    <route>
                                        <destination-prefix>0.0.0.0/0</destination-prefix>
                                        <source-protocol>static</source-protocol>
                                        <next-hop>
                                            <next-hop-address>82.66.83.254</next-hop-address>
                                            <outgoing-interface>GigabitEthernet0/0/0</outgoing-interface>
                                        </next-hop>
                                        <metric>1</metric>
                                    </route>
                                </routes>
                            </rib>
                        </ribs>
                    </routing-instance>
                </routing-state>
            </data>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXERoutingParsersMixin.get_routing_table_default_routes(self.mock_device)

        # Verify the call was made with the correct filter
        self.mock_device.netconf_get.assert_called_once()
        call_args = self.mock_device.netconf_get.call_args[1]['filter']
        self.assertIn('urn:ietf:params:xml:ns:yang:ietf-routing', call_args)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['prefix'], '0.0.0.0/0')
        self.assertEqual(result[0]['next_hop'], '82.66.83.254')


if __name__ == '__main__':
    unittest.main()
