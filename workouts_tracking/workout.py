import datetime as dt


class Workout:
    def __init__(self, date: dt.date, start_time: dt.time, end_time: dt.time,
                 comment: str):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.comment = comment
