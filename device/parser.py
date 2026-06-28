# device/parser.py

VALID_ACTIONS = {
    "torch": ["on", "off"],
    "wifi": ["on", "off"],
    "bluetooth": ["on", "off"],
    "volume": ["set", "get"],
    "brightness": ["set", "get"],
    "battery": ["get"]
}


def parse(normalized):

    action = normalized.get("action")
    target = normalized.get("target")

    if not action or not target:
        return {
            "success": False,
            "message": "Could not understand device command"
        }

    # enforce rules
    if target in VALID_ACTIONS:
        if action not in VALID_ACTIONS[target]:
            return {
                "success": False,
                "message": f"Invalid action '{action}' for {target}"
            }

    value = None

    # optional value extraction
    import re
    match = re.search(r"\b\d+\b", normalized.get("raw", ""))

    if match:
        value = int(match.group())

    return {
        "success": True,
        "action": action,
        "target": target,
        "value": value
    }
