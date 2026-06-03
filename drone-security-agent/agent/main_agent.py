import json
from groq import Groq
from agent.alert_engine import check_alerts
from agent.context_manager import ContextManager
from storage.db_handler import init_db, insert_frame, search_frames
from storage.event_logger import log_event
from storage.vector_store import add_frame, semantic_search
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"
context = ContextManager()

def analyze_frame(frame, telemetry):
    history_summary = context.get_history_summary()
    false_positive_warning = context.get_false_positives()

    prompt = f"""You are a drone security analyst AI. Analyze this surveillance frame and provide:
1. Objects detected (people, vehicles, etc.)
2. Activity summary in one sentence
3. Threat level: NONE / LOW / MEDIUM / HIGH / CRITICAL

Recent history:
{history_summary}

{false_positive_warning}

Current frame:
- Frame ID   : {frame['frame_id']}
- Time       : {frame['time']}
- Location   : {frame['location']}
- Description: {frame['description']}
- Telemetry  : Battery {telemetry['battery']}%, Altitude {telemetry['altitude']}m

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
    print(f"[LLM]   Objects: {objects}")
    print(f"[LLM]   Summary: {summary}")
    print(f"[LLM]   Threat : {threat}")

    # Step 2 — Rule-based alerts
    alerts = check_alerts(frame, telemetry, context.frame_history)
    for alert in alerts:
        print(f"[ALERT] {alert['severity']} — {alert['message']}")

    # Step 3 — Store in SQLite
    insert_frame(
        frame_id=frame["frame_id"],
        time=frame["time"],
        location=frame["location"],
        description=frame["description"],
        objects=objects,
        alert_level=threat
    )

    # Step 4 — Store in ChromaDB
    add_frame(
        frame_id=frame["frame_id"],
        description=frame["description"],
        metadata={
            "time": frame["time"],
            "location": frame["location"],
            "threat": threat
        }
    )

    # Step 5 — Log event
    alert_msg = alerts[0]["message"] if alerts else None
    log_event(frame["frame_id"], frame["time"], frame["location"], summary, alert=alert_msg)

    # Step 6 — Update context memory
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

    print("\n" + "="*60)
    print("   ALL FRAMES PROCESSED")
    print("="*60)

    # Bonus — Q&A session
    print("\nQ&A Mode — Ask anything about today's surveillance.")
    print("Type 'exit' to quit.\n")
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
        print(f"\n[AGENT] {response.choices[0].message.content}\n")

if __name__ == "__main__":
    run_agent()