#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# 1. Move into the lab1 directory so NS2 outputs files there
cd "$SCRIPT_DIR" || exit

TCL_SCRIPT="lab1.tcl"
PYTHON_SCRIPT="visualize_nam.py"
NAM_OUTPUT="out.nam"

# 2. Run NS2
if [ -f "$TCL_SCRIPT" ]; then
    echo "--- Running NS2 ---"
    ns "$TCL_SCRIPT"
    echo "NS2 run complete."
else
    echo "Error: Cannot find $TCL_SCRIPT in $SCRIPT_DIR"
    exit 1
fi

# 3. Run Python Visualizer
if [ -f "$NAM_OUTPUT" ]; then
    echo "--- Generating Diagram ---"
    python3 "$PYTHON_SCRIPT" "$NAM_OUTPUT"
else
    echo "Error: $NAM_OUTPUT was not generated. Check TCL script for errors."
    exit 1
fi