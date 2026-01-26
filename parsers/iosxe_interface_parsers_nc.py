#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 23.01.2026 22:58:12
# Author: Jeremie Rouzet
#
# Last Modified: 26.01.2026 13:55:03
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Pyats IOS XE Interface parsers using Netconf
This module contains parsers to retrieve interface status from IOS XE devices via Netconf.
It includes functions to get interface status using both OpenConfig and Cisco IOS XE YANG models.
The parsers utilize XML filters to query the device and parse the XML responses into structured data.
Each function is designed to handle specific YANG models and return relevant information in a user-friendly format.
The module leverages the Genie and lxml libraries for XML parsing and data extraction.
'''
