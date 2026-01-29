#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 23.01.2026 22:58:12
# Author: Jeremie Rouzet
#
# Last Modified: 28.01.2026 16:47:18
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2026 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
This PyATS script aims to test the failover functionality on Cisco IOS XE devices.
It will verify that when the primary route fails, the secondary route takes over seamlessly.
It uses the pyATS framework for test automation.
The setups consists of a Cisco IOS-XE router jey-isr1k-ce-03 configured with EEM scripts to simulate failover scenarios.
The mechanism involves monitoring the state of interfaces and routes, and triggering failover actions accordingly.
To simulate a failure a switch jey-c3560-sw-01 has been installed in between the IOS-XE router supporting the public IP and the ISP modem.
The test will toggle the switch port to simulate link failures and restorations.
A LTE access configured on the same router will serve as the secondary route to the internet.
The test will validate that traffic is rerouted to the LTE link when the primary link goes down and returns to the primary link when it is restored.
The test will include checks for route availability, interface status, and connectivity to external networks.
The results will be logged for analysis and verification of the failover functionality.
The test assumes that the devices are pre-configured with the necessary routing and EEM scripts to handle failover scenarios.
The test will shut and no shut the switch port connected to the isp modem to simulate a routing failure and restoration.
The link between jey-c3560-sw-01 and the isp modem represents the primary route to the internet.
The link between jey-isr1k-ce-03 and jey-c3560-sw-01 will remain up at all times.
'''

import logging
from pyats import aetest
from pyats.topology import loader
from jeypyats.parsers.iosxe.iosxe_routing_parsers_nc import IOSXERoutingParsersMixin
from jeypyats.parsers.iosxe.iosxe_interface_parsers_nc import IOSXEInterfacesParsersMixin
from jeypyats.utils.utils import block_if_fails
from jeypyats.utils.utils import teardown
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JeylanCommonSetup(aetest.CommonSetup):
    """
    Common setup for Jeylan failover tests.
    This section connects to all devices defined in the testbed.
    """
    @aetest.subsection
    def connect_to_devices(self, testbed):
        """ Connect to all devices in the testbed """
        self.testbed = loader.load(testbed)
        for device in self.testbed.devices.values():
            logger.info(f"Connecting to device: {device.name}")
            device.connect()
        logger.info("All devices connected successfully.")

    @aetest.subsection
    def check_connectivity(self):
        """ Check connectivity to all devices """
        for device in self.testbed.devices.values():
            if device.is_connected():
                logger.info(f"Device {device.name} is connected.")
            else:
                logger.error(f"Device {device.name} is not connected.")
                raise Exception(f"Failed to connect to device {device.name}.")

    @aetest.subsection
    def check_os_version(self):
        """ Check OS version of all devices """
        for device in self.testbed.devices.values():
            os_version = device.os_version
            logger.info(f"Device {device.name} is running OS version: {os_version}")


class FailoverTestcase(aetest.Testcase, IOSXERoutingParsersMixin, IOSXEInterfacesParsersMixin):
    """
    This testcase verifies the failover functionality on Cisco IOS XE devices.
    In this testcase, we will simulate a failure on the primary route and check if the secondary route takes over.
    The failure will happen on jey-c3560-sw-01 by shutting down the port connected to the ISP modem Teng1/0/1.
    The port connected to jey-isr1k-ce-03 will remain up at all times.
    The test will connect to jey-isr1k-ce-03 to check the routing table before and after the failover.
    The test will also verify connectivity to an external network such as the internet.
    Then the jey-c3560-sw-01 switch port Teng1/0/1 will be shutdown to simulate the failure.
    After a short wait, the test will verify that the secondary route is now active.
    Finally, the test will restore the primary route by bringing the port back up and verify that traffic returns to the primary route.
    """
    # Setup for the testcase
    @aetest.setup
    def setup(self):
        """ Setup for the failover testcase """
        self.ce = self.parent.testbed.devices['jey-isr1k-ce-03']
        self.sw = self.parent.testbed.devices['jey-c3560-sw-01']
        logger.info("Failover testcase setup complete.")

    # Check primary route before failover on jey-isr1k-ce-03 using netconf parsers
    @block_if_fails
    @aetest.test
    def check_primary_route(self):
        """ Check primary route is active before failover """
        primary_route = self.ce.get_routing_table_default_routes()
        logger.info(f"Primary route before failover: {primary_route}")
        assert primary_route, "Primary route is not active before failover."
        # Confirm that the primary route is via the ISP modem through interface GigabitEthernet0/0/0
        assert any(route['interface'] == 'GigabitEthernet0/0/0' for route in primary_route), "Primary route is not via the expected interface."
        logger.info("Primary route is active and correct before failover.")

    @block_if_fails
    @aetest.test
    def check_lte_connectivity(self):
        """ Check that LTE connectivity is available before failover """
        lte_status = self.ce.get_interfaces_cellular_status()
        logger.info(f"LTE interface status before failover: {lte_status}")
        assert lte_status, "LTE interface is not available before failover."
        assert any(status['oper_status'] == 'up' for status in lte_status.values()), "LTE interface is not up before failover."
        logger.info("LTE connectivity is available before failover.")

    @aetest.test
    def simulate_failover(self, steps):
        """ Simulate failover by shutting down the switch port connected to the ISP modem """
        logger.info("Simulating failover by shutting down switch port Teng1/0/1 on jey-c3560-sw-01.")
        with steps.start("Shut down switch port Teng1/0/1 to simulate ISP link failure"):
            self.sw.configure('interface Teng1/0/1', 'shutdown')
            logger.info("Switch port Teng1/0/1 is now shut down.")
            # Wait for a short period to allow failover to take effect
            time.sleep(30)
        with steps.start("Check secondary route is active after failover"):
            secondary_route = self.ce.get_routing_table_default_routes()
            logger.info(f"Route after failover: {secondary_route}")
            assert secondary_route, "No route found after failover."
            # Confirm that the secondary route is via the LTE interface GigabitEthernet0/0/1
            assert any(route['interface'] == 'GigabitEthernet0/0/1' for route in secondary_route), "Secondary route is not via the expected interface."
            logger.info("Secondary route is active and correct after failover.")

    @aetest.test
    def restore_primary_route(self, steps):
        """ Restore primary route by bringing the switch port back up """
        logger.info("Restoring primary route by bringing switch port Teng1/0/1 back up on jey-c3560-sw-01.")
        with steps.start("Bring up switch port Teng1/0/1 to restore ISP link"):
            self.sw.configure('interface Teng1/0/1', 'no shutdown')
            logger.info("Switch port Teng1/0/1 is now up.")
            # Wait for a short period to allow route restoration to take effect
            time.sleep(30)
        with steps.start("Check primary route is active after restoration"):
            restored_route = self.ce.get_routing_table_default_routes()
            logger.info(f"Route after restoration: {restored_route}")
            assert restored_route, "No route found after restoration."
            # Confirm that the primary route is again via the ISP modem through interface GigabitEthernet0/0/0
            assert any(route['interface'] == 'GigabitEthernet0/0/0' for route in restored_route), "Primary route is not via the expected interface after restoration."
            logger.info("Primary route is active and correct after restoration.")

    # Teardown for the testcase
    @teardown
    def teardown(self):
        """ Teardown for the failover testcase """
        logger.info("Failover testcase teardown complete.")


if __name__ == '__main__':
    aetest.main()
