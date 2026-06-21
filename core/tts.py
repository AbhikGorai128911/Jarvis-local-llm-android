from pathlib import Path
from piper import PiperVoice
import wave
import subprocess


VOICE_PATH = Path(
    "models/piper/en_US-lessac-medium.onnx"
)

voice = PiperVoice.load(
    str(VOICE_PATH)
)


def speak(text):

    output_file = "output.wav"

    with wave.open(output_file, "wb") as wav_file:

        voice.synthesize_wav(
            text,
            wav_file
        )

    subprocess.run(
        [
            "aplay",
            output_file
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )