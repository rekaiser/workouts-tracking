import sqlite3 as sql

from workouts_tracking.exercise import Exercise
from workouts_tracking.measure import Measure
from workouts_tracking.constants import (DATABASE_TABLES_DICTIONARY, DATABASE_TABLE_ENTRIES,
                                         DATABASE_TABLE_COLUMNS, DATABASE_EXERCISE,
                                         DATABASE_EXERCISE_COLUMNS, DATABASE_CATEGORY,
                                         DATABASE_DIFFICULTY, DATABASE_MUSCLE_GROUP,
                                         DATABASE_MEASURE_TYPE, DATABASE_MEASURE)
from workouts_tracking.utils import (record_list_to_string, columns_list_to_string,
                                     )


class DatabaseError(Exception):
    """Exception class for errors related to the database."""
    pass


class Database:
    """This class handles the methods connected to the sqlite3 database."""

    def __init__(self, filename):
        self.filename = filename
        self.connection = sql.connect(self.filename)
        self.cursor = self.connection.cursor()
        self._open_connection = True
        if self._is_empty():
            self.initialize_database()
        elif not self.check_database_integrity():
            raise DatabaseError(f"The loaded database (filename:{self.filename}) is corrupt."
                                f"It does not fit to this program's specifications.")

    def _is_empty(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        tables = self.cursor.fetchall()
        if len(tables) == 0:
            return True
        else:
            return False

    def close_connection(self):
        """Closes the connection in self.connection."""
        self.connection.commit()
        self.connection.close()
        self._open_connection = False

    def initialize_database(self):
        with self.connection:
            for table, columns in DATABASE_TABLES_DICTIONARY.items():
                create_columns_string = ", ".join(columns)
                self.cursor.execute(f"CREATE TABLE {table} ({create_columns_string});")
                for record in DATABASE_TABLE_ENTRIES[table]:
                    columns_string = columns_list_to_string(DATABASE_TABLE_COLUMNS[table])
                    entry_string = record_list_to_string(record)
                    self.cursor.execute(f"INSERT INTO {table} ({columns_string}) "
                                        f"values ({entry_string});")

    def check_database_integrity(self):
        with self.connection:
            for table_name in DATABASE_TABLES_DICTIONARY:
                if table_name not in self.get_table_names():
                    return False
                self.cursor.execute(f"PRAGMA table_info ({table_name});")
                raw_columns = self.cursor.fetchall()
                actual_table_columns = []
                for raw_column in raw_columns:
                    actual_table_columns.append(raw_column[1])
                for column in DATABASE_TABLE_COLUMNS[table_name]:
                    if column not in actual_table_columns:
                        return False
                for column in actual_table_columns:
                    if column not in DATABASE_TABLE_COLUMNS[table_name]:
                        return False
            return True

    def new_exercise(self, exercise: Exercise):
        max_id = self.get_max_id_from_table(DATABASE_EXERCISE)
        exercise_id = max_id + 1
        with self.connection:
            columns = ", ".join(DATABASE_EXERCISE_COLUMNS)
            values = exercise.values_for_exercise_table()
            values = (exercise_id, *values)
            place_holders = ("?," * len(DATABASE_EXERCISE_COLUMNS))[:-1]
            self.cursor.execute(f"INSERT INTO {DATABASE_EXERCISE} ({columns}) "
                                f"VALUES ({place_holders});", values)
            for muscle_group_id in exercise.muscle_group_ids:
                self.cursor.execute("INSERT INTO exercise_muscle_group "
                                    "(exercise_id, muscle_group_id) values "
                                    "(?,?);", (exercise_id, muscle_group_id))
        return exercise_id

    def get_table_names(self):
        with self.connection:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
            raw_table_tuples = self.cursor.fetchall()
        table_names = []
        for raw_table_tuple in raw_table_tuples:
            table_names.append(raw_table_tuple[0])
        return table_names

    def get_exercise_names(self):
        with self.connection:
            self.cursor.execute("SELECT name FROM exercise;")
            raw_exercise_names_tuple = self.cursor.fetchall()
        exercise_names = []
        for raw_tuple in raw_exercise_names_tuple:
            exercise_names.append(raw_tuple[0])
        return exercise_names

    def get_column_names_for_table(self, table_name):
        with self.connection:
            self.cursor.execute(f"PRAGMA table_info ({table_name});")
            raw_columns = self.cursor.fetchall()
        column_names = []
        for raw_column in raw_columns:
            column_names.append(raw_column[1])
        return column_names

    def get_max_id_from_table(self, table_name):
        with self.connection:
            self.cursor.execute(f"SELECT MAX(id) FROM {table_name};")
            max_id = self.cursor.fetchone()[0]
        if max_id is None:
            return 0
        else:
            return max_id

    def get_categories(self):
        with self.connection:
            self.cursor.execute(f"SELECT id, name FROM {DATABASE_CATEGORY};")
            return self.cursor.fetchall()

    def get_difficulties(self):
        with self.connection:
            self.cursor.execute(f"SELECT id, name FROM {DATABASE_DIFFICULTY};")
            return self.cursor.fetchall()

    def get_muscle_groups(self):
        with self.connection:
            self.cursor.execute(f"SELECT id, name FROM {DATABASE_MUSCLE_GROUP};")
            return self.cursor.fetchall()

    def get_measure_types(self):
        with self.connection:
            self.cursor.execute(f"SELECT id, name, unit FROM {DATABASE_MEASURE_TYPE};")
            return self.cursor.fetchall()

    def get_measure_type_for_id(self, measure_type_id: int):
        with self.connection:
            self.cursor.execute(f"SELECT id, name, unit "
                                f"FROM {DATABASE_MEASURE_TYPE} "
                                f"WHERE id = ?;",
                                [measure_type_id])
            return self.cursor.fetchone()

    def get_exercises(self, with_id=True):
        with self.connection:
            if with_id:
                self.cursor.execute("SELECT id, name, comment, url, category_id, difficulty_id "
                                    "FROM exercise;")
            else:
                self.cursor.execute("SELECT name, comment, url, category_id, difficulty_id "
                                    "FROM exercise;")
            return self.cursor.fetchall()

    def get_id_for_exercise_name(self, name):
        with self.connection:
            self.cursor.execute("SELECT id FROM exercise WHERE name=?;", (name,))
            exercise_id = self.cursor.fetchone()
            return exercise_id[0]

    def get_exercise_muscle_groups(self):
        with self.connection:
            self.cursor.execute("SELECT exercise_id, muscle_group_id FROM exercise_muscle_group;")
            return self.cursor.fetchall()

    def get_measures(self, with_id=True):
        with self.connection:
            if with_id:
                self.cursor.execute("SELECT id, name, type_id, per_set, exercise_id FROM measure;")
            else:
                self.cursor.execute("SELECT name, type_id, per_set, exercise_id FROM measure;")
            return self.cursor.fetchall()

    def new_measure(self, measure: Measure, exercise_id: int):
        max_id = self.get_max_id_from_table(DATABASE_MEASURE)
        measure_id = max_id + 1
        with self.connection:
            values = measure.values_for_measure_table()
            values = (measure_id, *values, exercise_id)
            self.cursor.execute(f"INSERT INTO measure (id, name, type_id, per_set, exercise_id) "
                                f"VALUES (?, ?, ?, ?, ?);", values)
        return measure_id

    def get_measure_type_string_for_id(self, measure_type_id: int):
        measure_type_id, name, unit = self.get_measure_type_for_id(measure_type_id)
        return f"{name} ({unit})"

    def get_exercise_table_rows(self):
        with self.connection:
            self.cursor.execute("SELECT e.name, e.comment, e.url, c.name, d.name "
                                "FROM exercise e, difficulty d, category c "
                                "WHERE e.category_id = c.id AND e.difficulty_id = d.id;")
            return self.cursor.fetchall()
