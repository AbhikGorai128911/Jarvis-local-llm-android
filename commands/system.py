import json
import os
import subprocess
from datetime import datetime


# Built-in Android intents
INTENTS = {
    "settings": [
        "am", "start",
        "-a", "android.settings.SETTINGS"
    ],

    "camera": [
        "am", "start",
        "-a", "android.media.action.IMAGE_CAPTURE"
    ],

    "browser": [
        "am", "start",
        "-a", "android.intent.action.VIEW",
        "-d", "https://www.google.com"
    ],

    "contacts": [
        "am", "start",
        "-a", "android.intent.action.VIEW",
        "-t", "vnd.android.cursor.dir/contact"
    ],

    "dialer": [
        "am", "start",
        "-a", "android.intent.action.DIAL"
    ]
}


REPLACEMENTS = {
    "phone": "dialer",
    "call": "dialer",
    "map": "maps"
}


APPS_FILE = os.path.join("data", "apps.json")


def load_apps():
    try:
        with open(APPS_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return {}


def save_apps(apps):
    os.makedirs(os.path.dirname(APPS_FILE), exist_ok=True)

    with open(APPS_FILE, "w") as file:
        json.dump(apps, file, indent=4)


def normalize(text):
    text = text.lower().strip()

    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)

    return text


def open_url(url):
    try:
        subprocess.run(
            ["termux-open-url", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return {
            "success": True,
            "message": f"Opening {url}"
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }


def launch_component(component):
    """
    Returns True if Android accepted the command.
    """

    try:
        result = subprocess.run(
            [
                "am",
                "start",
                "--user", "0",
                "-n",
                component
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return result.returncode == 0

    except Exception:
        return False


def launch_intent(intent):
    try:
        subprocess.run(
            intent,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return {
            "success": True,
            "message": "Opening app"
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }


def guess_component(package_name):
    """
    Try common Android launcher activities.
    """

    guesses = [
        ".Main",
        ".MainActivity",
        ".HomeActivity",
        ".LaunchActivity",
        ".ui.MainActivity",
        ".activities.MainActivity",
    ]

    for activity in guesses:

        component = package_name + "/" + activity

        if launch_component(component):
            return component

    return None


def execute(command):

    text = normalize(command)

    try:

        # Time
        if "time" in text or "clock" in text:

            current_time = datetime.now().strftime("%H:%M:%S")

            return {
                "success": True,
                "message": f"The time is {current_time}"
            }

        # Open commands
        if text.startswith("open "):

            target = text[5:].strip()

            # Built-in intents
            if target in INTENTS:
                return launch_intent(INTENTS[target])

            # Maps search
            if target.startswith("maps "):

                place = target[5:].strip()

                return launch_intent([
                    "am",
                    "start",
                    "-a",
                    "android.intent.action.VIEW",
                    "-d",
                    f"geo:0,0?q={place}"
                ])

            # Website
            if "." in target and "/" not in target:

                url = target

                if not url.startswith(("http://", "https://")):
                    url = "https://" + url

                return open_url(url)

            apps = load_apps()

            # Already learned
            if target in apps:

                component = apps[target]

                if launch_component(component):

                    return {
                        "success": True,
                        "message": f"Opening {target}"
                    }

                else:
                    del apps[target]
                    save_apps(apps)

                    print(
                        f'JARVIS > Forgot broken entry for "{target}".'
                    )

            # Learning mode
            print(
                f'JARVIS > I do not know "{target}" yet.'
            )

            package = input(
                "Package name (or cancel): "
            ).strip()

            if package.lower() == "cancel":

                return open_url(
                    "https://www.google.com/search?q="
                    + target.replace(" ", "+")
                )

            # User already provided full component
            if "/" in package:

                component = package

                if launch_component(component):

                    apps[target] = component
                    save_apps(apps)

                    return {
                        "success": True,
                        "message": (
                            f"I'll remember {target}. "
                            "Opening app."
                        )
                    }

            else:

                # Try to discover component
                component = guess_component(package)

                if component:

                    apps[target] = component
                    save_apps(apps)

                    return {
                        "success": True,
                        "message": (
                            f"I figured out how to open "
                            f"{target}. I'll remember it."
                        )
                    }

            # Final fallback
            print(
                "JARVIS > Automatic discovery failed."
            )

            component = input(
                "Full component (or cancel): "
            ).strip()

            if component.lower() != "cancel":

                if launch_component(component):

                    apps[target] = component
                    save_apps(apps)

                    return {
                        "success": True,
                        "message": (
                            f"I'll remember {target}. "
                            "Opening app."
                        )
                    }

            return open_url(
                "https://www.google.com/search?q="
                + target.replace(" ", "+")
            )

        return {
            "success": False,
            "message": "System command not recognized"
        }

    except Exception as error:

        return {
            "success": False,
            "message": f"Error: {error}"
        }
