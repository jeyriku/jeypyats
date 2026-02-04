#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 27.01.2026 20:00:00
# Author: GitHub Copilot
#
# Last Modified: 27.01.2026 19:44:42
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

__author__ = ["GitHub Copilot"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

"""
PyATS Job file for running Parse Device Facts NCC script
"""

import logging
from pyats.easypy import run

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(runtime):
    """
    Main job function that will run the Parse Device Facts NCC script
    """

    # Default testbed path
    default_testbed = "/Users/jeremierouzet/Documents/Dev/pyats/testbed/xrd/xrd_sw_tb_ncc_v1.0_clab.yaml"

    # Get testbed from runtime arguments or use default
    testbed_file = runtime.testbed or default_testbed

    logger.info(f"Using testbed file: {testbed_file}")

    # Run the test script
    run(
        testscript='/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/scripts/xrd/parse_device_facts/parse_device_facts_ncc_jeylab.py',
        runtime=runtime,
        taskid='Parse_Device_Facts_NCC',
        testbed=testbed_file,
        description='Parse device facts via NCC'
    )
