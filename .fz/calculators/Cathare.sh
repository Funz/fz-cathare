#!/bin/bash

# Cathare calculator script
# Compatible with fz framework
# Based on the original CATHARE plugin script

# Declaration of CATHARE installation directory
export VERS="${CATHARE_HOME:-/opt/CATHARE2_V25_3_MOD931}"
echo "CATHARE VERSION: $VERS"

export v25_1=$VERS
export v25_2=$VERS
export v25_3=$VERS

# if directory as input, cd into it
if [ -d "$1" ]; then
  cd "$1"
  # Find the first input file (not .out or .msg)
  input=$(ls | grep -v '\.out$' | grep -v '\.msg$' | grep -v '\.sh$' | grep -v 'g$' | head -n 1)
  if [ -z "$input" ]; then
    echo "No input file found in directory. Exiting."
    exit 1
  fi
  shift
# if $1 is a file, use it
elif [ -f "$1" ]; then
  input=$1
  shift
else
  echo "Usage: $0 <input_file or input_directory>"
  exit 2
fi

cwd=`pwd`

PID_FILE=$cwd/PID
if [ "$pid""zz" == "zz" ] ; then
  pid=$PID_FILE
fi

# process number in "PID" file
echo $$ >> $pid

echo "Initialisation..."
# convert to unix (EoL issue)
dos2unix * 2>/dev/null || true

echo "Version check..."
# Launch the reader with reader mask management
if [ -d "reader" ] ; then
  sh $VERS/unix-procedur/vers.unix reader &
    PID=$!
    echo $PID >> $pid
    wait $PID
else
  sh $VERS/unix-procedur/vers.unix &
    PID=$!
    echo $PID >> $pid
    wait $PID
fi

# Process permanent initial calculation if needed
LS_NO1=`ls -I $input -I PILOT.f -I reader.listing -F 2>/dev/null | grep -v "@" | cut -d':' -f1 | uniq | tr '\n' ' '`
PERMINIT=`grep PERMINIT $LS_NO1 2>/dev/null | cut -d':' -f1 | uniq`
PERMINIT=`echo $PERMINIT | tr -d '\n'`

if [ ! "$PERMINIT""zz" == "zz" ] ; then
  echo "Permanent initial calculation: $PERMINIT"
  sh $VERS/unix-procedur/read.unix $PERMINIT > perminit.listing &
    PID=$!
    echo $PID >> $pid
    wait $PID
  sh $VERS/unix-procedur/cathar.unix > perm.listing &
    PID=$!
    echo $PID >> $pid
    wait $PID
  PERMINIT_POSTPRO=`grep CHRONO *$PERMINIT* 2>/dev/null | cut -d: -f1 | uniq`
  if [ ! "$PERMINIT_POSTPRO""zz" == "zz" ] ; then
    echo "Permanent initial postpro"
    sh $VERS/unix-procedur/postpro.unix $PERMINIT_POSTPRO > perminit_postpro.listing &
      PID=$!
      echo $PID >> $pid
      wait $PID
  fi
else
  echo "No permanent initial calculation"
fi  

echo "Launching reader..."
# Launch the reader with reader mask management
if [ -d "reader" ] ; then
  sh $VERS/unix-procedur/read.unix $input mask > reader.listing &
    PID=$!
    echo $PID >> $pid
    wait $PID
else
  sh $VERS/unix-procedur/read.unix $input > reader.listing &
    PID=$!
    echo $PID >> $pid
    wait $PID
fi

# Check for reader errors
if [ `grep ERROR reader.listing 2>/dev/null | wc -w` != 0 ] ; then
  echo "Reader error!"
  cd $cwd
  exit 1
else
  echo "  No reader error"
fi

echo "Launching CATHARE..."
# Launch CATHARE
sh $VERS/unix-procedur/cathar.unix > listing &
  PID=$!
  echo $PID >> $pid
  wait $PID

# Check for calculation errors
if [ `grep " NORMAL END OF CATHAR RUN" listing 2>/dev/null | wc -l` != 1 ] ; then
# calculation failed
  echo "Calculation error!"
  cd $cwd
  exit 1
else
  echo "  No calculation error"
fi

echo "Launching post-processing..."
# Launch post-processing
POSTPRO=`grep CHRONO *$input* 2>/dev/null | cut -d: -f1 | uniq`
if [ ! "$POSTPRO""zz" == "zz" ] ; then
  echo "Launching post-processing..."
  sh $VERS/unix-procedur/postpro.unix $POSTPRO > postpro.listing &
    PID=$!
    echo $PID >> $pid
    wait $PID
else
  echo "(!!!) No post-processing..."
fi

# Check for post-processing errors
if [ `grep "ERROR" postpro.listing 2>/dev/null | wc -l` != 0 ] ; then
# postpro failed
  echo "Post-processing error!"
  cd $cwd
  exit 2
else
  echo "  No post-processing error"
fi

# Cleanup
rm -f *.f
rm -f *.H
rm -f *.exe
rm -f *.unix
rm -f DICO
rm -f FORT21
rm -f *.INIT
rm -f *.STOP
rm -f *.SUIVI

# Suppress "PID" file
if [ -f $pid ]; then
  rm -f $pid
fi

echo "CATHARE calculation completed successfully."

