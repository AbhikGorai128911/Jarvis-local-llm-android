# device/normalize.py
import re

ACTION_MAP = {
    "on": ["on", "enable", "turn on", "switch on", "activate", "start", "increase", "up", "louder"],
    "off": ["off", "disable", "turn off", "switch off", "deactivate", "stop", "mute"],
    "set": ["set", "change", "adjust"]
}

TARGET_MAP = {
    "torch": ["torch", "flash", "flashlight", "light"],
    "wifi": ["wifi", "wi-fi", "internet", "network"],
    "bluetooth": ["bluetooth", "bt"],
    "volume": ["volume", "sound", "audio"],
    "brightness": ["brightness", "screen"],
    "battery": ["battery", "power"]
}


def _match(text, words):
    return any(w in text for w in words)


def normalize(text: str):
    text = text.lower().strip()

    action = None
    target = None
    value = None

    # extract number FIRST (important for volume/brightness)
    match = re.search(r"\b(\d{1,3})\b", text)
    if match:
        value = int(match.group(1))

    # detect target
    for t, aliases in TARGET_MAP.items():
        if _match(text, aliases):
            target = t
            break

    # detect action
    for a, aliases in ACTION_MAP.items():
        if _match(text, aliases):
            action = a
            break

    # SMART DEFAULTS
    if target == "volume":
        if value is not None:
            action = "set"
        elif action is None:
            action = "set"

    if target == "brightness":
        if value is not None:
            action = "set"
        elif action is None:
            action = "set"

    if target in ["wifi", "bluetooth", "torch"] and action is None:
        action = "on"

    if target == "battery":
        action = "get"

    return {
        "action": action,
        "target": target,
        "value": value,
        "raw": text
    }
