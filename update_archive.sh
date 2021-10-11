#!/bin/sh
source /home/janpf/bots/venv/bin/activate

echo "Downloading files"
python download_files.py
python download_files.py -c EUR

echo "creating jsons"
bash create_json.sh
bash create_json_EUR.sh

echo "generating bash"
python generate_bash.py

echo "creating plaintext"
bash create_plaintext.sh

echo "creating users"
bash create_users.sh

echo "generating html"
python generate_html.py

echo "generating filehashes"
python generate_filehashes.py
python generate_filehashes.py -c EUR
