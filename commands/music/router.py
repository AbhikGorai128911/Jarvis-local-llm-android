# commands/music/router.py

from commands.music.parser import parse
from commands.music.fallback import spotify, ytmusic, download
from commands.music.player import play_song, control
from commands.music.fallback import spotify, ytmusic, download
import subprocess

def execute(user_input):

    parsed = parse(user_input)
    print(parsed)
    if not parsed["success"]:
        return parsed

    action = parsed["action"]

    # -------------------
    # PLAY SONG
    # -------------------
    if action == "play_song":

        query = parsed["query"]

        result = play_song(query)

        # fallback decision
        if result["success"]:
            return result

        print("\nSong not found locally.")

        choice = input(
            "1. Spotify\n"
            "2. YouTube Music\n"
            "3. Paste link\n"
            "4. Cancel\n"
            "Choose: "
        ).strip()

        if choice == "1":
            return spotify(query)

        if choice == "2":
            return ytmusic(query)

        if choice == "3":
            link = input("Paste link: ").strip()
            return download(link)

        return {
            "success": False,
            "message": "Cancelled."
        }

    # -------------------
    # CONTROLS
    # -------------------
    if action in ["pause", "resume", "next", "previous"]:
        return control(action)

    if action == "volume_up":
        subprocess.run(["playerctl", "volume", "0.1+"])
        return {"success": True, "message": "Volume up"}

    if action == "volume_down":
        subprocess.run(["playerctl", "volume", "0.1-"])
        return {"success": True, "message": "Volume down"}
    
    if action == "play_song":
        print("INSIDE PLAY_SONG BLOCK")

        query = parsed["query"]
        result = play_song(query)


    return {
        "success": False,
        "message": "Unhandled action"
    }
