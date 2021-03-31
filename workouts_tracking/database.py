import sqlite3 as sql


class DatabaseError(Exception):
    """Exception class for errors related to the database."""
    pass


class Database:
    """This class handles the methods connected to the sqlite3 database."""
    def __init__(self, filename):
        self.filename = filename
        self.connection = sql.connect(self.filename)
        self.open_connection = True

    def close_connection(self):
        """Closes the connection in self.connection."""
        self.connection.close()
        self.open_connection = False
