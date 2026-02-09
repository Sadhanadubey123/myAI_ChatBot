import streamlit as st
import requests

st.title("MDSO Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:")

if st.button("Send") and user_input.strip():
    try:
        res = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"message": user_input}
        )
        data = res.json()
        answer = data.get("response", "No response.")
    except Exception as e:
        answer = f"Backend error: {e}"

    st.session_state.history.append((user_input, answer))

st.write("### Conversation")
for q, a in st.session_state.history:
    st.write(f"**You:** {q}")
    st.write(f"**Bot:** {a}")
