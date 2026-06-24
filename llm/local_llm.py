import os
import pty
import errno
import subprocess
import threading
import itertools
import time
import sys

MODEL = "models/gemma-3-1b-it-Q4_K_M.gguf"
BINARY = "./llama.cpp/build/bin/llama-completion"




def spinner(stop_event):
    for char in itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\rJARVIS is thinking {char}")
        sys.stdout.flush()
        time.sleep(0.08)
    
    # Instead of clearing, print a newline so the next text doesn't overwrite it
    sys.stdout.write("\n")
    sys.stdout.flush()







#def spinner(stop_event):
#    for char in itertools.cycle("|/-\\"):
#        if stop_event.is_set():
#            break

#        sys.stdout.write(f"\rJARVIS is thinking {char}")
#        sys.stdout.flush()

#        time.sleep(0.1)

    # Clear the line
#    sys.stdout.write("\r" + " " * 40 + "\r")
#    sys.stdout.flush()


def ask(prompt):
    stop_event = threading.Event()

    spinner_thread = threading.Thread(
        target=spinner,
        args=(stop_event,),
        daemon=True,
    )
    start_time = time.perf_counter()
    spinner_thread.start()

    try:
        master, slave = pty.openpty()

        process = subprocess.Popen(
            [
                BINARY,
                "-m", MODEL,
                "-p", prompt,
                "-n", "128",
                "-t", "4",
                "-c", "512",
                "-st",
                "--log-disable",
                "--no-perf",
            ],
            stdin=subprocess.DEVNULL,
            stdout=slave,
            stderr=slave,
        )

        os.close(slave)

        output = ""

        while True:
            try:
                chunk = os.read(master, 1024)

                if not chunk:
                    break

                output += chunk.decode(errors="ignore")

            except OSError as e:
                if e.errno == errno.EIO:
                    break
                raise

        process.wait()
        os.close(master)

    finally:
        stop_event.set()
        spinner_thread.join()

    elapsed_time = time.perf_counter() - start_time
    try:
        response = output.split("model", 1)[1]

        if "[end of text]" in response:
            response = response.split("[end of text]", 1)[0]

        cleaned = []

        for line in response.splitlines():
            line = line.strip()

            if (
                not line
                or "common_perf_print:" in line
                or line.startswith("0.")
            ):
                continue

            cleaned.append(line)

        response = " ".join(cleaned).strip()

        if not response:
            return "The model returned an empty response."

        print(f"\n[Response time: {elapsed_time:.2f} seconds]")
        return response

    except Exception:
        return "The model returned an empty response."
