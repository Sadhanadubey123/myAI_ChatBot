import sqlite3
import requests

def init_db():
    conn = sqlite3.connect("chatbot.db")
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
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM knowledge_base WHERE question=?", (question,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def save_answer_to_db(question, answer):
    conn = sqlite3.connect("chatbot.db")
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