import sqlite3
import json
from ddgs import DDGS
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

def fetch_from_web(query: str) -> str:
    try:
        print(f"[DEBUG] Fetching for query: {query}")

        # DuckDuckGo search with context
        with DDGS() as ddgs:
            results = list(ddgs.text(query + " definition", max_results=3))
            print(f"[DEBUG] DuckDuckGo results: {results}")
            if results:
                return f"(DuckDuckGo) {results[0]['body']}"

        # Wikipedia fallback
        search_results = wikipedia.search(query)
        print(f"[DEBUG] Wikipedia search results: {search_results}")
        if search_results:
            try:
                summary = wikipedia.summary(search_results[0], sentences=2)
                return f"(Wikipedia) {summary}"
            except wikipedia.exceptions.DisambiguationError as e:
                print(f"[DEBUG] Wikipedia disambiguation options: {e.options}")
                return f"(Wikipedia) {wikipedia.summary(e.options[0], sentences=2)}"

        return "No answer found."
    except Exception as e:
        print(f"[DEBUG] Error in fetch_from_web: {e}")
        return f"Web search error: {e}"

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