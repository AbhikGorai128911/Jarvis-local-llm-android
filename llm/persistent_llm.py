import subprocess
import threading
import itertools
import time
import sys
import requests

MODEL = "models/gemma-3-1b-it-Q4_K_M.gguf"
BINARY = "./llama.cpp/build/bin/llama-server"

SERVER_URL = "http://127.0.0.1:8080"

SERVER_PROCESS = None


def spinner(stop_event):
    for char in itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"):
        if stop_event.is_set():
            break

        sys.stdout.write(f"\rJARVIS is thinking {char}")
        sys.stdout.flush()

        time.sleep(0.08)

    sys.stdout.write("\n")
    sys.stdout.flush()


def start_llm():
    global SERVER_PROCESS

    if SERVER_PROCESS is not None:
        return

    print("[AI] Loading Gemma...")

    SERVER_PROCESS = subprocess.Popen(
        [
            BINARY,
            "-m", MODEL,
            "--port", "8080",
            "-t", "4",
            "--log-disable",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    while True:
        try:
            response = requests.get(
                f"{SERVER_URL}/health",
                timeout=1,
            )

            if response.status_code == 200:
                print("[AI] Gemma ready.")
                break

        except requests.RequestException:
            pass

        time.sleep(1)


def ask_persistent(prompt):
    stop_event = threading.Event()

    spinner_thread = threading.Thread(
        target=spinner,
        args=(stop_event,),
        daemon=True,
    )

    start_time = time.perf_counter()

    spinner_thread.start()

    try:
        response = requests.post(
            f"{SERVER_URL}/v1/chat/completions",
            json={
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            },
            timeout=300,
        )

        data = response.json()

        message = (
            data["choices"][0]
            ["message"]["content"]
            .strip()
        )

    except Exception:
        message = (
            "Sorry, I couldn't get a response "
            "from the local model."
        )

    finally:
        stop_event.set()
        spinner_thread.join()

    elapsed_time = time.perf_counter() - start_time

    print(
        f"\n[Response time: "
        f"{elapsed_time:.2f} seconds]"
    )

    return message


def stop_llm():
    global SERVER_PROCESS

    if SERVER_PROCESS is None:
        return

    print("[AI] Unloading Gemma...")

    SERVER_PROCESS.terminate()

    try:
        SERVER_PROCESS.wait(timeout=5)

    except subprocess.TimeoutExpired:
        SERVER_PROCESS.kill()

    SERVER_PROCESS = None

    print("[AI] Gemma unloaded.")
