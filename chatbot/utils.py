import sqlite3
import json
import wikipedia

DB_FILE = "chatbot.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            question TEXT PRIMARY KEY,
            answer TEXT
        )
    """)
    conn.commit()
    conn.close()

def normalize(text: str) -> str:
    return text.lower().strip()

def get_answer_from_db(question: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT answer FROM knowledge_base WHERE question=?",
        (normalize(question),)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def save_answer_to_db(question: str, answer: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO knowledge_base (question, answer) VALUES (?, ?)",
        (normalize(question), answer)
    )
    conn.commit()
    conn.close()

def fetch_from_web(query: str) -> str:
    """Fetch answer from Wikipedia only."""
    try:
        search_results = wikipedia.search(query)
        if search_results:
            try:
                summary = wikipedia.summary(search_results[0], sentences=2)
                return f"(Wikipedia) {summary}"
            except wikipedia.exceptions.DisambiguationError as e:
                summary = wikipedia.summary(e.options[0], sentences=2)
                return f"(Wikipedia) {summary}"
        return "No answer found on Wikipedia."
    except Exception as e:
        return f"Wikipedia search error: {e}"

def seed_db_from_json():
    try:
        with open("data/knowledge.json", "r", encoding="utf-8") as f:
            knowledge = json.load(f)
        for q, a in knowledge.items():
            save_answer_to_db(q, a)
        print("Database seeded from knowledge.json")
    except Exception as e:
        print(f"Skipping DB seed: {e}")
