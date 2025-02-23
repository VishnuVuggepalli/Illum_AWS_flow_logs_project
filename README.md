# Illum_AWS_flow_logs_project

## Overview

This program processes AWS VPC Flow Logs in **version 2 format** and maps each row to a tag based on a lookup table. The lookup table is a CSV file containing mappings of `(dstport, protocol) → tag`, which are used to classify flow log records. The program then generates two output files:

1. **Tag Counts:** Number of occurrences per tag.
2. **Port/Protocol Combination Counts:** Number of times each `(port, protocol)` combination appears.

## **Assumptions & Constraints**
### ✅ **What the Program Supports**
- **Log Format:** The program **only supports the default AWS VPC Flow Log format (version 2).** Custom formats are **not** supported.
- **File Encoding:** Both the lookup table (`lookup.csv`) and flow logs (`flow_logs.txt`) are **plain ASCII**.
- **Flow Log Size:** The flow log file can be **up to 10MB**.
- **Lookup Entries:** The lookup CSV can contain **up to 10,000 mappings**.

### ❌ **What is NOT Supported**
- Custom log formats or different field orders.
- Flow log versions **other than version 2**.
- Binary or non-ASCII-encoded log files.
- Streaming log input (only **file-based processing** is supported).


## Prerequisites & How to Run:

### **Clone Repository**
```bash
git clone https://github.com/VishnuVuggepalli/Illum_AWS_flow_logs_project.git
cd Illum_AWS_flow_logs_project
```

### Generate the mock files 

```bash
python generate_data.py --num_mappings 10000 --num_logs 10000
```

### Run the application

```bash
python main.py <mapping.csv> <logs.log> output_tags.csv output_port_proto.csv
Example : python main.py lookup.csv flow_logs.log output_tags.csv output_port_proto.csv
```