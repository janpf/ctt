#!/bin/sh
for f in page/keys_EUR/*
do
  echo parsing $f
  python ../diagnosis-keys/parse_keys_json.py -d $f > page/json_EUR/$(basename $f .zip).json
done
