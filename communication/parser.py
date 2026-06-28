def parse(user_input):

    text = user_input.lower().strip()

    if text.startswith("call "):

        return {
            "success": True,
            "action": "call",
            "contact": text[5:].strip()
        }

    if text.startswith("dial "):

        return {
            "success": True,
            "action": "dial",
            "contact": text[5:].strip()
        }

    if text.startswith("message "):

        parts = text.split(" ", 2)

        if len(parts) < 3:
            return {
                "success": False,
                "message": "Usage: message <contact> <text>"
            }

        return {
            "success": True,
            "action": "message",
            "contact": parts[1],
            "message": parts[2]
        }

    return {
        "success": False,
        "message": "Communication command not recognized."
    }
