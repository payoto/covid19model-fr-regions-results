#!/bin/bash

url_geo_france="https://data.opendatasoft.com/explore/dataset/code-postal-code-insee-2015@public/download/?format=shp&timezone=Europe/Berlin"
url_geo_europe="https://ec.europa.eu/eurostat/cache/GISCO/distribution/v2/countries/download/ref-countries-2016-20m.shp.zip"


wget -O code-postal-code-insee-2015.zip ${url_geo_france}
wget -O ref-countries-2016-20m.shp.zip ${url_geo_europe}

unzip code-postal-code-insee-2015.zip -d code-postal-code-insee-2015
unzip ref-countries-2016-20m.shp.zip -d ref-countries-2016-20m

cd ref-countries-2016-20m

for foo in `ls *.zip`
do
	unzip $foo
done

cd ..
