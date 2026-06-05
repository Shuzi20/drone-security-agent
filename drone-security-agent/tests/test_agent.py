import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.main_agent import parse_llm_response
from agent.context_manager import ContextManager

def test_parse_normal_response():
    raw = "OBJECTS: person\nSUMMARY: A person in dark clothing near main gate\nTHREAT: MEDIUM"
    objects, summary, threat = parse_llm_response(raw)
    assert objects == "person"
    assert summary == "A person in dark clothing near main gate"
    assert threat == "MEDIUM"
    print("PASS — test_parse_normal_response")

def test_parse_multiple_objects():
    raw = "OBJECTS: person, main gate\nSUMMARY: Unknown person attempting to open gate\nTHREAT: HIGH"
    objects, summary, threat = parse_llm_response(raw)
    assert "person" in objects
    assert "main gate" in objects
    assert threat == "HIGH"
    print("PASS — test_parse_multiple_objects")

def test_parse_threat_none():
    raw = "OBJECTS: people\nSUMMARY: Two people having normal conversation\nTHREAT: NONE"
    objects, summary, threat = parse_llm_response(raw)
    assert threat == "NONE"
    print("PASS — test_parse_threat_none")

def test_context_stores_frames():
    ctx = ContextManager()
    frame1 = {"frame_id": 1, "time": "00:01", "location": "Main Gate", "description": "Person in dark clothing"}
    frame2 = {"frame_id": 2, "time": "00:03", "location": "Garage", "description": "Blue Ford F150 truck"}
    ctx.add_frame(frame1)
    ctx.add_frame(frame2)
    assert len(ctx.frame_history) == 2
    print("PASS — test_context_stores_frames")

def test_context_history_summary_content():
    ctx = ContextManager()
    ctx.add_frame({"frame_id": 1, "time": "00:01", "location": "Main Gate", "description": "Person loitering"})
    summary = ctx.get_history_summary()
    assert "Frame 1" in summary
    assert "Main Gate" in summary
    print("PASS — test_context_history_summary_content")

def test_context_empty_history():
    ctx = ContextManager()
    summary = ctx.get_history_summary()
    assert summary == "No previous frames."
    print("PASS — test_context_empty_history")

def test_context_stores_alerts():
    ctx = ContextManager()
    ctx.add_alert({"severity": "HIGH", "rule": "Late night activity", "message": "Activity at Main Gate"})
    assert len(ctx.alert_history) == 1
    assert ctx.alert_history[0]["severity"] == "HIGH"
    print("PASS — test_context_stores_alerts")

def test_context_history_max_five_frames():
    ctx = ContextManager()
    for i in range(7):
        ctx.add_frame({"frame_id": i, "time": "00:01", "location": "Gate", "description": f"Frame {i}"})
    summary = ctx.get_history_summary()
    # Only last 5 frames shown
    assert "Frame 2" not in summary
    assert "Frame 6" in summary
    print("PASS — test_context_history_max_five_frames")

if __name__ == "__main__":
    test_parse_normal_response()
    test_parse_multiple_objects()
    test_parse_threat_none()
    test_context_stores_frames()
    test_context_history_summary_content()
    test_context_empty_history()
    test_context_stores_alerts()
    test_context_history_max_five_frames()
    print("\nAll agent tests passed!")