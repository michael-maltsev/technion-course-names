import json
import re
from pathlib import Path


def to_new_course_number(course):
    match = re.match(r'^9730(\d\d)$', course)
    if match:
        return '970300' + match.group(1)

    match = re.match(r'^(\d\d\d)(\d\d\d)$', course)
    if match:
        return '0' + match.group(1) + '0' + match.group(2)

    return course


names_path = Path(".") / "base_names.json"

with open(names_path) as f:
    names = json.load(f)

names_new = {}

for dir in ["technion-ug-info-fetcher", "technion-sap-info-fetcher"]:
    for file in sorted((Path('..') / dir).glob("courses_*.json")):
        print(f"{dir}: {file}")

        with open(file) as f:
            data = json.load(f)

        for course in data:
            general = course["general"]
            number = general["מספר מקצוע"]
            name = re.sub(r"\s+", " ", general["שם מקצוע"].strip())
            names[number] = name

            if dir == "technion-sap-info-fetcher":
                names_new[number] = name

for number in list(names.keys()):
    new_number = to_new_course_number(number)
    if new_number != number and new_number not in names:
        names[new_number] = names[number]

output_path = Path(".") / "names"
output_path.mkdir(exist_ok=True, parents=True)

with open(output_path / "names.json", "w") as f:
    json.dump(names, f, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

with open(output_path / "names_new.json", "w") as f:
    json.dump(names_new, f, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

output_path_num = output_path / "num"
output_path_num.mkdir(exist_ok=True, parents=True)

for number, name in names.items():
    with open(output_path_num / number, "w") as f:
        f.write(name)
