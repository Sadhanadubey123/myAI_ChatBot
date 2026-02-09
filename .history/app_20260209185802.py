from flask import Flask, request, jsonify
from chatbot.intents import get_intent_response
from chatbot.utils import init_db, seed_db_from_json

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    answer = get_intent_response(user_input)
    return jsonify({"response": answer})

if __name__ == "__main__":
    init_db()
    seed_db_from_json()  # optional: load initial knowledge.json
    app.run(port=8000)