import json
from pathlib import Path

keys = []

data = dict()
data["overall"] = dict()
data["overall"]["publishDate"] = dict()
data["overall"]["validDate"] = dict()
data["overall"]["publishDateRisk"] = dict()
data["overall"]["validDateRisk"] = dict()

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

for date in set([val["validOn"] for val in keys]):
    data["overall"]["validDate"][date] = int(len([val for val in keys if val["validOn"] == date]) / 10)

values = []
for date in set([val["publishedOn"] for val in keys] + [val["validOn"] for val in keys]):
    values.append({"date": date, "published": data["overall"]["publishDate"].get(date, 0), "valid": data["overall"]["validDate"].get(date, 0)})

print(json.dumps(values))
