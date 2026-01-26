#!/Users/taarojek/Documents/Swisscom/DEV/pyats/bin/python3
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: second_script.py
# This file is a part of Swisscom.com
#
# Created: 2025/01/24 15:20:34
# Author: Jeremie Rouzet
#
# Last Modified: 2025/01/24 15:20:34
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Swisscom.com
########################################################################################################################

from genie.testbed import load
import json
import yaml


result = ""


def pretty_print_dict(d, indent=0):
    result = ""
    for k, v in d.items():
        result += "\t"*indent + str(k) + "\n"
        if isinstance(v, dict):
            result += pretty_print_dict(v, indent+1)
        else:
            result += "\t"*(indent+1) + str(v) + "\n"
    return result


testbed = load('sw_tb_v1.0.yaml')
device = testbed.devices['ipt-bei922-g-cme-01.bblab.ch']
device.connect(init_exec_commands=[],
               init_config_commands=[],
               log_stdout=False)
parser = device.parse('show inventory')
print()
formatted_result = pretty_print_dict(parser)
print(formatted_result)
print()
print('The serial number for this chassis is : ' + parser['module_name']['Rack 0']['sn'])
print()
print("Generate YAML and Json File from previous output")
print()
json_inventory = json.dumps(parser)
with open('json_inventory_v1.0.json', 'w') as file:
    json.dump(json_inventory, file, sort_keys=True, indent=4)
print()
yaml_inventory = yaml.safe_load(json_inventory)
with open('yaml_inventory_v1.0.yaml', 'w') as file:
    yaml.dump(yaml_inventory, file, indent=4)
