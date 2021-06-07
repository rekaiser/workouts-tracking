import sqlite3 as sql
import pytest

from workouts_tracking.database import Database, DatabaseError
from workouts_tracking.constants import (DATABASE_EXERCISE_COLUMNS as EXERCISE_COLUMNS,
                                         DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS as
                                         EXERCISE_MUSCLE_GROUP_COLUMNS,
                                         DATABASE_EXERCISE_MUSCLE_GROUP as EXERCISE_MUSCLE_GROUP,
                                         DATABASE_EXERCISE as EXERCISE)
from workouts_tracking.utils import record_list_to_string, columns_list_to_string


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


class TestDifferentInitialDatabases:
    def test_correct_database_with_initial_entries(self, basic_database_fixture):
        connection, cursor = basic_database_fixture
        exercise_records = [(1, "Test exercise", "some comment", "juo.de", 1, 1),
                            (2, "TRst Exercise", "", "juo.com", 2, 2),
                            (3, "EXE2", "test comment", "juo.fr", 1, 3),
                            ]
        exercise_muscle_group_records = [(1, 1), (1, 2), (1, 4), (2, 3), (2, 7), (3, 1)]
        with connection:
            cursor.execute(f"INSERT INTO {EXERCISE} "
                           f"({columns_list_to_string(EXERCISE_COLUMNS)}) values "
                           f"({record_list_to_string(exercise_records[0])}),"
                           f"({record_list_to_string(exercise_records[1])}),"
                           f"({record_list_to_string(exercise_records[2])});")
            cursor.execute(f"INSERT INTO {EXERCISE_MUSCLE_GROUP} "
                           f"({columns_list_to_string(EXERCISE_MUSCLE_GROUP_COLUMNS)}) "
                           f"values "
                           f"({record_list_to_string(exercise_muscle_group_records[0])}),"
                           f"({record_list_to_string(exercise_muscle_group_records[1])}),"
                           f"({record_list_to_string(exercise_muscle_group_records[2])}),"
                           f"({record_list_to_string(exercise_muscle_group_records[3])}),"
                           f"({record_list_to_string(exercise_muscle_group_records[4])}),"
                           f"({record_list_to_string(exercise_muscle_group_records[5])});")
            cursor.execute("PRAGMA database_list;")
            file_name = cursor.fetchone()[2]
        db = Database(file_name)
        with db.connection:
            db.cursor.execute(f"SELECT {columns_list_to_string(EXERCISE_COLUMNS)} "
                              f"from {EXERCISE};")
            test_exercise_records = db.cursor.fetchall()
            for exercise_record in exercise_records:
                assert exercise_record in test_exercise_records
            db.cursor.execute(f"SELECT {columns_list_to_string(EXERCISE_MUSCLE_GROUP_COLUMNS)} "
                              f"from {EXERCISE_MUSCLE_GROUP};")
            test_exercise_muscle_group_records = db.cursor.fetchall()
            for exercise_muscle_group_record in exercise_muscle_group_records:
                assert exercise_muscle_group_record in test_exercise_muscle_group_records

    def test_corrupt_database_is_not_loaded_missing_table(self, basic_database_fixture):
        connection, cursor = basic_database_fixture
        with connection:
            cursor.execute(f"DROP TABLE {EXERCISE};")
            cursor.execute("PRAGMA database_list;")
            file_name = cursor.fetchone()[2]
        with pytest.raises(DatabaseError):
            Database(file_name)


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
