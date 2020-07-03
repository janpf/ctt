#!/bin/sh
for f in page/keys_hourly/*
do
  echo parsing $f
  python ../diagnosis-keys/parse_keys_json.py -d $f > page/json_hourly/$(basename $f .zip).json
done
