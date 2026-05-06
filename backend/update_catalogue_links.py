import json
from urllib.parse import quote_plus

path = "app/data/catalogue.json"
# This script updates the catalogue.json file to add "link" and "image" fields for each item.
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data["items"]:
    name = item["name"]
    query = quote_plus(name)

    item["link"] = f"https://www.google.com/search?tbm=shop&q={query}"
    item["image"] = f"https://placehold.co/400x500/png?text={quote_plus(name)}"

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated all catalogue links and images.")