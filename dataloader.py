import csv

def load_plants():
    plants = []
    with open('dataset1/plants.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            plants.append(row)
    return plants
