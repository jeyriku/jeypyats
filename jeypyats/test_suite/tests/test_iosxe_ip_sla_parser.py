#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: test_iosxe_ip_sla_parser.py
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
from jeypyats.parsers.iosxe.iosxe_ip_sla_parsers_nc import IOSXEIPSLAParsersMixin


class TestIOSXEIPSLAParser(unittest.TestCase):
    """Unit tests for IOS-XE IP SLA parsers"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_device = MagicMock()

    @patch('jeypyats.parsers.iosxe.iosxe_ip_sla_parsers_nc.logger')
    def test_get_ip_sla_states_success(self, mock_logger):
        """Test successful IP SLA states retrieval"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <ip-sla-stats xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ip-sla-oper">
                    <ip-sla-stat>
                        <sla-index>1</sla-index>
                        <oper-state>active</oper-state>
                    </ip-sla-stat>
                </ip-sla-stats>
            </data>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXEIPSLAParsersMixin.get_ip_sla_states(self.mock_device)

        self.mock_device.netconf_get.assert_called_once()
        self.assertIsInstance(result, dict)
        self.assertIn('1', result)
        self.assertEqual(result['1']['oper_state'], 'active')

    @patch('jeypyats.parsers.iosxe.iosxe_ip_sla_parsers_nc.logger')
    def test_get_ip_sla_states_none_response(self, mock_logger):
        """Test IP SLA states retrieval with None response"""
        self.mock_device.netconf_get.return_value = None

        result = IOSXEIPSLAParsersMixin.get_ip_sla_states(self.mock_device)

        self.assertEqual(result, {})
        mock_logger.warning.assert_called_with("NETCONF response is invalid or empty for IP SLA states")

    @patch('jeypyats.parsers.iosxe.iosxe_ip_sla_parsers_nc.logger')
    def test_get_ip_sla_states_no_xml_attribute(self, mock_logger):
        """Test IP SLA states retrieval with response missing xml attribute"""
        mock_response = MagicMock()
        del mock_response.xml  # Remove xml attribute

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXEIPSLAParsersMixin.get_ip_sla_states(self.mock_device)

        self.assertEqual(result, {})
        mock_logger.warning.assert_called_with("NETCONF response is invalid or empty for IP SLA states")

    @patch('jeypyats.parsers.iosxe.iosxe_ip_sla_parsers_nc.logger')
    def test_get_ip_sla_states_none_xml(self, mock_logger):
        """Test IP SLA states retrieval with None xml content"""
        mock_response = MagicMock()
        mock_response.xml = None

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXEIPSLAParsersMixin.get_ip_sla_states(self.mock_device)

        self.assertEqual(result, {})
        mock_logger.warning.assert_called_with("NETCONF response is invalid or empty for IP SLA states")

    @patch('jeypyats.parsers.iosxe.iosxe_ip_sla_parsers_nc.logger')
    def test_get_ip_sla_states_rpc_error(self, mock_logger):
        """Test IP SLA states retrieval with RPC error"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <rpc-error>
                <error-type>application</error-type>
                <error-tag>operation-failed</error-tag>
                <error-message>YANG model not supported</error-message>
            </rpc-error>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXEIPSLAParsersMixin.get_ip_sla_states(self.mock_device)

        self.assertEqual(result, {})
        mock_logger.error.assert_called_with("NETCONF RPC error in IP SLA response: <rpc-reply xmlns=\"urn:ietf:params:xml:ns:netconf:base:1.0\" message-id=\"1\">\n            <rpc-error>\n                <error-type>application</error-type>\n                <error-tag>operation-failed</error-tag>\n                <error-message>YANG model not supported</error-message>\n            </rpc-error>\n        </rpc-reply>")

    @patch('jeypyats.parsers.iosxe.iosxe_ip_sla_parsers_nc.logger')
    def test_get_ip_sla_states_parse_error(self, mock_logger):
        """Test IP SLA states retrieval with XML parse error"""
        mock_response = MagicMock()
        mock_response.xml = "invalid xml content"

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXEIPSLAParsersMixin.get_ip_sla_states(self.mock_device)

        self.assertEqual(result, {})
        mock_logger.error.assert_called_once()
        self.assertIn("Error parsing IP SLA response:", mock_logger.error.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
