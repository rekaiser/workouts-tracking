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
            raise ProcedureError("The CurrentWorkout has already been started. Cannot start again.")
        self.date = dt.date.today()
        self.start_time = dt.datetime.now().time()
        self.status = "active"

    def end_workout(self):
        if self.status not in ["active", "paused"]:
            raise ProcedureError("The CurrentWorkout has not yet been started. Cannot end the"
                                 " workout.")
        if self.status == "finished":
            raise ProcedureError("The CurrentWorkout was already finished. Cannot end the workout"
                                 "again.")
        self.end_time = dt.datetime.now().time()
        self.status = "finished"

    def set_comment(self, comment: str):
        self.comment = comment

    def create_workout(self):
        if self.status == "finished":
            workout = Workout(self.date, self.start_time, self.end_time, self.comment)
        else:
            raise ProcedureError("The Workout cannot be created from the CurrentWorkout as it has"
                                 "not been finished yet.")
        return workout

