import logging
from iosxe_cellular_parsers_nc import IOSXECellularParsersNC
from iosxe_syslog_parsers_nc import IOSXESyslogParsersNC
from iosxe_ip_sla_parsers_nc import IOSXEIPSLAParsersNC
from iosxe_track_parsers_nc import IOSXETrackParsersNC
from iosxe_routing_parsers_nc import IOSXERoutingParsersNC
from iosxe_interface_parsers_nc import IOSXEInterfaceParsersNC

logger = logging.getLogger(__name__)

def apply_netconf_parsers(device):
    """
    Apply NETCONF parser mixins to the device.
    """
    device.__class__ = type('IOSXENETCONFDevice', (device.__class__, IOSXECellularParsersNC, IOSXESyslogParsersNC, IOSXEIPSLAParsersNC, IOSXETrackParsersNC, IOSXERoutingParsersNC, IOSXEInterfaceParsersNC), {})
    logger.info("Applied NETCONF parser mixins to device.")
