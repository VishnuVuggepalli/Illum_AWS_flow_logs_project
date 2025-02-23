"""
Configuration module for the flow_log_parser package.
"""

# Mapping of protocol numbers to names.
PROTOCOL_MAP = {
    '1': 'icmp',
    '6': 'tcp',
    '17': 'udp'
}

# Field indices for AWS flow log version 2 (0-based indexing)
FLOW_LOG_FIELDS = {
    'destport': 6,   # Destination port index
    'protocol': 7    # Protocol number index
}

# Default tag if no lookup match is found.
DEFAULT_TAG = "Untagged"
