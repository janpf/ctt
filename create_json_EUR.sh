#!/bin/sh
for f in page/keys_EUR/*
do
  if [ -f page/json_EUR/$(basename $f .zip).json ]; then
    continue
  fi
  echo parsing $f
  python ../diagnosis-keys/parse_keys_json.py -d $f > page/json_EUR/$(basename $f .zip).json
done
