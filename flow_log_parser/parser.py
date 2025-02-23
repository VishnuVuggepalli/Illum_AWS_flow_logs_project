import logging
from collections import defaultdict
from flow_log_parser import config

logger = logging.getLogger(__name__)

class FlowLogParser:
    """
    FlowLogParser reads a lookup CSV file and then processes a flow log file
    to generate counts of tags and port/protocol combinations.

    The lookup CSV is assumed to have a header row and three columns:
      dstport,protocol,tag
    Matching is performed in a case-insensitive manner.
    """

    def __init__(self, lookup_filename):
        """
        Initialize the parser by reading the lookup CSV file.
        """
        self.lookup_dict = {}
        try:
            with open(lookup_filename, 'r', encoding='ascii') as f:
                headers = next(f).strip().split(',')  # Assume header is present
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(',')
                    if len(parts) < 3:
                        continue
                    dstport = parts[0].strip().lower()
                    protocol = parts[1].strip().lower()
                    tag = parts[2].strip()
                    key = (dstport, protocol)
                    self.lookup_dict[key] = tag
            logger.info("Loaded %d lookup entries.", len(self.lookup_dict))
        except Exception as e:
            logger.exception("Error reading lookup file: %s", e)
            raise

    def process_flow_log_file(self, flow_log_filename):
        """
        Process the flow log file and return two dictionaries:
          - tag_counts: { tag: count }
          - port_protocol_counts: { (port, protocol): count }

        The flow log file is assumed to be an ASCII file with at least 14 whitespace-separated fields.
        Uses the destination port (from config.FLOW_LOG_FIELDS['destport']) and the protocol
        (from config.FLOW_LOG_FIELDS['protocol']) for matching.
        """
        tag_counts = defaultdict(int)
        port_protocol_counts = defaultdict(int)

        try:
            with open(flow_log_filename, 'r', encoding='ascii') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    fields = line.split()
                    if len(fields) < 14:
                        continue
                    try:
                        dstport = fields[config.FLOW_LOG_FIELDS['destport']].lower()
                        protocol_num = fields[config.FLOW_LOG_FIELDS['protocol']]
                    except IndexError:
                        continue

                    protocol_str = config.PROTOCOL_MAP.get(protocol_num, protocol_num).lower()
                    port_protocol_key = (dstport, protocol_str)
                    port_protocol_counts[port_protocol_key] += 1

                    lookup_key = (dstport, protocol_str)
                    tag = self.lookup_dict.get(lookup_key, config.DEFAULT_TAG)
                    tag_counts[tag] += 1

            logger.info("Finished processing flow log file: %s", flow_log_filename)
        except Exception as e:
            logger.exception("Error processing flow log file: %s", e)
            raise

        return tag_counts, port_protocol_counts
