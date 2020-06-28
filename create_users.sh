#!/bin/sh
for f in page/keys/*
do
  echo parsing $f
  python ./create_users.py -d $f > page/users/$(basename $f .zip).txt
done
