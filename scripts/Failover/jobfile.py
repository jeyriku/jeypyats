#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 23.01.2026 22:59:22
# Author: Jeremie Rouzet
#
# Last Modified: 26.01.2026 13:57:02
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

"""
PyATS Job file for running Huawei VRP BGP parser tests
"""

import logging
from pyats.easypy import run

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(runtime):
    """
    Main job function that will run the BGP parser tests
    """

    # Default testbed path if not provided in runtime
    default_testbed = "/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/testbed/jeylan_testbed.yml"

    # Get testbed from runtime arguments or use default
    testbed_file = runtime.testbed or default_testbed

    logger.info(f"Using testbed file: {testbed_file}")

    # Run the test script
    run(
        testscript='/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/scripts/Failover/failover.py',
        runtime=runtime,
        taskid='Tests_Failover',
        testbed=testbed_file,
        description='Test Cisco IOS XE Failover functionality'
    )
    logger.info("Test script execution completed.")

if __name__ == '__main__':
    import argparse
    from pyats.easypy import main as easypy_main

    # If run directly, use easypy to run the job
    easypy_main()
