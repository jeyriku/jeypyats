#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: file_manager.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/24 14:41:10
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 14:41:10
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

import yaml

def load_yaml(file_path):
    """
    Charger un fichier YAML.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def save_yaml(data, file_path):
    """
    Sauvegarder un fichier YAML.
    """
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)