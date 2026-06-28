def parse(text: str):

    text = text.lower().strip()

    # --------------------
    # PLAY SONG
    # --------------------
    if text.startswith("play song "):
        return {
            "success": True,
            "action": "play_song",
            "query": text[len("play song "):].strip()
        }

    if text.startswith("play music "):
        return {
            "success": True,
            "action": "play_song",
            "query": text[len("play music "):].strip()
        }

    if text.startswith("play "):
        return {
            "success": True,
            "action": "play_song",
            "query": text[5:].strip()
        }

    # --------------------
    # CONTROL (flexible matching)
    # --------------------
    if "pause" in text:
        return {"success": True, "action": "pause"}

    if "resume" in text or text == "play":
        return {"success": True, "action": "resume"}

    if "next" in text:
        return {"success": True, "action": "next"}

    if "previous" in text or "back" in text:
        return {"success": True, "action": "previous"}

    if "stop" in text:
        return {"success": True, "action": "stop"}

    # --------------------
    # VOLUME (fix your issue)
    # --------------------
    if "volume up" in text or text == "volume up":
        return {"success": True, "action": "volume_up"}

    if "volume down" in text or text == "volume down":
        return {"success": True, "action": "volume_down"}

    if text.startswith("volume "):
        # optional numeric volume support later
        return {"success": True, "action": "volume_set", "value": text}

    return {
        "success": False,
        "message": "Unknown music command."
    }
