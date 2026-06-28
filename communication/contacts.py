import json
import subprocess


def load_contacts():
    """
    Load contacts from the Termux API.
    """

    try:
        result = subprocess.run(
            ["termux-contact-list"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return []

        return json.loads(result.stdout)

    except Exception:
        return []


def find_contacts(query):

    contacts = load_contacts()

    query = query.lower().strip()

    matches = []

    for contact in contacts:

        name = contact.get("name", "").lower()
        number = contact.get("number", "")

        if query in name:
            matches.append({
                "name": contact.get("name", "Unknown"),
                "number": number
            })

    return matches
