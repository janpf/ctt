#!/bin/sh
for f in page/keys_hourly/*
do
  echo parsing $f
  python ./create_users.py -d $f > page/users_hourly/$(basename $f .zip).txt
done
