import subprocess
import sys

MODEL = "models/llm/gemma-3-1b-it-Q4_K_M.gguf"
BINARY = "llama.cpp/build/bin/llama-completion"


def ask(prompt):
    command = [
        BINARY,
        "-m", MODEL,
        "-p", prompt,
        "-n", "32",
        "-t", "2",
        "-c", "256",
        "-no-cnv",
        "--log-disable",
    ]

    print("\n\033[94mJARVIS > ", end="")
    sys.stdout.flush()

    result = subprocess.run(
        command,
        text=True
    )

    print("\033[0m", end="")

    return result.returncode == 0