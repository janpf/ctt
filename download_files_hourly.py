import requests

# https://svc90.main.px.t-online.de/version/v1/diagnosis-keys/country/DE/date
protocol = "https://"
host = "svc90.main.px.t-online.de"
version = "v1"
country = "DE"

dates_url = f"{protocol}{host}/version/{version}/diagnosis-keys/country/{country}/date"
available_dates = requests.get(dates_url).json()
print(f"available dates: {available_dates}")

for date in available_dates:
    hours_url = f"{dates_url}/{date}/hour"
    available_hours = requests.get(hours_url).json()

    print(f"hourly available keys on {date}: {available_hours}")
    for hour in available_hours:
        with open(f"page/keys_hourly/{date}-{hour}.zip", "wb") as f:
            f.write(requests.get(f"{hours_url}/{hour}").content)
