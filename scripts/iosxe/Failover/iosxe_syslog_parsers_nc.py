import json
import logging
import re
from lxml import etree
from ncclient import manager
import xmltodict

logger = logging.getLogger(__name__)

class IOSXESyslogParsersNC:
    def get_buffered_syslog_messages(self, filter_text=None):
        """
        Retrieve buffered syslog messages via NETCONF.
        Returns list of dicts with timestamp, facility, text.
        """
        filter_xml = '''
        <filter>
          <logging xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-logging">
            <buffered>
              <messages/>
            </buffered>
          </logging>
        </filter>
        '''
        try:
            with self.netconf_manager() as m:
                response = m.get(filter=filter_xml)
                logger.debug(f"Raw NETCONF response for syslog: {etree.tostring(response.data, encoding='unicode')}")
                data_dict = xmltodict.parse(etree.tostring(response.data))
                logger.debug(f"Parsed data_dict for syslog: {json.dumps(data_dict, indent=2)}")
                messages_str = data_dict.get('rpc-reply', {}).get('data', {}).get('logging', {}).get('buffered', {}).get('messages', '')
                if not messages_str:
                    logger.warning("No syslog messages found in NETCONF response.")
                    return []
                # Split the string into lines
                lines = messages_str.strip().split('\n')
                messages = []
                for line in lines:
                    # Parse line, assuming format like: *Feb  4 17:20:35.123: %SYS-5-CONFIG_I: Configured from console by console
                    match = re.match(r'\*(\w+\s+\d+\s+\d+:\d+:\d+\.\d+):\s+%(\w+-\d+-\w+):\s+(.*)', line)
                    if match:
                        timestamp, facility, text = match.groups()
                        if filter_text and filter_text.lower() not in text.lower():
                            continue
                        messages.append({
                            'timestamp': timestamp,
                            'facility': facility,
                            'text': text
                        })
                return messages
        except Exception as e:
            logger.error(f"Failed to retrieve syslog messages via NETCONF: {e}")
            return []
