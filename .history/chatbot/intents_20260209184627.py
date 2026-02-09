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
        return (
            "Blue Planet Multi-Domain Service Orchestration (MDSO) is Ciena's open "
            "software solution that automates end-to-end service design and activation "
            "across physical and virtual domains. It enables intent-based networking, "
            "integrates with OSS/BSS systems, and supports advanced use cases like "
            "5G slicing, SD-WAN, and cloud migration."
        )
    elif intent == "OSS_BSS":
        return (
            "OSS (Operations Support Systems) manage network operations, provisioning, "
            "and monitoring. BSS (Business Support Systems) handle customer-facing "
            "processes such as billing, orders, and revenue. Together, OSS/BSS form the "
            "backbone of telecom operations."
        )
    elif intent == "OSS":
        return (
            "OSS (Operations Support Systems) are tools for managing network operations, "
            "including provisioning, monitoring, and fault management."
        )
    elif intent == "BSS":
        return (
            "BSS (Business Support Systems) are tools for managing customer-facing "
            "processes such as billing, CRM, and revenue management."
        )
    elif intent == "MULTI_DOMAIN":
        return (
            "Multi-Domain networking refers to managing and orchestrating across multiple "
            "network domains such as WAN, LAN, cloud, and security. It enables unified "
            "policies, automation, and end-to-end service delivery."
        )
    elif intent == "ORCHESTRATION":
        return (
            "Orchestration in networking means automating the coordination of multiple "
            "systems, applications, and services to deliver end-to-end functionality. "
            "It ensures that workflows and resources are managed consistently."
        )
    else:
        # Fallback: DB first, then web, then save
        answer = get_answer_from_db(user_input)
        if answer:
            return answer
        answer = fetch_from_web(user_input)
        save_answer_to_db(user_input, answer)
        return answer