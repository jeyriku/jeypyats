#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 11.07.2025 11:22:06
# Author: Jeremie Rouzet
#
# Last Modified: 26.01.2026 13:52:12
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Setup file for parsers module
This setup file is used to package the parsers module for distribution.
It defines the package name, version, and included packages.
'''

from setuptools import setup, find_packages

setup(
    name='parsers',
    version='1.0.0',
    packages=find_packages(),
)
