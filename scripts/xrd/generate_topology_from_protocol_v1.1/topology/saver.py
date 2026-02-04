#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: saver.py
# This file is a part of Netalps.fr
#
# Created: 2025/01/24 14:43:31
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 14:43:31
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################

from utils.file_manager import save_yaml

def save_topology(testbed, topology, output_file):
    """
    Ajouter la topologie générée au testbed et sauvegarder dans un fichier.
    """
    testbed["topology"] = topology
    save_yaml(testbed, output_file)
    print(f"Topology saved to {output_file}")