import datetime as dt

from workouts_tracking.errors import ProcedureError


class Workout:
    states = ["inactive", "active", "paused", "finished"]
    def __init__(self, date: dt.date, start_time: dt.time, end_time: dt.time,
                 comment: str):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.comment = comment


class CurrentWorkout:
    def __init__(self):
        self.date = None
        self.start_time = None
        self.end_time = None
        self.comment = None
        self.status = "inactive"

    def start_workout(self):
        if self.status != "inactive":
            raise ProcedureError("The CurrenWorkout has already been started. Cannot start again.")
        self.date = dt.date.today()
        self.start_time = dt.datetime.now().time()
        self.status = "active"

    def end_workout(self):
        if self.status not in ["active", "paused"]:
            raise ProcedureError("The CurrentWorkout has not yet been started. Cannot end the"
                                 " workout.")
        self.end_time = dt.datetime.now().time()
        self.status = "finished"
