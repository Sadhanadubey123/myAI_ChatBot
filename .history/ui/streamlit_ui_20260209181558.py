import streamlit as st
import requests

st.title("MDSO Chatbot")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_input("You:", "")

if st.button("Send") and user_input.strip():
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"message": user_input}
        )
        if response.status_code == 200:
            answer = response.json().get("response", "No response from backend.")
        else:
            answer = f"Error: Backend returned status {response.status_code}"
    except Exception as e:
        answer = f"Error connecting to backend: {e}"

    st.session_state["history"].append((user_input, answer))

for q, a in st.session_state["history"]:
    st.write(f"**You:** {q}")
    st.write(f"**Bot:** {a}")