import datetime as dt

from workouts_tracking.workout import Workout


class TestWorkoutAttributes:
    def test_workout_attributes(self):
        test_date = dt.date.fromisoformat("2001-12-02")
        test_start_time = dt.time.fromisoformat("12:10:00")
        test_end_time = dt.time.fromisoformat("12:45:00")
        w = Workout(test_date, test_start_time, test_end_time, "Test...")
        assert w.date.isoformat() == "2001-12-02"
        assert w.start_time.isoformat() == "12:10:00"
        assert w.end_time.isoformat() == "12:45:00"
        assert w.comment == "Test..."
