#!/bin/sh
for f in page/keys/*
do
  echo parsing $f
  python ../diagnosis-keys/parse_keys_json.py -d $f > page/json/$(basename $f .zip).json &
done
wait
