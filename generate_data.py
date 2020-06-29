import json
from pathlib import Path

keys = []

data = dict()
data["overall"] = dict()
data["overall"]["publishDate"] = dict()
data["overall"]["validDate"] = dict()

data["byRisk"] = dict()
data["byRisk"]["publishDate"] = dict()
data["byRisk"]["validDate"] = dict()

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
        keys.append(k)

for date in set([val["publishedOn"] for val in keys]):
    data["overall"]["publishDate"][date] = int(len([val for val in keys if val["publishedOn"] == date]) / 10)
    data["byRisk"]["publishDate"][date] = dict()
    for risk in range(20):
        data["byRisk"]["publishDate"][date][risk] = int(len([val for val in keys if val["publishedOn"] == date and val["transmissionRiskLevel"] == risk]) / 10)

for date in set([val["validOn"] for val in keys]):
    data["overall"]["validDate"][date] = int(len([val for val in keys if val["validOn"] == date]) / 10)
    data["byRisk"]["validDate"][date] = dict()
    for risk in range(risk_levels):
        data["byRisk"]["validDate"][date][risk] = int(len([val for val in keys if val["validOn"] == date and val["transmissionRiskLevel"] == risk]) / 10)


values = []
valuesByRisk = []
for date in set([val["publishedOn"] for val in keys] + [val["validOn"] for val in keys]):
    values.append({"date": date, "published": data["overall"]["publishDate"].get(date, 0), "valid": data["overall"]["validDate"].get(date, 0), "users_published": 0})
    for risk in range(risk_levels):
        valuesByRisk.append({"date": date, "published": data["byRisk"]["publishDate"].get(date, dict()).get(risk, 0), "valid": data["byRisk"]["validDate"].get(date, dict()).get(risk, 0), "risk": risk})

usersByCount = []

for f in Path("page/users").iterdir():
    if f.name == ".gitkeep":
        continue
    print(f)
    with open(f) as tmp:
        last_line = tmp.readlines()[-1]
    user_count = int(last_line.split("/")[0].strip())
    for val in values:
        if val["date"] == f.stem:
            val["users_published"] = user_count

    user_dist = last_line.split("/")[1].split(",")
    if "(" in user_dist[-1]:
        user_dist[-1] = user_dist[-1].split("(")[0]
    user_dist = [val.strip() for val in user_dist]

    for tpl in user_dist:
        user_count, key_count = tpl.split("*")
        user_count = int(user_count)
        key_count = int(key_count)
        date = dict()
        date["date"] = f.stem
        date["user_count"] = user_count
        date["key_count"] = key_count
        usersByCount.append(date)


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
