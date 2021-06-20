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
