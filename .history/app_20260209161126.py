import json
from flask import Flask, request, jsonify
from chatbot.intents import IntentClassifier
from chatbot.mdso_client import call_mdso_api

app = Flask(__name__)

# Load training data from JSON
with open("data/training_data.json", "r", encoding="utf-8") as f:
    training_data = json.load(f)

# Load knowledge base
with open("data/knowledge.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

classifier = IntentClassifier()
classifier.train(training_data)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    intent = classifier.predict(user_input)

    if intent == "provision":
        response = call_mdso_api("provision", {"name": "Test Service"})
    elif intent == "status":
        response = call_mdso_api("status", {"service_id": "svc_1"})
    elif intent == "optimize":
        response = call_mdso_api("optimize", {"service_id": "svc_1", "bandwidth": "5Gbps"})
    elif intent == "knowledge":
        response = {"reply": knowledge_base.get("MDSO", "I don’t have information on that yet.")}
    else:
        response = {"reply": "Sorry, I didn’t understand."}

    return jsonify(response)

if __name__ == "__main__":
    app.run(port=8000, debug=True)