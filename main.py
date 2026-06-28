from urllib import response
from llm.local_llm import ask
from core.network import is_online
from core.router import route_command
from core.tts import speak
from core.logger import log
from memory.memory import initialize
from memory.memory import save_message
from llm.local_llm import ask as ask_dynamic
from llm.persistent_llm import start_llm, stop_llm, ask_persistent
from control.confirmation import handle_confirmation
from control.pending_actions import clear_pending
from control.pending_actions import (
    get_pending,
    clear_pending
)

def boot():
    print("=" * 40)
    print("JARVIS V1 INITIALIZING")
    print("=" * 40)

    if is_online():
        print("[NETWORK] ONLINE")
    else:
        print("[NETWORK] OFFLINE")

    choice = input(
        "[AI] Enable persistent LLM mode? (Y/n): "
    ).strip().lower()

    persistent_ai = choice not in ["n", "no"]

    print("[SYSTEM] READY")

    speak("Jarvis ready for command")

    return persistent_ai

def main():

    persistent_ai = boot()

    initialize()

    while True:

        user_input = input("\nYou > ").strip()
        log(f"USER: {user_input}")

        save_message(
            "USER",
            user_input
        )
        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            
            if persistent_ai:
                # stop_llm() will be added later
                pass

            print("JARVIS > Shutting down.")
            break


        
        if user_input.lower() in ["", "y", "yes"]:

                response = handle_confirmation()

                if response["success"]:
                     print(f"JARVIS > {response['message']}")
                else:
                     print(f"JARVIS > {response['message']}")

                continue

        if user_input.lower() in ["n", "no"]:
             clear_pending()
             print("JARVIS > Cancelled.")

             continue




        response = route_command(user_input)
        


        if response.get("llm_candidate"):

            choice = input(
                "JARVIS > Use local model? (Y/n): "
            ).strip().lower()

            if choice in ["y", "yes", ""]:

                message = ask(user_input)

                #print(f"\nJARVIS > {message}")

                speak(message)

                log(f"JARVIS: {message}")

                save_message(
                    "JARVIS",
                    message
                )

            continue




        log(
        f"JARVIS: {response['message']}"
        )

        #print(f"JARVIS > {response['message']}")
        speak(response["message"])



        save_message(
            "JARVIS",
            response["message"]
        )

if __name__ == "__main__":
    main()
