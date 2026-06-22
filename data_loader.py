import csv
import os

def load_plants():
    plants = []

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "dataset1", "plants.csv")

    with open(csv_path, encoding="latin-1", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            plants.append({
                "name": row.get("Plant Name", "").strip(),
                "growth": row.get("Growth", "").strip(),
                "soil": row.get("Soil", "").strip(),
                "sunlight": row.get("Sunlight", "").strip(),
                "watering": row.get("Watering", "").strip(),
                "fertilization": row.get("Fertilization Type", "").strip(),
                "type": row.get("Type", "General").strip()
            })

    return plants
