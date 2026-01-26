"""
This module provides a collection of L2VPN RPCs for configuring IOS-XR devices using NETCONF.
"""

__author__ = ["Jeremie Rouzet <jeremie.rouzet@swisscom.com>"]

__contact__ = "jeremie.rouzet@swisscom.com"
__copyright__ = "Swisscom AG, 2025"
__license__ = "Apache 2.0"

#RP/0/RP0/CPU0:ipt-far923-a-aea-01#sh l2vpn bridge-domain brief
#Cisco-IOS-XR-l2vpn-oper:l2vpnv2/active/bridge-domains/bridge-domain/bridge-domain-info

import xmltodict
import logging
from genie.utils import Dq
from lxml import etree
from packaging import version
from stayp.utils.libs.exceptions import StaypValueError, StaypNotImplementedError
from stayp.utils.libs.rpc_msgs import BASE_RPC
from stayp.utils.libs.utils import sanitize_xml

parser = etree.XMLParser()
parser.set_element_class_lookup(
    etree.ElementDefaultClassLookup(element=etree.ElementBase)
)

log = logging.getLogger(__name__)


class L2vpnParsersMixin:
    """
    Collection of RPCs for parsing L2VPNs on IOS-XR devices
    """

    __os_version__ = version.parse("7.10.2")  # Min version tested

    def get_l2vpn_bridge_domain_brief(self):
        """
        Retrieve L2VPN informations such as Bridge-Groups & Bridge-Domains.

        Note:
            Equivalent to the following CLI command:
            ::
               show l2vpn bridge-domain brief 
        Returns:
            dict: A dictionary where the keys could be (not mandatory here) :
                - bridge-domain-group-name
                - bridge-domain-name
            and the values are 
                - their status.
                - Number of ACs
                - Number of PWs
                - Number of PBBs
                - Number of VNIs
        Raises:
            Any exceptions raised by the request or XML parsing functions.
        Example:
            bridge_domain = get_bridge-domain bd-name("BD_IB_MGMT_0001")
            print(neighbors)
        """
        xml_rpc = """
        <l2vpnv2 xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-l2vpn-oper">
            <nodes>
            <node>
                <bridge-domains>
                <bridge-domain>
                    <bridge-domain-info>
                    <bridge-state/>
                    </bridge-domain-info>
                </bridge-domain>
                </bridge-domains>
            </node>
            </nodes>
        </l2vpnv2>
        """

        root = etree.fromstring(xml_rpc, parser)
#        element = root.xpath(".//*[name()='vrf-name']")[0]
#        element.text = vrf_name

        xml_rpc = etree.tostring(root, encoding="utf-8").decode()
        xml_rpc = BASE_RPC.format(xml_rpc=xml_rpc)
        xml_rpc = sanitize_xml(xml_rpc)

        reply = self.request(msg=xml_rpc, return_obj=True)
        reply_dict = xmltodict.parse(reply.xml)
        if not reply.ok or reply_dict["rpc-reply"]["data"] is None:
            return {}

        reply_dict = reply_dict["rpc-reply"]["data"]["l2vpnv2"]["nodes"]["node"]["bridge-domains"]["bridge-domain"]

        result = {}
#        reply_dict = reply_dict["bridge-domain-info"]
        if not isinstance(reply_dict, list):
            reply_dict = [reply_dict]
        for bridge_domain_info in reply_dict:
            bridge_domain = Dq(bridge_domain_info).get_values("bridge-domain-name")[0]
            bridge_state = Dq(bridge_domain_info).get_values("bridge-state")[0]
            if bridge_domain and bridge_state:
                result[bridge_domain] = {'state': bridge_state}

        return result