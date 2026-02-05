#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: test_iosxe_interface_parser.py
# This file is a part of Netalps.fr
#
# Created: 05.02.2026 10:00:00
# Author: GitHub Copilot
#
# Last Modified: 05.02.2026 09:28:54
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

import unittest
from unittest.mock import MagicMock, patch
from jeypyats.parsers.iosxe.iosxe_interface_parsers_nc import IOSXEInterfacesParsersMixin


class TestIOSXEInterfaceParser(unittest.TestCase):
    """Unit tests for IOS-XE interface parsers"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_device = MagicMock()

    @patch('jeypyats.parsers.iosxe.iosxe_interface_parsers_nc.logger')
    def test_get_interfaces_status_openconfig_success(self, mock_logger):
        """Test successful interface status retrieval using OpenConfig"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <interfaces xmlns="http://openconfig.net/yang/interfaces">
                    <interface>
                        <name>GigabitEthernet0/0</name>
                        <state>
                            <oper-status>up</oper-status>
                            <admin-status>up</admin-status>
                        </state>
                    </interface>
                </interfaces>
            </data>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXEInterfacesParsersMixin.get_interfaces_status_openconfig(self.mock_device)

        self.mock_device.netconf_get.assert_called_once()
        self.assertIsInstance(result, dict)
        self.assertIn('GigabitEthernet0/0', result)
        self.assertEqual(result['GigabitEthernet0/0']['oper_status'], 'up')

    @patch('jeypyats.parsers.iosxe.iosxe_interface_parsers_nc.logger')
    def test_get_interfaces_cellular_status_success(self, mock_logger):
        """Test successful cellular interface status retrieval"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <interfaces-state xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
                    <interface>
                        <name>Cellular0/2/0</name>
                        <oper-status>up</oper-status>
                        <admin-status>up</admin-status>
                    </interface>
                </interfaces-state>
            </data>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXEInterfacesParsersMixin.get_interfaces_cellular_status(self.mock_device)

        self.mock_device.netconf_get.assert_called_once()
        self.assertIsInstance(result, dict)
        self.assertIn('Cellular0/2/0', result)
        self.assertEqual(result['Cellular0/2/0']['oper_status'], 'up')

    @patch('jeypyats.parsers.iosxe.iosxe_interface_parsers_nc.logger')
    def test_get_interface_status_success(self, mock_logger):
        """Test successful specific interface status retrieval"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                    <interface>
                        <name>GigabitEthernet0/0</name>
                        <oper-status>up</oper-status>
                        <admin-status>up</admin-status>
                    </interface>
                </interfaces-state>
            </data>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXEInterfacesParsersMixin.get_interface_status(self.mock_device, 'GigabitEthernet0/0')

        self.mock_device.netconf_get.assert_called_once()
        self.assertIsInstance(result, dict)
        self.assertEqual(result['oper_status'], 'up')
        self.assertEqual(result['admin_status'], 'up')


if __name__ == '__main__':
    unittest.main()
