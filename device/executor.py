import subprocess
import json


def _run(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout.strip()

    except Exception as e:
        return False, str(e)


def execute(command):

    action = command.get("action")
    target = command.get("target")
    value = command.get("value")

    if target is None:
        return {
            "success": False,
            "message": "No device specified."
        }

    # --------------------
    # WIFI
    # --------------------
    if target == "wifi":
        subprocess.run(["am", "start", "-a", "android.settings.WIFI_SETTINGS"])
        return {"success": True, "message": "Opened Wi-Fi settings"}

    # --------------------
    # BLUETOOTH
    # --------------------
    if target == "bluetooth":
        subprocess.run(["am", "start", "-a", "android.settings.BLUETOOTH_SETTINGS"])
        return {"success": True, "message": "Opened Bluetooth settings"}

    # --------------------
    # TORCH
    # --------------------
    if target == "torch":
        if action == "on":
            _run(["termux-torch", "on"])
        elif action == "off":
            _run(["termux-torch", "off"])
        else:
            return {"success": False, "message": "Torch requires on/off"}

        return {"success": True, "message": f"Torch {action}"}

    # --------------------
    # BATTERY
    # --------------------
    if target == "battery":
        ok, out = _run(["termux-battery-status"])
        if not ok:
            return {"success": False, "message": out}

        data = json.loads(out)
        return {"success": True, "message": f"{data['percentage']}%"}

    # --------------------
    # VOLUME
    # --------------------
    if target == "volume":

        if target == "volume":

            if value is None:
                import re
                match = re.search(r"\b\d+\b", command.get("raw", ""))
                if match:
                    value = int(match.group())
                else:
                    return {
                        "success": False,
                        "message": "Volume value missing"
                    }


        ok, out = _run(["termux-volume", "music", str(value)])

        if not ok:
            return {"success": False, "message": out}

        return {"success": True, "message": f"Volume set to {value}"}

    # --------------------
    # FALLBACK
    # --------------------
    return {
        "success": False,
        "message": f"Unsupported device: {target}"
    }
