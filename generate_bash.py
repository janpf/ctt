import datetime
from pathlib import Path

# plaintext
with open("create_plaintext.sh", "w") as cb:
    for f in sorted(Path("page/keys").iterdir()):
        if f.name == ".gitkeep" or f.name == "removed" or f.name == "updated":
            continue
        cb.write(f"echo parsing {f}; python ../diagnosis-keys/parse_keys.py -u -d {f} > page/plaintext/{f.stem}.txt &\n")

    cb.write("wait")

# users
with open("create_users.sh", "w") as cb:
    for f in sorted(Path("page/keys").iterdir()):
        if f.name == ".gitkeep" or f.name == "removed" or f.name == "updated":
            continue

        if datetime.datetime.fromisoformat(f.stem) > datetime.datetime.fromisoformat("2020-10-17"):
            cb.write(f"echo parsing {f}; python ./create_users.py -m 1 -v v1.5 -d {f} > page/users/{f.stem}.txt &\n")

        elif datetime.datetime.fromisoformat(f.stem) >= datetime.datetime.fromisoformat("2020-07-02"):
            cb.write(f"echo parsing {f}; python ./create_users.py -n -m 5 -d {f} > page/users/{f.stem}.txt &\n")

        elif "2020-06-23" in f.stem:
            cb.write(f"echo parsing {f}; python ./create_users.py -m 10 -d {f} > page/users/{f.stem}.txt &\n")

        else:
            cb.write(f"echo parsing {f}; python ./create_users.py -d {f} > page/users/{f.stem}.txt &\n")

    cb.write("wait")

# users hourly
with open("create_users_hourly.sh", "w") as cb:
    for f in sorted(Path("page/keys_hourly").iterdir()):
        if f.name == ".gitkeep" or f.name == "removed" or f.name == "updated":
            continue

        if datetime.datetime.fromisoformat(f.stem[: f.stem.rfind("-")]) > datetime.datetime.fromisoformat("2020-10-17"):
            cb.write(f"echo parsing {f}; python ./create_users.py -m 1 -v v1.5 -d {f} > page/users_hourly/{f.stem}.txt &\n")

        elif datetime.datetime.fromisoformat(f.stem[: f.stem.rfind("-")]) > datetime.datetime.fromisoformat("2020-07-02"):
            cb.write(f"echo parsing {f}; python ./create_users.py -n -m 5 -d {f} > page/users_hourly/{f.stem}.txt &\n")

        elif datetime.datetime.fromisoformat(f.stem[: f.stem.rfind("-")]) == datetime.datetime.fromisoformat("2020-07-02"):
            if int(f.stem[f.stem.rfind("-") + 1 :]) > 11:
                cb.write(f"echo parsing {f}; python ./create_users.py -n -a -d {f} > page/users_hourly/{f.stem}.txt &\n")
            else:
                cb.write(f"echo parsing {f}; python ./create_users.py -a -d {f} > page/users_hourly/{f.stem}.txt &\n")

        elif "2020-06-23" in f.stem:
            cb.write(f"echo parsing {f}; python ./create_users.py -m 10 -d {f} > page/users_hourly/{f.stem}.txt &\n")

        else:
            cb.write(f"echo parsing {f}; python ./create_users.py -d {f} > page/users_hourly/{f.stem}.txt &\n")

    cb.write("wait")
