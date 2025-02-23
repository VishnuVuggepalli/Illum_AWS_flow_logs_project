"""
Custom exceptions for the flow_log_parser package.
"""

class LookupFileError(Exception):
    """Raised when there is an error loading or parsing the lookup CSV file."""
    pass

class FlowLogFileError(Exception):
    """Raised when there is an error processing the flow log file."""
    pass
