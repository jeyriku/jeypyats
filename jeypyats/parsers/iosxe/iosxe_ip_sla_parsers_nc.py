#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 04.02.2026 12:00:00
# Author: Jeremie Rouzet
#
# Last Modified: 05.02.2026 09:32:42
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
import xml.etree.ElementTree as ET
from ...utils import BASE_RPC

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

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
        response = self.nc.get(filter=sla_filter)
        data = response.data_xml
        root = ET.fromstring(data)
        data_dict = xmltodict.parse(ET.tostring(root))

        sla_states = {}
        ip_sla_stats = data_dict.get('data', {}).get('ns0:ip-sla-stats', {})
        ip_sla_stat_list = ip_sla_stats.get('ns0:ip-sla-stat', [])
        if isinstance(ip_sla_stat_list, dict):
            ip_sla_stat_list = [ip_sla_stat_list]
        for sla in ip_sla_stat_list:
            sla_id = sla.get('ns0:sla-index')
            oper_state = sla.get('ns0:oper-state')
            if sla_id:
                sla_states[str(sla_id)] = {'oper_state': oper_state}
        return sla_states
