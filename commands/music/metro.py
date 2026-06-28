# commands/music/metro.py

import subprocess


def open_and_search(query):

    subprocess.run([
        "am", "start",
        "-n", "com.metro.player/.MainActivity",
        "--es", "query", query
    ])

    return {
        "success": True,
        "message": f"Searching Metro for: {query}"
    }


def control(action):

    mapping = {
        "play": "play",
        "pause": "pause",
        "next": "next",
        "previous": "previous"
    }

    cmd = mapping.get(action)

    if not cmd:
        return {"success": False, "message": "Unsupported Metro action"}

    subprocess.run(["playerctl", cmd])

    return {
        "success": True,
        "message": f"Metro {action}"
    }
