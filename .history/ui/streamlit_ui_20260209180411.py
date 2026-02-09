import streamlit as st
import requests

st.set_page_config(page_title="MDSO Chatbot", layout="centered")
st.title("🤖 MDSO Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Input box
user_input = st.text_input("You:", "")

if st.button("Send"):
    response = requests.post("http://127.0.0.1:8000/chat", json={"message": user_input})
    st.write("Response:", response.json()["response"])

if st.button("Send") and user_input.strip():
    try:
        # Call your Flask chatbot backend
        response = requests.post("http://127.0.0.1:8000/chat",
                                 json={"message": user_input})
        bot_reply = response.json()

        # Extract reply cleanly
        if "reply" in bot_reply:
            bot_text = bot_reply["reply"]
        elif "message" in bot_reply:
            bot_text = bot_reply["message"]
        else:
            bot_text = str(bot_reply)

        # Save conversation
        st.session_state["messages"].append(("You", user_input))
        st.session_state["messages"].append(("Response", bot_text))

    except requests.exceptions.ConnectionError:
        st.error("!! Backend not running. Please start app.py before using the UI.")

# Display chat history
for sender, msg in st.session_state["messages"]:
    if sender == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Response:** {msg}")