import sqlite3

DB_FILE = "storage/frames.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS frames (
            frame_id    INTEGER PRIMARY KEY,
            time        TEXT,
            location    TEXT,
            description TEXT,
            objects     TEXT,
            alert_level TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("[DB]    Database initialized.")

def insert_frame(frame_id, time, location, description, objects="", alert_level="NONE"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO frames
        (frame_id, time, location, description, objects, alert_level)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (frame_id, time, location, description, objects, alert_level))
    conn.commit()
    conn.close()
    print(f"[INDEX] Frame {frame_id} indexed — objects: {objects}, alert: {alert_level}")

def search_frames(keyword):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT frame_id, time, location, description, objects, alert_level
        FROM frames
        WHERE description LIKE ? OR objects LIKE ? OR location LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_frames():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM frames ORDER BY time")
    results = cursor.fetchall()
    conn.close()
    return results