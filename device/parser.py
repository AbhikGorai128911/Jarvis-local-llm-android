# device/parser.py

VALID = {
    "torch": ["on", "off"],
    "wifi": ["on", "off"],
    "bluetooth": ["on", "off"],
    "volume": ["set"],
    "brightness": ["set"],
    "battery": ["get"]
}


def parse(normalized):
    action = normalized.get("action")
    target = normalized.get("target")
    value = normalized.get("value")

    if not target:
        return {
            "success": False,
            "message": "No device detected"
        }

    if target in VALID:
        if action not in VALID[target]:
            return {
                "success": False,
                "message": f"Invalid action {action} for {target}"
            }

    return {
        "success": True,
        "action": action,
        "target": target,
        "value": value
    }
