from pydoc import text


def classify(user_input):

    text = user_input.lower()

    if any(word in text for word in [
        "open",
        "launch",
        "start"
    ]):
        return "system"

    if any(word in text for word in [
        "search",
        "google",
        "web",
        "internet"
    ]):
        return "web"

    if any(word in text for word in [
        "music",
        "song",
        "play"
    ]):
        return "music"

    if any(word in text for word in [
        "time",
        "clock"
    ]):
        return "time"



    if any(word in text for word in [
        "file",
        "folder",
        "directory",
        "list files",
        "create"
    ]):
        return "files"
    
    if any(word in text for word in [
        "youtube",
        "github",
        "reddit",
        "chatgpt",
        "stackoverflow"
    ]):
        return "browser"
    

    if any(word in text for word in [
        "music",
        "play",
        "pause",
        "next",
        "previous",
        "volume"
    ]):
        return "music"



    if text.startswith("remember"):
        return "memory"

    if text.startswith("what is"):
        return "memory"
    



    return "unknown"