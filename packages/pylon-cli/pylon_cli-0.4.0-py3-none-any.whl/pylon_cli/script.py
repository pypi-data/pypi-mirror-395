import ast
import enum
import hashlib
import os
import shutil
import sys
import tomllib
import venv

import colorama

from . import TAG_RUNTIME, VENV_ROOT, syscall

__all__ = ["Script", "ScriptKind", "discover_user_scripts", "discover_project_scripts"]

TAG_VENV = "   VENV"


def extract_docstring(file_path: str) -> str | None:
    """
    Extract docstring from a Python file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Look for triple-quoted string at the beginning of the file
    try:
        tree = ast.parse(content)
        if tree.body and isinstance(tree.body[0], ast.Expr):
            if isinstance(tree.body[0].value, ast.Constant):
                docstring = tree.body[0].value.value
                if isinstance(docstring, str):
                    return docstring.strip()
    except (SyntaxError, ValueError):
        pass  # No docstring found
    return None


def extract_description(pyproject_path: str) -> str:
    """
    Extract description from pyproject.toml
    """
    try:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
            return data.get("project", {}).get("description")
    except Exception:
        pass


class ScriptKind(enum.Enum):
    SIMPLE = "simple"
    PROJECT = "project"


class Script(object):
    """Represents a script found by Pylon"""

    name: str
    path: str
    kind: ScriptKind
    project_dir: str | None
    docstring: str | None
    _venv_path: str | None

    def __init__(
        self,
        name: str,
        path: str,
        kind: ScriptKind,
        project_dir: str | None = None,
        docstring: str | None = None,
    ):
        self.name = name
        self.path = path
        self.kind = kind
        self.project_dir = project_dir
        self.docstring = docstring
        self._venv_path = None

    def run(self, args: list[str]) -> None:
        """Run this script with given arguments"""
        if self.kind == ScriptKind.SIMPLE:
            python_path = sys.executable
            if python_path is None:
                raise RuntimeError("Python executable not found")
            print(colorama.Fore.CYAN + TAG_RUNTIME, f"Python {sys.version}")
        else:
            if not self.project_dir:
                raise ValueError("Project directory not specified for project script")
            python_path = self.prepare_venv()
        syscall(python_path, self.path, *args)

    @property
    def venv_path(self) -> str:
        """Virtual environment path for this project"""
        if not self._venv_path:
            if not self.project_dir:
                raise ValueError("No project directory for simple script")

            project_hash = hashlib.md5(self.project_dir.encode()).hexdigest()
            self._venv_path = os.path.join(VENV_ROOT, project_hash)
        return self._venv_path

    def prepare_venv(self) -> str:
        """Get or create virtual environment for this project"""
        if sys.platform == "win32":
            python_path = os.path.join(self.venv_path, "Scripts", "python.exe")
        else:
            python_path = os.path.join(self.venv_path, "bin", "python")

        if os.path.exists(python_path):
            print(colorama.Fore.BLUE + TAG_VENV, f"Using existing virtual environment at {self.venv_path}")
            return python_path

        os.makedirs(os.path.dirname(self.venv_path), exist_ok=True)
        try:
            print(colorama.Fore.BLUE + TAG_VENV, f"Creating virtual environment at {self.venv_path}")
            builder = venv.EnvBuilder(with_pip=True)
            builder.create(self.venv_path)
            syscall(python_path, "-m", "pip", "install", "--upgrade", "pip")
            print(colorama.Fore.BLUE + TAG_VENV, f"Installing dependencies from {self.project_dir}")
            pyproject_toml = os.path.join(self.project_dir, "pyproject.toml")
            if os.path.exists(pyproject_toml):
                syscall(python_path, "-m", "pip", "install", "-e", self.project_dir)
            return python_path
        except Exception as e:
            shutil.rmtree(self.venv_path, ignore_errors=True)
            raise RuntimeError(f"Failed to setup virtual environment: {e}")


def discover_user_scripts(root: str) -> dict[str, Script]:
    scripts: dict[str, Script] = {}
    if not os.path.exists(root):
        return scripts

    for entry in os.scandir(root):
        if entry.is_file():
            if entry.name.endswith(".py"):
                name = entry.name[:-3]
                if name in scripts:
                    raise ValueError(f"Duplicate script name '{name}'")
                docstring = extract_docstring(entry.path)
                scripts[name] = Script(name=name, path=entry.path, kind=ScriptKind.SIMPLE, docstring=docstring)
        elif entry.is_dir():
            project_toml = os.path.join(entry.path, "pyproject.toml")
            if not os.path.exists(project_toml):
                continue
            project_description = extract_description(project_toml)

            for file_entry in os.scandir(entry.path):
                if file_entry.is_file() and file_entry.name.endswith(".py"):
                    name = file_entry.name[:-3]
                    if name in scripts:
                        raise ValueError(f"Duplicate script name '{name}'")
                    scripts[name] = Script(
                        name=name,
                        path=file_entry.path,
                        kind=ScriptKind.PROJECT,
                        project_dir=entry.path,
                        docstring=project_description,
                    )
    return scripts


def discover_project_scripts(root: str) -> dict[str, Script]:
    scripts: dict[str, Script] = {}
    if not os.path.exists(root):
        return scripts
    has_pyproject = os.path.exists(os.path.join(root, "pyproject.toml"))

    # Extract project description if pyproject.toml exists
    project_description = None
    if has_pyproject:
        project_description = extract_description(os.path.join(root, "pyproject.toml"))

    for entry in os.scandir(root):
        if not entry.is_file():
            continue
        if entry.name.endswith(".py"):
            name = entry.name[:-3]
            if name in scripts:
                raise ValueError(f"Duplicate script name '{name}'")
            script_type = ScriptKind.PROJECT if has_pyproject else ScriptKind.SIMPLE
            project_dir = root if has_pyproject else None

            # For simple scripts, extract docstring from file
            # For project scripts, use project description
            docstring = None
            if has_pyproject:
                docstring = project_description
            else:
                docstring = extract_docstring(entry.path)

            scripts[name] = Script(name, entry.path, script_type, project_dir, docstring)
    return scripts
