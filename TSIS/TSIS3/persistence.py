import json

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

def save_score(name, score, coins, distance):
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []
    
    data.append({"name": name, "score": score, "coins": coins, "distance": distance})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_scores():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def load_settings():
    default = {"volume": 0.5, "car_color": "red", "difficulty": "Medium"}
    try:
        with open(SETTINGS_FILE, "r") as f:
            user_settings = json.load(f)
            for key in default:
                if key not in user_settings:
                    user_settings[key] = default[key]
            return user_settings
    except:
        return default

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)