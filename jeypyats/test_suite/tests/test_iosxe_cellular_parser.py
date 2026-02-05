#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: test_iosxe_cellular_parser.py
# This file is a part of Netalps.fr
#
# Created: 05.02.2026 10:00:00
# Author: GitHub Copilot
#
# Last Modified: 05.02.2026 11:18:37
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

import unittest
from unittest.mock import MagicMock, patch
from jeypyats.parsers.iosxe.iosxe_cellular_parsers_nc import IOSXECellularParsersMixin


class TestIOSXECellularParser(unittest.TestCase):
    """Unit tests for IOS-XE cellular parsers"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_device = MagicMock()

    @patch('jeypyats.parsers.iosxe.iosxe_cellular_parsers_nc.logger')
    def test_get_cellular_sim_config_success(self, mock_logger):
        """Test successful cellular SIM config retrieval"""
        mock_response = MagicMock()
        mock_response.data_xml = '''<cellular>
            <cellular>
                <interface>
                    <name>Cellular0/2/0</name>
                    <sim>
                        <slot>1</slot>
                        <data-profile>1</data-profile>
                    </sim>
                </interface>
            </cellular>
        </cellular>'''

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXECellularParsersMixin.get_cellular_sim_config(self.mock_device, 'Cellular0/2/0')

        expected = {'slot': 1, 'data_profile': 1}
        self.assertEqual(result, expected)

    @patch('jeypyats.parsers.iosxe.iosxe_cellular_parsers_nc.logger')
    def test_get_cellular_sim_config_no_sim(self, mock_logger):
        """Test cellular SIM config retrieval when no SIM data"""
        mock_response = MagicMock()
        mock_response.data_xml = '''<cellular>
            <cellular>
                <interface>
                    <name>Cellular0/2/0</name>
                </interface>
            </cellular>
        </cellular>'''

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXECellularParsersMixin.get_cellular_sim_config(self.mock_device, 'Cellular0/2/0')

        expected = {'slot': None, 'data_profile': None}
        self.assertEqual(result, expected)

    @patch('jeypyats.parsers.iosxe.iosxe_cellular_parsers_nc.logger')
    def test_get_cellular_sim_config_none_response(self, mock_logger):
        """Test cellular SIM config retrieval with None response"""
        self.mock_device.netconf_get.return_value = None

        result = IOSXECellularParsersMixin.get_cellular_sim_config(self.mock_device, 'Cellular0/2/0')

        self.assertEqual(result, {'slot': None, 'data_profile': None})
        mock_logger.warning.assert_called_with("NETCONF response is invalid or empty for cellular SIM config on Cellular0/2/0")

    @patch('jeypyats.parsers.iosxe.iosxe_cellular_parsers_nc.logger')
    def test_get_cellular_sim_config_no_data_xml_attribute(self, mock_logger):
        """Test cellular SIM config retrieval with response missing data_xml attribute"""
        mock_response = MagicMock()
        del mock_response.data_xml  # Remove data_xml attribute

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXECellularParsersMixin.get_cellular_sim_config(self.mock_device, 'Cellular0/2/0')

        self.assertEqual(result, {'slot': None, 'data_profile': None})
        mock_logger.warning.assert_called_with("NETCONF response is invalid or empty for cellular SIM config on Cellular0/2/0")

    @patch('jeypyats.parsers.iosxe.iosxe_cellular_parsers_nc.logger')
    def test_get_cellular_sim_config_none_data_xml(self, mock_logger):
        """Test cellular SIM config retrieval with None data_xml content"""
        mock_response = MagicMock()
        mock_response.data_xml = None

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXECellularParsersMixin.get_cellular_sim_config(self.mock_device, 'Cellular0/2/0')

        self.assertEqual(result, {'slot': None, 'data_profile': None})
        mock_logger.warning.assert_called_with("NETCONF response is invalid or empty for cellular SIM config on Cellular0/2/0")

    @patch('jeypyats.parsers.iosxe.iosxe_cellular_parsers_nc.logger')
    def test_get_cellular_sim_config_parse_error(self, mock_logger):
        """Test cellular SIM config retrieval with XML parse error"""
        mock_response = MagicMock()
        mock_response.data_xml = "invalid xml content"

        self.mock_device.netconf_get.return_value = mock_response

        result = IOSXECellularParsersMixin.get_cellular_sim_config(self.mock_device, 'Cellular0/2/0')

        self.assertEqual(result, {'slot': None, 'data_profile': None})
        mock_logger.error.assert_called_once()
        self.assertIn("Error parsing cellular SIM config response for Cellular0/2/0:", mock_logger.error.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
