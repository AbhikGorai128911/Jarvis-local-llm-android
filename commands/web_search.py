from core.network import is_online
import webbrowser


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
        "for"
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

    webbrowser.open(url)

    return {
        "success": True,
        "message": f"Searching for {query}"
    }