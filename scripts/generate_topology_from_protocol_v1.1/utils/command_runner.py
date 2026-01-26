#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: command_runner.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/24 14:41:47
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 14:41:47
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

import subprocess

def run_command_on_device(alias, command):
    """
    Exécuter une commande distante sur un appareil.
    """
    try:
        output = subprocess.check_output(
            f"ssh {alias} '{command}'",
            shell=True,
            text=True,
        )
        return output
    except subprocess.CalledProcessError as e:
        print(f"Erreur d'exécution de la commande sur {alias}: {e}")
        return None