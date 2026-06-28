# device/normalize.py
import re

ACTION_MAP = {
    "on": ["on", "enable", "turn on", "switch on", "activate", "start"],
    "off": ["off", "disable", "turn off", "switch off", "deactivate", "stop"],
    "set": ["set", "change", "adjust"],
    "get": ["what is", "check", "show", "status", "how much"]
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
    return any(re.search(rf"\b{re.escape(w)}\b", text) for w in words)


def normalize(text: str):

    text = text.lower().strip()

    action = None
    target = None

    # resolve target first (more stable)
    for t, aliases in TARGET_MAP.items():
        if _match(text, aliases):
            target = t
            break

    # resolve action
    for a, aliases in ACTION_MAP.items():
        if _match(text, aliases):
            action = a
            break

    # smart fallback rules
    if target == "battery":
        action = "get"

    if target in ["wifi", "bluetooth", "torch"] and action == "set":
        action = "on"

    return {
        "action": action,
        "target": target,
        "raw": text
    }
