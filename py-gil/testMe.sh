#!/bin/bash

# check command line parameter
if [ "$1" == "" ]; then
    echo "$0 <python script to test>"
    exit
else
    SCRIPT_TO_TEST=$1
fi

if [ ! -e ${SCRIPT_TO_TEST} ]; then
    echo "Cannot find Python script [${SCRIPT_TO_TEST}] !"
    exit 1
fi

# do a warm up
echo "Warming up..."
python ${SCRIPT_TO_TEST} >/dev/null

# run the test 20 times
echo "Running tests"
COUNT=1
while [ $COUNT -le 20 ]
do
    echo "---- RUN #${COUNT} ----"
    python ${SCRIPT_TO_TEST}
    COUNT=$((COUNT + 1))
done
