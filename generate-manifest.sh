#!/bin/bash

./get-run-stats.sh > run-manifest.csv
./generate-commit-msg.sh > run-manifest-short.csv