import json
import logging
from lxml import etree
from ncclient import manager
import xmltodict

logger = logging.getLogger(__name__)

class IOSXEIPSLAParsersNC:
    def get_ip_sla_states(self):
        """
        Retrieve IP SLA operational states via NETCONF.
        Returns dict of sla_index: oper_state
        """
        filter_xml = '''
        <filter>
          <ip-sla-stats xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ip-sla-oper">
            <ip-sla-stat>
              <sla-index/>
              <oper-state/>
            </ip-sla-stat>
          </ip-sla-stats>
        </filter>
        '''
        try:
            with self.netconf_manager() as m:
                response = m.get(filter=filter_xml)
                logger.debug(f"Raw NETCONF response for IP SLA: {etree.tostring(response.data, encoding='unicode')}")
                data_dict = xmltodict.parse(etree.tostring(response.data))
                logger.debug(f"Parsed data_dict for IP SLA: {json.dumps(data_dict, indent=2)}")
                sla_data = data_dict.get('rpc-reply', {}).get('data', {}).get('ip-sla-stats', {}).get('ip-sla-stat', [])
                if not sla_data:
                    logger.warning("No IP SLA data found in NETCONF response.")
                    return {}
                if isinstance(sla_data, dict):
                    sla_data = [sla_data]
                sla_states = {}
                for sla in sla_data:
                    index = sla.get('sla-index')
                    state = sla.get('oper-state')
                    if index and state:
                        sla_states[str(index)] = state
                return sla_states
        except Exception as e:
            logger.error(f"Failed to retrieve IP SLA states via NETCONF: {e}")
            return {}
