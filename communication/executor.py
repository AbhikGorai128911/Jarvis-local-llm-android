from communication.parser import parse
from communication.contacts import find_contacts
from communication.caller import call, dial
from communication.whatsapp import send_message
from control.confirmation import confirm


def execute(user_input):

    parsed = parse(user_input)

    if not parsed["success"]:
        return parsed

    matches = find_contacts(parsed["contact"])

    if len(matches) == 0:
        return {
            "success": False,
            "message": "No contact found."
        }

    #
    # Multiple matches
    #
    if len(matches) > 1:

        print("\nJARVIS > Multiple contacts found:\n")

        for i, contact in enumerate(matches, 1):
            print(f"{i}. {contact['name']} ({contact['number']})")

        choice = input(
            f"\nChoose contact (1-{len(matches)}, Enter=1): "
        ).strip()

        if choice == "":
            index = 0

        else:
            try:
                index = int(choice) - 1

            except ValueError:
                return {
                    "success": False,
                    "message": "Invalid selection."
                }

            if index < 0 or index >= len(matches):
                return {
                    "success": False,
                    "message": "Invalid selection."
                }

        contact = matches[index]

    else:

        contact = matches[0]

    name = contact["name"]
    number = contact["number"]

    if parsed["action"] == "call":

        return confirm(
            f"Call {name} ({number})? (Y/n)",
            lambda: call(number)
        )

    if parsed["action"] == "message":
        print("DEBUG PARSED:", parsed)
        message = parsed["message"]

    return confirm(
        f"Send WhatsApp to {name} ({number})?\nMessage: {message}",
        lambda: send_message(number, message)
    )


    return {
        "success": False,
        "message": "Unknown communication action."
    }
