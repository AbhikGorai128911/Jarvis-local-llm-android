import subprocess


def run_playerctl(command):

    try:

        subprocess.run(
            ["playerctl"] + command,
            check=True
        )

        return True

    except Exception:
        return False
    
def get_current_song():

    import subprocess

    try:
        result = subprocess.run(
            ["playerctl", "metadata", "--format",
             "{{artist}} - {{title}}"],
            capture_output=True,
            text=True
        )

        return result.stdout.strip()

    except Exception:
        return None


def execute(user_input):

    text = user_input.lower()

    if "play music" in text or text == "play":

        if run_playerctl(["play"]):

            return {
                "success": True,
                "message": "Playing music"
            }

    if "pause" in text:

        if run_playerctl(["pause"]):

            return {
                "success": True,
                "message": "Pausing music"
            }

    if "next" in text:

        if run_playerctl(["next"]):

            return {
                "success": True,
                "message": "Skipping to next track"
            }

    if "previous" in text:

        if run_playerctl(["previous"]):

            return {
                "success": True,
                "message": "Going to previous track"
            }

    if "volume up" in text:

        subprocess.run(
            ["playerctl", "volume", "0.1+"]
        )

        return {
            "success": True,
            "message": "Increasing volume"
        }

    if "volume down" in text:

        subprocess.run(
            ["playerctl", "volume", "0.1-"]
        )

        return {
            "success": True,
            "message": "Decreasing volume"
        }

    return {
        "success": False,
        "message": "Music command not recognized"
    }