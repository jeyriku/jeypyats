#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr
#
# Created: 27.01.2026
# Author: Jeremie Rouzet
#
# Last Modified: 27.01.2026 19:16:47
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

"""
JeyPyats - Network Device Parsing Framework

A comprehensive framework for parsing network device configurations and operational data
using various protocols including NETCONF, CLI, and REST APIs.

This package provides parsers for different network operating systems and protocols,
utilities for device connectivity, and a complete test suite.
"""

__version__ = "1.1.3"
__author__ = "Jeremie Rouzet"
__email__ = "jeremie.rouzet@netalps.fr"

# Import main modules to make them available at package level
from . import parsers
from . import utils
from . import test_suite

__all__ = ['parsers', 'utils', 'test_suite']
