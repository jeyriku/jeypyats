import json
import logging
from lxml import etree
from ncclient import manager
import xmltodict

logger = logging.getLogger(__name__)

class IOSXERoutingParsersNC:
    def get_default_routes(self):
        """
        Retrieve default routes via NETCONF.
        Returns list of dicts with prefix, protocol, next_hop, metric, interface
        """
        filter_xml = '''
        <filter>
          <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
            <routing-instance>
              <name>default</name>
              <ribs>
                <rib>
                  <name>ipv4-default</name>
                  <routes>
                    <route>
                      <destination-prefix>0.0.0.0/0</destination-prefix>
                    </route>
                  </routes>
                </rib>
              </ribs>
            </routing-instance>
          </routing-state>
        </filter>
        '''
        try:
            with self.netconf_manager() as m:
                response = m.get(filter=filter_xml)
                logger.debug(f"Raw NETCONF response for routing: {etree.tostring(response.data, encoding='unicode')}")
                data_dict = xmltodict.parse(etree.tostring(response.data))
                logger.debug(f"Parsed data_dict for routing: {json.dumps(data_dict, indent=2)}")
                routes_data = data_dict.get('rpc-reply', {}).get('data', {}).get('routing-state', {}).get('routing-instance', {}).get('ribs', {}).get('rib', {}).get('routes', {}).get('route', [])
                if not routes_data:
                    logger.warning("No default routes found in NETCONF response.")
                    return []
                if isinstance(routes_data, dict):
                    routes_data = [routes_data]
                routes = []
                for route in routes_data:
                    prefix = route.get('destination-prefix')
                    protocol = route.get('source-protocol')
                    metric = route.get('metric')
                    next_hop_addr = route.get('next-hop', {}).get('next-hop-address')
                    interface = route.get('next-hop', {}).get('outgoing-interface')
                    routes.append({
                        'prefix': prefix,
                        'protocol': protocol,
                        'next_hop': next_hop_addr,
                        'metric': metric,
                        'interface': interface
                    })
                return routes
        except Exception as e:
            logger.error(f"Failed to retrieve default routes via NETCONF: {e}")
            return []
