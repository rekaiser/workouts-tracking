from pathlib import Path

APPLICATION_NAME = "Workouts Tracking"
INSTALL_DIR = Path(__file__).resolve().parent.parent
TESTS_DIR = INSTALL_DIR / "tests"
CODE_DIR = INSTALL_DIR / "workouts_tracking"

DATABASE_TABLES = {
    # dictionary of the name of the tables and its columns
    # ("name": ["column_name type", "primary key (id)"])
    "measure_type": ["id integer", "primary key (id)"],
    "workout": ["id integer"],
    "category": ["id integer"],
    "difficulty": ["id integer"],
    "exercise": ["id integer", "name text"],
    "muscle_group": ["id integer"],
    "exercise_muscle_group": ["id integer"],
    "exe_exercise": ["id integer"],
    "performance": ["id integer"],
    "measure": ["id integer"],
}
