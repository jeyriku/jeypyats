#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: generate_topology.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/24 14:04:30
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 14:04:30
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

import yaml

def load_testbed(file_path):
    """
    Charger le fichier YAML de testbed.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_topology(devices):
    """
    Générer une topologie simple basée sur la liste des appareils.
    Les connexions sont définies par des règles simples : chaque appareil est connecté à son voisin suivant.
    """
    topology = {}
    device_names = list(devices.keys())

    for i, device in enumerate(device_names):
        # Connect each device to the next one (circular connection)
        neighbors = []
        if i + 1 < len(device_names):
            neighbors.append(device_names[i + 1])
        if i - 1 >= 0:
            neighbors.append(device_names[i - 1])
        
        topology[device] = {
            "interfaces": [
                {
                    "connected_to": neighbor,
                    "interface": f"eth{i+1}"  # Example interface name
                }
                for neighbor in neighbors
            ]
        }
    return topology

def save_topology(testbed, topology, output_file):
    """
    Ajouter la topologie générée au testbed existant et sauvegarder dans un nouveau fichier.
    """
    testbed["topology"] = topology
    with open(output_file, 'w') as file:
        yaml.dump(testbed, file, default_flow_style=False)
    print(f"Topology saved to {output_file}")

if __name__ == "__main__":
    # Fichier d'entrée et de sortie
    input_yaml = "sw_tb_v1.0.yaml"  # Testbed YAML existant
    output_yaml = "sw_tb_generate_topology.yaml"  # Fichier avec la topologie

    # Charger le testbed
    testbed = load_testbed(input_yaml)

    # Vérifier si des appareils existent
    devices = testbed.get("devices", {})
    if not devices:
        print("No devices found in the testbed file.")
    else:
        # Générer la topologie
        topology = generate_topology(devices)

        # Sauvegarder le testbed avec la topologie
        save_topology(testbed, topology, output_yaml)