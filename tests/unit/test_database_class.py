import sqlite3 as sql

from workouts_tracking.database import Database
from workouts_tracking.constants import TESTS_DIR


class TestBasicDatabase:
    def test_existence_tables(self, tmp_path, basic_database_fixture):
        reference_connection, reference_cursor = basic_database_fixture
        test_database = Database(tmp_path / "test_database.db")
        with reference_connection:
            reference_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            reference_tables = reference_cursor.fetchall()
        with test_database.connection:
            test_database.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            test_tables = test_database.cursor.fetchall()
        assert len(test_tables) == len(reference_tables)
        for table in test_tables:
            assert table in reference_tables

    def test_columns_of_tables(self, tmp_path, basic_database_fixture):
        reference_connection, reference_cursor = basic_database_fixture
        test_database = Database(tmp_path / "test_database.db")
        test_table_names = test_database.get_table_names()
        for table_name in test_table_names:
            with reference_connection:
                reference_cursor.execute(f"PRAGMA table_info ({table_name});")
                reference_pragma_table = reference_cursor.fetchall()
            with test_database.connection:
                test_database.cursor.execute(f"PRAGMA table_info ({table_name});")
                test_pragma_table = test_database.cursor.fetchall()
            assert reference_pragma_table == test_pragma_table

    def test_initial_table_entries(self, tmp_path, basic_database_fixture):
        reference_connection, reference_cursor = basic_database_fixture
        test_database = Database(tmp_path / "test_database.db")
        test_table_names = test_database.get_table_names()
        for table_name in test_table_names:
            column_names = test_database.get_column_names_for_table(table_name)
            column_names_string = ", ".join(column_names)
            with reference_connection:
                reference_cursor.execute(f"SELECT {column_names_string} FROM {table_name};")
                reference_content = reference_cursor.fetchall()
            with test_database.connection:
                test_database.cursor.execute(f"SELECT {column_names_string} FROM {table_name};")
                test_content = test_database.cursor.fetchall()
            for line in reference_content:
                assert line in test_content
        assert False


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
