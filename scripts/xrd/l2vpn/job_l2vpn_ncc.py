#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 27.01.2026 20:00:00
# Author: GitHub Copilot
#
# Last Modified: 27.01.2026 19:43:37
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

__author__ = ["GitHub Copilot"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

"""
PyATS Job file for running L2VPN Bridge Domain Brief NCC script
"""

import logging
from pyats.easypy import run

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(runtime):
    """
    Main job function that will run the L2VPN NCC script
    """

    # Default testbed path
    default_testbed = "/Users/jeremierouzet/Documents/Dev/pyats/testbed/xrd/xrd_sw_tb_v1.0_ncc.yaml"

    # Get testbed from runtime arguments or use default
    testbed_file = runtime.testbed or default_testbed

    logger.info(f"Using testbed file: {testbed_file}")

    # Run the test script
    run(
        testscript='/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/scripts/xrd/l2vpn/l2vpn_bgbd_script_ncc.v1.0.py',
        runtime=runtime,
        taskid='L2VPN_NCC_Test',
        testbed=testbed_file,
        description='Test L2VPN Bridge Domain Brief via NCC'
    )
