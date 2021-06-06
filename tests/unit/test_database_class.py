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

    def test_initialize_tables(self, empty_database_fixture):
        edf = empty_database_fixture
        with edf.connection:
            edf.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = edf.cursor.fetchall()
            for table in [("exercises",), ("workouts",)]:
                assert table in tables

    def test_new_exercise(self, empty_database_fixture, exercise_fixture):
        edf = empty_database_fixture
        edf.new_exercise(exercise_fixture)
        with edf.connection:
            edf.cursor.execute("SELECT ROWID, * FROM exercises;")
            exercises = edf.cursor.fetchall()
            assert len(exercises) == 1
            edf.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = edf.cursor.fetchall()
            assert ("exercise_1",) in tables

    def test_get_table_names(self, empty_database_fixture, exercise_fixture):
        edf = empty_database_fixture
        tables = edf.get_table_names()
        initial_tables = ["exercises", "workouts"]
        for table in initial_tables:
            assert table in tables
        assert "exercise_1" not in tables
        edf.new_exercise(exercise_fixture)
        edf.new_exercise(exercise_fixture)
        assert "exercise_2" in edf.get_table_names()

    def test_get_exercise_names(self, empty_database_fixture):
        edf = empty_database_fixture
        exercises_to_be_added = [
            Exercise("Exercise 1", 3),
            Exercise("Must Have", 1),
            Exercise("Running", 5)
        ]
        for exercise in exercises_to_be_added:
            edf.new_exercise(exercise)
        for exercise in exercises_to_be_added:
            assert exercise.name in edf.get_exercise_names()
