CAPABILITIES = {
    # HARD EXECUTION (Termux API)
    "torch": {
        "type": "direct",
        "on": ["termux-torch", "on"],
        "off": ["termux-torch", "off"]
    },

    "volume": {
        "type": "direct",
        "command": "termux-volume"
    },

    "battery": {
        "type": "read",
        "command": "termux-battery-status"
    },

    "sensor": {
        "type": "stream",
        "command": "termux-sensor"
    },

    "contacts": {
        "type": "read",
        "command": "termux-contact-list"
    },

    # ANDROID INTENTS (UI CONTROL)
    "bluetooth": {
        "type": "intent",
        "action": "android.settings.BLUETOOTH_SETTINGS"
    },

    "wifi": {
        "type": "intent",
        "action": "android.settings.WIFI_SETTINGS"
    },

    "display": {
        "type": "intent",
        "action": "android.settings.DISPLAY_SETTINGS"
    },

    # NOT POSSIBLE DIRECTLY
    "mobile_data": {
        "type": "unsupported"
    },

    "dark_mode": {
        "type": "unsupported"
    }
}
