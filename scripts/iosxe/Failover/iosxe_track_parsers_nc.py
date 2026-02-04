import json
import logging
from lxml import etree
from ncclient import manager
import xmltodict

logger = logging.getLogger(__name__)

class IOSXETrackParsersNC:
    def get_track_states(self):
        """
        Retrieve track states via NETCONF.
        Returns a dict of track_id: {'state': state}
        """
        filter_xml = '''
        <filter>
          <track xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-track">
            <track>
              <track-id/>
              <state/>
            </track>
          </track>
        </filter>
        '''
        try:
            with self.netconf_manager() as m:
                response = m.get(filter=filter_xml)
                logger.debug(f"Raw NETCONF response for track: {etree.tostring(response.data, encoding='unicode')}")
                data_dict = xmltodict.parse(etree.tostring(response.data))
                logger.debug(f"Parsed data_dict for track: {json.dumps(data_dict, indent=2)}")
                track_data = data_dict.get('rpc-reply', {}).get('data', {}).get('track', {}).get('track', [])
                if not track_data:
                    logger.warning("No track data found in NETCONF response.")
                    return {}
                if isinstance(track_data, dict):
                    track_data = [track_data]
                track_states = {}
                for track in track_data:
                    track_id = track.get('track-id')
                    state = track.get('state')
                    if track_id and state:
                        track_states[str(track_id)] = {'state': state}
                return track_states
        except Exception as e:
            logger.error(f"Failed to retrieve track states via NETCONF: {e}")
            return {}
