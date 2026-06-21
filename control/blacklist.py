from pathlib import Path

WORKSPACE = Path.home() / "JARVIS_WORKSPACE"

PROTECTED_PATHS = [
    Path("/"),
    Path("/boot"),
    Path("/etc"),
    Path("/usr"),
    Path("/bin"),
    Path("/sbin"),
    Path("/lib"),
    Path("/var"),
    Path.home()
]

DANGEROUS_COMMANDS = [
    "rm -rf",
    "mkfs",
    "dd",
    "shutdown",
    "reboot",
    "poweroff",
    "halt"
]