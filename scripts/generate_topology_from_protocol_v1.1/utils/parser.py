#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: parser.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/24 14:42:33
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 14:42:33
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

def parse_neighbors(output):
    """
    Analyser la sortie LLDP/CDP pour extraire les voisins.
    """
    neighbors = []

    if output:
        for line in output.splitlines():
            # Supposons que la sortie contienne des colonnes Device-ID et Port-ID
            parts = line.split()
            if len(parts) >= 2:
                neighbors.append({"device": parts[0], "interface": parts[1]})

    return neighbors