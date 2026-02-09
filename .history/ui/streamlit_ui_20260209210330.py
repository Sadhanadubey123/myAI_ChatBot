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
            backend_json = response.json()
            answer = backend_json.get("response", "No response from backend.")
            # Debug line so you can see the raw backend payload
            st.write("### Debug Output")
            st.json(backend_json)
        else:
            answer = f"Error: Backend returned status {response.status_code}"
    except Exception as e:
        answer = f"Error connecting to backend: {e}"

    st.session_state["history"].append((user_input, answer))

# Display chat history with source highlighting
st.write("### Conversation History")
for q, a in st.session_state["history"]:
    st.write(f"**You:** {q}")
    if "(DuckDuckGo)" in a:
        st.write(f"**Response (DuckDuckGo):** {a}")
    elif "(Wikipedia)" in a:
        st.write(f"**Response (Wikipedia):** {a}")
    else:
        st.write(f"**Response:** {a}")