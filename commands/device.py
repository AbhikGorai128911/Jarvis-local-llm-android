from device.parser import parse
from device.executor import execute as execute_device


def execute(user_input):
    """
    Device command entry point.

    Flow:
        Raw text
            ↓
        Parser
            ↓
        Executor
            ↓
        Response
    """

    command = parse(user_input)

    return execute_device(command)
