#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: main.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/24 14:38:57
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 14:38:57
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

from utils.file_manager import load_yaml
from topology.builder import generate_topology
from topology.saver import save_topology

def main():
    # Fichiers d'entrée et de sortie
    input_yaml = "sw_tb_v1.0.yaml"
    output_yaml = "sw_tb_generate_topology_from_protocol_v1.1.yaml"

    # Charger le testbed
    testbed = load_yaml(input_yaml)

    # Vérifier si des appareils existent
    devices = testbed.get("devices", {})
    if not devices:
        print("Aucun appareil trouvé dans le fichier testbed.")
        return

    # Générer la topologie basée sur LLDP/CDP
    topology = generate_topology(devices)

    # Sauvegarder le testbed avec la topologie
    save_topology(testbed, topology, output_yaml)

if __name__ == "__main__":
    main()