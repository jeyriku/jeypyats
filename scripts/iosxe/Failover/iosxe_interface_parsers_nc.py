import json
import logging
from lxml import etree
from ncclient import manager
import xmltodict

logger = logging.getLogger(__name__)

class IOSXEInterfaceParsersNC:
    def get_interface_status(self, interface_name):
        """
        Retrieve interface operational status via NETCONF.
        Returns dict with oper_status, admin_status
        """
        filter_xml = f'''
        <filter>
          <interfaces xmlns="http://openconfig.net/yang/interfaces">
            <interface>
              <name>{interface_name}</name>
              <state>
                <oper-status/>
                <admin-status/>
              </state>
            </interface>
          </interfaces>
        </filter>
        '''
        try:
            with self.netconf_manager() as m:
                response = m.get(filter=filter_xml)
                logger.debug(f"Raw NETCONF response for interface {interface_name}: {etree.tostring(response.data, encoding='unicode')}")
                data_dict = xmltodict.parse(etree.tostring(response.data))
                logger.debug(f"Parsed data_dict for interface {interface_name}: {json.dumps(data_dict, indent=2)}")
                intf_data = data_dict.get('rpc-reply', {}).get('data', {}).get('interfaces', {}).get('interface', {}).get('state', {})
                if not intf_data:
                    logger.warning(f"No interface data found for {interface_name} in NETCONF response.")
                    return {}
                return {
                    'oper_status': intf_data.get('oper-status'),
                    'admin_status': intf_data.get('admin-status')
                }
        except Exception as e:
            logger.error(f"Failed to retrieve interface status for {interface_name} via NETCONF: {e}")
            return {}
