import streamlit as st
import requests

st.title("MDSO Chatbot")

# Keep chat history in session state
if "history" not in st.session_state:
    st.session_state["history"] = []

# Input box for user query
user_input = st.text_input("You:", "")

# Send query when button is clicked
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

    # Save to chat history
    st.session_state["history"].append((user_input, answer))

# Display chat history
for q, a in st.session_state["history"]:
    st.write(f"**You:** {q}")
    st.write(f"**Response:** {a}")