from chatbot.utils import get_answer_from_db, save_answer_to_db, fetch_from_wikipedia

def get_intent_response(user_input: str) -> str:
    # 1. Check DB first (cache)
    answer = get_answer_from_db(user_input)
    if answer:
        return answer

    # 2. Fetch dynamically from Wikipedia
    answer = fetch_from_wikipedia(user_input)
    if answer:
        save_answer_to_db(user_input, answer)
        return answer

    return f"Sorry, could not find an answer for '{user_input}'."
