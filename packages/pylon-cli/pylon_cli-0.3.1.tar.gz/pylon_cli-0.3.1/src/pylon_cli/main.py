import sys

import colorama

from . import PROJECT_SCRIPTS_ROOT, TAG_ERROR, TAG_SCRIPT, USER_SCRIPTS_ROOT
from .script import Script, discover_project_scripts, discover_user_scripts


def main() -> None:
    colorama.init(autoreset=True)

    # Discover scripts
    try:
        project_scripts = discover_project_scripts(PROJECT_SCRIPTS_ROOT)
        user_scripts = discover_user_scripts(USER_SCRIPTS_ROOT)
    except ValueError as e:
        print(colorama.Fore.RED + TAG_ERROR, str(e))
        sys.exit(1)

    # Print usage if no script name is provided
    if len(sys.argv) == 1:
        usage(project_scripts, user_scripts)
        return

    # Find target script in discovered scripts
    script_name = sys.argv[1]
    if script_name in project_scripts:
        script_info = project_scripts[script_name]
    elif script_name in user_scripts:
        script_info = user_scripts[script_name]
    else:
        usage(project_scripts, user_scripts)  # print usage if not found
        return

    # Print info and run script
    print(colorama.Fore.GREEN + TAG_SCRIPT, f"{script_name} ({script_info.path})")
    try:
        script_info.run(sys.argv[2:])
    except Exception as e:
        print(colorama.Fore.RED + TAG_ERROR, str(e))


def usage(project_scripts: dict[str, Script], user_scripts: dict[str, Script]) -> None:
    print(colorama.Fore.RED + "Usage: pylon <script-name> [args...]")
    print("")
    print("Pylon is a script runner that searches for scripts in the following order:")
    print(f"  1. Current (project) directory ({PROJECT_SCRIPTS_ROOT})")
    print(f"  2. User scripts directory ({USER_SCRIPTS_ROOT})")
    print("and runs the first script with the following args.")
    print("")
    print("Available scripts:")

    for name, info in sorted(project_scripts.items()):
        location = "project" if info.project_dir is None else "project-dir"
        print("  -", colorama.Fore.CYAN + name, f"({location}, {info.path})")

    for name, info in sorted(user_scripts.items()):
        location = "user" if info.project_dir is None else "user-dir"
        print("  -", colorama.Fore.CYAN + name, f"({location}, {info.path})")

    if not project_scripts and not user_scripts:
        print("  No scripts found.")
    print("")


if __name__ == "__main__":
    main()
