import re


# Canonical names
ACTION_ALIASES = {
    "on": [
        "on",
        "enable",
        "start",
        "activate"
    ],

    "off": [
        "off",
        "disable",
        "stop",
        "deactivate"
    ],

    "set": [
        "set"
    ],

    "get": [
        "get",
        "show",
        "what",
        "check"
    ]
}


TARGET_ALIASES = {
    "torch": [
        "torch",
        "flashlight",
        "flash light"
    ],

    "wifi": [
        "wifi",
        "wi-fi"
    ],

    "bluetooth": [
        "bluetooth",
        "bt"
    ],

    "battery": [
        "battery",
        "battery percentage",
        "battery level"
    ],

    "volume": [
        "volume",
        "sound"
    ],

    "brightness": [
        "brightness",
        "diaplay",
        "screen"
    ],

    "hotspot": [
        "hotspot"
    ],

    "mobile_data": [
        "mobile data",
        "data"
    ]
}


def _find_action(text):

    for canonical, aliases in ACTION_ALIASES.items():
        for alias in aliases:
            if alias in text:
                return canonical

    return None


def _find_target(text):

    for canonical, aliases in TARGET_ALIASES.items():
        for alias in aliases:
            if alias in text:
                return canonical

    return None


def _find_value(text):

    match = re.search(r"\b\d+\b", text)

    if match:
        return int(match.group())

    return None


def parse(user_input):

    text = user_input.lower().strip()

    action = _find_action(text)
    target = _find_target(text)
    value = _find_value(text)

    # Default action for queries
    if action is None and target in [
        "battery",
        "volume"
    ]:
        action = "get"

    return {
        "action": action,
        "target": target,
        "value": value,
        "raw": user_input
    }
