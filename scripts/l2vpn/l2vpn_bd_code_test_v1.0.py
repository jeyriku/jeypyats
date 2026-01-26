"""Stores Unit-Tests for IOS-XR L2VPN Netconf parsers"""

__author__ = ["Jeremie Rouzet <jeremie.rouzet@swisscom.com>"]

__contact__ = "jeremie.rouzet@swisscom.com"
__copyright__ = "Swisscom AG, 2025"
__license__ = "Apache 2.0"

import unittest
from stayp.utils.libs.assertions import CustomAssertions
from unittest.mock import MagicMock

from stayp.parsers.libs.iosxr.netconf import ParsersMixin
from stayp.utils.libs.rpc_msgs import BASE_RPC
from stayp.utils.libs.utils import sanitize_xml
from stayp.utils.libs.exceptions import StaypValueError


class TestL2vpnParsersMixin(unittest.TestCase, CustomAssertions):
    """Stores Unit-Tests for L2VPN IOS-XR Netconf parsers"""

    def setUp(self):
        """Method for creating a mocked_device
        Used for Unit-Tests
        """
        self.mocked_device = ParsersMixin()
        # Mock the configure method to avoid making actual network requests
        self.mocked_device.request = MagicMock()
        self.maxDiff = None

    def test_get_l2vpn_bridge_domain_brief(self):
        """Tests the get_l2vpn_bridge_domain parser brief mode
        """
        node_id = "0/RP0/CPU0"
        l2vpn_bdgn = "BG_IB_MGMT"
        l2vpn_bdn = "BD_IB_MGMT_0001"
        l2vpn_bds = "bridge-up"
        reply_xml = L2VPN_BD_BRIEF
        self.mocked_device.request.return_value.xml = reply_xml
        
        result = self.mocked_device.get_l2vpn_bridge_domain_brief()

        expected_result = {
            "BD_IB_MGMT_0001": {'state': 'bridge-up'}
        }

        self.assertDictContainsSubDict(result, expected_result)

        expected_rpc = f"""
        <l2vpnv2 xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-l2vpn-oper">
          <nodes>
            <node>
            <node-id>{node_id}</node-id>
            <bridge-domains>
              <bridge-domain>
              <bridge-domain-group-name>{l2vpn_bdgn}</bridge-domain-group-name>
              <bridge-domain-name>{l2vpn_bdn}</bridge-domain-name>
              <bridge-domain-info>
                <bridge-state>{l2vpn_bds}</bridge-state>
              </bridge-domain-info>
              </bridge-domain>
            </bridge-domains>
            </node>
          </nodes>
        </l2vpnv2>
        """
        expected_rpc = BASE_RPC.format(xml_rpc=expected_rpc)
        expected_rpc = sanitize_xml(expected_rpc)
        self.mocked_device.request.assert_called_with(msg=expected_rpc, return_obj=True)


########################
# REPLYS GO AT THE END #
########################
L2VPN_BD_BRIEF = """
<rpc-reply xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:ed9cfaaf-c66d-4be2-b833-1f28a070a5d5">
 <data>
  <l2vpnv2 xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-l2vpn-oper">
   <nodes>
    <node>
     <node-id>0/RP0/CPU0</node-id>
     <bridge-domains>
      <bridge-domain>
       <bridge-domain-group-name>BG_IB_MGMT</bridge-domain-group-name>
       <bridge-domain-name>BD_IB_MGMT_0001</bridge-domain-name>
       <bridge-domain-info>
        <bridge-state>bridge-up</bridge-state>
       </bridge-domain-info>
      </bridge-domain>
     </bridge-domains>
    </node>
   </nodes>
  </l2vpnv2>
 </data>
</rpc-reply>
"""