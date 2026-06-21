import subprocess
import webbrowser
from datetime import datetime


APPS = {
    "firefox": "firefox",
    "terminal": "xfce4-terminal",
    "files": "thunar",
    "file manager": "thunar",
    "calculator": "galculator",
    "vlc": "vlc",
    "code": "code",
    "vscode": "code",
}


def normalize(text):

    text = text.lower().strip()

    replacements = {
        "fire fox": "firefox",
        "vs code": "vscode",
        "visual studio code": "vscode",
        "file explorer": "files",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def open_app(app_name):

    try:

        subprocess.Popen(
            [APPS[app_name]],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return {
            "success": True,
            "message": f"Opening {app_name}"
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }


def execute(command):

    text = normalize(command)

    try:

        # time
        if "time" in text or "clock" in text:

            current_time = datetime.now().strftime(
                "%H:%M:%S"
            )

            return {
                "success": True,
                "message": f"The time is {current_time}"
            }

        # open applications
        if text.startswith("open "):

            app = text[5:].strip()

            if app in APPS:

                return open_app(app)

            return {
                "success": False,
                "message": f"Unknown application: {app}"
            }

        return {
            "success": False,
            "message": "System command not recognized"
        }

    except Exception as error:

        return {
            "success": False,
            "message": f"Error: {error}"
        }