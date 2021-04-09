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
        self.initialize_tables()

    def close_connection(self):
        """Closes the connection in self.connection."""
        self.connection.commit()
        self.connection.close()
        self.open_connection = False

    def initialize_tables(self):
        with self.connection:
            self.cursor.execute("CREATE TABLE exercises "
                                "(name text);")
            self.cursor.execute("CREATE TABLE workouts "
                                "(name text,"
                                "date int);")

    def new_exercise(self, exercise: Exercise):
        with self.connection:
            self.cursor.execute("INSERT INTO exercises VALUES (?);", exercise.record())
            last_row_id = self.cursor.lastrowid
            self.cursor.execute(f"CREATE TABLE exercise_{last_row_id} (date int);")
