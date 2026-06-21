from commands.system import execute as system_execute
from commands.web_search import execute as web_execute
from commands.files import execute as file_execute
from commands.memory_commands import execute as memory_execute
from commands.browser import execute as browser_execute
from commands.music import execute as music_execute
from llm.local_llm import ask

def execute(intent, user_input):

    if intent in ["system", "time"]:
        return system_execute(user_input)

    if intent == "web":
        return web_execute(user_input)
    
    if intent == "files":
        return file_execute(user_input)
    
    if intent == "memory":
        return memory_execute(user_input)
    
    if intent == "browser":
        return browser_execute(user_input)
    
    if intent == "music":
        return music_execute(user_input)
    


    if intent == "unknown":
        ask(user_input)

        return {
            "success": True,
            "message": ""
        }

    return {
        "success": False,
        "message": f"I don't know how to handle '{intent}' yet."
    }