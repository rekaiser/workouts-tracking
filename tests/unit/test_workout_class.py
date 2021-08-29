import datetime as dt

import pytest

from workouts_tracking.workout import Workout, CurrentWorkout
from workouts_tracking.errors import ProcedureError


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


class TestCurrentWorkout:
    def test_current_workout_attributes(self):
        cw = CurrentWorkout()
        assert cw.date is None
        assert cw.start_time is None
        assert cw.end_time is None
        assert cw.comment is None
        assert cw.status == "inactive"

    def test_start_workout(self):
        cw = CurrentWorkout()
        current_datetime = dt.datetime.now()
        date = current_datetime.date()
        start_time1 = current_datetime.time()
        cw.start_workout()
        start_time2 = dt.datetime.now().time()
        assert date == cw.date
        assert start_time1 < cw.start_time < start_time2
        assert cw.status == "active"
        with pytest.raises(ProcedureError):
            cw.start_workout()

    def test_end_workout(self):
        cw = CurrentWorkout()
        with pytest.raises(ProcedureError):
            cw.end_workout()
        cw.start_workout()
        end_time1 = dt.datetime.now().time()
        cw.end_workout()
        end_time2 = dt.datetime.now().time()
        assert end_time1 < cw.end_time < end_time2
        assert cw.status == "finished"
