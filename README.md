
# JeyPyats - Network Device Parsing Framework

[![Version](https://img.shields.io/badge/version-1.1.2-blue.svg)](https://github.com/your-repo/jeypyats)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive framework for parsing network device configurations and operational data using various protocols including NETCONF, CLI, and REST APIs.

## Features

- **Multi-Platform Support**: Parsers for Cisco IOS-XE, IOS-XR, and other network platforms
- **NETCONF Integration**: Full NETCONF support with ncclient for device communication
- **Comprehensive Testing**: 22 unit tests covering all parsers with pytest
- **Modern Packaging**: Proper Python package structure with console scripts
- **Extensible Architecture**: Easy to add new parsers and utilities
- **Failover Testing**: Automated failover scripts for testing network resilience

## Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Quick Install

```bash
# Clone the repository
git clone <repository-url>
cd pyats-jeyws01

# Install in development mode
pip install -e .
```

### Manual Installation

```bash
# Clone the repository
git clone <repository-url>
cd pyats-jeyws01

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Usage

### Running Tests

The package includes a comprehensive test suite that can be run with a single command:

```bash
jeypyats-test
```

This will run all 22 unit tests covering:
- IOS-XE routing parsers (BGP, OSPF, routing tables)
- IOS-XE L2VPN parsers (bridge domain information)
- IOS-XE IP SLA and track parsers
- IOS-XE cellular and syslog parsers
- XRD interface parsers (OpenConfig, XR, OC variants)

### Using the Parsers

```python
import jeypyats

# Connect to a NETCONF device
from jeypyats.utils import connect_netconf
connection = connect_netconf('192.168.1.1', 830, 'username', 'password')

# Parse interface status
from jeypyats.parsers.xrd.xrd_interface_parser_nc import get_interface_status
status = get_interface_status(connection)
print(status)

# Parse routing information
from jeypyats.parsers.iosxe import ParsersMixin
parser = ParsersMixin()
bgp_routes = parser.get_bgp_routes()
```

### Failover Testing

The framework includes automated failover testing scripts for network resilience:

```bash
# Run failover test for IOS-XE devices
python scripts/iosxe/Failover/failover.py --testbed testbed.yaml
```

This script tests automatic failover between FTTH and LTE connections using IP SLA, object tracking, and EEM applets.

## Project Structure

```
jeypyats/
├── __init__.py                 # Package initialization
├── parsers/                    # Network device parsers
│   ├── __init__.py
│   ├── iosxe/                  # IOS-XE specific parsers
│   │   ├── __init__.py
│   │   ├── iosxe_cellular_parsers_nc.py    # Cellular SIM config parsers
│   │   ├── iosxe_eem_parsers_nc.py         # EEM script parsers
│   │   ├── iosxe_interface_parsers_nc.py   # Interface status parsers
│   │   ├── iosxe_ip_sla_parsers_nc.py      # IP SLA state parsers
│   │   ├── iosxe_routing_parsers_nc.py     # Routing table parsers
│   │   ├── iosxe_syslog_parsers_nc.py      # Syslog parsers
│   │   ├── iosxe_track_parsers_nc.py       # Object tracking parsers
│   │   └── parsers.egg-info/
│   └── xrd/                    # IOS-XR specific parsers
│       ├── __init__.py
│       ├── xrd_interface_parser_nc.py
│       ├── xrd_interface_parser_nc_oc.py
│       └── xrd_interface_parser_nc_xr.py
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── netconf_connector.py    # NETCONF connection utilities
│   ├── rpc_msgs.py            # NETCONF RPC message templates
│   └── utils.py               # General utilities
└── test_suite/                # Test suite
    ├── __init__.py
    ├── scripts/
    │   └── run_all_tests.py   # Test runner script
    └── tests/                 # Unit tests (22 test files)
```

## Configuration

### Testbed Configuration

Create a testbed YAML file in the `testbed/` directory following pyATS conventions:

```yaml
devices:
  my_device:
    type: iosxe
    connections:
      netconf:
        class: ncclient
        ip: 192.168.1.1
        port: 830
        username: admin
        password: password
```

### Environment Variables

Set the following environment variables for device access:

```bash
export NETCONF_HOST=192.168.1.1
export NETCONF_PORT=830
export NETCONF_USERNAME=admin
export NETCONF_PASSWORD=password
```

## Development

### Adding New Parsers

1. Create a new parser file in the appropriate platform directory
2. Add the parser function with proper error handling
3. Create corresponding unit tests
4. Update imports in `__init__.py` files if needed

### Running Tests During Development

```bash
# Run all tests
jeypyats-test

# Run specific test file
python -m pytest jeypyats/test_suite/tests/test_iosxe_routing_parser.py -v

# Run with coverage
python -m pytest jeypyats/test_suite/tests/ --cov=jeypyats --cov-report=html
```

### Building Distribution

```bash
# Build source distribution and wheel
python -m build

# Upload to PyPI (requires API token)
twine upload dist/*
```

## Dependencies

### Core Dependencies
- `lxml>=4.9.0` - XML processing
- `xmltodict>=0.12.0` - XML to dictionary conversion
- `ncclient>=0.6.0` - NETCONF client
- `genie>=23.0` - Cisco test automation framework
- `pyats>=23.0` - Cisco pyATS framework

### Development Dependencies
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `yamllint>=1.30.0` - YAML linting

## Testing

The framework includes comprehensive unit tests with mocks for all external dependencies:

```bash
# Run complete test suite
jeypyats-test

# Expected output: 22 passed tests
============================= 22 passed, 2 warnings in 0.49s =============================
```

### Test Coverage

- **IOS-XE Parsers**: Routing tables, BGP/OSPF routes, L2VPN bridge domains
- **XRD Parsers**: Interface status for OpenConfig, XR, and OC variants
- **Error Handling**: Invalid responses, connection failures, malformed XML
- **Edge Cases**: Empty data, missing fields, network timeouts

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the package is installed with `pip install -e .`
2. **NETCONF Connection Failed**: Check device credentials and network connectivity
3. **XML Parsing Errors**: Verify device YANG models and response format
4. **Test Failures**: Run `jeypyats-test` to verify all components work

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your parser code here
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 1.1.2 (February 4, 2026)
- ✅ **Failover Script Updates**: Enhanced failover.py to use NETCONF parsers exclusively for all checks (routing, IP SLA, tracks, SIM config, syslog)
- ✅ **Modular Parser Architecture**: Separated parsers into dedicated files with mixin classes for device binding
- ✅ **Robust Error Handling**: Made SLA, track, and SIM checks optional if NETCONF data is not retrievable
- ✅ **Syslog Parsing Improvements**: Updated syslog parser to handle buffered messages as strings and parse into dicts
- ✅ **Cellular Parser Fix**: Corrected XML filter for SIM configuration retrieval

### Version 1.1.1 (January 28, 2026)
- ✅ **Failover Script Enhancements**: Added more methods to testscript failover.py
- ✅ **Testbed Loading Harmonization**: Harmonized testbed loading in scripts and added jobfiles

### Version 1.1.0 (January 27, 2026)
- ✅ **Complete Package Restructure**: Migrated to proper Python package with `jeypyats` namespace
- ✅ **Console Script**: Added `jeypyats-test` command for easy test execution
- ✅ **Modern Packaging**: Implemented `pyproject.toml` with comprehensive dependencies
- ✅ **Import Fixes**: Updated all relative imports for proper package structure
- ✅ **Test Suite**: 22 unit tests covering all parsers with pytest integration
- ✅ **Documentation**: Updated README with installation and usage instructions

### Version 1.0.0 (January 26, 2026)
- Initial release with basic NETCONF parsers
- Support for Cisco IOS-XE and IOS-XR platforms
- Basic utility functions and connection management

## Support

For questions or issues:
- Check the [pyATS documentation](https://developer.cisco.com/docs/pyats/)
- Review the test suite for usage examples
- Open an issue on the project repository

---

**JeyPyats** - Automating Network Device Testing with Python
