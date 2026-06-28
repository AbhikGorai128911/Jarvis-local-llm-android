# commands/music/fallback.py

import os
import subprocess

MUSIC_ROOT = os.path.expanduser(
    "~/storage/music"
)

DOWNLOAD_DIR = os.path.join(
    MUSIC_ROOT,
    "downloads"
)

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def spotify(song):

    subprocess.run([
        "am", "start",
        "-a", "android.intent.action.VIEW",
        "-d", f"spotify:search:{song}"
    ])

    return {
        "success": True,
        "message": "Opened Spotify."
    }


def ytmusic(song):

    url = (
        "https://music.youtube.com/search?q="
        + song.replace(" ", "+")
    )

    subprocess.run([
        "am", "start",
        "-a", "android.intent.action.VIEW",
        "-d", url
    ])

    return {
        "success": True,
        "message": "Opened YouTube Music."
    }


def download(link):

    output = os.path.join(
        DOWNLOAD_DIR,
        "%(title)s.%(ext)s"
    )

    try:

        subprocess.run(
            [
                "yt-dlp",
                "-x",
                "--audio-format", "mp3",
                "--embed-thumbnail",
                "--embed-metadata",
                "--add-metadata",
                "-o", output,
                link
            ],
            check=True
        )

        return {
            "success": True,
            "message": "Download started."
        }

    except subprocess.CalledProcessError:

        return {
            "success": False,
            "message": "Download failed."
        }
