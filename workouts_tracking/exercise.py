from typing import List


class Exercise:
    def __init__(self, name: str, comment: str, url: str, category_id: int, difficulty_id: int,
                 muscle_group_ids: List[int]):
        self.name = name
        self.comment = comment
        self.url = url
        self.category_id = category_id
        self.difficulty_id = difficulty_id
        self.muscle_group_ids = muscle_group_ids

    def values_for_exercise_table(self):
        return self.name, self.comment, self.url, self.category_id, self.difficulty_id

    def __eq__(self, other):
        bool_list = [
            self.name == other.name,
            self.comment == other.comment,
            self.url == other.url,
            self.category_id == other.category_id,
            self.difficulty_id == other.difficulty_id,
            self.muscle_group_ids == other.muscle_group_ids,
        ]
        return all(bool_list)
