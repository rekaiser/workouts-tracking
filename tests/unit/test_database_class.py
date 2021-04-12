import sqlite3 as sql

from workouts_tracking.database import Database


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
