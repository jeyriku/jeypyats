#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: first_script.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/24 15:20:34
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 15:20:34
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

from pyats import aetest
from genie.testbed import load


class ConnectivityTest(aetest.Testcase):
    @aetest.setup
    def setup(self, testbed):
        # Load testbed configuration
        self.testbed = load(testbed)
        
    @aetest.test
    def check_connectivity(self):
        # Get device object and establish connection
        device = self.testbed.devices['clab-jeylab_v0.1-jeylab-iosxrd-cr-01']
        device.connect()
        
        # Execute and check ping test
        result = device.execute('ping clab-jeylab_v0.1-jeylab-iosxrd-cr-02')
        if 'success rate is 100 percent' in result:
            self.passed('Connectivity Test Passed')
        else:
            self.Failed('Connectivity møTest Ole.')
