import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.risk_scorer import calculate_risk_score

frame_night_gate = {"frame_id": 1, "time": "00:01", "location": "Main Gate",
                    "description": "A person in dark clothing looking around suspiciously"}

frame_day_backyard = {"frame_id": 5, "time": "14:30", "location": "Backyard",
                      "description": "Two people having a normal conversation"}

frame_tampering = {"frame_id": 6, "time": "23:58", "location": "Main Gate",
                   "description": "Unknown person attempting to open the main gate"}

frame_garage_night = {"frame_id": 2, "time": "00:03", "location": "Garage",
                      "description": "A blue Ford F150 truck has entered the garage"}

telemetry_normal = {"battery": 80}
telemetry_low    = {"battery": 15}

def test_night_gate_suspicious_high_score():
    score, reasons = calculate_risk_score(frame_night_gate, telemetry_normal, [])
    assert score >= 50
    assert "Night time" in reasons
    assert "Gate location" in reasons
    print(f"PASS — test_night_gate_suspicious_high_score | Score: {score}")

def test_daytime_normal_zero_score():
    score, reasons = calculate_risk_score(frame_day_backyard, telemetry_normal, [])
    assert score == 0
    print(f"PASS — test_daytime_normal_zero_score | Score: {score}")

def test_tampering_gets_high_score():
    score, reasons = calculate_risk_score(frame_tampering, telemetry_normal, [])
    assert score >= 70
    assert "Tampering detected" in reasons
    print(f"PASS — test_tampering_gets_high_score | Score: {score}")

def test_score_capped_at_100():
    high_alerts = [
        {"severity": "CRITICAL"},
        {"severity": "HIGH"},
        {"severity": "HIGH"},
        {"severity": "MEDIUM"},
    ]
    score, _ = calculate_risk_score(frame_tampering, telemetry_normal, high_alerts)
    assert score <= 100
    print(f"PASS — test_score_capped_at_100 | Score: {score}")

def test_low_battery_adds_to_score():
    score_normal, _ = calculate_risk_score(frame_garage_night, telemetry_normal, [])
    score_low, _    = calculate_risk_score(frame_garage_night, telemetry_low, [])
    assert score_low > score_normal
    print(f"PASS — test_low_battery_adds_to_score | Normal: {score_normal}, Low battery: {score_low}")

def test_garage_night_medium_score():
    score, reasons = calculate_risk_score(frame_garage_night, telemetry_normal, [])
    assert score > 0
    assert "Night time" in reasons
    print(f"PASS — test_garage_night_medium_score | Score: {score}")

def test_alert_severity_increases_score():
    no_alert_score, _       = calculate_risk_score(frame_night_gate, telemetry_normal, [])
    critical_alert_score, _ = calculate_risk_score(frame_night_gate, telemetry_normal,
                                                    [{"severity": "CRITICAL"}])
    assert critical_alert_score > no_alert_score
    print(f"PASS — test_alert_severity_increases_score | No alert: {no_alert_score}, Critical: {critical_alert_score}")

if __name__ == "__main__":
    test_night_gate_suspicious_high_score()
    test_daytime_normal_zero_score()
    test_tampering_gets_high_score()
    test_score_capped_at_100()
    test_low_battery_adds_to_score()
    test_garage_night_medium_score()
    test_alert_severity_increases_score()
    print("\nAll risk scorer tests passed!")