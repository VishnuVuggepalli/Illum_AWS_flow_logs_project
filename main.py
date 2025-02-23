#!/usr/bin/env python3
import argparse
import logging
import sys
from flow_log_parser.parser import FlowLogParser
from flow_log_parser.output import write_output_file

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Parse AWS VPC flow logs and tag records based on a lookup CSV file."
    )
    parser.add_argument("lookup_csv_file", help="Path to the lookup CSV file (columns: dstport,protocol,tag)")
    parser.add_argument("flow_log_file", help="Path to the flow log file")
    parser.add_argument("output_tags_file", help="Path to the output file for tag counts")
    parser.add_argument("output_port_proto_file", help="Path to the output file for port/protocol counts")
    return parser.parse_args()

def main():
    """
    Main entry point for processing flow logs.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    args = parse_arguments()

    try:
        parser_instance = FlowLogParser(args.lookup_csv_file)
        tag_counts, port_proto_counts = parser_instance.process_flow_log_file(args.flow_log_file)
        write_output_file(args.output_tags_file, args.output_port_proto_file, tag_counts, port_proto_counts)
        logging.info("Processing complete. Results written to output files.")
    except Exception as e:
        logging.exception("Error processing flow logs: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
