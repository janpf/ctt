import hashlib
import json
import zipfile
from pathlib import Path


hashes = dict()
for zfile in sorted(Path("page/keys/").iterdir(), reverse=True):
    if ".gitkeep" in str(zfile):
        continue
    zip_data = zipfile.ZipFile(zfile)
    infolist = zip_data.infolist()
    with zip_data.open([f for f in infolist if ".bin" in f.filename][0], "r") as bin_file:
        hashes[hashlib.sha256(bin_file.read()).hexdigest()] = zfile.stem

with open("page/json/filehashes.json", "w") as f:
    json.dump(hashes, f, indent=True)
