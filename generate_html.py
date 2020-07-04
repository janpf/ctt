from jinja2 import Template
from pathlib import Path

available_dates = Path("page/keys/").iterdir()
available_dates = sorted([val.stem for val in available_dates if not val.name == ".gitkeep"], reverse=True)
print(available_dates)

with open("page/template.html") as f:
    template = Template(f.read())

with open("page/index.html", "w") as f:
    f.write(template.render(dates=available_dates))
