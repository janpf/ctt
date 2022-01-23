#!/bin/bash
shopt -s expand_aliases

echo "Downloading files"
python3 download_files.py
python3 download_files.py -c EUR

echo "creating jsons"
bash create_json.sh
bash create_json_EUR.sh

echo "generating bash"
python3 generate_bash.py

echo "creating plaintext"
bash create_plaintext.sh

echo "creating users"
bash create_users.sh

echo "generating html"
python3 generate_html.py

echo "generating filehashes"
python3 generate_filehashes.py
python3 generate_filehashes.py -c EUR
