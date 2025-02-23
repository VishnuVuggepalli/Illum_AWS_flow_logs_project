import csv
import logging

from flow_log_parser import config
from flow_log_parser.exceptions import LookupFileError

logger = logging.getLogger(__name__)

def load_lookup_table(lookup_filename):
    """
    Loads the lookup CSV file and returns a dictionary mapping (dstport, protocol) to tag.
    
    :param lookup_filename: Path to the lookup CSV file.
    :return: Dictionary with keys as (int(dstport), protocol.lower()) and values as tag.
    :raises LookupFileError: If the file cannot be read or parsed.
    """
    lookup = {}
    try:
        with open(lookup_filename, "r", encoding="ascii") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    port = int(row["dstport"].strip())
                    # Force protocol to lower case for case-insensitive matching.
                    proto = row["protocol"].strip().lower()
                    tag = row["tag"].strip()
                    lookup[(port, proto)] = tag
                except Exception as e:
                    logger.warning("Skipping malformed row in lookup file: %s. Error: %s", row, e)
                    continue
    except Exception as e:
        raise LookupFileError(f"Error reading lookup file {lookup_filename}: {e}")
    
    logger.info("Loaded %d lookup entries", len(lookup))
    return lookup
