import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.alert_engine import check_alerts

# Frame 1 — person at Main Gate 00:01
frame1 = {"frame_id": 1, "time": "00:01", "location": "Main Gate",
          "description": "A person in dark clothing is standing near the main gate looking around suspiciously."}

# Frame 2 — truck at Garage 00:03
frame2 = {"frame_id": 2, "time": "00:03", "location": "Garage",
          "description": "A blue Ford F150 truck has entered the garage area and parked."}

# Frame 3 — same person at Main Gate 00:05
frame3 = {"frame_id": 3, "time": "00:05", "location": "Main Gate",
          "description": "The same person in dark clothing is still loitering near the main gate."}

# Frame 4 — truck again at Garage 12:00
frame4 = {"frame_id": 4, "time": "12:00", "location": "Garage",
          "description": "The blue Ford F150 truck is seen again at the garage."}

# Frame 5 — normal activity Backyard 14:30
frame5 = {"frame_id": 5, "time": "14:30", "location": "Backyard",
          "description": "Two people are having a normal conversation near the backyard fence."}

# Frame 6 — gate breach 23:58
frame6 = {"frame_id": 6, "time": "23:58", "location": "Main Gate",
          "description": "An unknown person is attempting to open the main gate at night."}

telemetry_normal = {"battery": 80, "altitude": 15}
telemetry_low    = {"battery": 15, "altitude": 10}

def test_late_night_alert_frame1():
    alerts = check_alerts(frame1, telemetry_normal, [])
    rules = [a["rule"] for a in alerts]
    assert "Late night activity" in rules
    print("PASS — test_late_night_alert_frame1")

def test_late_night_alert_frame6():
    alerts = check_alerts(frame6, telemetry_normal, [])
    rules = [a["rule"] for a in alerts]
    assert "Late night activity" in rules
    print("PASS — test_late_night_alert_frame6")

def test_no_late_night_alert_daytime():
    alerts = check_alerts(frame5, telemetry_normal, [])
    rules = [a["rule"] for a in alerts]
    assert "Late night activity" not in rules
    print("PASS — test_no_late_night_alert_daytime")

def test_loitering_detected_frame3():
    # frame1 already in history — same person same location
    alerts = check_alerts(frame3, telemetry_normal, [frame1])
    rules = [a["rule"] for a in alerts]
    assert "Loitering detected" in rules
    print("PASS — test_loitering_detected_frame3")

def test_no_loitering_first_occurrence():
    # frame1 is first occurrence — no history yet
    alerts = check_alerts(frame1, telemetry_normal, [])
    rules = [a["rule"] for a in alerts]
    assert "Loitering detected" not in rules
    print("PASS — test_no_loitering_first_occurrence")

def test_repeated_vehicle_frame4():
    # frame2 already in history
    alerts = check_alerts(frame4, telemetry_normal, [frame2])
    rules = [a["rule"] for a in alerts]
    assert "Repeated vehicle" in rules
    print("PASS — test_repeated_vehicle_frame4")

def test_no_repeated_vehicle_first_visit():
    alerts = check_alerts(frame2, telemetry_normal, [])
    rules = [a["rule"] for a in alerts]
    assert "Repeated vehicle" not in rules
    print("PASS — test_no_repeated_vehicle_first_visit")

def test_gate_tampering_frame6():
    alerts = check_alerts(frame6, telemetry_normal, [])
    rules = [a["rule"] for a in alerts]
    assert "Gate tampering" in rules
    severities = [a["severity"] for a in alerts if a["rule"] == "Gate tampering"]
    assert severities[0] == "CRITICAL"
    print("PASS — test_gate_tampering_frame6")

def test_no_gate_tampering_normal_frame():
    alerts = check_alerts(frame5, telemetry_normal, [])
    rules = [a["rule"] for a in alerts]
    assert "Gate tampering" not in rules
    print("PASS — test_no_gate_tampering_normal_frame")

def test_low_battery_alert():
    alerts = check_alerts(frame5, telemetry_low, [])
    rules = [a["rule"] for a in alerts]
    assert "Low battery" in rules
    print("PASS — test_low_battery_alert")

def test_no_low_battery_normal_level():
    alerts = check_alerts(frame1, telemetry_normal, [])
    rules = [a["rule"] for a in alerts]
    assert "Low battery" not in rules
    print("PASS — test_no_low_battery_normal_level")

def test_multiple_alerts_frame6():
    # Frame 6 should trigger late night + gate tampering at minimum
    alerts = check_alerts(frame6, telemetry_normal, [frame1, frame3])
    rules = [a["rule"] for a in alerts]
    assert "Late night activity" in rules
    assert "Gate tampering" in rules
    assert len(alerts) >= 2
    print("PASS — test_multiple_alerts_frame6")

if __name__ == "__main__":
    test_late_night_alert_frame1()
    test_late_night_alert_frame6()
    test_no_late_night_alert_daytime()
    test_loitering_detected_frame3()
    test_no_loitering_first_occurrence()
    test_repeated_vehicle_frame4()
    test_no_repeated_vehicle_first_visit()
    test_gate_tampering_frame6()
    test_no_gate_tampering_normal_frame()
    test_low_battery_alert()
    test_no_low_battery_normal_level()
    test_multiple_alerts_frame6()
    print("\nAll alert tests passed!")