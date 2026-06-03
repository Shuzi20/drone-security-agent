import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.alert_engine import check_alerts

def test_late_night_alert():
    frame = {"frame_id": 1, "time": "23:58", "location": "Main Gate", "description": "Person seen at gate"}
    telemetry = {"battery": 80}
    alerts = check_alerts(frame, telemetry, [])
    assert any(a["rule"] == "Late night activity" for a in alerts)
    print("PASS — test_late_night_alert")

def test_no_alert_daytime():
    frame = {"frame_id": 2, "time": "14:30", "location": "Backyard", "description": "Two people talking"}
    telemetry = {"battery": 80}
    alerts = check_alerts(frame, telemetry, [])
    late_night = [a for a in alerts if a["rule"] == "Late night activity"]
    assert len(late_night) == 0
    print("PASS — test_no_alert_daytime")

def test_loitering_alert():
    history = [{"frame_id": 1, "time": "00:01", "location": "Main Gate", "description": "Person standing near gate"}]
    frame = {"frame_id": 3, "time": "00:05", "location": "Main Gate", "description": "Same person still at gate"}
    telemetry = {"battery": 80}
    alerts = check_alerts(frame, telemetry, history)
    assert any(a["rule"] == "Loitering detected" for a in alerts)
    print("PASS — test_loitering_alert")

def test_gate_tampering_alert():
    frame = {"frame_id": 6, "time": "23:58", "location": "Main Gate", "description": "Person attempting to open the gate forcefully"}
    telemetry = {"battery": 80}
    alerts = check_alerts(frame, telemetry, [])
    assert any(a["rule"] == "Gate tampering" for a in alerts)
    print("PASS — test_gate_tampering_alert")

def test_low_battery_alert():
    frame = {"frame_id": 5, "time": "10:00", "location": "Rooftop", "description": "All clear"}
    telemetry = {"battery": 15}
    alerts = check_alerts(frame, telemetry, [])
    assert any(a["rule"] == "Low battery" for a in alerts)
    print("PASS — test_low_battery_alert")

if __name__ == "__main__":
    test_late_night_alert()
    test_no_alert_daytime()
    test_loitering_alert()
    test_gate_tampering_alert()
    test_low_battery_alert()
    print("\nAll alert tests passed!")