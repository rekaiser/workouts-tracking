import sqlite3 as sql

from workouts_tracking.database import Database
from workouts_tracking.exercise import Exercise
from workouts_tracking.constants import TESTS_DIR


class TestBasicDatabase:
    def test_existence_tables(self, tmp_path):
        reference_connection = sql.connect(TESTS_DIR / 'database' / 'basic_database.db')
        reference_cursor = reference_connection.cursor()
        test_database = Database(tmp_path / "test_database.db")
        with reference_connection:
            reference_cursor.execute("select name from sqlite_master where type='table';")
            reference_tables = reference_cursor.fetchall()
        with test_database.connection:
            test_database.cursor.execute("select name from sqlite_master where type='table';")
            test_tables = test_database.cursor.fetchall()
        assert len(test_tables) == len(reference_tables)
        for table in test_tables:
            assert table in reference_tables


class TestDatabaseMethods:
    def test_init_method(self, tmp_path):
        database = Database(tmp_path / "test_database.db")
        assert isinstance(database.connection, sql.Connection)
        assert isinstance(database.cursor, sql.Cursor)
        assert database.filename == tmp_path / "test_database.db"
        assert database.connection

    def test_close_connection(self, empty_database_fixture):
        edf = empty_database_fixture
        edf.close_connection()
        assert not edf.open_connection