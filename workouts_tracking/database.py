import sqlite3 as sql

from workouts_tracking.exercise import Exercise


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
            columns_string = Exercise("", 0).create_columns_string()
            self.cursor.execute(f"CREATE TABLE exercises ({columns_string});")
            self.cursor.execute("CREATE TABLE workouts (name text, date int);")

    def new_exercise(self, exercise: Exercise):
        with self.connection:
            self.cursor.execute("INSERT INTO exercises VALUES (?, ?);", exercise.record())
            last_row_id = self.cursor.lastrowid
            self.cursor.execute(f"CREATE TABLE exercise_{last_row_id} (date int);")

    def get_table_names(self):
        with self.connection:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
            raw_table_tuples = self.cursor.fetchall()
        table_names = []
        for raw_table_tuple in raw_table_tuples:
            table_names.append(raw_table_tuple[0])
        return table_names
