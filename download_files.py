import argparse
from pathlib import Path

import requests

parser = argparse.ArgumentParser(description="Exposure Notification Diagnosis Key Parser.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--country", type=str, default="DE", help="key server country")
args = parser.parse_args()

# https://svc90.main.px.t-online.de/version/v1/diagnosis-keys/country/DE/date
protocol = "https://"
host = "svc90.main.px.t-online.de"
version = "v1"
if args.country == "DE":
    out_dir = Path("page") / "keys"
else:
    out_dir = Path("page") / f"keys_{args.country}"

dates_url = f"{protocol}{host}/version/{version}/diagnosis-keys/country/{args.country}/date"
available_dates = set(requests.get(dates_url).json())
print(f"available dates: {available_dates}")
downloaded_dates = {f.stem for f in out_dir.iterdir()}

for date in available_dates.difference(downloaded_dates):
    print(f"downloading file for {date}")
    file_url = f"{dates_url}/{date}"
    r = requests.get(file_url)
    with open(out_dir / f"{date}.zip", "wb") as f:
        f.write(r.content)
