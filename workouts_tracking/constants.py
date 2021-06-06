from pathlib import Path

APPLICATION_NAME = "Workouts Tracking"
INSTALL_DIR = Path(__file__).resolve().parent.parent
TESTS_DIR = INSTALL_DIR / "tests"
CODE_DIR = INSTALL_DIR / "workouts_tracking"

DATABASE_MEASURE_TYPE_COLUMNS = (
    "id",
    "name",
    "unit",
)

DATABASE_CATEGORY_COLUMNS = (
    "id",
    "name",
)

DATABASE_DIFFICULTY_COLUMNS = (
    "id",
    "name",
)

DATABASE_MUSCLE_GROUP_COLUMNS = (
    "id",
    "name",
)

DATABASE_WORKOUT_COLUMNS = (
    "id",
    "date",
    "start_time",
    "end_time",
    "comment",
)

DATABASE_EXERCISE_COLUMNS = (
    "id",
    "name",
    "command",
    "url",
    "category_id",
    "difficulty_id",
)

DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS = (
    "exercise_id",
    "muscle_group_id",
)

DATABASE_EXE_EXERCISE_COLUMNS = (
    "workout_id",
    "no_exe_exercise",
    "exercise_id",
    "comment",
)

DATABASE_MEASURE_COLUMNS = (
    "id",
    "name",
    "type_id",
    "per_set",
    "exercise_id",
)

DATABASE_PERFORMANCE_COLUMNS = (
    "workout_id",
    "no_exe_exercise",
    "measure_id",
    "value",
)

DATABASE_TABLE_COLUMNS = {
    "measure_type": DATABASE_MEASURE_TYPE_COLUMNS,
    "category": DATABASE_CATEGORY_COLUMNS,
    "difficulty": DATABASE_DIFFICULTY_COLUMNS,
    "muscle_group": DATABASE_MUSCLE_GROUP_COLUMNS,
    "workout": DATABASE_WORKOUT_COLUMNS,
    "exercise": DATABASE_EXERCISE_COLUMNS,
    "exercise_muscle_group": DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS,
    "exe_exercise": DATABASE_EXE_EXERCISE_COLUMNS,
    "measure": DATABASE_MEASURE_COLUMNS,
    "performance": DATABASE_PERFORMANCE_COLUMNS,
}

