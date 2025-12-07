from flower import WORKOUT_FILE


import json
import os


def load_workouts():
    if os.path.exists(WORKOUT_FILE):
        with open(WORKOUT_FILE, "r") as f:
            return json.load(f)
    return {}