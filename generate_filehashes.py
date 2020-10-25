import hashlib
import json
import zipfile
from pathlib import Path


hashes = []
for zfile in sorted(Path("page/keys/").iterdir(), reverse=True):
    if ".gitkeep" in str(zfile):
        continue
    data = dict()
    hashes.append(data)

    data["date"] = zfile.stem
    zip_data = zipfile.ZipFile(zfile)
    infolist = zip_data.infolist()
    with zip_data.open([f for f in infolist if ".bin" in f.filename][0], "r") as bin_file:
        data["hash"] = hashlib.sha256(bin_file.read()).hexdigest()

    with open(Path("page/json/") / (zfile.stem + ".json")) as j_file:
        data["keyCount"] = json.load(j_file)["keyCount"]

with open("page/json/filehashes.json", "w") as f:
    json.dump(hashes, f, indent=True)
