#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
# This file is a part of Netalps.fr.
#
# Created: 23.01.2026 22:58:12
# Author: Jeremie Rouzet
#
# Last Modified: 04.02.2026 10:08:08
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
from jeypyats.utils.utils import block_if_fails
from jeypyats.utils.utils import teardown
from utils import apply_netconf_parsers
from jeypyats.utils.netconf_connector import NetconfConnectorConnection
import time
import json


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JeylanCommonSetup(aetest.CommonSetup, NetconfConnectorConnection):
    """
    Common setup for Jeylan failover tests.
    This section connects to all devices defined in the testbed.
    """
    @block_if_fails
    @aetest.subsection
    def load_testbed(self):
        """ Load the testbed file """
        self.testbed = self.parameters['testbed']
        logger.info("Testbed loaded successfully.")

    @block_if_fails
    @aetest.subsection
    def connect_to_devices(self):
        """ Connect to all devices in the testbed """
        self.testbed = self.parameters['testbed']
        self.parent.testbed = self.testbed
        for device in self.testbed.devices.values():
            logger.info(f"Connecting to device: {device.name}")
            device.connect()
            if device.name == 'jey-isr1k-ce-03':
                # Get the NETCONF connection from the custom class
                self.connect()
        logger.info("All devices connected successfully.")

    @block_if_fails
    @aetest.subsection
    def check_connectivity(self):
        """ Check connectivity to all devices """
        for device in self.testbed.devices.values():
            if device.is_connected():
                logger.info(f"Device {device.name} is connected.")
            else:
                logger.error(f"Device {device.name} is not connected.")
                raise Exception(f"Failed to connect to device {device.name}.")


