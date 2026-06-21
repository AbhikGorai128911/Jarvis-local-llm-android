from pathlib import Path
from control.blacklist import (
    WORKSPACE,
    PROTECTED_PATHS
)


def is_inside_workspace(path_str):

    try:

        target = Path(path_str).resolve()

        workspace = WORKSPACE.resolve()

        return str(target).startswith(
            str(workspace)
        )

    except Exception:
        return False


def is_protected(path_str):

    try:

        target = Path(path_str).resolve()

        for protected in PROTECTED_PATHS:

            if target == protected.resolve():
                return True

        return False

    except Exception:
        return True