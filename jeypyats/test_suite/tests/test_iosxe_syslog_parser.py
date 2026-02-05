#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: test_iosxe_syslog_parser.py
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
from jeypyats.parsers.iosxe.iosxe_syslog_parsers_nc import IOSXESyslogParsersMixin


class TestIOSXESyslogParser(unittest.TestCase):
    """Unit tests for IOS-XE syslog parsers"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_device = MagicMock()

    @patch('jeypyats.parsers.iosxe.iosxe_syslog_parsers_nc.logger')
    def test_get_syslog_messages_success(self, mock_logger):
        """Test successful syslog messages retrieval"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <logging xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-logging">
                    <buffered>
                        <messages>*Jan  1 00:00:00: %SYS-5-CONFIG_I: Configured from console by console
*Jan  1 00:00:01: %LINK-3-UPDOWN: Interface GigabitEthernet0/0, changed state to up</messages>
                    </buffered>
                </logging>
            </data>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXESyslogParsersMixin.get_syslog_messages(self.mock_device)

        self.mock_device.netconf_get.assert_called_once()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('timestamp', result[0])

    @patch('jeypyats.parsers.iosxe.iosxe_syslog_parsers_nc.logger')
    def test_get_syslog_messages_with_filter(self, mock_logger):
        """Test syslog messages retrieval with filter"""
        mock_response = MagicMock()
        mock_response.xml = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1">
            <data>
                <logging xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-logging">
                    <buffered>
                        <messages>*Jan  1 00:00:00: %SYS-5-CONFIG_I: Configured from console by console
*Jan  1 00:00:01: %LINK-3-UPDOWN: Interface GigabitEthernet0/0, changed state to up</messages>
                    </buffered>
                </logging>
            </data>
        </rpc-reply>"""

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXESyslogParsersMixin.get_syslog_messages(self.mock_device, filter_text='LINK')

        self.mock_device.netconf_get.assert_called_once()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn('LINK', result[0]['text'])


if __name__ == '__main__':
    unittest.main()
