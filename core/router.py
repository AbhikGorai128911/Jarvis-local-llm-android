from llm.local_llm import ask
from reasoning.intent_classifier import classify
from reasoning.decision_engine import should_execute
from control.executor import execute


def route_command(user_input):

    intent = classify(user_input)

    print(f"DEBUG: Intent = {intent}")

    if not should_execute(intent):
        return {
            "success": False,
            "message": "I don't understand that command yet."
        }
    
    if intent == "unknown":
        ask(user_input)
        return {
            "success": True,
            "message": ""
        }

    return execute(intent, user_input)