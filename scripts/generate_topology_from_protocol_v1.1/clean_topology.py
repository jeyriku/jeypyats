#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: clean_topology.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/24 15:42:06
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 15:42:06
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

import yaml


def clean_topology(input_file, output_file):
    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)

    topology = data.get("topology", {})
    cleaned_topology = {}

    for device, details in topology.items():
        cleaned_interfaces = []

        for interface in details.get("interfaces", []):
            connected_to = interface.get("connected_to", "").strip()
            iface = interface.get("interface", "").strip()

            # Conditions pour ignorer les entrées invalides
            if (
                not connected_to
                or not iface
                or connected_to in {"*", "UNAUTHORIZED", "WARNING:", "Total"}
                or iface in {"*", "UNAUTHORIZED", "WARNING:", "entries", "Accessing", "not"}
                or len(iface.split()) > 3  # Évite les phrases hors contexte
            ):
                continue

            # Ajoute uniquement les connexions valides
            cleaned_interfaces.append({"connected_to": connected_to, "interface": iface})

        if cleaned_interfaces:
            cleaned_topology[device] = {"interfaces": cleaned_interfaces}

    # Mise à jour des données avec la topologie nettoyée
    data["topology"] = cleaned_topology

    # Sauvegarde dans un nouveau fichier
    with open(output_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    print(f"Cleaned topology saved to {output_file}")