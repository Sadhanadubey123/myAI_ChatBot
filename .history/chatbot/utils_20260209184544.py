import sqlite3
import requests
import json

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

def get_answer_from_db(question):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM knowledge_base WHERE question=?", (question,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def save_answer_to_db(question, answer):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO knowledge_base (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

def fetch_from_web(query):
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": "YOUR_BING_API_KEY"}  # Replace with your Bing API key
    params = {"q": query}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if "webPages" in data and "value" in data["webPages"]:
        return data["webPages"]["value"][0]["snippet"]
    return "Sorry, I couldn't find an answer."

def seed_db_from_json():
    """Optional: Pre-populate DB from data/knowledge.json"""
    try:
        with open("data/knowledge.json", "r", encoding="utf-8") as f:
            knowledge = json.load(f)
        for q, a in knowledge.items():
            save_answer_to_db(q, a)
    except Exception as e:
        print(f"Skipping DB seed: {e}")