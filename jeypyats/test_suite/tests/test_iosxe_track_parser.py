#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: test_iosxe_track_parser.py
# This file is a part of Netalps.fr
#
# Created: 05.02.2026 10:00:00
# Author: GitHub Copilot
#
# Last Modified: 05.02.2026 09:29:27
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

import unittest
from unittest.mock import MagicMock, patch
from jeypyats.parsers.iosxe.iosxe_track_parsers_nc import IOSXETrackParsersMixin


class TestIOSXETrackParser(unittest.TestCase):
    """Unit tests for IOS-XE track parsers"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_device = MagicMock()

    @patch('jeypyats.parsers.iosxe.iosxe_track_parsers_nc.logger')
    def test_get_track_states_success(self, mock_logger):
        """Test successful track states retrieval"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <tracks xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-track-oper">
                    <track>
                        <track-number>1</track-number>
                        <track-state>up</track-state>
                    </track>
                </tracks>
            </data>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXETrackParsersMixin.get_track_states(self.mock_device)

        self.mock_device.netconf_get.assert_called_once()
        self.assertIsInstance(result, dict)
        self.assertIn('1', result)
        self.assertEqual(result['1']['state'], 'up')

    @patch('jeypyats.parsers.iosxe.iosxe_track_parsers_nc.logger')
    def test_get_track_states_none_response(self, mock_logger):
        """Test track states retrieval with None response"""
        self.mock_device.netconf_get.return_value = None

        result = IOSXETrackParsersMixin.get_track_states(self.mock_device)

        self.assertEqual(result, {})
        mock_logger.warning.assert_called_with("NETCONF response is invalid or empty for track states")

    @patch('jeypyats.parsers.iosxe.iosxe_track_parsers_nc.logger')
    def test_get_track_states_none_xml(self, mock_logger):
        """Test track states retrieval with None xml content"""
        mock_response = MagicMock()
        mock_response.xml = None

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXETrackParsersMixin.get_track_states(self.mock_device)

        self.assertEqual(result, {})
        mock_logger.warning.assert_called_with("NETCONF response is invalid or empty for track states")

    @patch('jeypyats.parsers.iosxe.iosxe_track_parsers_nc.logger')
    def test_get_track_states_rpc_error(self, mock_logger):
        """Test track states retrieval with RPC error"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <rpc-error>
                <error-type>application</error-type>
                <error-tag>operation-failed</error-tag>
                <error-message>YANG model not supported</error-message>
            </rpc-error>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXETrackParsersMixin.get_track_states(self.mock_device)

        self.assertEqual(result, {})
        mock_logger.error.assert_called_with("NETCONF RPC error in track response: <rpc-reply xmlns=\"urn:ietf:params:xml:ns:netconf:base:1.0\" message-id=\"1\">\n            <rpc-error>\n                <error-type>application</error-type>\n                <error-tag>operation-failed</error-tag>\n                <error-message>YANG model not supported</error-message>\n            </rpc-error>\n        </rpc-reply>")

    @patch('jeypyats.parsers.iosxe.iosxe_track_parsers_nc.logger')
    def test_get_track_states_parse_error(self, mock_logger):
        """Test track states retrieval with XML parse error"""
        mock_response = MagicMock()
        mock_response.xml = "invalid xml content"

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXETrackParsersMixin.get_track_states(self.mock_device)

        self.assertEqual(result, {})
        mock_logger.error.assert_called_once()
        self.assertIn("Error parsing track response:", mock_logger.error.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
