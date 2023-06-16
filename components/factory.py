from specification import Specification

class Factory:
    def __init__(self):
        self.dataset_fields = {}


    def get_specification(self, dataset):
        specification = Specification()
        mandatory_fields = specification.schema_field[dataset]
        self.dataset_fields[dataset] = mandatory_fields
        return self