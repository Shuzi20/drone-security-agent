# Drone Security Analyst Agent

A prototype AI-powered drone security system that processes simulated telemetry data and video frames in real-time to detect security events, generate alerts, and provide intelligent surveillance analysis.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Running Tests](#running-tests)
- [AI Tools Used](#ai-tools-used)
- [Design Decisions](#design-decisions)
- [Assumptions](#assumptions)

---

## Overview

The Drone Security Analyst Agent is designed for a docked drone that monitors a fixed property daily. It processes simulated video frame descriptions and GPS telemetry data to:

- Identify objects and activities such as vehicles and persons
- Log events with location and time context
- Generate real-time security alerts based on predefined rules
- Index frames in a searchable database
- Produce a daily surveillance summary and recommendations

---

## Features

**Core Features**

- Frame-by-frame video analysis using a Large Language Model via Groq API
- Rule-based alert engine with 5 predefined security rules
- Real-time risk scoring per frame (0-100)
- Pattern detection across frames (loitering, repeated vehicles, high-risk zones)
- Frame indexing in SQLite for structured queries
- Semantic search using ChromaDB and sentence-transformers
- Event logging in JSON format
- Daily summary report with key findings and recommendations
- Interactive Q&A interface to query surveillance data
- Streamlit dashboard for visual monitoring

**Bonus Features**

- Video summarization — 2-3 sentence natural language summary of the day
- Follow-up Q&A — agent answers questions about today's activity

---

## Architecture

```
+------------------------------------------------------------------+
|  INPUT LAYER                                                      |
|  frames.json          telemetry.json          rules.json          |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|  PROCESSING LAYER                                                 |
|                                                                   |
|   VLM Processor    Alert Engine    Risk Scorer    Summarizer      |
|                                                                   |
|          Context Manager (memory across all frames)               |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|  STORAGE LAYER                                                    |
|   SQLite               ChromaDB              Event Log (JSON)     |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|  OUTPUT LAYER                                                     |
|   Console Logs       Streamlit Dashboard      Q&A Interface       |
+------------------------------------------------------------------+
...
```

---

## Tech Stack

| Component | Tool | Reason |
|-----------|------|--------|
| LLM | Groq API — Qwen3-32B | Free tier, fast inference, strong reasoning |
| Agent Framework | LangChain | Industry standard for AI agents |
| Structured Storage | SQLite | Built-in Python, no setup required |
| Semantic Search | ChromaDB | Free, local vector database |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) | Free, runs locally |
| Dashboard | Streamlit | Rapid Python-based UI |
| Language | Python 3.10+ | Assignment requirement |

---

## Project Structure

```
drone-security-agent/
|
|-- data/
|   |-- frames.json              # Simulated video frame descriptions
|   |-- telemetry.json           # GPS, altitude, timestamp data
|   |-- rules.json               # Alert trigger rules
|
|-- agent/
|   |-- main_agent.py            # Core agent — orchestrates all components
|   |-- vlm_processor.py         # Frame analysis using Groq LLM
|   |-- alert_engine.py          # Rule-based alert logic
|   |-- context_manager.py       # Conversation memory and history
|   |-- risk_scorer.py           # Per-frame risk scoring
|   |-- summarizer.py            # Daily report and video summary generation
|
|-- storage/
|   |-- db_handler.py            # SQLite frame indexing
|   |-- vector_store.py          # ChromaDB semantic search
|   |-- event_logger.py          # JSON event log writer
|
|-- dashboard/
|   |-- app.py                   # Streamlit dashboard
|
|-- notifications/
|   |-- telegram_bot.py          # Telegram alert (future enhancement)
|
|-- tests/
|   |-- test_agent.py            # Agent reasoning and parsing tests
|   |-- test_alerts.py           # Alert trigger rule tests
|   |-- test_indexing.py         # Frame indexing and search tests
|
|-- main.py                      # Entry point
|-- requirements.txt             # Dependencies
|-- .env                         # API keys (not committed)
|-- .gitignore
|-- README.md
...
```
---

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Groq API key — free at https://console.groq.com

### Step 1 — Clone the repository

```bash
git clone https://github.com/your-username/drone-security-agent.git
cd drone-security-agent
```

### Step 2 — Create and activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment variables

Create a `.env` file in the root directory:
GROQ_API_KEY=your_groq_api_key_here

---

## Running the Project

### Run the agent

```bash
python main.py
```

This will:
1. Process all 6 simulated frames
2. Generate LLM analysis, alerts, risk scores, and patterns for each frame
3. Index all frames in SQLite and ChromaDB
4. Save event log to `storage/event_log.json`
5. Generate daily report to `storage/daily_report.txt`
6. Open Q&A mode for follow-up questions

### Run the dashboard

```bash
streamlit run dashboard/app.py
```

Open `http://localhost:8501` in your browser.

Note: Run `python main.py` before the dashboard so that data is available.

---

## Running Tests

```bash
python tests/test_agent.py
python tests/test_alerts.py
python tests/test_indexing.py
```

### Test coverage

**test_agent.py**
- LLM response parsing with normal output
- LLM response parsing with DeepSeek think tags
- Context manager history tracking
- Context manager feedback logging

**test_alerts.py**
- Late night activity alert triggers correctly
- No alert fires for daytime normal activity
- Loitering alert triggers on repeated person at same location
- Gate tampering alert triggers on breach keywords
- Low battery alert triggers below 20 percent

**test_indexing.py**
- Frame inserts and retrieves correctly from SQLite
- Keyword search returns correct results
- Search for non-existent keyword returns empty list

---

## AI Tools Used

**Claude (Anthropic)**
- Used throughout development for architecture design, code generation, and debugging
- Generated initial boilerplate for LangChain agent, alert engine, and Streamlit dashboard
- All generated code was reviewed, customized, and integrated manually

**Groq API — Qwen3-32B**
- Powers the core LLM analysis of each surveillance frame
- Used for daily summary generation and Q&A responses

**Impact on workflow**
- Reduced development time significantly for repetitive components
- Enabled rapid iteration on prompt design for frame analysis
- Architecture decisions were validated through AI-assisted reasoning

---

## Design Decisions

**Why simulated text frames instead of real video**
The assignment specifies simulation. Text descriptions allow controlled testing of all alert rules and edge cases without hardware dependency.

**Why Groq API instead of local model**
Groq provides free, fast inference without requiring GPU hardware. Qwen3-32B was chosen as it is a production model on Groq with strong reasoning capabilities, distinct from Llama-based models used in prior projects.

**Why SQLite + ChromaDB together**
SQLite handles structured queries such as filtering by time, location, or alert level. ChromaDB handles semantic queries such as "show all suspicious activity" where exact keyword matching is insufficient. Both are free and require no external server.

**Why Streamlit for dashboard**
Streamlit allows rapid UI development in pure Python without requiring a separate frontend framework. Appropriate for a prototype submission.

**Why rule-based alerts alongside LLM**
LLM threat assessment can be inconsistent across runs. Rule-based alerts provide deterministic, auditable triggers that always fire under defined conditions regardless of LLM output.

---

## Assumptions

- Video frames are represented as text descriptions simulating what a drone camera would capture
- Telemetry data is matched to frames by timestamp
- "Late night" is defined as 22:00 to 06:00
- A vehicle appearing 2 or more times in the same day is flagged as a repeated vehicle event
- A person at the same location across 2 or more frames is flagged as loitering
- Gate tampering is detected through keyword matching in frame descriptions
- Battery below 20 percent triggers a low battery alert
- The Groq free tier rate limits are sufficient for the 6-frame prototype demonstration