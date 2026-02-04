import json
import logging
from lxml import etree
from ncclient import manager
import xmltodict

logger = logging.getLogger(__name__)

class IOSXECellularParsersNC:
    def get_sim_config(self):
        """
        Retrieve SIM configuration via NETCONF.
        Returns dict with slot and data_profile or empty if not found.
        """
        filter_xml = '''
        <filter>
          <cellular xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-cellular-oper">
            <cellular>
              <interface>
                <name>Cellular0/2/0</name>
                <sim/>
              </interface>
            </cellular>
          </cellular>
        </filter>
        '''
        try:
            with self.netconf_manager() as m:
                response = m.get(filter=filter_xml)
                logger.debug(f"Raw NETCONF response for cellular: {etree.tostring(response.data, encoding='unicode')}")
                data_dict = xmltodict.parse(etree.tostring(response.data))
                logger.debug(f"Parsed data_dict for cellular: {json.dumps(data_dict, indent=2)}")
                sim_data = data_dict.get('rpc-reply', {}).get('data', {}).get('cellular', {}).get('cellular', {}).get('interface', {}).get('sim', {})
                if not sim_data:
                    logger.warning("No SIM data found in NETCONF response.")
                    return {}
                return {
                    'slot': sim_data.get('slot'),
                    'data_profile': sim_data.get('data-profile')
                }
        except Exception as e:
            logger.error(f"Failed to retrieve SIM config via NETCONF: {e}")
            return {}
