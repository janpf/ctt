#!/bin/sh
for f in page/keys/*
do
  echo parsing $f
  python ../diagnosis-keys/parse_keys.py -u -d $f > page/plaintext/$(basename $f .zip).txt
done
