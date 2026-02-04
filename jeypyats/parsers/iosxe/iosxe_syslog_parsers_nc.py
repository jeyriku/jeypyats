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
Pyats IOS XE Syslog parsers using Netconf
This module contains parsers to retrieve syslog messages from Cisco IOS XE devices via Netconf.
It includes functions to get syslog messages and filter them.
The parsers utilize XML filters to query the device and parse the XML responses into structured data.
Each function is designed to handle specific syslog operations and return relevant information in a user-friendly format.
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

class IOSXESyslogParsersMixin:
    '''
    Collection of RPCs for parsing syslog information on IOS-XE devices
    '''
    def get_syslog_messages(self, filter_text=None):
        '''
        Get syslog messages
        Args:
            filter_text (str): Text to filter messages containing this string
        Returns:
            list: List of syslog messages
        '''
        filter_xml = '''
            <filter>
                <logging xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-logging">
                    <buffered>
                        <messages>
                        </messages>
                    </buffered>
                </logging>
            </filter>
        '''
        response = self.netconf_get(filter=filter_xml)
        # Remove XML declaration if present
        xml_content = response.xml
        if xml_content.startswith('<?xml'):
            xml_content = xml_content.split('?>', 1)[1].strip()
        xml_data = etree.fromstring(xml_content.encode('utf-8'), parser)
        data_dict = xmltodict.parse(etree.tostring(xml_data))

        print(f"DEBUG SYSLOG: data_dict = {json.dumps(data_dict, indent=2)}")  # Debug print

        # Check if data is None
        data = data_dict.get('rpc-reply', {}).get('data')
        if data is None:
            return []

        # Navigate to syslog messages
        logging_data = data.get('logging', {}).get('buffered', {}).get('messages')
        if not logging_data:
            return []

        # messages is a string, split into lines
        messages_text = logging_data if isinstance(logging_data, str) else str(logging_data)
        lines = messages_text.strip().split('\n')

        parsed_messages = []

        for line in lines:
            if line.strip():
                # Parse line: *timestamp: %facility-severity-MNEMONIC: message
                if line.startswith('*'):
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        timestamp = parts[0][1:].strip()  # remove *
                        facility = parts[1].strip()
                        text = parts[2].strip()
                        parsed_msg = {
                            'timestamp': timestamp,
                            'facility': facility,
                            'text': text,
                        }
                        if filter_text:
                            if filter_text.lower() in text.lower():
                                parsed_messages.append(parsed_msg)
                        else:
                            parsed_messages.append(parsed_msg)

        return parsed_messages

    @classmethod
    def bind_to_device(cls, device):
        setattr(device, 'get_syslog_messages', cls.get_syslog_messages.__get__(device, type(device)))
