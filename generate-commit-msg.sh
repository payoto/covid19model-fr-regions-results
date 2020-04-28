#!/bin/bash

# Generates a human readable version of the manifest
# The change of this file must be in the commit message

./get-run-stats.sh $1 | awk -F "," '{printf "%s , %s , %s , %s , %s \n", $1, $2, $3, $4, $5}'