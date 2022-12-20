import csv
import json


def csv_to_json(csvFilePath, jsonFilePath, model):
    jsonArray = []

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            record = {"model": model, "pk": row["id"]}
            del row["id"]
            if "price" in row:
                row["price"] = int(row["price"])
            if "is_published" in row:
                if row["is_published"] == "TRUE":
                    row["is_published"] = True
                else:
                    row["is_published"] = False
            record["fields"] = row
            jsonArray.append(record)

    # convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, ensure_ascii=False, indent=4)
        jsonf.write(jsonString)


csv_to_json('data/categories.csv', 'data/categories.json', 'categories.category')
csv_to_json('data/data.csv', 'data/data.json', 'ads.ad')
csv_to_json('data/location.csv', 'data/location.json', 'locations.location')
csv_to_json('data/user.csv', 'data/user.json', 'users.user')


