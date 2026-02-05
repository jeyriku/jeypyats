#!/usr/bin/env python
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
    version='1.1.3',
    packages=find_packages(),
    package_dir={'': '.'},
    install_requires=[
        'lxml>=4.9.0',
        'xmltodict>=0.12.0',
        'packaging>=21.0',
        'ncclient>=0.6.0',
        'genie>=23.0',
        'pytest>=7.0.0',
        'pytest-cov>=4.0.0',
        'pyats>=23.0',
        'unicon>=23.0',
        'paramiko>=2.0.0',
        'requests>=2.25.0',
        'pyyaml>=6.0',
        'jinja2>=3.0.0',
    ],
    extras_require={
        'dev': [
            'coverage>=7.0.0',
            'yamllint>=1.30.0',
        ],
    },
    author='Jeremie Rouzet',
    author_email='jeremie.rouzet@netalps.fr',
    description='JeyPyats: Automated testing framework for network equipment via NETCONF',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jeyriku/jeypyats',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Networking',
    ],
    python_requires='>=3.8',
    keywords='networking netconf automation testing cisco ios-xe ios-xr pyats',
    project_urls={
        'Bug Reports': 'https://github.com/jeyriku/jeypyats/issues',
        'Source': 'https://github.com/jeyriku/jeypyats',
    },
    entry_points={
        'console_scripts': [
            'jeypyats-test=test_suite.scripts.run_all_tests:main',
        ],
    },
)
