import subprocess


def dial(number):
    """
    Open the dialer with a phone number.
    """

    try:
        subprocess.run(
            [
                "am",
                "start",
                "-a",
                "android.intent.action.DIAL",
                "-d",
                f"tel:{number}"
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return {
            "success": True,
            "message": "Dialer opened."
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }


def call(number):
    """
    Place a phone call.
    """

    try:
        subprocess.run(
            [
                "am",
                "start",
                "-a",
                "android.intent.action.CALL",
                "-d",
                f"tel:{number}"
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return {
            "success": True,
            "message": "Calling..."
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }
