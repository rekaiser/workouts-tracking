import sqlite3 as sql


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

    def close_connection(self):
        """Closes the connection in self.connection."""
        self.connection.close()
        self.open_connection = False

    def initialize_tables(self):
        with self.connection as con:
            con.execute("CREATE TABLE exercises "
                        "(id int,"
                        "name text,"
                        "category text,"
                        "muscles_groups text,"
                        "difficulty text);")
            con.execute("CREATE TABLE workouts "
                        "(id int,"
                        "date int)")
