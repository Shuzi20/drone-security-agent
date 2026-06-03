import streamlit as st
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage.db_handler import get_all_frames, search_frames, init_db

st.set_page_config(
    page_title="Drone Security Dashboard",
    page_icon="🚁",
    layout="wide"
)

st.title("🚁 Drone Security Analyst Dashboard")
st.markdown("---")

init_db()

# Sidebar
st.sidebar.title("Search & Filter")
search_query = st.sidebar.text_input("Search frames", placeholder="e.g. truck, person, gate")
filter_alert = st.sidebar.selectbox(
    "Filter by alert level",
    ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW", "NONE"]
)

# Load event log
LOG_FILE = "storage/event_log.json"
alerts_today = []
if os.path.exists(LOG_FILE):
    with open(LOG_FILE) as f:
        logs = json.load(f)
    alerts_today = [l for l in logs if l.get("alert")]

# Top metrics
col1, col2, col3, col4 = st.columns(4)
all_frames = get_all_frames()

col1.metric("Total Frames", len(all_frames))
col2.metric("Alerts Today", len(alerts_today))
critical = len([f for f in all_frames if f[5] == "CRITICAL"])
col3.metric("Critical Events", critical)
high = len([f for f in all_frames if f[5] == "HIGH"])
col4.metric("High Severity", high)

st.markdown("---")

# Alerts section
if alerts_today:
    st.subheader("🚨 Active Alerts")
    for alert in alerts_today:
        severity_color = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }
        with st.expander(f"{alert['time']} — {alert['location']} — {alert['alert']}"):
            st.write(f"**Frame ID:** {alert['frame_id']}")
            st.write(f"**Time:** {alert['time']}")
            st.write(f"**Location:** {alert['location']}")
            st.write(f"**Description:** {alert['description']}")
            st.write(f"**Alert:** {alert['alert']}")

st.markdown("---")

# Frame index table
st.subheader("📋 Frame Index")

if search_query:
    frames = search_frames(search_query)
    st.info(f"Search results for: '{search_query}'")
else:
    frames = all_frames

if filter_alert != "ALL":
    frames = [f for f in frames if f[5] == filter_alert]

if frames:
    st.table({
        "Frame ID"   : [f[0] for f in frames],
        "Time"       : [f[1] for f in frames],
        "Location"   : [f[2] for f in frames],
        "Objects"    : [f[4] for f in frames],
        "Alert Level": [f[5] for f in frames],
    })
else:
    st.warning("No frames found.")

st.markdown("---")

# Q&A section
st.subheader("💬 Ask the Agent")
st.caption("Ask questions about today's surveillance activity")

question = st.text_input("Your question", placeholder="e.g. How many times did the truck appear?")

if st.button("Ask") and question:
    results = search_frames(question)
    if results:
        st.success("Relevant frames found:")
        for r in results[:3]:
            st.write(f"- Frame {r[0]} | {r[1]} | {r[2]}: {r[3][:100]}...")
    else:
        st.warning("No relevant frames found for this query.")