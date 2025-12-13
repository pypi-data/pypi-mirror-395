import os
import subprocess
import sys

USER_SCRIPTS_ROOT = os.path.abspath(os.path.join(os.path.expanduser("~"), ".pylon"))
PROJECT_SCRIPTS_ROOT = os.path.abspath(".")
VENV_ROOT = os.path.join(os.path.expanduser("~"), ".pylon", ".venvs")

TAG_RUNTIME = "RUNTIME"
TAG_SCRIPT = " SCRIPT"
TAG_ERROR = "  ERROR"
TAG_VENV = "   VENV"


def syscall(*command: str, shell: bool = False) -> None:
    _ = subprocess.run(command, check=True, stdout=sys.stdout, stderr=sys.stderr, shell=shell)
