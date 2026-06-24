from core.network import is_online
import subprocess


def execute(command):

    if not is_online():
        return {
            "success": False,
            "message": "You are offline. Cannot search the web."
        }

    query = command.lower()

    keywords = [
        "search",
        "google",
        "web",
        "internet",
        "for",
    ]

    for keyword in keywords:
        query = query.replace(keyword, "")

    query = query.strip()

    if not query:
        return {
            "success": False,
            "message": "No search query provided."
        }

    url = f"https://www.google.com/search?q={query}"

    try:
        subprocess.run(
            ["termux-open-url", url],
            check=True,
        )

        return {
            "success": True,
            "message": f"Searching for {query}"
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }
