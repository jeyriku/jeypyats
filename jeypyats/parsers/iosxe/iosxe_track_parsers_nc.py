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
from lxml import etree
from ...utils import BASE_RPC

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

parser = etree.XMLParser()
parser.set_element_class_lookup(
    etree.ElementDefaultClassLookup(element=etree.ElementBase)
)

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
        # Remove XML declaration if present
        xml_content = response.xml
        if xml_content.startswith('<?xml'):
            xml_content = xml_content.split('?>', 1)[1].strip()
        xml_data = etree.fromstring(xml_content.encode('utf-8'), parser)
        data_dict = xmltodict.parse(etree.tostring(xml_data))

        track_states = {}
        tracks = data_dict.get('rpc-reply', {}).get('data', {}).get('tracks', {})
        track_list = tracks.get('track', [])
        if isinstance(track_list, dict):
            track_list = [track_list]
        for track in track_list:
            track_id = track.get('track-number')
            state = track.get('track-state')
            if track_id:
                track_states[str(track_id)] = {'state': state}
        return track_states

    @classmethod
    def bind_to_device(cls, device):
        setattr(device, 'get_track_states', cls.get_track_states.__get__(device, type(device)))
