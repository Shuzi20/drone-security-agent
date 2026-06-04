import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "qwen/qwen3-32b"

def generate_daily_summary(frame_history, alert_history, patterns):
    # Prepare data
    total_frames = len(frame_history)
    total_alerts = len(alert_history)

    from collections import Counter
    severity_counts = Counter([a["severity"] for a in alert_history])
    location_counts = Counter([f["location"] for f in frame_history])
    most_active = location_counts.most_common(1)[0][0] if location_counts else "N/A"

    frames_text = "\n".join([
        f"- Frame {f['frame_id']} | {f['time']} | {f['location']}: {f['description'][:100]}"
        for f in frame_history
    ])

    alerts_text = "\n".join([
        f"- {a['severity']}: {a['message']}"
        for a in alert_history
    ])

    patterns_text = "\n".join(patterns) if patterns else "No patterns detected."

    prompt = f"""You are a drone security analyst. Generate a comprehensive daily surveillance report.

Frames analyzed today:
{frames_text}

Alerts triggered:
{alerts_text}

Patterns detected:
{patterns_text}

Generate a report with these exact sections:

DAILY SUMMARY:
- Total frames analyzed: {total_frames}
- Total alerts: {total_alerts}
- Critical alerts: {severity_counts.get('CRITICAL', 0)}
- High alerts: {severity_counts.get('HIGH', 0)}
- Medium alerts: {severity_counts.get('MEDIUM', 0)}
- Most active location: {most_active}

VIDEO SUMMARY:
<Write a 2-3 sentence natural language summary of everything that happened today>

KEY FINDINGS:
<List 3-4 most important observations>

RECOMMENDATIONS:
<List 2-3 security recommendations based on today's activity>
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    result = response.choices[0].message.content
    if "<think>" in result:
        result = result.split("</think>")[-1].strip()

    return result