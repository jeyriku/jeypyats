#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr
#
# Created: 26.01.2026
# Author: Jeremie Rouzet
#
# Last Modified: 26.01.2026 14:15:14
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps.fr, 2026'
__license__ = "Netalps.fr, Copyright 2026. All rights reserved."

'''
Setup file for JeyPyats package
This setup file is used to package the JeyPyats framework for distribution.
It defines the package name, version, and included packages.
'''

from setuptools import setup, find_packages

setup(
    name='jeypyats',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'lxml',
        'xmltodict',
        'packaging',
        # Add other dependencies as needed
    ],
    author='Jeremie Rouzet',
    author_email='jeremie.rouzet@netalps.fr',
    description='JeyPyats: Automated testing framework for network equipment via NETCONF',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/jeypyats',  # Update with actual repo URL
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # Adjust license
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)
