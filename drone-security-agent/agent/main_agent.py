import json
import os
from groq import Groq
from agent.alert_engine import check_alerts
from agent.context_manager import ContextManager
from agent.risk_scorer import calculate_risk_score
from agent.summarizer import generate_daily_summary
from storage.db_handler import init_db, insert_frame, search_frames
from storage.event_logger import log_event
from storage.vector_store import add_frame, semantic_search
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "qwen/qwen3-32b"
context = ContextManager()

def analyze_frame(frame, telemetry):
    history_summary = context.get_history_summary()

    prompt = f"""You are a drone security analyst AI. Analyze this surveillance frame and provide:
1. Objects detected (people, vehicles, etc.)
2. Activity summary in one sentence
3. Threat level: NONE / LOW / MEDIUM / HIGH / CRITICAL

Recent history:
{history_summary}

Current frame:
- Frame ID   : {frame['frame_id']}
- Time       : {frame['time']}
- Location   : {frame['location']}
- Description: {frame['description']}
- Telemetry  : Battery {telemetry.get('battery', 'N/A')}%, Altitude {telemetry.get('altitude', 'N/A')}m

Respond in this exact format:
OBJECTS: <comma separated list>
SUMMARY: <one sentence>
THREAT: <NONE/LOW/MEDIUM/HIGH/CRITICAL>
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

def parse_llm_response(response_text):
    if "<think>" in response_text:
        response_text = response_text.split("</think>")[-1].strip()

    objects = ""
    summary = ""
    threat = "NONE"
    for line in response_text.strip().split("\n"):
        if line.startswith("OBJECTS:"):
            objects = line.replace("OBJECTS:", "").strip()
        elif line.startswith("SUMMARY:"):
            summary = line.replace("SUMMARY:", "").strip()
        elif line.startswith("THREAT:"):
            threat = line.replace("THREAT:", "").strip()
    return objects, summary, threat

def process_frame(frame, telemetry):
    print(f"\n{'='*60}")
    print(f"Processing Frame {frame['frame_id']} | {frame['time']} | {frame['location']}")
    print(f"{'='*60}")

    # Step 1 — LLM analysis
    llm_response = analyze_frame(frame, telemetry)
    objects, summary, threat = parse_llm_response(llm_response)
    print(f"[LLM]   Objects : {objects}")
    print(f"[LLM]   Summary : {summary}")
    print(f"[LLM]   Threat  : {threat}")

    # Step 2 — Rule-based alerts
    alerts = check_alerts(frame, telemetry, context.frame_history)
    for alert in alerts:
        print(f"[ALERT] {alert['severity']} — {alert['message']}")

    # Step 3 — Risk Score
    risk_score, risk_reasons = calculate_risk_score(frame, telemetry, alerts)
    print(f"[RISK]  Frame {frame['frame_id']} | Score: {risk_score}/100 | Reason: {risk_reasons}")

    # Step 4 — Pattern Detection
    patterns = context.get_patterns()
    for pattern in patterns:
        print(pattern)

    # Step 5 — Store in SQLite
    insert_frame(
        frame_id=frame["frame_id"],
        time=frame["time"],
        location=frame["location"],
        description=frame["description"],
        objects=objects,
        alert_level=threat
    )

    # Step 6 — Store in ChromaDB
    add_frame(
        frame_id=frame["frame_id"],
        description=frame["description"],
        metadata={
            "time": frame["time"],
            "location": frame["location"],
            "threat": threat,
            "risk_score": str(risk_score)
        }
    )

    # Step 7 — Log event
    alert_msg = alerts[0]["message"] if alerts else None
    log_event(frame["frame_id"], frame["time"], frame["location"], summary, alert=alert_msg)

    # Step 8 — Update context memory
    context.add_frame(frame)
    for alert in alerts:
        context.add_alert(alert)

def run_agent():
    print("\n" + "="*60)
    print("   DRONE SECURITY ANALYST AGENT — STARTING")
    print("="*60)

    init_db()

    with open("data/frames.json") as f:
        frames = json.load(f)
    with open("data/telemetry.json") as f:
        telemetry_data = json.load(f)

    telemetry_map = {t["time"]: t for t in telemetry_data}

    for frame in frames:
        telemetry = telemetry_map.get(frame["time"], {})
        process_frame(frame, telemetry)

    # Daily Summary + Text Summary
    print("\n" + "="*60)
    print("   ALL FRAMES PROCESSED — GENERATING REPORT")
    print("="*60)

    patterns = context.get_patterns()
    report = generate_daily_summary(
        context.frame_history,
        context.alert_history,
        patterns
    )
    print("\n" + report)

    # Save report to file
    with open("storage/daily_report.txt", "w") as f:
        f.write(report)
    print("\n[REPORT] Saved to storage/daily_report.txt")

    # Q&A session
    print("\n" + "="*60)
    print("Q&A Mode — Ask anything about today's surveillance.")
    print("Type 'exit' to quit.")
    print("="*60 + "\n")

    while True:
        query = input("Your question: ").strip()
        if query.lower() == "exit":
            break
        results = semantic_search(query)
        context_text = "\n".join(results["documents"][0]) if results["documents"] else "No data found."
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{
                "role": "user",
                "content": f"Based on today's surveillance data:\n{context_text}\n\nAnswer this question: {query}"
            }]
        )
        result = response.choices[0].message.content
        if "<think>" in result:
            result = result.split("</think>")[-1].strip()
        print(f"\n[AGENT] {result}\n")

if __name__ == "__main__":
    run_agent()