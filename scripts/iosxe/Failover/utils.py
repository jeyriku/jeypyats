import logging
from jeypyats.parsers.iosxe.iosxe_cellular_parsers_nc import IOSXECellularParsersMixin
from jeypyats.parsers.iosxe.iosxe_syslog_parsers_nc import IOSXESyslogParsersMixin
from jeypyats.parsers.iosxe.iosxe_ip_sla_parsers_nc import IOSXEIPSLAParsersMixin
from jeypyats.parsers.iosxe.iosxe_track_parsers_nc import IOSXETrackParsersMixin
from jeypyats.parsers.iosxe.iosxe_routing_parsers_nc import IOSXERoutingParsersMixin
from jeypyats.parsers.iosxe.iosxe_interface_parsers_nc import IOSXEInterfacesParsersMixin

logger = logging.getLogger(__name__)

def apply_netconf_parsers(device):
    """
    Apply NETCONF parser mixins to the device.
    """
    device.__class__ = type('IOSXENETCONFDevice', (device.__class__, IOSXECellularParsersMixin, IOSXESyslogParsersMixin, IOSXEIPSLAParsersMixin, IOSXETrackParsersMixin, IOSXERoutingParsersMixin, IOSXEInterfacesParsersMixin), {})
    logger.info("Applied NETCONF parser mixins to device.")
