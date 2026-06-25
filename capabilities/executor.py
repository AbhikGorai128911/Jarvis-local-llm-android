import subprocess
from capabilities.capabilities import CAPABILITIES


def execute(resolved):
    if not resolved:
        return {"success": False, "message": "Nothing resolved"}

    cap, mode = resolved

    if cap not in CAPABILITIES:
        return {"success": False, "message": "Unknown capability"}

    data = CAPABILITIES[cap]

    # DIRECT TERMUX CONTROL
    if data["type"] == "direct":
        if cap == "torch":
            subprocess.run([data[mode][0], data[mode][1]])
            return {"success": True, "message": f"Torch {mode}"}

        subprocess.run([data["command"]])
        return {"success": True, "message": f"Executed {cap}"}

    # INTENT BASED
    if data["type"] == "intent":
        subprocess.run([
            "am", "start",
            "-a", data["action"]
        ])
        return {"success": True, "message": f"Opened {cap} settings"}

    # UNSUPPORTED
    if data["type"] == "unsupported":
        return {
            "success": False,
            "message": f"{cap} is not directly controllable on this device"
        }

    return {"success": False, "message": "Unknown execution type"}
