import json
import os

BASE_DIR = os.path.dirname(__file__)

settings_file = os.path.join(BASE_DIR, "settings_racer.json")
leaderboard_file = os.path.join(BASE_DIR, "leaderboard.json")

default_settings = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal"
}

def load_json(filename, default):
    if not os.path.exists(filename):
        save_json(filename, default)
        return default

    with open(filename, "r") as file:
        return json.load(file)

def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def load_settings():
    return load_json(settings_file, default_settings)

def save_settings(settings):
    save_json(settings_file, settings)

def load_leaderboard():
    return load_json(leaderboard_file, [])

def save_score(name, score, distance):
    leaderboard = load_leaderboard()

    leaderboard.append({
        "name": name,
        "score": score,
        "distance": int(distance)
    })

    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]

    save_json(leaderboard_file, leaderboard)