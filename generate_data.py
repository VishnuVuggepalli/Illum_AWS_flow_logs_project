#!/usr/bin/env python3
import csv
import random
import argparse
import time

# List of well-known ports
COMMON_PORTS = [22, 25, 53, 80, 110, 443, 993, 143, 3389, 8080]

# List of tags to distribute evenly
TAGS = ["sv_P1", "sv_P2", "email", "web", "db", "app", "vpn", "backup"]

# Protocol mapping (ensuring even distribution)
PROTOCOLS = ["tcp", "udp", "icmp"]
PROTOCOL_MAP = {"tcp": 6, "udp": 17, "icmp": 1}

def random_eni_id():
    """Generate a random ENI ID of the form 'eni-' followed by 8 hexadecimal digits."""
    return "eni-" + ''.join(random.choices('0123456789abcdef', k=8))

def random_ip(private=False):
    """Generate a random IPv4 address.
    
    If `private` is True, generate an address in the private 10.x.x.x range;
    otherwise, generate a public-like IP.
    """
    if private:
        return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    else:
        return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_lookup_file(lookup_filename, num_mappings):
    """
    Generate a lookup CSV file with header "dstport,protocol,tag".
    Ensures even distribution of ports, protocols, and tags.
    """
    mappings = {}
    tag_cycle = iter(TAGS * (num_mappings // len(TAGS) + 1))  # Cycle through TAGS evenly
    
    for _ in range(num_mappings):
        dstport = random.choice(COMMON_PORTS + [random.randint(1024, 65535)])  # Mix common & random ports
        protocol = random.choice(PROTOCOLS)  # Evenly distribute protocols
        tag = next(tag_cycle)  # Ensure even distribution of tags
        
        key = (dstport, protocol.lower())  # Normalize keys for lookup
        if key not in mappings:
            mappings[key] = tag

    with open(lookup_filename, "w", newline='', encoding="ascii") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["dstport", "protocol", "tag"])
        for (dstport, protocol), tag in mappings.items():
            writer.writerow([dstport, protocol, tag])

    print(f"Lookup file '{lookup_filename}' generated with {len(mappings)} mappings.")
    return mappings

def generate_logs_file(log_filename, num_logs, lookup_mappings):
    """
    Generate a diverse flow logs file with evenly distributed records.
    
    - 70% of logs will match lookup mappings.
    - 30% will be random (non-matching) entries.
    """
    account_id = "123456789012"
    version = "2"
    
    lookup_keys = list(lookup_mappings.keys())  # Precompute lookup keys

    with open(log_filename, "w", encoding="ascii") as f:
        for _ in range(num_logs):
            if random.random() < 0.7 and lookup_keys:
                # Matching log: Choose a port/protocol from lookup mappings.
                dstport, protocol = random.choice(lookup_keys)
                protocol_str = protocol
            else:
                # Non-matching log: Generate a random dstport/protocol not in lookup.
                while True:
                    dstport = random.randint(1, 65535)
                    protocol = random.choice(PROTOCOLS)
                    if (dstport, protocol) not in lookup_mappings:
                        protocol_str = protocol
                        break
            
            protocol_num = PROTOCOL_MAP.get(protocol_str.lower(), 0)  # Convert protocol to number

            eni = random_eni_id()
            srcaddr = random_ip(private=True)
            dstaddr = random_ip(private=False)
            srcport = random.randint(1024, 65535)
            packets = random.randint(1, 100)
            bytes_val = random.randint(500, 10000)
            start_time = int(time.time()) - random.randint(0, 86400)
            end_time = start_time + random.randint(1, 60)
            action = random.choice(["ACCEPT", "REJECT"])
            log_status = "OK"

            log_line = f"{version} {account_id} {eni} {srcaddr} {dstaddr} {srcport} {dstport} {protocol_num} {packets} {bytes_val} {start_time} {end_time} {action} {log_status}\n"
            f.write(log_line)

    print(f"Log file '{log_filename}' generated with {num_logs} entries.")

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic lookup and flow logs files.")
    parser.add_argument("--lookup", type=str, default="lookup.csv", help="Output lookup CSV file name.")
    parser.add_argument("--logs", type=str, default="flow_logs.log", help="Output flow logs file name.")
    parser.add_argument("--num_mappings", type=int, default=500, help="Number of lookup mappings to generate (max 10000).")
    parser.add_argument("--num_logs", type=int, default=1000, help="Number of log entries to generate.")
    args = parser.parse_args()
    
    num_mappings = min(args.num_mappings, 10000)

    lookup_mappings = generate_lookup_file(args.lookup, num_mappings)
    generate_logs_file(args.logs, args.num_logs, lookup_mappings)

if __name__ == "__main__":
    main()