class FailoverTestcase(aetest.Testcase):
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
        self.testbed = loader.load(self.parameters['testbed'])
        self.ce = self.testbed.devices['jey-isr1K-ce-03']
        self.sw = self.testbed.devices['jey-c3560-sw-01']
        self.ce.connect()
        self.sw.connect()
        # Ajouter les méthodes aux instances des devices
        apply_netconf_parsers(self.ce)
        logger.info("Failover testcase setup complete.")

    @aetest.test
    def check_initial_state(self, steps):
        """ Check initial state: primary route active, SLA/tracks up, SIM slot 0 """
        with steps.start("Check primary route is active initially"):
            primary_route = self.ce.get_routing_table_default_routes()
            logger.info(f"Primary route initially: {json.dumps(primary_route, indent=2)}")
            assert primary_route, "No default route found initially."
            # Check for tracked default route via FTTH gateway
            assert any(route.get('next_hop') == '82.66.83.254' for route in primary_route), "Tracked default route via FTTH not found."
            logger.info("Primary route is active and correct initially.")

        with steps.start("Check IP SLA and track states initially"):
            sla_states = self.ce.get_ip_sla_states()
            logger.info(f"IP SLA states: {json.dumps(sla_states, indent=2)}")
            if sla_states:
                assert sla_states.get('1', {}).get('oper_state') == 'active', "SLA 1 not active."
            else:
                logger.warning("No SLA states found, assuming SLA not configured or not retrievable via NETCONF.")

            track_states = self.ce.get_track_states()
            logger.info(f"Track states: {json.dumps(track_states, indent=2)}")
            if track_states:
                assert track_states.get('1', {}).get('state') == 'up', "Track 1 not up."
            else:
                logger.warning("No track states found, assuming tracks not configured or not retrievable via NETCONF.")
            logger.info("SLA and tracks checked initially.")

        with steps.start("Check initial SIM slot (should be 0 for Free)"):
            sim_config = self.ce.get_cellular_sim_config('Cellular0/2/0')
            logger.info(f"Initial SIM config: {json.dumps(sim_config, indent=2)}")
            if sim_config:
                assert sim_config.get('slot') == 0, "SIM not on slot 0 initially."
                assert sim_config.get('data_profile') == 1, "Data profile not 1 initially."
                logger.info("SIM is on slot 0 (Free) initially.")
            else:
                logger.warning("No SIM config found, assuming cellular not configured or not retrievable via NETCONF.")

        with steps.start("Check LTE interface status"):
            lte_status = self.ce.get_interface_status('Cellular0/2/0')
            logger.info(f"LTE interface Cellular0/2/0 status: {json.dumps(lte_status, indent=2)}")
            assert lte_status.get('oper_status') == 'up', f"LTE interface is not up: {lte_status}"
            logger.info("LTE interface is up initially.")

    @aetest.test
    def simulate_failover(self, steps):
        """ Simulate failover by shutting down the switch port connected to the ISP modem """
        logger.info("Simulating failover by shutting down switch port Teng1/0/1 on jey-c3560-sw-01.")
        # Shut down the switch port to simulate ISP link failure
        with steps.start("Shut down switch port Teng1/0/1 to simulate ISP link failure"):
            self.sw.configure(['interface Teng1/0/1', 'shutdown'])
            logger.info("Switch port Teng1/0/1 is now shut down.")
            # Wait for a short period to allow failover to take effect
            time.sleep(45)
        # Check logs for EEM failover event on jey-isr1k-ce-03 using netconf parsers
        with steps.start("check router log for eem failover event"):
            syslog_messages = self.ce.get_syslog_messages(filter_text='Bascule automatique vers SIM1')
            logger.info(f"Syslog messages for SIM switch: {json.dumps(syslog_messages, indent=2)}")
            if not syslog_messages:
                logger.warning("No SIM switch messages found in syslog after shutdown. This may indicate EEM script is not configured or triggered.")
            else:
                logger.info("SIM switch messages found in syslog.")
            # Wait for a short period to allow failover to take effect
            time.sleep(45)
        # Check secondary route after failover on jey-isr1k-ce-03 using netconf parsers
        with steps.start("Check secondary route is active after failover"):
            secondary_route = self.ce.get_routing_table_default_routes()
            logger.info(f"Route after failover: {json.dumps(secondary_route, indent=2)}")
            assert secondary_route, "No route found after failover."
            # Confirm that the secondary route is via the LTE interface Cellular0/2/0
            assert any(route['interface'] == 'Cellular0/2/0' for route in secondary_route), "Secondary route is not via the expected interface."
            logger.info("Secondary route is active and correct after failover.")
        with steps.start("check router log for eem failover event"):
            syslog_messages = self.ce.get_syslog_messages(filter_text='Bascule automatique vers SIM1')
            logger.info(f"Syslog messages for SIM switch: {json.dumps(syslog_messages, indent=2)}")
            if not syslog_messages:
                logger.warning("No SIM switch messages found in syslog after route check. This may indicate EEM script is not configured or triggered.")
            else:
                logger.info("SIM switch messages found in syslog.")

        with steps.start("Check SIM slot switched to 1 (Orange)"):
            sim_config = self.ce.get_cellular_sim_config('Cellular0/2/0')
            logger.info(f"SIM config after failover: {json.dumps(sim_config, indent=2)}")
            if sim_config:
                assert sim_config.get('slot') == 1, "SIM not switched to slot 1."
                assert sim_config.get('data_profile') == 2, "Data profile not switched to 2."
                logger.info("SIM switched to slot 1 (Orange) after failover.")
            else:
                logger.warning("No SIM config found after failover.")

    @aetest.test
    def restore_primary_route(self, steps):
        """ Restore primary route by bringing the switch port back up """
        logger.info("Restoring primary route by bringing switch port Teng1/0/1 back up on jey-c3560-sw-01.")
        # Bring the switch port back up to restore ISP link
        with steps.start("Bring up switch port Teng1/0/1 to restore ISP link"):
            self.sw.configure(['interface Teng1/0/1', 'no shutdown'])
            logger.info("Switch port Teng1/0/1 is now up.")
            # Wait for a short period to allow route restoration to take effect
            time.sleep(20)
        # Check primary route after restoration on jey-isr1k-ce-03 using netconf parsers
        with steps.start("Check primary route is active after restoration"):
            restored_route = self.ce.get_routing_table_default_routes()
            logger.info(f"Route after restoration: {json.dumps(restored_route, indent=2)}")
            assert restored_route, "No route found after restoration."
            # Confirm that the primary route is again via the FTTH gateway
            assert any(route.get('next_hop') == '82.66.83.254' for route in restored_route), "Primary route is not via the expected next hop after restoration."
            logger.info("Primary route is active and correct after restoration.")

        with steps.start("Check syslog for FTTH restore message"):
            syslog_messages = self.ce.get_syslog_messages(filter_text='FTTH restored')
            logger.info(f"Syslog messages for FTTH restore: {json.dumps(syslog_messages, indent=2)}")
            assert syslog_messages, "No EEM FTTH restore message found in syslog."
            logger.info("EEM confirmed FTTH restoration.")

        with steps.start("Check SIM slot restored to 0 (Free)"):
            sim_config = self.ce.get_cellular_sim_config('Cellular0/2/0')
            logger.info(f"SIM config after restoration: {json.dumps(sim_config, indent=2)}")
            if sim_config:
                assert sim_config.get('slot') == 0, "SIM not restored to slot 0."
                assert sim_config.get('data_profile') == 1, "Data profile not restored to 1."
                logger.info("SIM restored to slot 0 (Free) after FTTH recovery.")
            else:
                logger.warning("No SIM config found after restoration.")

class common_teardown(aetest.CommonCleanup):
    """
    Common teardown for Jeylan failover tests.
    This section disconnects from all devices defined in the testbed.
    """
    # Teardown for the testcase
    @aetest.subsection
    def teardown(self, steps):
        """ Teardown for the failover testcase """
        with steps.start("Disconnect from devices"):
            # Disconnect from devices
            if hasattr(self, 'ce') and self.ce:
                self.ce.disconnect()
            if hasattr(self, 'sw') and self.sw:
                self.sw.disconnect()
            logger.info("Disconnected from all devices.")
        logger.info("Failover testcase teardown complete.")


if __name__ == '__main__':
    aetest.main()
