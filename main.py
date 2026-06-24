from urllib import response
from llm.local_llm import ask
from core.network import is_online
from core.router import route_command
from core.tts import speak
from core.logger import log
from memory.memory import initialize
from memory.memory import save_message
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

    print("[SYSTEM] READY")

    speak("Jarvis ready for command")

def main():

    boot()

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
            print("JARVIS > Shutting down.")
            break


        if user_input.lower() == "yes":

            action = get_pending()

            if action:

                response = action()

                clear_pending()

                print(
                f"JARVIS > {response['message']}"
                )

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
