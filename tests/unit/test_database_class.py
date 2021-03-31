import sqlite3 as sql

from workouts_tracking.database import Database


class TestDatabaseMethods:
    def test_init_method(self, tmp_path):
        database = Database(tmp_path / "test_database.db")
        assert isinstance(database.connection, sql.Connection)
        assert database.filename == tmp_path / "test_database.db"
        assert database.connection

    def test_close_connection(self, empty_database_fixture):
        edf = empty_database_fixture
        edf.close_connection()
        assert not edf.open_connection
