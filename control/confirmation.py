from control.pending_actions import get_pending, clear_pending


def confirm(message, action):
    """
    Register a confirmation request.

    message: Text shown to the user.
    action: Callable executed after confirmation.
    """

    from control.pending_actions import set_pending

    set_pending(action)

    return {
        "success": True,
        "awaiting_confirmation": True,
        "message": message
    }


def handle_confirmation():

    action = get_pending()

    if action is None:
        return {
            "success": False,
            "message": "Nothing to confirm."
        }

    response = action()

    clear_pending()

    return response
