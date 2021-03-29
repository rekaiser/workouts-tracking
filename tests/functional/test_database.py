import pytest

from workouts_tracking.database import Database
from workouts_tracking.exercise import Exercise


@pytest.fixture()
def empty_database_fixture(tmp_path):
    database_filename = tmp_path / "test_database.db"
    database = Database(database_filename)
    yield database


@pytest.fixture()
def exercise_fixture():
    exercise = Exercise("some name for an exercise")
    yield exercise


class TestEmptyDatabase:
    def test_new_exercise(self, empty_database_fixture, exercise_fixture):
        edf = empty_database_fixture
        edf.new_exercise(exercise_fixture)
