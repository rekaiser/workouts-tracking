class Measure:
    def __init__(self, name: str, type_id: int, per_set: bool, exercise_id: int):
        self.name = name
        self.type_id = type_id
        self.per_set = per_set
        self.exercise_id = exercise_id

    def values_for_measure_table(self):
        return self.name, self.type_id, int(self.per_set), self.exercise_id
