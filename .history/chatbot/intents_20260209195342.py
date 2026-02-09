from chatbot.utils import get_answer_from_db, save_answer_to_db, fetch_from_web

def classify_intent(user_input: str) -> str:
    text = user_input.lower()
    if "mdso" in text:
        return "MDSO"
    elif "oss" in text and "bss" in text:
        return "OSS_BSS"
    elif "oss" in text:
        return "OSS"
    elif "bss" in text:
        return "BSS"
    elif "multi-domain" in text:
        return "MULTI_DOMAIN"
    elif "orchestration" in text:
        return "ORCHESTRATION"
    else:
        return "UNKNOWN"

def get_intent_response(user_input: str) -> str:
    intent = classify_intent(user_input)

    if intent == "MDSO":
        return "Blue Planet Multi-Domain Service Orchestration (MDSO) is Ciena's open software solution..."
    elif intent == "OSS_BSS":
        return "OSS manages network operations, BSS handles customer-facing processes..."
    elif intent == "OSS":
        return "OSS are tools for managing network operations..."
    elif intent == "BSS":
        return "BSS are tools for managing customer-facing processes..."
    elif intent == "MULTI_DOMAIN":
        return "Multi-Domain networking refers to managing and orchestrating across multiple domains..."
    elif intent == "ORCHESTRATION":
        return "Orchestration means automating the coordination of multiple systems..."
    else:
        # Fallback: DB first, then web, then save
        answer = get_answer_from_db(user_input)
        if answer:
            return answer
        answer = fetch_from_web(user_input)
        save_answer_to_db(user_input, answer)
        return answer