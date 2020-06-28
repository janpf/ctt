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
    values.append({"date": date, "published": data["overall"]["publishDate"].get(date, 0), "valid": data["overall"]["validDate"].get(date, 0)})
    for risk in range(risk_levels):
        valuesByRisk.append({"date": date, "published": data["byRisk"]["publishDate"].get(date, dict()).get(risk, 0), "valid": data["byRisk"]["validDate"].get(date, dict()).get(risk, 0), "risk": risk})

values.sort(key=lambda x: x["date"])
valuesByRisk.sort(key=lambda x: x["date"])

if values[-1]["valid"] == 0:
    for val in valuesByRisk:
        if val["date"] == values[-1]["date"]:
            del val["valid"]
    del values[-1]["valid"]


with open("page/plots/data.json", "w") as f:
    json.dump(values, f, sort_keys=True)

with open("page/plots/dataByRisk.json", "w") as f:
    json.dump(valuesByRisk, f, sort_keys=True)
