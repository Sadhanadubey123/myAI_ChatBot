import sqlite3
import json
from duckduckgo_search import DDGS
import wikipedia

DB_FILE = "chatbot.db"

# -----------------------------
# Database Setup
# -----------------------------
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

def get_answer_from_db(question: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM knowledge_base WHERE question=?", (question,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def save_answer_to_db(question: str, answer: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO knowledge_base (question, answer) VALUES (?, ?)",
        (question, answer)
    )
    conn.commit()
    conn.close()

# -----------------------------
# Web Search Fallback (DuckDuckGo + Wikipedia)
# -----------------------------
def fetch_from_web(query: str) -> str:
    """
    Try DuckDuckGo first. If no snippet found, fallback to Wikipedia.
    """
    try:
        # DuckDuckGo search
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                return results[0]["body"]

        # Wikipedia fallback
        try:
            return wikipedia.summary(query, sentences=2)
        except Exception:
            return "No answer found."
    except Exception as e:
        return f"Web search error: {e}"

# -----------------------------
# Optional: Seed DB from JSON
# -----------------------------
def seed_db_from_json():
    try:
        with open("data/knowledge.json", "r", encoding="utf-8") as f:
            knowledge = json.load(f)
        for q, a in knowledge.items():
            save_answer_to_db(q, a)
        print("Database seeded from knowledge.json")
    except FileNotFoundError:
        print("No knowledge.json found, skipping seed.")
    except Exception as e:
        print(f"Skipping DB seed due to error: {e}")