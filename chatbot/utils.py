import sqlite3
import json
import wikipedia

DB_FILE = "chatbot.db"

def init_db():
    """Initialize SQLite DB with knowledge_base table."""
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
    """Normalize text for consistent DB storage."""
    return text.lower().strip()

def get_answer_from_db(question: str):
    """Return answer from DB if exists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM knowledge_base WHERE question=?", (normalize(question),))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def save_answer_to_db(question: str, answer: str):
    """Save answer to DB (cache)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO knowledge_base (question, answer) VALUES (?, ?)",
        (normalize(question), answer)
    )
    conn.commit()
    conn.close()

def fetch_from_wikipedia(query: str) -> str:
    """Fetch answer from Wikipedia dynamically, handle disambiguation and page errors."""
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            return f"No results found on Wikipedia for '{query}'."

        # Try top 3 results
        for title in search_results[:3]:
            try:
                page = wikipedia.page(title)
                summary = page.summary
                if summary:
                    # Return first 3 sentences
                    sentences = '. '.join(summary.split('. ')[:3])
                    return f"(Wikipedia) {sentences}"
            except wikipedia.exceptions.DisambiguationError as e:
                # Pick first option from disambiguation list
                for option in e.options:
                    try:
                        page = wikipedia.page(option)
                        summary = page.summary
                        if summary:
                            sentences = '. '.join(summary.split('. ')[:3])
                            return f"(Wikipedia) {sentences}"
                    except Exception:
                        continue
            except wikipedia.exceptions.PageError:
                continue
        return f"No good summary found on Wikipedia for '{query}'."
    except Exception as e:
        return f"Wikipedia search error: {e}"

def seed_db_from_json():
    """Seed database from data/knowledge.json if exists."""
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
