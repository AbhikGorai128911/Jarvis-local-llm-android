import subprocess
import urllib.parse


def send_message(number, message):

    try:
        encoded = urllib.parse.quote(message)

        url = f"https://wa.me/{number}?text={encoded}"

        subprocess.run([
            "am", "start",
            "-a", "android.intent.action.VIEW",
            "-d", url
        ])

        return {
            "success": True,
            "message": "WhatsApp opened directly with prefilled message"
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
