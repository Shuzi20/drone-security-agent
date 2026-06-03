def check_alerts(frame, telemetry, history):
    alerts = []
    time = frame["time"]
    description = frame["description"].lower()
    location = frame["location"]

    # Rule 1 — late night activity
    hour = int(time.split(":")[0])
    if hour >= 22 or hour < 6:
        alerts.append({
            "severity": "HIGH",
            "rule": "Late night activity",
            "message": f"Activity detected at {location} during late night hours ({time})"
        })

    # Rule 2 — loitering (same location 2+ times)
    same_location = [
        f for f in history
        if f["location"] == location and "person" in f["description"].lower()
    ]
    if len(same_location) >= 1 and "person" in description:
        alerts.append({
            "severity": "HIGH",
            "rule": "Loitering detected",
            "message": f"Person loitering at {location} — seen {len(same_location)+1} times"
        })

    # Rule 3 — repeated vehicle
    same_vehicle = [
        f for f in history
        if "truck" in f["description"].lower() or "vehicle" in f["description"].lower()
    ]
    if len(same_vehicle) >= 1 and ("truck" in description or "vehicle" in description):
        alerts.append({
            "severity": "MEDIUM",
            "rule": "Repeated vehicle",
            "message": f"Vehicle seen again at {location} — visit #{len(same_vehicle)+1} today"
        })

    # Rule 4 — gate tampering
    tamper_keywords = ["attempting", "opening", "breaking", "tampering", "forcing"]
    if any(word in description for word in tamper_keywords) and "gate" in description:
        alerts.append({
            "severity": "CRITICAL",
            "rule": "Gate tampering",
            "message": f"Possible gate breach attempt at {location} ({time})"
        })

    # Rule 5 — low battery
    if telemetry and telemetry.get("battery", 100) < 20:
        alerts.append({
            "severity": "LOW",
            "rule": "Low battery",
            "message": f"Drone battery at {telemetry['battery']}% — return to dock"
        })

    return alerts