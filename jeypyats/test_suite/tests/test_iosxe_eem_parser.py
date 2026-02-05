#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: test_iosxe_eem_parser.py
# This file is a part of Netalps.fr
#
# Created: 05.02.2026 10:00:00
# Author: GitHub Copilot
#
# Last Modified: 05.02.2026 10:00:00
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

import unittest
from unittest.mock import MagicMock, patch
from jeypyats.parsers.iosxe.iosxe_eem_parsers_nc import IOSXEEEMParsersMixin


class TestIOSXEEEMParser(unittest.TestCase):
    """Unit tests for IOS-XE EEM parsers"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_device = MagicMock()

    @patch('jeypyats.parsers.iosxe.iosxe_eem_parsers_nc.logger')
    def test_get_eem_event_history_success(self, mock_logger):
        """Test successful EEM event history retrieval"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <event-history xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-eem">
                    <event>
                        <name>event1</name>
                        <type>timer</type>
                        <time>2023-01-01T00:00:00Z</time>
                        <description>Test event</description>
                    </event>
                </event-history>
            </data>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXEEEMParsersMixin.get_eem_event_history(self.mock_device)

        self.mock_device.netconf_get.assert_called_once()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'event1')


if __name__ == '__main__':
    unittest.main()
