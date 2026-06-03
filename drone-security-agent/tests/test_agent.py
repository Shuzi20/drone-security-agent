import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.main_agent import parse_llm_response
from agent.context_manager import ContextManager

def test_parse_llm_response_normal():
    raw = "OBJECTS: person, truck\nSUMMARY: A person near gate\nTHREAT: HIGH"
    objects, summary, threat = parse_llm_response(raw)
    assert objects == "person, truck"
    assert summary == "A person near gate"
    assert threat == "HIGH"
    print("PASS — test_parse_llm_response_normal")

def test_parse_llm_response_with_think_tags():
    raw = "<think>thinking...</think>\nOBJECTS: car\nSUMMARY: Car at garage\nTHREAT: LOW"
    objects, summary, threat = parse_llm_response(raw)
    assert objects == "car"
    assert threat == "LOW"
    print("PASS — test_parse_llm_response_with_think_tags")

def test_context_manager_history():
    ctx = ContextManager()
    ctx.add_frame({"frame_id": 1, "time": "00:01", "location": "Gate", "description": "Person seen"})
    ctx.add_frame({"frame_id": 2, "time": "00:03", "location": "Garage", "description": "Truck seen"})
    summary = ctx.get_history_summary()
    assert "Frame 1" in summary
    assert "Frame 2" in summary
    print("PASS — test_context_manager_history")

def test_context_manager_feedback():
    ctx = ContextManager()
    ctx.add_feedback(1, "Late night activity", False)
    warning = ctx.get_false_positives()
    assert "Late night activity" in warning
    print("PASS — test_context_manager_feedback")

if __name__ == "__main__":
    test_parse_llm_response_normal()
    test_parse_llm_response_with_think_tags()
    test_context_manager_history()
    test_context_manager_feedback()
    print("\nAll agent tests passed!")