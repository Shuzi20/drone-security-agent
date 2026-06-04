def calculate_risk_score(frame, telemetry, alerts):
    score = 0
    reasons = []

    time = frame["time"]
    description = frame["description"].lower()
    location = frame["location"]
    hour = int(time.split(":")[0])

    # Time based
    if hour >= 22 or hour < 6:
        score += 30
        reasons.append("Night time")
    elif hour >= 18 or hour < 8:
        score += 10
        reasons.append("Evening/early morning")

    # Location based
    if "gate" in location.lower():
        score += 20
        reasons.append("Gate location")
    elif "garage" in location.lower():
        score += 10
        reasons.append("Garage location")

    # Description based
    if "loitering" in description or "suspicious" in description:
        score += 20
        reasons.append("Suspicious behavior")
    if "attempting" in description or "forcing" in description or "tampering" in description:
        score += 30
        reasons.append("Tampering detected")
    if "unknown" in description:
        score += 15
        reasons.append("Unknown person")
    if "dark clothing" in description:
        score += 10
        reasons.append("Dark clothing")

    # Alert based
    for alert in alerts:
        if alert["severity"] == "CRITICAL":
            score += 20
        elif alert["severity"] == "HIGH":
            score += 10
        elif alert["severity"] == "MEDIUM":
            score += 5

    # Battery based
    if telemetry and telemetry.get("battery", 100) < 20:
        score += 5
        reasons.append("Low battery")

    # Cap at 100
    score = min(score, 100)

    return score, " + ".join(reasons)