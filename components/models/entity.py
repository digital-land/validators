import csv
import json
import os
from shapely import wkt
from shapely.geometry import Point

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'config', 'globalConfig.json')

class Entity:

    def __init__(self, Reference=None, Name=None, Geometry=None, Point=None, Start_date=None, End_date=None, Notes=None, Legislation=None, Document_url=None):
        self.Reference = Reference
        self.Name = Name
        self.Geometry = Geometry
        self.Point = Point
        self.Start_date = Start_date
        self.End_date = End_date
        self.Notes = Notes
        self.Legislation = Legislation
        self.Document_url = Document_url

        self.errors = []

        self.load_config(CONFIG_FILE_PATH)


    def load_config(self, CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            self.mapping = json.load(config_file)


    def fetch_data_from_csv(self,file_path):
         data = []
         with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                entity = Entity()
                for field, field_values in self.mapping.items():
                    field_value = None
                    if not field_values:
                        field_value = row.get(field)
                    if field_value is None and field == 'Point':
                        geometry = wkt.loads(entity.Geometry)
                        centroid = geometry.centroid
                        lat, lon = centroid.x, centroid.y
                        field_value = Point(lat, lon)
                   
                    for value in field_values:
                        if value in row:
                            field_value = row[value]
                            break
                    if field_value is None:
                        field_value = ''
                    setattr(entity, field, field_value)
                data.append(entity)
         return data
    
    def fetch_data_from_arcgis(data):
        pass
