from .database import Database


class Measure:
    def __init__(self, name: str, type_id: int, per_set: bool):
        self.name = name
        self.type_id = type_id
        self.per_set = per_set

    def values_for_measure_table(self):
        return self.name, self.type_id, int(self.per_set)

    def __eq__(self, other):
        bool_list = [
            self.name == other.name,
            self.type_id == other.type_id,
            self.per_set == other.per_set,
        ]
        return all(bool_list)

    def get_type_string(self, database: Database):
        type_id, type_name, type_unit = database.get_measure_type_for_id(self.type_id)
        return f"{type_name} ({type_unit})"
