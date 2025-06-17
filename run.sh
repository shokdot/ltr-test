#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOGFILE="$SCRIPT_DIR/research/ltr390.log"
ERRORFILE="$SCRIPT_DIR/research/ltr390.err"

source "$SCRIPT_DIR/venv/bin/activate"
python3 "$SCRIPT_DIR/ltr390.py" >> "$LOGFILE" 2>> "$ERRORFILE"