def execute(command):

    text = command.lower()

    action = None

    if any(word in text for word in [
        "turn on",
        "enable",
        "start"
    ]):
        action = "on"

    elif any(word in text for word in [
        "turn off",
        "disable",
        "stop"
    ]):
        action = "off"

    target = None

    if "bluetooth" in text or "bt" in text:
        target = "bluetooth"

    elif "wifi" in text:
        target = "wifi"

    elif "mobile data" in text:
        target = "mobile_data"

    elif "hotspot" in text:
        target = "hotspot"

    elif "airplane mode" in text:
        target = "airplane_mode"

    if action is None:
        return {
            "success": False,
            "message": "No action detected."
        }

    if target is None:
        return {
            "success": False,
            "message": "No device detected."
        }

    return {
        "success": True,
        "message": f"Detected: {action} {target}"
    }
