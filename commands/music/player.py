import os
import subprocess


MUSIC_ROOT = os.path.expanduser(
    "~/storage/music"
)

DOWNLOAD_DIR = os.path.join(
    MUSIC_ROOT,
    "downloads"
)

MUSIC_DIRS = [
    MUSIC_ROOT
]



SUPPORTED_EXTENSIONS = (
    ".mp3",
    ".flac",
    ".wav",
    ".m4a",
    ".ogg",
    ".aac",
)


def _find_song(query):
    query = query.lower().strip()
    matches = []

    for directory in MUSIC_DIRS:
        print("Searching:", directory)
        if not os.path.isdir(directory):
            continue

        for root, _, files in os.walk(directory):
            print(root, len(files))
            for file in files:

                if not file.lower().endswith(SUPPORTED_EXTENSIONS):
                    continue

                if query in file.lower():

                    path = os.path.realpath(
                        os.path.join(root, file)
                    )

                    if path not in matches:
                        matches.append(path)
    print("Matches:", matches)
    return matches


def play_song(query):

    matches = _find_song(query)

    if len(matches) == 0:
        return {
            "success": False,
            "message": "Song not found locally."
        }

    if len(matches) > 1:

        print("\nJARVIS > Multiple songs found:\n")

        for i, song in enumerate(matches, 1):
            print(f"{i}. {os.path.basename(song)}")

        choice = input(
            f"\nChoose song (1-{len(matches)}, Enter=1): "
        ).strip()

        if choice == "":
            index = 0
        else:
            try:
                index = int(choice) - 1
            except ValueError:
                return {
                    "success": False,
                    "message": "Invalid selection."
                }

            if index < 0 or index >= len(matches):
                return {
                    "success": False,
                    "message": "Invalid selection."
                }

        song = matches[index]

    else:

        song = matches[0]

    try:

        subprocess.run(
            [
                "termux-media-player",
                "play",
                song
            ],
            check=True
        )

        return {
            "success": True,
            "message": f"Playing {os.path.basename(song)}"
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


def control(action):

    mapping = {
        "resume": ["play"],
        "pause": ["pause"],
        "stop": ["stop"],
        "next": ["next"],
        "previous": ["previous"],
    }

    if action not in mapping:
        return {
            "success": False,
            "message": "Unsupported control."
        }

    try:
        subprocess.run(
            ["termux-media-player"] + mapping[action],
            check=True
        )

        return {
            "success": True,
            "message": action.capitalize()
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }


def info():

    result = subprocess.run(
        [
            "termux-media-player",
            "info"
        ],
        capture_output=True,
        text=True
    )

    return result.stdout
