import os
import subprocess
import sys

import colorama

TAG_RUNTIME = "RUNTIME"
TAG_SCRIPT = " SCRIPT"

USER_SCRIPTS_ROOT = os.path.abspath(os.path.join(os.path.expanduser("~"), ".pylon"))
PROJECT_SCRIPTS_ROOT = os.path.abspath(".")


def main() -> None:
    colorama.init(autoreset=True)

    # No script specified
    if len(sys.argv) == 1:
        usage()
        return

    # Script specified but not found
    path = search_scripts_root(PROJECT_SCRIPTS_ROOT, sys.argv[1])
    if path is None and os.path.exists(USER_SCRIPTS_ROOT):
        path = search_scripts_root(USER_SCRIPTS_ROOT, sys.argv[1])
    if path is None:
        usage()
        return

    # Run script
    print(colorama.Fore.CYAN + TAG_RUNTIME, f"Python {sys.version}")
    print(colorama.Fore.GREEN + TAG_SCRIPT, f"{sys.argv[1]} ({path})")
    try:
        syscall(sys.executable, path, *sys.argv[2:])
    except Exception:  # we're not responsible for the exception thrown by failures of the script
        pass


def search_scripts_root(root: str, name: str) -> str | None:
    script_name = f"{name}.py"
    for entry in os.scandir(root):
        if not entry.is_file():
            continue
        if entry.name == script_name:
            return entry.path


def usage() -> None:
    print(colorama.Fore.RED + "Usage: pylon <script-name> [args...]")
    print("")
    print("Pylon is a script runner that searches for scripts in the following order:")
    print(f"  1. Current (project) directory ({PROJECT_SCRIPTS_ROOT})")
    print(f"  2. User scripts directory ({USER_SCRIPTS_ROOT})")
    print("and runs the first script with the following args.")
    print("")
    print("Available scripts:")
    for entry in os.scandir(PROJECT_SCRIPTS_ROOT):
        if entry.is_file() and entry.name.endswith(".py"):
            print("  -", colorama.Fore.CYAN + entry.name[:-3], f"(project, {entry.path})")
    if os.path.exists(USER_SCRIPTS_ROOT):
        for entry in os.scandir(USER_SCRIPTS_ROOT):
            if entry.is_file() and entry.name.endswith(".py"):
                print("  -", colorama.Fore.CYAN + entry.name[:-3], f"(user, {entry.path})")
    print("")


def syscall(*command: str, shell: bool = False) -> None:
    _ = subprocess.run(command, check=True, stdout=sys.stdout, stderr=sys.stderr, shell=shell)
