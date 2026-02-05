#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 04.02.2026 12:00:00
# Author: Jeremie Rouzet
#
# Last Modified: 05.02.2026 09:32:47
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
import xmltodict
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
        data_dict = xmltodict.parse(ET.tostring(root))

        track_states = {}
        tracks = data_dict.get('data', {}).get('ns0:tracks', {})
        track_list = tracks.get('ns0:track', [])
        if isinstance(track_list, dict):
            track_list = [track_list]
        for track in track_list:
            track_id = track.get('ns0:track-number')
            state = track.get('ns0:track-state')
            if track_id:
                track_states[str(track_id)] = {'state': state}
        return track_states

    @classmethod
    def bind_to_device(cls, device):
        setattr(device, 'get_track_states', cls.get_track_states.__get__(device, type(device)))
