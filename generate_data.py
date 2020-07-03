import datetime
import json
from collections import defaultdict
from pathlib import Path

keys = []

data = dict()
data["overall"] = dict()
data["overall"]["publishDate"] = dict()
data["overall"]["validDate"] = defaultdict(int)

data["byRisk"] = dict()
data["byRisk"]["publishDate"] = dict()
data["byRisk"]["validDate"] = dict()

multiplier = dict()
for f in Path("page/users_hourly").iterdir():
    if f.name == ".gitkeep":
        continue
    with open(f) as tmp:
        lines = tmp.readlines()

    for line in lines:
        if "Padding" in line:
            multiplierForPacket = int(line.split(":")[-1])

    with open(f"page/json_hourly/{f.stem}.json") as f:
        hourly_packet = json.load(f)

    for key in hourly_packet["diagnosisKeys"]:
        multiplier[key["TemporaryExposureKey"]] = multiplierForPacket

risk_levels = 9

for f in sorted(Path("page/json").iterdir()):
    if f.name == ".gitkeep":
        continue
    print(f)
    jf = json.loads(f.read_text())
    for dk in jf["diagnosisKeys"]:
        k = dict()
        k["publishedOn"] = jf["timeWindowStart"].split(" ")[0]
        k["validOn"] = dk["validity"]["start"].split(" ")[0]
        k["transmissionRiskLevel"] = dk["transmissionRiskLevel"]
        k["multiplier"] = multiplier.get(dk["TemporaryExposureKey"], 10)
        keys.append(k)

for valDate in set([val["validOn"] for val in keys]):
    data["byRisk"]["validDate"][valDate] = defaultdict(int)

for date in set([val["publishedOn"] for val in keys]):
    publishedOnDay = [val for val in keys if val["publishedOn"] == date]
    data["overall"]["publishDate"][date] = round(sum([1 / val["multiplier"] for val in publishedOnDay]))
    data["byRisk"]["publishDate"][date] = dict()
    for risk in range(20):
        data["byRisk"]["publishDate"][date][risk] = round(sum([1 / val["multiplier"] for val in publishedOnDay if val["transmissionRiskLevel"] == risk]))

    for valDate in set([val["validOn"] for val in keys]):
        validOnDay = [val for val in publishedOnDay if val["validOn"] == valDate]
        data["overall"]["validDate"][valDate] += round(sum([1 / val["multiplier"] for val in validOnDay]))
        for risk in range(risk_levels):
            data["byRisk"]["validDate"][valDate][risk] += round(sum([1 / val["multiplier"] for val in validOnDay if val["transmissionRiskLevel"] == risk]))


values = []
valuesByRisk = []
for date in set([val["publishedOn"] for val in keys] + [val["validOn"] for val in keys]):
    values.append({"date": date, "published": data["overall"]["publishDate"].get(date, 0), "users_published": round(sum([1 / k["multiplier"] for k in keys if k["publishedOn"] == date and k["transmissionRiskLevel"] == 6])), "valid": data["overall"]["validDate"].get(date, 0)})
    for risk in range(risk_levels):
        valuesByRisk.append({"date": date, "published": data["byRisk"]["publishDate"].get(date, dict()).get(risk, 0), "valid": data["byRisk"]["validDate"].get(date, dict()).get(risk, 0), "risk": risk})

usersByCount = []
for f in sorted(Path("page/users_hourly").iterdir()):
    if f.name == ".gitkeep":
        continue
    print(f)
    with open(f) as tmp:
        last_line = tmp.readlines()[-1]

    user_dist = last_line.split("/")[1].split(",")
    if "(" in user_dist[-1]:
        user_dist[-1] = user_dist[-1].split("(")[0]
    user_dist = [val.strip() for val in user_dist]

    for tpl in user_dist:
        user_count, key_count = tpl.split("*")
        user_count = int(user_count)
        key_count = int(key_count)
        current_date = [date for date in usersByCount if date["key_count"] == key_count and date["date"] == f.stem[: f.stem.rfind("-")]]
        if len(current_date) == 0:
            current_date = dict()
            current_date["date"] = f.stem[: f.stem.rfind("-")]
            current_date["key_count"] = key_count
            current_date["user_count"] = 0
            usersByCount.append(current_date)
        else:
            current_date = current_date[0]
        current_date["user_count"] += user_count


values.sort(key=lambda x: x["date"])
valuesByRisk.sort(key=lambda x: x["date"])
usersByCount.sort(key=lambda x: x["date"])


if values[-1]["valid"] == 0:
    for val in valuesByRisk:
        if val["date"] == values[-1]["date"]:
            del val["valid"]
    del values[-1]["valid"]

for date in usersByCount:
    s = sum([(val["user_count"] * val["key_count"]) for val in usersByCount if val["date"] == date["date"]])
    if s > 0:
        date["average_key_count_per_user"] = s / [val for val in values if val["date"] == date["date"]][0]["users_published"]

for val in values:
    if val["date"] not in [v["date"] for v in usersByCount]:
        filler = dict()
        filler["date"] = val["date"]
        filler["user_count"] = 0
        filler["key_count"] = 1
        usersByCount.append(filler)

with open("page/plots/data.json", "w") as f:
    json.dump(values, f, sort_keys=True)

with open("page/plots/dataByRisk.json", "w") as f:
    json.dump(valuesByRisk, f, sort_keys=True)

with open("page/plots/usersByCount.json", "w") as f:
    json.dump(usersByCount, f, sort_keys=True)
