import datetime
from pathlib import Path

# plaintext
with open("create_plaintext.sh", "w") as cb:
    for f in sorted(Path("page/keys").iterdir()):
        if f.name == ".gitkeep" or f.name == "removed" or f.name == "updated":
            continue
        if Path(f"page/plaintext/{f.stem}.txt").exists():
            continue

        cb.write(f"echo parsing {f}; python ../diagnosis-keys/parse_keys.py -d {f} > page/plaintext/{f.stem}.txt\n")

# users
with open("create_users.sh", "w") as cb:
    for f in sorted(Path("page/keys").iterdir()):
        if f.name == ".gitkeep" or f.name == "removed" or f.name == "updated":
            continue
        if Path(f"page/users/{f.stem}.txt").exists():
            continue

        if datetime.datetime.fromisoformat(f.stem) > datetime.datetime.fromisoformat("2020-10-17"):
            cb.write(f"echo parsing {f}; python ./create_users.py -m 1 -v v1.5 -d {f} > page/users/{f.stem}.txt\n")

        elif datetime.datetime.fromisoformat(f.stem) >= datetime.datetime.fromisoformat("2020-07-02"):
            cb.write(f"echo parsing {f}; python ./create_users.py -n -m 5 -d {f} > page/users/{f.stem}.txt\n")

        elif "2020-06-23" in f.stem:
            cb.write(f"echo parsing {f}; python ./create_users.py -m 10 -d {f} > page/users/{f.stem}.txt\n")

        else:
            cb.write(f"echo parsing {f}; python ./create_users.py -d {f} > page/users/{f.stem}.txt\n")
