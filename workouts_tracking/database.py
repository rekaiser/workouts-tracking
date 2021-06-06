import sqlite3 as sql

from workouts_tracking.exercise import Exercise
from workouts_tracking.constants import (DATABASE_TABLES_DICTIONARY, DATABASE_TABLE_ENTRIES,
                                         DATABASE_TABLE_COLUMNS,
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
        self.open_connection = True
        if self.is_empty():
            self.initialize_tables()

    def is_empty(self):
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
        self.open_connection = False

    def initialize_tables(self):
        with self.connection:
            for table, columns in DATABASE_TABLES_DICTIONARY.items():
                columns_string = ", ".join(columns)
                self.cursor.execute(f"CREATE TABLE {table} ({columns_string});")
                for entry in DATABASE_TABLE_ENTRIES[table]:
                    columns_string = ", ".join(DATABASE_TABLE_COLUMNS[table])
                    entry_string_list = []
                    for value in entry:
                        if isinstance(value, str):
                            entry_string_list.append(f"'{value}'")
                        else:
                            entry_string_list.append(f"{value}")
                    entry_string = ", ".join(entry_string_list)
                    self.cursor.execute(f"INSERT INTO {table} ({columns_string}) "
                                        f"values ({entry_string});")

    def new_exercise(self, exercise: Exercise):
        pass

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
        return  column_names
