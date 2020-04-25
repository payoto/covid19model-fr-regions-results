#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
./get-run-stats.sh > ${DIR}/run-manifest.csv
./generate-commit-msg.sh > ${DIR}/run-manifest-short.csv