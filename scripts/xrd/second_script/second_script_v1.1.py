#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: second_script.py
# This file is a part of Netalps.fr
#
# Created: 2025/01/24 15:20:34
# Author: Jeremie Rouzet
#
# Last Modified: 27.01.2026 19:42:57
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################

from genie.testbed import load
import json
import yaml
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Second Script v1.1')
    parser.add_argument('--testbed',
                       default='../testbed/xrd/xrd_sw_tb_v1.0.yaml',
                       help='Path to the testbed YAML file')
    args = parser.parse_args()

    testbed_file = args.testbed
    if not os.path.exists(testbed_file):
        print(f"Error: Testbed file {testbed_file} not found")
        return

    testbed = load(testbed_file)
    device = testbed.devices['ipt-bei922-g-cme-01.bblab.ch']
    device.connect(init_exec_commands=[],
                   init_config_commands=[],
                   log_stdout=False)
    parser = device.parse('show inventory')
    pparse = json.dumps(parser, indent=4)
    print("The chassis inventory is as follows : \n", pparse)
    print()
    print('The serial number for this chassis is : ' + parser['module_name']['Rack 0']['sn'])
    print()
    print("Generate YAML and Json File from previous output")
    print()
    json_inventory = json.dumps(parser)
    with open('json_inventory_v1.1.json', 'w') as file:
        json.dump(json_inventory, file, sort_keys=True, indent=4)
    print()
    yaml_inventory = yaml.safe_load(json_inventory)
    with open('yaml_inventory_v1.1.yaml', 'w') as file:
        yaml.dump(yaml_inventory, file, indent=4)

if __name__ == "__main__":
    main()
