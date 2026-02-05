#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 04.02.2026 12:00:00
# Author: Jeremie Rouzet
#
# Last Modified: 05.02.2026 11:22:43
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Pyats IOS XE IP SLA parsers using Netconf
This module contains parsers to retrieve IP SLA information from Cisco IOS XE devices via Netconf.
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

class IOSXEIPSLAParsersMixin:
    '''
    Collection of RPCs for parsing IP SLA information on IOS-XE devices
    '''
    def get_ip_sla_states(self):
        '''
        Retrieves IP SLA states via NETCONF.

        Returns:
            dict: Dictionary of SLA IDs and their states.
        '''
        sla_filter = '''
        <filter>
            <ip-sla-stats xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ip-sla-oper">
                <ip-sla-stat/>
            </ip-sla-stats>
        </filter>
        '''
        response = self.netconf_get(filter=sla_filter)

        # Check if response is valid
        if not response or not hasattr(response, 'xml') or response.xml is None:
            logger.warning("NETCONF response is invalid or empty for IP SLA states")
            return {}

        # Check for RPC errors
        if '<rpc-error>' in response.xml:
            logger.error(f"NETCONF RPC error in IP SLA response: {response.xml}")
            return {}

        try:
            # Remove XML declaration if present
            xml_content = response.xml
            if xml_content.startswith('<?xml'):
                xml_content = xml_content.split('?>', 1)[1].strip()
            xml_data = etree.fromstring(xml_content.encode('utf-8'), parser)
            data_dict = xmltodict.parse(etree.tostring(xml_data))

            if data_dict is None:
                logger.warning("Failed to parse XML response for IP SLA states")
                return {}

            sla_states = {}
            ip_sla_stats = data_dict.get('rpc-reply', {}).get('data', {}).get('ip-sla-stats', {})
            ip_sla_stat_list = ip_sla_stats.get('ip-sla-stat', [])
            if isinstance(ip_sla_stat_list, dict):
                ip_sla_stat_list = [ip_sla_stat_list]
            for sla in ip_sla_stat_list:
                sla_id = sla.get('sla-index')
                oper_state = sla.get('oper-state')
                if sla_id:
                    sla_states[str(sla_id)] = {'oper_state': oper_state}
            return sla_states
        except Exception as e:
            logger.error(f"Error parsing IP SLA response: {e}")
            return {}
