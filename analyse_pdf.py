import datetime
import json
from typing import Dict, List

from pathlib import Path

print("how close are we to https://www.coronawarn.app/assets/documents/2020-09-23-cwa-daten-fakten.pdf")

with open("page/plots/data.json") as f:
    users = json.load(f)

known_ranges: List[Dict] = []

known_ranges.append({"start": "2020-08-31", "end": "2020-09-21", "known_count": 2350})  # 3 wochen
known_ranges.append({"start": "2020-06-14", "end": "2020-09-21", "known_count": 5032})  # overall
known_ranges.append({"start": "2020-08-22", "end": "2020-09-21", "known_count": 3200})  # last 30 days

known_ranges.append({"start": "2020-06-14", "end": "2020-10-01", "known_count": 7120})  # overall
known_ranges.append({"start": "2020-09-01", "end": "2020-10-01", "known_count": 4323})  # last month
known_ranges.append({"start": "2020-09-03", "end": "2020-10-01", "known_count": 4302})  # last 4 weeks
known_ranges.append({"start": "2020-09-24", "end": "2020-10-01", "known_count": 1435})  # last week

for k_range in known_ranges:
    k_range["my_count"] = 0
    k_range["daily_count"] = 0

for day in users:
    for k_range in known_ranges:
        if datetime.datetime.fromisoformat(k_range["start"]) <= datetime.datetime.fromisoformat(day["date"]) <= datetime.datetime.fromisoformat(k_range["end"]):
            k_range["my_count"] += day["users_published"]

for daily_file in Path("page/users").iterdir():
    if daily_file.name == ".gitkeep":
        continue
    with open(daily_file) as f:
        content = f.readlines()
    for line in content:
        if "user(s) found" in line:
            count = int(line.split(" ")[0])
        if "Invalid Transmission Risk Profile" in line:
            inv = int(line.split(" ")[0])
            count -= inv
    for k_range in known_ranges:
        if datetime.datetime.fromisoformat(k_range["start"]) <= datetime.datetime.fromisoformat(daily_file.stem) <= datetime.datetime.fromisoformat(k_range["end"]):
            k_range["daily_count"] += count
print(json.dumps(known_ranges, indent=True))


""" my_count == using hourly files, skipping 3 oclock packages
[
 {
  "start": "2020-08-31",
  "end": "2020-09-21",
  "known_count": 2350,
  "my_count": 2591,
  "daily_count": 2589
 },
 {
  "start": "2020-06-14",
  "end": "2020-09-21",
  "known_count": 5032,
  "my_count": 4967,
  "daily_count": 4978
 },
 {
  "start": "2020-08-22",
  "end": "2020-09-21",
  "known_count": 3200,
  "my_count": 3252,
  "daily_count": 3250
 },
 {
  "start": "2020-06-14",
  "end": "2020-10-01",
  "known_count": 7120,
  "my_count": 6459,
  "daily_count": 6946
 },
 {
  "start": "2020-09-01",
  "end": "2020-10-01",
  "known_count": 4323,
  "my_count": 4018,
  "daily_count": 4492
 },
 {
  "start": "2020-09-03",
  "end": "2020-10-01",
  "known_count": 4302,
  "my_count": 3811,
  "daily_count": 4285
 },
 {
  "start": "2020-09-24",
  "end": "2020-10-01",
  "known_count": 1435,
  "my_count": 1066,
  "daily_count": 1542
 }
]
"""
""" my_count == using hourly files, not skipping 3 oclock packages
[
 {
  "start": "2020-08-31",
  "end": "2020-09-21",
  "known_count": 2350,
  "my_count": 2591,
  "daily_count": 2589
 },
 {
  "start": "2020-06-14",
  "end": "2020-09-21",
  "known_count": 5032,
  "my_count": 4967,
  "daily_count": 4978
 },
 {
  "start": "2020-08-22",
  "end": "2020-09-21",
  "known_count": 3200,
  "my_count": 3252,
  "daily_count": 3250
 },
 {
  "start": "2020-06-14",
  "end": "2020-10-01",
  "known_count": 7120,
  "my_count": 6936,
  "daily_count": 6946
 },
 {
  "start": "2020-09-01",
  "end": "2020-10-01",
  "known_count": 4323,
  "my_count": 4495,
  "daily_count": 4492
 },
 {
  "start": "2020-09-03",
  "end": "2020-10-01",
  "known_count": 4302,
  "my_count": 4288,
  "daily_count": 4285
 },
 {
  "start": "2020-09-24",
  "end": "2020-10-01",
  "known_count": 1435,
  "my_count": 1543,
  "daily_count": 1542
 }
]

"""
