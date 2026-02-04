#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 04.02.2026 12:00:00
# Author: Jeremie Rouzet
#
# Last Modified: 04.02.2026 10:07:10
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
        sla_states = {}
        for sla in root.findall('.//ip-sla-stat'):
            sla_id_elem = sla.find('sla-index')
            oper_state_elem = sla.find('oper-state')
            sla_id = sla_id_elem.text if sla_id_elem is not None else None
            oper_state = oper_state_elem.text if oper_state_elem is not None else None
            if sla_id:
                sla_states[sla_id] = {'oper_state': oper_state}
        return sla_states

    @classmethod
    def bind_to_device(cls, device):
        setattr(device, 'get_ip_sla_states', cls.get_ip_sla_states.__get__(device, type(device)))
