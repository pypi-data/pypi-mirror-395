# Scapy Socket Logger

[![Build](https://github.com/antoniovazquezblanco/scapy-socketlogger/actions/workflows/build.yml/badge.svg)](https://github.com/antoniovazquezblanco/scapy-socketlogger/actions/workflows/build.yml)
[![PyPI](https://img.shields.io/pypi/v/scapy-socketlogger)](https://pypi.org/project/scapy-socketlogger/)
[![Snyk](https://snyk.io/advisor/python/scapy-socketlogger/badge.svg)](https://snyk.io/advisor/python/scapy-socketlogger)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.md)

Log all traffic going through an Scapy socket to a PCAP file.

## Installation

Just use pip :)

```
pip install scapy-socketlogger
```

## Usage

Practical examples can be found in the [Examples](examples/) folder.

For a plain quick usage reference, you may look into the following snippet:

```python
from scapy.all import SuperSocket, PcapWriter
from scapy_socketlogger import SocketLogger

# Create your socket
sock = SuperSocket(...)

# Create a PCAP writer
pcap_writer = PcapWriter("traffic.pcap")

# Wrap the socket with the logger
logger = SocketLogger(sock, pcap_writer)

# Use the socket normally - all traffic will be logged
# ...

# Close the logger when done
logger.close()
```

Or use as a context manager:

```python
with SocketLogger(sock, pcap_writer) as logger:
    # Use sock here
    pass
# Automatically closes and restores socket methods
```
