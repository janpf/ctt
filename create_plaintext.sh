#!/bin/sh
for f in keys/*
do
  echo parsing $f
  python ../diagnosis-keys/parse_keys.py -d $f > plaintext/$(basename $f .zip).txt
done
