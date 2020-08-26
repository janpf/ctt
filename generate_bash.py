import datetime
from pathlib import Path

# plaintext
with open("create_plaintext.sh", "w") as cb:
    for f in sorted(Path("page/keys").iterdir()):
        if f.name == ".gitkeep" or f.name == "removed" or f.name == "updated":
            continue
        if datetime.datetime.fromisoformat(f.stem) >= datetime.datetime.fromisoformat("2020-07-02"):
            cb.write(f"echo parsing {f}; python ../diagnosis-keys/parse_keys.py -u -n -a -m 9 -d {f} > page/plaintext/{f.stem}.txt\n")
        else:
            cb.write(f"echo parsing {f}; python ../diagnosis-keys/parse_keys.py -u -a -d {f} > page/plaintext/{f.stem}.txt\n")


# users
with open("create_users.sh", "w") as cb:
    for f in sorted(Path("page/keys").iterdir()):
        if f.name == ".gitkeep" or f.name == "removed" or f.name == "updated":
            continue
        if datetime.datetime.fromisoformat(f.stem) >= datetime.datetime.fromisoformat("2020-07-02"):
            cb.write(f"echo parsing {f}; python ./create_users.py -n -m 5 -d {f} > page/users/{f.stem}.txt\n")
        elif "2020-06-23" in f.stem:
            cb.write(f"echo parsing {f}; python ./create_users.py -m 10 -d {f} > page/users/{f.stem}.txt\n")
        else:
            cb.write(f"echo parsing {f}; python ./create_users.py -d {f} > page/users/{f.stem}.txt\n")


# users hourly
with open("create_users_hourly.sh", "w") as cb:
    for f in sorted(Path("page/keys_hourly").iterdir()):
        if f.name == ".gitkeep" or f.name == "removed" or f.name == "updated":
            continue

        if f.stem in ["2020-08-04-9", "2020-08-08-18", "2020-08-08-8", "2020-08-12-10", "2020-08-15-8", "2020-08-18-15", "2020-08-18-19", "2020-08-22-12", "2020-08-24-5", "2020-08-25-10"]:
            cb.write(f"echo parsing {f}; python ./create_users.py -n -m 5 -d {f} > page/users_hourly/{f.stem}.txt\n")

        elif datetime.datetime.fromisoformat(f.stem[: f.stem.rfind("-")]) > datetime.datetime.fromisoformat("2020-07-02"):
            cb.write(f"echo parsing {f}; python ./create_users.py -n -a -m 5 -d {f} > page/users_hourly/{f.stem}.txt\n")

        elif datetime.datetime.fromisoformat(f.stem[: f.stem.rfind("-")]) == datetime.datetime.fromisoformat("2020-07-02"):
            if int(f.stem[f.stem.rfind("-") + 1 :]) > 11:
                cb.write(f"echo parsing {f}; python ./create_users.py -n -a -d {f} > page/users_hourly/{f.stem}.txt\n")
            else:
                cb.write(f"echo parsing {f}; python ./create_users.py -a -d {f} > page/users_hourly/{f.stem}.txt\n")

        elif "2020-06-23" in f.stem:
            cb.write(f"echo parsing {f}; python ./create_users.py -m 10 -d {f} > page/users_hourly/{f.stem}.txt\n")

        else:
            cb.write(f"echo parsing {f}; python ./create_users.py -d {f} > page/users_hourly/{f.stem}.txt\n")
