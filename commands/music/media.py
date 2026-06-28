import subprocess


def media(command):
    try:
        subprocess.run(
            ["termux-media-player", command],
            check=True
        )
        return True
    except Exception:
        return False


def play():
    return media("play")


def pause():
    return media("pause")


def stop():
    return media("stop")


def info():
    try:
        result = subprocess.run(
            ["termux-media-player", "info"],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception:
        return None
