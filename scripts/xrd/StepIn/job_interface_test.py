#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: job_interface_test.py
# This file is a part of Netalps.fr
#
# Created: 2025/06/25 13:41:04
# Author: Jeremie Rouzet
#
# Last Modified: 11.07.2025 11:51:26
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################
import logging
import os
from pyats.easypy import run


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


def main(runtime):
    logger = logging.getLogger(__name__)
    testscript = os.path.join(os.path.dirname(__file__), 'interface_test.py')
    logger.info(f"Resolved testscript path: {testscript}")
    logger.info("Starting pyATS run with testbed 'jeytestbed.yaml'")
    try:
        run(testscript=testscript, testbed='/Users/jeremierouzet/Documents/Dev/pyats/testbed/jeytestbed.yaml')
        logger.info("pyATS run completed successfully.")
    except Exception as e:
        logger.error(f"pyATS run failed: {e}", exc_info=True)
        raise
