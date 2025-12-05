#!/bin/bash

# Cathare calculator script
# Compatible with fz framework
#
# This script launches CATHARE calculations.

# if directory as input, cd into it
if [ -d "$1" ]; then
  cd "$1"
  # Find the first input file (not .out or .msg)
  input=$(ls | grep -v '\.out$' | grep -v '\.msg$' | grep -v '\.sh$' | head -n 1)
  if [ -z "$input" ]; then
    echo "No input file found in directory. Exiting."
    exit 1
  fi
  shift
# if $1 is a file, use it
elif [ -f "$1" ]; then
  input="$1"
  shift
else
  echo "Usage: $0 <input_file or input_directory>"
  exit 2
fi

PID_FILE=$PWD/PID
echo $$ >> $PID_FILE

# CATHARE execution
# The CATHARE code produces a FORT07 file with results
# which will be automatically parsed by the Cathare.json output configuration

echo "Running CATHARE on $input..."

# Execute CATHARE with the input file
# Adjust the command based on your CATHARE installation
cathare < "$input" > listing 2> err.txt

echo "CATHARE calculation completed."

if [ -f "$PID_FILE" ]; then
    rm -f "$PID_FILE"
fi
