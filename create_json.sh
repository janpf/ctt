#!/bin/sh
for f in keys/*
do
  echo parsing $f
  python ../diagnosis-keys/parse_keys_json.py -u -d $f | tr -d '\n' | sed -r 's/,\{\}//g' | python -m json.tool > json/$(basename $f .zip).json
done