DATABASE_TABLES_DICTIONARY = {
    # dictionary of the name of the tables and its specification for sqlite3
    # ("name": ["column_name type", "primary key (id)"])
    "measure_type": [f"{DATABASE_MEASURE_TYPE_COLUMNS[0]} integer not null",
                     f"{DATABASE_MEASURE_TYPE_COLUMNS[1]} text",
                     f"{DATABASE_MEASURE_TYPE_COLUMNS[2]} text",
                     f"primary key ({DATABASE_MEASURE_TYPE_COLUMNS[0]})",
                     ],
    "category": [f"{DATABASE_CATEGORY_COLUMNS[0]} integer not null",
                 f"{DATABASE_CATEGORY_COLUMNS[1]} text",
                 f"primary key ({DATABASE_CATEGORY_COLUMNS[0]})",
                 ],
    "difficulty": [f"{DATABASE_DIFFICULTY_COLUMNS[0]} integer not null",
                   f"{DATABASE_DIFFICULTY_COLUMNS[1]} text",
                   f"primary key ({DATABASE_DIFFICULTY_COLUMNS[0]})",
                   ],
    "workout": [f"{DATABASE_WORKOUT_COLUMNS[0]} integer not null",
                f"{DATABASE_WORKOUT_COLUMNS[1]} text",
                f"{DATABASE_WORKOUT_COLUMNS[2]} text",
                f"{DATABASE_WORKOUT_COLUMNS[3]} text",
                f"{DATABASE_WORKOUT_COLUMNS[4]} text",
                f"primary key ({DATABASE_WORKOUT_COLUMNS[0]})",
                ],
    "exercise": [f"{DATABASE_EXERCISE_COLUMNS[0]} integer not null",
                 f"{DATABASE_EXERCISE_COLUMNS[1]} text",
                 f"{DATABASE_EXERCISE_COLUMNS[2]} text",
                 f"{DATABASE_EXERCISE_COLUMNS[3]} text",
                 f"{DATABASE_EXERCISE_COLUMNS[4]} integer",
                 f"{DATABASE_EXERCISE_COLUMNS[5]} integer",
                 f"primary key ({DATABASE_EXERCISE_COLUMNS[0]})",
                 f"foreign key ({DATABASE_EXERCISE_COLUMNS[4]}) "
                 f"references category({DATABASE_CATEGORY_COLUMNS[0]})",
                 f"foreign key ({DATABASE_EXERCISE_COLUMNS[5]}) "
                 f"references difficulty({DATABASE_CATEGORY_COLUMNS[0]})",
                 ],
    "muscle_group": [f"{DATABASE_MUSCLE_GROUP_COLUMNS[0]} integer not null",
                     f"{DATABASE_MUSCLE_GROUP_COLUMNS[1]} text",
                     f"primary key ({DATABASE_MUSCLE_GROUP_COLUMNS[0]})",
                     ],
    "exercise_muscle_group": [f"{DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS[0]} integer not null",
                              f"{DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS[1]} integer not null",
                              f"primary key ({DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS[0]}, "
                              f"{DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS[1]})",
                              f"foreign key ({DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS[0]}) "
                              f"references exercise({DATABASE_EXERCISE_COLUMNS[0]})",
                              f"foreign key ({DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS[1]}) "
                              f"references muscle_group({DATABASE_MUSCLE_GROUP_COLUMNS[0]})",
                              ],
    "exe_exercise": [f"{DATABASE_EXE_EXERCISE_COLUMNS[0]} integer not null",
                     f"{DATABASE_EXE_EXERCISE_COLUMNS[1]} integer not null",
                     f"{DATABASE_EXE_EXERCISE_COLUMNS[2]} integer",
                     f"{DATABASE_EXE_EXERCISE_COLUMNS[3]} text",
                     f"primary key ({DATABASE_EXE_EXERCISE_COLUMNS[0]}, "
                     f"{DATABASE_EXE_EXERCISE_COLUMNS[1]})",
                     f"foreign key ({DATABASE_EXE_EXERCISE_COLUMNS[0]}) "
                     f"references workout({DATABASE_WORKOUT_COLUMNS[0]})",
                     f"foreign key ({DATABASE_EXE_EXERCISE_COLUMNS[2]}) "
                     f"references exercise({DATABASE_EXERCISE_COLUMNS[0]})",
                     ],
    "measure": [f"{DATABASE_MEASURE_COLUMNS[0]} integer not null",
                f"{DATABASE_MEASURE_COLUMNS[1]} text",
                f"{DATABASE_MEASURE_COLUMNS[2]} integer",
                f"{DATABASE_MEASURE_COLUMNS[3]} integer "
                f"check ({DATABASE_MEASURE_COLUMNS[3]} = 0 or {DATABASE_MEASURE_COLUMNS[3]} = 1)",
                f"{DATABASE_MEASURE_COLUMNS[4]} integer",
                f"primary key ({DATABASE_MEASURE_COLUMNS[0]})",
                f"foreign key ({DATABASE_MEASURE_COLUMNS[2]}) "
                f"references measure_type({DATABASE_MEASURE_TYPE_COLUMNS[0]})",
                f"foreign key ({DATABASE_MEASURE_COLUMNS[4]}) "
                f"references exercise({DATABASE_EXERCISE_COLUMNS[0]})",
                ],
    "performance": [f"{DATABASE_PERFORMANCE_COLUMNS[0]} integer not null",
                    f"{DATABASE_PERFORMANCE_COLUMNS[1]} integer not null",
                    f"{DATABASE_PERFORMANCE_COLUMNS[2]} integer not null",
                    f"{DATABASE_PERFORMANCE_COLUMNS[3]} text",
                    f"primary key ({DATABASE_PERFORMANCE_COLUMNS[0]}, "
                    f"{DATABASE_PERFORMANCE_COLUMNS[1]}, {DATABASE_PERFORMANCE_COLUMNS[2]})",
                    f"foreign key ({DATABASE_PERFORMANCE_COLUMNS[0]}) "
                    f"references workout({DATABASE_WORKOUT_COLUMNS[0]})",
                    f"foreign key ({DATABASE_PERFORMANCE_COLUMNS[1]}) "
                    f"references exe_exercise({DATABASE_EXE_EXERCISE_COLUMNS[1]})",
                    f"foreign key ({DATABASE_PERFORMANCE_COLUMNS[2]}) "
                    f"references measure({DATABASE_MEASURE_COLUMNS[0]})",
                    ],
}

DATABASE_MEASURE_TYPE_ENTRIES = [
    (1, "weight", "kg"),
    (2, "long time", "hh:mm:ss"),
    (3, "time", "mm:ss"),
    (4, "short time", "mm:ss.sss"),
    (5, "sets", "integer"),
    (6, "repetitions", "integer"),
    (7, "distance", "m"),
    (8, "integer number", "integer"),
    (9, "real number", "float"),
]

DATABASE_CATEGORY_ENTRIES = [
    (1, "strength training"),
    (2, "endurance training"),
    (3, "coordination training"),
]

DATABASE_DIFFICULTY_ENTRIES = [
    (1, "very easy"),
    (2, "easy"),
    (3, "medium"),
    (4, "hard"),
    (5, "very hard"),
]

DATABASE_MUSCLE_GROUP_ENTRIES = [
    (1, "chest"),
    (2, "abdominal muscles"),
    (3, "neck"),
    (4, "upper back"),
    (5, "upper arms"),
    (6, "shoulders"),
    (7, "forearms"),
    (8, "lower back"),
    (9, "gluteal muscles"),
    (10, "upper legs"),
    (11, "lower legs")
]

DATABASE_TABLE_ENTRIES = {
    "measure_type": DATABASE_MEASURE_TYPE_ENTRIES,
    "category": DATABASE_CATEGORY_ENTRIES,
    "difficulty": DATABASE_DIFFICULTY_ENTRIES,
    "exercise": [],
    "workout": [],
    "muscle_group": DATABASE_MUSCLE_GROUP_ENTRIES,
    "exercise_muscle_group": [],
    "exe_exercise": [],
    "performance": [],
    "measure": [],
}
