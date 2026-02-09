import sqlite3
import requests
import json

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
    """Check if the answer exists in the local DB."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM knowledge_base WHERE question=?", (question,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def save_answer_to_db(question: str, answer: str):
    """Save a new Q&A pair into the DB."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO knowledge_base (question, answer) VALUES (?, ?)",
        (question, answer)
    )
    conn.commit()
    conn.close()

# -----------------------------
# Web Search Fallback (Bing API)
# -----------------------------
def fetch_from_web(query: str) -> str:
    """
    Fetch an answer from Bing Search API.
    Requires a valid API key from Azure Cognitive Services.
    """
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": "YOUR_BING_API_KEY"}  # Replace with your Bing API key
    params = {"q": query}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "webPages" in data and "value" in data["webPages"]:
            return data["webPages"]["value"][0]["snippet"]
        return "Sorry, I couldn't find an answer."
    except Exception as e:
        return f"Error fetching from web: {e}"

# -----------------------------
# Optional: Seed DB from JSON
# -----------------------------
def seed_db_from_json():
    """
    Pre-populate DB from data/knowledge.json if available.
    This avoids starting with an empty DB.
    """
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