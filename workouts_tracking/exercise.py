from typing import List


class Exercise:
    def __init__(self, name: str, comment: str, url: str, category_id: int, difficulty_id: int,
                 muscle_group_ids: List[int], measure_ids: List[int]):
        self.name = name
        self.comment = comment
        self.url = url
        self.category_id = category_id
        self.difficulty_id = difficulty_id
        self.muscle_group_ids = muscle_group_ids
        self.measure_ids = measure_ids

    def values_for_exercise_table(self):
        return self.name, self.comment, self.url, self.category_id, self.difficulty_id
