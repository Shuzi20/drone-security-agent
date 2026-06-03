import json
import os
from datetime import datetime

LOG_FILE = "storage/event_log.json"

def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

def log_event(frame_id, time, location, description, alert=None):
    init_log()
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    entry = {
        "frame_id": frame_id,
        "time": time,
        "location": location,
        "description": description,
        "alert": alert,
        "logged_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    logs.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"[LOG]   Frame {frame_id} | {time} | {location} — {description[:60]}...")