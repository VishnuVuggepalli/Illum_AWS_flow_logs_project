import logging

logger = logging.getLogger(__name__)

def write_output_file(output_tags_filename, output_port_proto_filename, tag_counts, port_protocol_counts):
    """
    Writes the computed counts to output files.

    :param output_tags_filename: File for tag counts.
    :param output_port_proto_filename: File for port/protocol counts.
    :param tag_counts: Dictionary {tag: count}.
    :param port_protocol_counts: Dictionary {(port, protocol): count}.
    """
    try:
        # Sorting tag counts (descending by count, then alphabetically)
        sorted_tags = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))
        untagged = None
        for i, (tag, _) in enumerate(sorted_tags):
            if tag == "Untagged":
                untagged = sorted_tags.pop(i)
                break
        if untagged:
            sorted_tags.append(untagged)

        with open(output_tags_filename, 'w', encoding='ascii') as f:
            f.write("Tag,Count\n")
            for tag, count in sorted_tags:
                f.write(f"{tag},{count}\n")

        # Sorting port/protocol counts
        sorted_port_proto = sorted(
            port_protocol_counts.items(),
            key=lambda x: (int(x[0][0]), x[0][1])
        )

        with open(output_port_proto_filename, 'w', encoding='ascii') as f:
            f.write("Port,Protocol,Count\n")
            for (port, proto), count in sorted_port_proto:
                f.write(f"{port},{proto},{count}\n")

        logger.info("Successfully wrote output files.")

    except Exception as e:
        logger.exception("Failed to write output files: %s", e)
        raise
