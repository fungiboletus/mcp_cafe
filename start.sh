#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment (.venv) not found in $SCRIPT_DIR"
    exit 1
fi

# Activate the Python virtual environment
source .venv/bin/activate

# Check if server.py exists
if [ ! -f "server.py" ]; then
    echo "Error: server.py not found in $SCRIPT_DIR"
    exit 1
fi

# Run the fastmcp server
fastmcp run server.py