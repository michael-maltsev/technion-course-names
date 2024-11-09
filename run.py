import json
from pathlib import Path

names_path = Path(".") / "base_names.json"

with open(names_path) as f:
    names = json.load(f)

for dir in ["technion-ug-info-fetcher", "technion-sap-info-fetcher"]:
    for file in sorted((Path('..') / dir).glob("courses_*.json")):
        print(f"{dir}: {file}")

        with open(file) as f:
            data = json.load(f)

        for course in data:
            general = course["general"]
            number = general["מספר מקצוע"]
            name = general["שם מקצוע"]
            names[number] = name

output_path = Path(".") / "names"
output_path.mkdir(exist_ok=True, parents=True)

with open(output_path / "names.json", "w") as f:
    json.dump(names, f, ensure_ascii=False)

output_path_num = output_path / "num"
output_path_num.mkdir(exist_ok=True, parents=True)

for number, name in names.items():
    with open(output_path_num / number, "w") as f:
        f.write(name)
