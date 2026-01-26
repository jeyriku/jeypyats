#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: builder.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/24 14:43:10
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 14:43:10
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

from utils.command_runner import run_command_on_device
from utils.parser import parse_neighbors

def generate_topology(devices):
    """
    Générer une topologie à partir des données LLDP/CDP.
    """
    topology = {}

    for device_name, device in devices.items():
        print(f"Collecte des voisins pour {device_name} ({device['alias']})...")

        # Exécuter une commande pour récupérer les voisins
        output = run_command_on_device(device["alias"], "show lldp neighbors")

        # Analyser les voisins
        neighbors = parse_neighbors(output)

        # Construire les connexions
        topology[device_name] = {
            "interfaces": [
                {"connected_to": neighbor["device"], "interface": neighbor["interface"]}
                for neighbor in neighbors
            ]
        }

    return topology