# Examples

This folder contains example scripts demonstrating how to use scapy-socketlogger.

## ping_example.py

A simple example that creates a Scapy socket, sends an ICMP ping packet to 8.8.8.8, and logs the traffic to `ping.pcap`.

To run:

```bash
python ping_example.py
```

Note: On some systems, sending raw packets may require administrator privileges. The example focuses on demonstrating the logging functionality.