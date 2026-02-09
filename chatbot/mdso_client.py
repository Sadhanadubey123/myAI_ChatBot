import requests

BASE_URL = "http://127.0.0.1:5000"

def call_mdso_api(action, payload=None):
    if action == "provision":
        return requests.post(f"{BASE_URL}/provision", json=payload).json()
    elif action == "status":
        return requests.get(f"{BASE_URL}/status", params=payload).json()
    elif action == "optimize":
        return requests.post(f"{BASE_URL}/optimize", json=payload).json()
    return {"error": "Unknown action"}