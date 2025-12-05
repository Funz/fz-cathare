#!/bin/bash

# Cathare calculator script
# Compatible with fz framework
#
# This script launches CATHARE calculations.
# Replace the mock implementation with actual CATHARE calls.

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
# Replace this section with actual CATHARE command
# For example:
#   cathare < "$input" > output.txt 2>&1
#
# The CATHARE code typically produces a FORT07 file with results
# which will be automatically parsed by the Cathare.json output configuration

echo "Running CATHARE on $input..."

# Mock implementation - replace with actual CATHARE execution
# In a real scenario, you would call the CATHARE executable here
# cathare < "$input" > listing 2> err.txt

# For testing purposes, create a minimal FORT07 file
cat > FORT07 << 'EOF'
EVOLUTION ML
TIME            SECONDS    
 0.00000000E+000 0.81098631E+000 0.13109863E+001 0.18109863E+001 0.23109863E+001
           5
LIQMASS         KG        CANAL:001
 0.29076885E+002 0.28502382E+002 0.28231470E+002 0.27992447E+002 0.27772408E+002
EOF

echo "CATHARE calculation completed."

if [ -f "$PID_FILE" ]; then
    rm -f "$PID_FILE"
fi
