from pathlib import Path

APPLICATION_NAME = "Workouts Tracking"
INSTALL_DIR = Path(__file__).resolve().parent.parent
TESTS_DIR = INSTALL_DIR / "tests"
CODE_DIR = INSTALL_DIR / "workouts_tracking"

DATABASE_MEASURE_TYPE = "measure_type"
DATABASE_WORKOUT = "workout"
DATABASE_CATEGORY = "category"
DATABASE_DIFFICULTY = "difficulty"
DATABASE_EXERCISE = "exercise"
DATABASE_MUSCLE_GROUP = "muscle_group"
DATABASE_EXERCISE_MUSCLE_GROUP = "exercise_muscle_group"
DATABASE_EXE_EXERCISE = "exe_exercise"
DATABASE_PERFORMANCE = "performance"
DATABASE_MEASURE = "measure"

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
    DATABASE_MEASURE_TYPE: DATABASE_MEASURE_TYPE_COLUMNS,
    DATABASE_CATEGORY: DATABASE_CATEGORY_COLUMNS,
    DATABASE_DIFFICULTY: DATABASE_DIFFICULTY_COLUMNS,
    DATABASE_MUSCLE_GROUP: DATABASE_MUSCLE_GROUP_COLUMNS,
    DATABASE_WORKOUT: DATABASE_WORKOUT_COLUMNS,
    DATABASE_EXERCISE: DATABASE_EXERCISE_COLUMNS,
    DATABASE_EXERCISE_MUSCLE_GROUP: DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS,
    DATABASE_EXE_EXERCISE: DATABASE_EXE_EXERCISE_COLUMNS,
    DATABASE_MEASURE: DATABASE_MEASURE_COLUMNS,
    DATABASE_PERFORMANCE: DATABASE_PERFORMANCE_COLUMNS,
}

