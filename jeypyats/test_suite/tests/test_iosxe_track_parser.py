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
        mock_response.data_xml = """<data>
            <tracks xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-track-oper">
                <track>
                    <track-number>1</track-number>
                    <track-state>up</track-state>
                </track>
            </tracks>
        </data>"""

        self.mock_device.nc.get.return_value = mock_response

        result = IOSXETrackParsersMixin.get_track_states(self.mock_device)

        self.mock_device.nc.get.assert_called_once()
        self.assertIsInstance(result, dict)
        self.assertIn('1', result)
        self.assertEqual(result['1']['state'], 'up')


if __name__ == '__main__':
    unittest.main()
