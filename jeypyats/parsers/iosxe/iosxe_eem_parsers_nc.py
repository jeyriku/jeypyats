#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 30.01.2026 00:00:00
# Author: Jeremie Rouzet
#
# Last Modified: 30.01.2026 00:00:00
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Pyats IOS XE EEM parsers using Netconf
This module contains parsers to retrieve EEM (Embedded Event Manager) information from Cisco IOS XE devices via Netconf.
It includes functions to get EEM event logs and history.
The parsers utilize XML filters to query the device and parse the XML responses into structured data.
Each function is designed to handle specific EEM operations and return relevant information in a user-friendly format.
The module leverages the Genie and lxml libraries for XML parsing and data extraction.
'''
import logging
import xmltodict
from genie.utils import Dq
from lxml import etree
from ...utils import BASE_RPC
from packaging import version
import json



logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

parser = etree.XMLParser()
parser.set_element_class_lookup(
    etree.ElementDefaultClassLookup(element=etree.ElementBase)
)

class IOSXEEEMParsersMixin:
    '''
    Collection of RPCs for parsing EEM information on IOS-XE devices
    '''
    def get_eem_event_history(self):
        '''
        Get EEM event history
        Returns:
            list: List of EEM event history entries
        '''
        filter_xml = '''
            <filter>
                <event-history xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-eem">
                </event-history>
            </filter>
        '''
        response = self.netconf_get(filter=filter_xml)
        # Remove XML declaration if present
        xml_content = response.xml
        if xml_content.startswith('<?xml'):
            xml_content = xml_content.split('?>', 1)[1].strip()
        xml_data = etree.fromstring(xml_content.encode('utf-8'), parser)
        data_dict = xmltodict.parse(etree.tostring(xml_data))

        print(f"DEBUG EEM: data_dict = {json.dumps(data_dict, indent=2)}")  # Debug print

        # Navigate to EEM event history
        event_history_data = data_dict.get('rpc-reply', {}).get('data', {}).get('event-history', {})
        events = event_history_data.get('event', [])

        # Handle both single event (dict) and multiple events (list)
        if isinstance(events, dict):
            events = [events]

        parsed_events = []

        for event in events:
            parsed_event = {
                'name': event.get('name'),
                'type': event.get('type'),
                'time': event.get('time'),
                'description': event.get('description'),
            }
            parsed_events.append(parsed_event)

        return parsed_events

    @classmethod
    def bind_to_device(cls, device):
        setattr(device, 'get_eem_event_history', cls.get_eem_event_history.__get__(device, type(device)))
