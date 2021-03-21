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

    def check_database_connection(self):
        """This method checks if the database connection is still open and raises an error if not."""
        if not self.open_connection:
            raise DatabaseError("The connection to the database has already been closed. "
                                "Cannot perform action. Aborting.")

    def close_connection(self):
        """Closes the connection in self.connection."""
        self.check_database_connection()
        self.connection.close()
        self.open_connection = False


def main():
    database = Database("test.db")
    database.close_connection()
    print(database.filename)


if __name__ == '__main__':
    main()
