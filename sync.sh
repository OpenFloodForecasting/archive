#!/bin/bash

# Check for python3 or python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "Error: Python not found."
    exit 1
fi

# sync river data
$PYTHON_CMD data/river/sync.py
