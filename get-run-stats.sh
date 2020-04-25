#!/bin/bash

# Script which generates a csv file with information about the runs
# in the folder
# Optionally taje a command line argument which is a pattern identifying specific
# runs.

echo "folder , last available data, number of countries , number of zones , countries , modelling zones , "
for foo in `find ./runs -maxdepth 1 -type d -name "*fullrun*${1}*"`
do
	echo -n "$foo , "
	forecastfile=`find $foo -name "*forecast*.csv"`
	activeregfile=`find $foo -name "*active_regions*.csv"`
	grep '"1"' $forecastfile | awk -F "," '{printf "%s , ", $2}'
	countries=`awk -F "," 'NR!=1 {printf "%s\n", $3}' ${activeregfile} | sort | uniq`
	regions=`awk -F "," 'NR!=1 {printf "%s\n", $2}' ${activeregfile} | sort | uniq`
	num_countries=`echo $countries | sed 's/" "/"\n"/g' | wc -l`
	num_regions=`echo $regions | sed 's/" "/"\n"/g' | wc -l`
	echo -n "${num_countries} , ${num_regions}, "
	echo $countries | sed 's/" "/"\n"/g' | awk '{printf "%s; ", $0}'
	echo -n ", "
	echo $regions | sed 's/" "/"\n"/g' | awk '{printf "%s; ", $0}'
	echo ", "
done | sort -k 1 | sort -k 3