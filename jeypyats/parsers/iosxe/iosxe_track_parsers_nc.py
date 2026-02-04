#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 04.02.2026 12:00:00
# Author: Jeremie Rouzet
#
# Last Modified: 04.02.2026 10:07:11
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Pyats IOS XE Track parsers using Netconf
This module contains parsers to retrieve Track information from Cisco IOS XE devices via Netconf.
'''
import logging
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

class IOSXETrackParsersMixin:
    '''
    Collection of RPCs for parsing Track information on IOS-XE devices
    '''
    def get_track_states(self):
        '''
        Retrieves Track states via NETCONF.

        Returns:
            dict: Dictionary of track IDs and their states.
        '''
        track_filter = '''
        <filter>
            <tracks xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-track-oper">
                <track/>
            </tracks>
        </filter>
        '''
        response = self.nc.get(filter=track_filter)
        data = response.data_xml
        root = ET.fromstring(data)
        track_states = {}
        for track in root.findall('.//track'):
            track_id_elem = track.find('track-number')
            state_elem = track.find('track-state')
            track_id = track_id_elem.text if track_id_elem is not None else None
            state = state_elem.text if state_elem is not None else None
            if track_id:
                track_states[track_id] = {'state': state}
        return track_states

    @classmethod
    def bind_to_device(cls, device):
        setattr(device, 'get_track_states', cls.get_track_states.__get__(device, type(device)))
