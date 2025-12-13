#!/bin/bash

# Go to the directory where this script resides
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Execute the extract scripts
python3 extract_jira.py >> "$SCRIPT_DIR/extract_jira.log" 2>&1
python3 extract_gitlab.py >> "$SCRIPT_DIR/extract_gitlab.log" 2>&1
python3 extract_jenkins.py >> "$SCRIPT_DIR/extract_jenkins.log" 2>&1

python3 sftp_upload.py >> "$SCRIPT_DIR/sftp_upload.log" 2>&1
