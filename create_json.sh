#!/bin/sh
for f in page/keys/*
do
  echo parsing $f
  python ./parse_keys_json.py -u -d $f | tr -d '\n' | sed -r 's/,\{\}//g' | python -m json.tool > page/json/$(basename $f .zip).json
  #python ./parse_keys_json.py -u -d $f > json/$(basename $f .zip).json
done
