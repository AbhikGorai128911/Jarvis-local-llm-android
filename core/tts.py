import subprocess


def speak(text):
    """
    Android/Termux TTS implementation.

    - Prints the response so JARVIS is usable even without TTS.
    - Uses Android's built-in TTS through Termux:API if available.
    """

    # Always show the response in the terminal
    print(f"\033[94mJARVIS > {text}\033[0m")

    # Try to speak it aloud
    try:
        subprocess.run(
            [
                "termux-tts-speak",
                text
            ],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    except FileNotFoundError:
        # Termux:API not installed
        pass

    except Exception:
        # Any other TTS-related issue shouldn't crash JARVIS
        pass
