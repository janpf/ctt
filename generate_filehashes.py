import argparse
import hashlib
import json
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser(description="Exposure Notification Diagnosis Key Parser.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--country", type=str, default="DE", help="key server country")
args = parser.parse_args()

if args.country == "DE":
    key_dir = Path("page") / "keys"
    json_dir = Path("page") / "json"
else:
    key_dir = Path("page") / f"keys_{args.country}"
    json_dir = Path("page") / f"json_{args.country}"

out_file = json_dir / "filehashes.json"

hashes = []
for zfile in sorted(key_dir.iterdir(), reverse=True):
    if ".gitkeep" in str(zfile):
        continue
    data = dict()
    hashes.append(data)

    data["date"] = zfile.stem
    zip_data = zipfile.ZipFile(zfile)
    infolist = zip_data.infolist()
    with zip_data.open([f for f in infolist if ".bin" in f.filename][0], "r") as bin_file:
        data["hash"] = hashlib.sha256(bin_file.read()).hexdigest()

    with open(json_dir / (zfile.stem + ".json")) as j_file:
        data["keyCount"] = json.load(j_file)["keyCount"]

with open(out_file, "w") as f:
    json.dump(hashes, f, indent=True)
