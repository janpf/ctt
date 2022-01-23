#!/bin/bash
for f in page/keys/*
do
  if [ -f page/json/$(basename $f .zip).json ]; then
    continue
  fi
  echo parsing $f
  python3 ../diagnosis-keys/parse_keys_json.py -d $f > page/json/$(basename $f .zip).json
done
