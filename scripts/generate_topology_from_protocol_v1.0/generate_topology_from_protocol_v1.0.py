#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: generate_topology_from_protocol.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/24 14:17:45
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 14:17:45
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

import yaml
import subprocess


def load_testbed(file_path):
    """
    Charger le fichier YAML du testbed.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def fetch_neighbors_via_lldp_or_cdp(device):
    """
    Récupérer les voisins d'un appareil en utilisant LLDP/CDP.
    Cette fonction exécute une commande distante (simulée ici).
    """
    try:
        # Simulation : Remplacez cela par une vraie commande à envoyer à l'appareil
        # Exemples : "show lldp neighbors" ou "show cdp neighbors"
        output = subprocess.check_output(
            f"ssh {device['alias']} 'show lldp neighbors'",
            shell=True,
            text=True,
        )
        return output

    except Exception as e:
        print(f"Erreur lors de la collecte des voisins pour {device['alias']}: {e}")
        return None


def parse_neighbors(output):
    """
    Analyser la sortie LLDP/CDP pour obtenir les voisins.
    """
    neighbors = []

    if output:
        for line in output.splitlines():
            # Supposons que la sortie contient un tableau avec des colonnes Device-ID et Port-ID
            # Ex : "Switch1     Gi1/0/1"
            parts = line.split()
            if len(parts) >= 2:
                neighbors.append({"device": parts[0], "interface": parts[1]})

    return neighbors


def generate_topology(devices):
    """
    Générer une topologie à partir des données LLDP/CDP.
    """
    topology = {}

    for device_name, device in devices.items():
        # Collecter les voisins
        print(f"Collecte des voisins pour {device_name} ({device['alias']})...")
        output = fetch_neighbors_via_lldp_or_cdp(device)

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


def save_topology(testbed, topology, output_file):
    """
    Ajouter la topologie générée au testbed existant et sauvegarder dans un fichier.
    """
    testbed["topology"] = topology
    with open(output_file, 'w') as file:
        yaml.dump(testbed, file, default_flow_style=False)
    print(f"Topology saved to {output_file}")


if __name__ == "__main__":
    # Fichiers d'entrée et de sortie
    input_yaml = "sw_tb_v1.0.yaml"  # Testbed YAML existant
    output_yaml = "sw_tb_generate_topology_from_protocol_v1.0.yaml"  # Fichier avec la topologie

    # Charger le testbed
    testbed = load_testbed(input_yaml)

    # Vérifier si des appareils existent
    devices = testbed.get("devices", {})
    if not devices:
        print("Aucun appareil trouvé dans le fichier testbed.")
    else:
        # Générer la topologie basée sur LLDP/CDP
        topology = generate_topology(devices)

        # Sauvegarder le testbed avec la topologie
        save_topology(testbed, topology, output_yaml)