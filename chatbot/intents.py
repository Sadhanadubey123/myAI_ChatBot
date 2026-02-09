from chatbot.utils import get_answer_from_db, save_answer_to_db, fetch_from_web

def classify_intent(user_input: str) -> str:
    text = user_input.lower()
    if "mdso" in text:
        return "mdso"
    elif "oss" in text and "bss" in text:
        return "oss bss"
    elif "oss" in text:
        return "oss"
    elif "bss" in text:
        return "bss"
    elif "multi-domain" in text:
        return "multi-domain orchestration"
    elif "orchestration" in text:
        return "orchestration"
    else:
        return user_input  # fallback = raw query

def get_intent_response(user_input: str) -> str:
    intent = classify_intent(user_input)
    key = intent.lower().strip()

    # Use DB first for known intents
    answer = get_answer_from_db(key)
    if answer:
        return answer

    # Otherwise, fetch from Wikipedia
    answer = fetch_from_web(user_input)
    if answer:
        save_answer_to_db(key, answer)
        return answer

    return f"Sorry, I couldn't find an answer for '{user_input}'."
