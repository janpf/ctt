import requests

# https://svc90.main.px.t-online.de/version/v1/diagnosis-keys/country/DE/date
protocol = "https://"
host = "svc90.main.px.t-online.de"
version = "v1"
country = "DE"

dates_url = f"{protocol}{host}/version/{version}/diagnosis-keys/country/{country}/date"
available_dates = requests.get(dates_url).json()
print(f"available date: {available_dates}")

for date in available_dates:
    print(f"downloading file for {date}")
    file_url = f"{dates_url}/{date}"
    r = requests.get(file_url)
    with open(f"keys/{date}.zip", "wb") as f:
        f.write(r.content)
