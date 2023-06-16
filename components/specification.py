import csv
import os
from datetime import datetime



specification_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "specification"
)


class Specification:
    def __init__(self, path=specification_path):
        self.schema_field = {}
        self.load_schema_field(path)




    def load_schema_field(self, path):
        reader = csv.DictReader(open(os.path.join(path, "schema-field.csv")))
        for row in reader:
            self.schema_field.setdefault(row["schema"], [])
            self.schema_field[row["schema"]].append(row["field"])
        

   
