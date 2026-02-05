#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 04.02.2026 12:00:00
# Author: Jeremie Rouzet
#
# Last Modified: 04.02.2026 10:07:22
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Pyats IOS XE Cellular parsers using Netconf
This module contains parsers to retrieve Cellular information from Cisco IOS XE devices via Netconf.
'''
import logging
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

class IOSXECellularParsersMixin:
    '''
    Collection of RPCs for parsing Cellular information on IOS-XE devices
    '''
    def get_cellular_sim_config(self, interface):
        '''
        Retrieves Cellular SIM config via NETCONF.

        Args:
            interface (str): Cellular interface name, e.g., 'Cellular0/2/0'

        Returns:
            dict: SIM config with slot and data_profile.
        '''
        cellular_filter = f'''
        <filter>
            <cellular xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-cellular-oper">
                <cellular>
                    <interface>
                        <name>{interface}</name>
                        <sim/>
                    </interface>
                </cellular>
            </cellular>
        </filter>
        '''
        response = self.netconf_get(filter=cellular_filter)
        data = response.data_xml
        root = ET.fromstring(data)
        sim_config = {'slot': None, 'data_profile': None}
        sim = root.find('.//sim')
        if sim is not None:
            slot_elem = sim.find('slot')
            data_profile_elem = sim.find('data-profile')
            slot_text = slot_elem.text if slot_elem is not None else None
            data_profile_text = data_profile_elem.text if data_profile_elem is not None else None
            sim_config['slot'] = int(slot_text) if slot_text is not None else None
            sim_config['data_profile'] = int(data_profile_text) if data_profile_text is not None else None
        return sim_config

    @classmethod
    def bind_to_device(cls, device):
        setattr(device, 'get_cellular_sim_config', cls.get_cellular_sim_config.__get__(device, type(device)))
