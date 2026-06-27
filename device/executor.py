import subprocess
import json


def _run(command):
    """
    Run a subprocess safely.
    Returns (success, stdout).
    """

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        return (
            result.returncode == 0,
            result.stdout.strip()
        )

    except Exception as error:
        return False, str(error)


def execute(command):
    """
    Execute a parsed device command.

    command format:
    {
        "action": "...",
        "target": "...",
        "value": ...
    }
    """

    action = command.get("action")
    target = command.get("target")
    value = command.get("value")

    if target is None:
        return {
            "success": False,
            "message": "No device specified."
        }

    #
    # Wi-Fi
    #
    if target == "wifi":

        subprocess.run([
            "am",
            "start",
            "-a",
            "android.settings.WIFI_SETTINGS"
        ])

        return {
            "success": True,
            "message": "Opened Wi-Fi settings."
        }

    #
    # Bluetooth
    #
    if target == "bluetooth":

        subprocess.run([
            "am",
            "start",
            "-a",
            "android.settings.BLUETOOTH_SETTINGS"
        ])

        return {
            "success": True,
            "message": "Opened Bluetooth settings."
        }

    #
    # Torch
    #
    if target == "torch":

        if action == "on":
            _run(["termux-torch", "on"])

        elif action == "off":
            _run(["termux-torch", "off"])

        else:
            return {
                "success": False,
                "message": "Torch requires on/off."
            }

        return {
            "success": True,
            "message": f"Torch turned {action}."
        }

    #
    # Battery
    #
    if target == "battery":

        ok, output = _run(["termux-battery-status"])

        if not ok:
            return {
                "success": False,
                "message": output
            }

        data = json.loads(output)

        return {
            "success": True,
            "message": f"Battery is {data['percentage']}%"
        }

    #
    # Volume
    #
    if target == "volume":

        if value is None:
            return {
                "success": False,
                "message": "Volume value missing."
            }

        ok, output = _run([
            "termux-volume",
            "music",
            str(value)
        ])

        if not ok:
            return {
                "success": False,
                "message": output
            }

        return {
            "success": True,
            "message": f"Volume set to {value}."
        }

    return {
        "success": False,
        "message": f"Unsupported device: {target}"
    }