DATABASE_TABLES_DICTIONARY = {
    # dictionary of the name of the tables and its specification for sqlite3
    # ("name": ["column_name type", "primary key (id)"])
    DATABASE_MEASURE_TYPE: [f"{DATABASE_MEASURE_TYPE_COLUMNS[0]} integer not null",
                            f"{DATABASE_MEASURE_TYPE_COLUMNS[1]} text",
                            f"{DATABASE_MEASURE_TYPE_COLUMNS[2]} text",
                            f"primary key ({DATABASE_MEASURE_TYPE_COLUMNS[0]})",
                            ],
    DATABASE_CATEGORY: [f"{DATABASE_CATEGORY_COLUMNS[0]} integer not null",
                        f"{DATABASE_CATEGORY_COLUMNS[1]} text",
                        f"primary key ({DATABASE_CATEGORY_COLUMNS[0]})",
                        ],
    DATABASE_DIFFICULTY: [f"{DATABASE_DIFFICULTY_COLUMNS[0]} integer not null",
                          f"{DATABASE_DIFFICULTY_COLUMNS[1]} text",
                          f"primary key ({DATABASE_DIFFICULTY_COLUMNS[0]})",
                          ],
    DATABASE_WORKOUT: [f"{DATABASE_WORKOUT_COLUMNS[0]} integer not null",
                       f"{DATABASE_WORKOUT_COLUMNS[1]} text",
                       f"{DATABASE_WORKOUT_COLUMNS[2]} text",
                       f"{DATABASE_WORKOUT_COLUMNS[3]} text",
                       f"{DATABASE_WORKOUT_COLUMNS[4]} text",
                       f"primary key ({DATABASE_WORKOUT_COLUMNS[0]})",
                       ],
    DATABASE_EXERCISE: [f"{DATABASE_EXERCISE_COLUMNS[0]} integer not null",
                        f"{DATABASE_EXERCISE_COLUMNS[1]} text",
                        f"{DATABASE_EXERCISE_COLUMNS[2]} text",
                        f"{DATABASE_EXERCISE_COLUMNS[3]} text",
                        f"{DATABASE_EXERCISE_COLUMNS[4]} integer",
                        f"{DATABASE_EXERCISE_COLUMNS[5]} integer",
                        f"primary key ({DATABASE_EXERCISE_COLUMNS[0]})",
                        f"foreign key ({DATABASE_EXERCISE_COLUMNS[4]}) "
                        f"references {DATABASE_CATEGORY}({DATABASE_CATEGORY_COLUMNS[0]})",
                        f"foreign key ({DATABASE_EXERCISE_COLUMNS[5]}) "
                        f"references {DATABASE_DIFFICULTY}({DATABASE_CATEGORY_COLUMNS[0]})",
                        ],
    DATABASE_MUSCLE_GROUP: [f"{DATABASE_MUSCLE_GROUP_COLUMNS[0]} integer not null",
                            f"{DATABASE_MUSCLE_GROUP_COLUMNS[1]} text",
                            f"primary key ({DATABASE_MUSCLE_GROUP_COLUMNS[0]})",
                            ],
    DATABASE_EXERCISE_MUSCLE_GROUP: [
        f"{DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS[0]} integer not null",
        f"{DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS[1]} integer not null",
        f"primary key ({DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS[0]}, "
        f"{DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS[1]})",
        f"foreign key ({DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS[0]}) "
        f"references {DATABASE_EXERCISE}({DATABASE_EXERCISE_COLUMNS[0]})",
        f"foreign key ({DATABASE_EXERCISE_MUSCLE_GROUP_COLUMNS[1]}) "
        f"references {DATABASE_MUSCLE_GROUP}({DATABASE_MUSCLE_GROUP_COLUMNS[0]})",
        ],
    DATABASE_EXE_EXERCISE: [f"{DATABASE_EXE_EXERCISE_COLUMNS[0]} integer not null",
                            f"{DATABASE_EXE_EXERCISE_COLUMNS[1]} integer not null",
                            f"{DATABASE_EXE_EXERCISE_COLUMNS[2]} integer",
                            f"{DATABASE_EXE_EXERCISE_COLUMNS[3]} text",
                            f"primary key ({DATABASE_EXE_EXERCISE_COLUMNS[0]}, "
                            f"{DATABASE_EXE_EXERCISE_COLUMNS[1]})",
                            f"foreign key ({DATABASE_EXE_EXERCISE_COLUMNS[0]}) "
                            f"references {DATABASE_WORKOUT}({DATABASE_WORKOUT_COLUMNS[0]})",
                            f"foreign key ({DATABASE_EXE_EXERCISE_COLUMNS[2]}) "
                            f"references {DATABASE_EXERCISE}({DATABASE_EXERCISE_COLUMNS[0]})",
                            ],
    DATABASE_MEASURE: [f"{DATABASE_MEASURE_COLUMNS[0]} integer not null",
                       f"{DATABASE_MEASURE_COLUMNS[1]} text",
                       f"{DATABASE_MEASURE_COLUMNS[2]} integer",
                       f"{DATABASE_MEASURE_COLUMNS[3]} integer "
                       f"check ({DATABASE_MEASURE_COLUMNS[3]} = 0 or "
                       f"{DATABASE_MEASURE_COLUMNS[3]} = 1)",
                       f"{DATABASE_MEASURE_COLUMNS[4]} integer",
                       f"primary key ({DATABASE_MEASURE_COLUMNS[0]})",
                       f"foreign key ({DATABASE_MEASURE_COLUMNS[2]}) "
                       f"references {DATABASE_MEASURE_TYPE}({DATABASE_MEASURE_TYPE_COLUMNS[0]})",
                       f"foreign key ({DATABASE_MEASURE_COLUMNS[4]}) "
                       f"references {DATABASE_EXERCISE}({DATABASE_EXERCISE_COLUMNS[0]})",
                       ],
    DATABASE_PERFORMANCE: [f"{DATABASE_PERFORMANCE_COLUMNS[0]} integer not null",
                           f"{DATABASE_PERFORMANCE_COLUMNS[1]} integer not null",
                           f"{DATABASE_PERFORMANCE_COLUMNS[2]} integer not null",
                           f"{DATABASE_PERFORMANCE_COLUMNS[3]} text",
                           f"primary key ({DATABASE_PERFORMANCE_COLUMNS[0]}, "
                           f"{DATABASE_PERFORMANCE_COLUMNS[1]}, {DATABASE_PERFORMANCE_COLUMNS[2]})",
                           f"foreign key ({DATABASE_PERFORMANCE_COLUMNS[0]}) "
                           f"references {DATABASE_WORKOUT}({DATABASE_WORKOUT_COLUMNS[0]})",
                           f"foreign key ({DATABASE_PERFORMANCE_COLUMNS[1]}) "
                           f"references {DATABASE_EXE_EXERCISE}({DATABASE_EXE_EXERCISE_COLUMNS[1]})",
                           f"foreign key ({DATABASE_PERFORMANCE_COLUMNS[2]}) "
                           f"references {DATABASE_MEASURE}({DATABASE_MEASURE_COLUMNS[0]})",
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
    DATABASE_MEASURE_TYPE: DATABASE_MEASURE_TYPE_ENTRIES,
    DATABASE_CATEGORY: DATABASE_CATEGORY_ENTRIES,
    DATABASE_DIFFICULTY: DATABASE_DIFFICULTY_ENTRIES,
    DATABASE_EXERCISE: [],
    DATABASE_WORKOUT: [],
    DATABASE_MUSCLE_GROUP: DATABASE_MUSCLE_GROUP_ENTRIES,
    DATABASE_EXERCISE_MUSCLE_GROUP: [],
    DATABASE_EXE_EXERCISE: [],
    DATABASE_PERFORMANCE: [],
    DATABASE_MEASURE: [],
}
