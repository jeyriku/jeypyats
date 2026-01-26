#!/usr/bin/env python3
# -*- coding:utf-8 -*-
########################################################################################################################

# File: basic_connectivity.py
# This file is a part of Swisscom.com

# Created: 2025-01-22 14:37:03
# Author: Jeremie Rouzet

# Last Modified: 2025-01-22 14:37:03
# Modified By: Jeremie Rouzet

# Copyright (c) 2025 Swisscom.com
########################################################################################################################


# Start by importing the necessary modules from pyATS. We'll need ‘aetest’ for creating test cases and ‘Topology’ for managing network states:
from pyats.aetest import Testcase, test
import subprocess
import sys
import yaml

# Next, load your network topology. Typically, you would have a YAML or JSON file that describes your network’s topology:
# testbed = loader.load('sw_tb_v1.0.yaml')
            
class ConnectivityTest(Testcase):

    def __init__(self, file_yaml):
        # Load data from the YAML file
        with open(file_yaml, 'r') as file:
            self.data = yaml.safe_load(file)
        self.devices = []

    @test
    def check_connectivity(self):
# Get the testbed from YAML file
        devices = self.data.get('devices', {})
        print()
        print("Testbed devices is :", devices)
        
# Loop through the devices in the testbed      
        for device_name, device_list in devices.items():
            try:
# Assuming you have a method to create device instances
                device = self.create_device(device_list) 
                print()
                print(f"Checking connectivity for device: {device_name} ({device.alias})")
                print()
                print(f"Connectivity for device: ({device.alias}) is fine")
                
# Attempt to ping a device (assuming device has a method for ping)
# Replace 'IP_ADDRESS' with a valid address
                connected = device.ping(device_list.get('alias', ''))
                assert connected, f"Connection failed for device {device_name}"
                
# If successful, add device to the list
                self.devices.append(device)
                print()
                print("Device list members are :", {device_name})
# Error handling is essential for understanding when and why a test fails. Update your test script to handle potential exceptions and provide meaningful error messages:            
            except Exception as e:
                self.failed(f"Test failed for device {device_name}\
                            due to: {str(e)}")
                print()
                print(f"Error for {device_name}: {str(e)}")

# After checking all devices, display the results
        print()
        print("Successfully connected devices:", (device_name))
# For learning purpose
        print()
        print("Successfully connected devices:",
              [device.alias for device in self.devices])
        print()

# Example method to create a device instance (adjust as per your logic)
    def create_device(self, device_list):
# This method will create and return a device instance based on the data in the YAML file
# Modify this according to your device management strategy.
        class Device:
            def __init__(self, alias, ip):
                self.alias = alias
                self.ip = ip

            def ping(self, ip_address):
                print()
                print(f"Performing real ping to {ip_address}...")

                try:
# Utilisation de la bibliothèque subprocess pour effectuer un ping
# Vérifie le système d'exploitation
                    param = "-n" if sys.platform.lower() == "win32" else "-c"

# Lancer la commande ping
                    command = ["ping", param, "4", ip_address]  # "4" est le nombre de paquets envoyés

# Exécuter la commande
                    response = subprocess.run(command, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)

# Vérifier si le ping a réussi en fonction du code de retour
                    if response.returncode == 0:
                        print()
                        print(f"Ping to {ip_address} successful!")
                        return True
                    else:
                        print(f"Ping to {ip_address} failed!")
                        print()
                        return False

                except Exception as e:
                    print(f"An error occurred during the ping test: {e}")
                    print()
                    return False
        return Device(device_list['alias'], device_list.get('alias', ''))


file_yaml = "sw_tb_v1.0.yaml"
device_list = ConnectivityTest(file_yaml)
device_list.check_connectivity()