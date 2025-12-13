# Pylon CLI

Pylon is a command-line tool that allows you to run Python scripts from either your current project directory or your user's `.pylon` directory. It supports both simple Python scripts and project-based scripts with `pyproject.toml` dependencies.

## Installation

To install Pylon CLI, you can use pip:

```bash
pip install pylon-cli
```

## Usage

```bash
pylon <script-name> [args...]
```

Pylon searches for scripts in the following order:
1. Current project directory (the directory you're in)
2. User scripts directory (`~/.pylon`)

## How It Works

### Script Types

Pylon supports two types of scripts:

**Simple Scripts**: Standalone Python files without dependencies. They run using the current Python interpreter.

**Project Scripts**: Scripts that are part of a Python project with a `pyproject.toml` file. They run in isolated virtual environments with project dependencies installed.

> **Note**
>
> Pylon invokes the builtin `venv` module to create virtual environments for project scripts. Currently we don't support managing Python installations. If your script requires a specific Python version that's different from the one powering Pylon, the `venv`-creation will fail and Pylon will exit with an error message.

#### Directory Structure Examples

**Simple Script (current directory):**
```
.
├── hello.py          # Script name: "hello"
└── other.py          # Script name: "other"
```

**Project Script (current directory with pyproject.toml):**
```
.
├── pyproject.toml    # Project configuration
├── main.py           # Script name: "main" (runs in project virtual environment)
└── utils.py          # Script name: "utils" (runs in same project virtual environment)
```

**User Simple Script:**
```
~/.pylon/
├── greet.py          # Script name: "greet"
└── backup.py         # Script name: "backup"
```

**User Project Script:**
```
~/.pylon/myproject/
├── pyproject.toml    # Project configuration
├── task1.py          # Script name: "task1" (has its own virtual environment)
└── task2.py          # Script name: "task2" (has its own virtual environment)
```

### Script Discovery

Pylon discovers scripts in two locations: the current project directory and the user scripts directory (`~/.pylon`).

In the current project directory, Pylon looks for `.py` files. If a `pyproject.toml` file exists in the current directory, all `.py` files are treated as project scripts and share a common virtual environment managed by the project dependencies.

In the user scripts directory, Pylon looks for both simple scripts (`.py` files directly in `~/.pylon`) and project scripts (directories containing `pyproject.toml` and `.py` files). For project scripts in the user directory, each `.py` file is treated as a separate script with its own virtual environment.

### Virtual Environment Management

For project-based scripts (those with `pyproject.toml`), Pylon:
1. Creates virtual environments in `~/.pylon/.venvs/` (hashed by project path)
2. Installs dependencies from `pyproject.toml` using `pip install -e .`
3. Reuses existing virtual environments when available

### Script Shadowing

If a script with the same name exists in both the current directory and user directory, the current directory script takes precedence (script shadowing).

### Duplicate Detection

Duplicate script names within the same search location (user or project) will cause an error.

## Examples

### Basic Usage

If you have a script named `hello.py` in your current directory:

```bash
pylon hello
```

This will execute `hello.py` using the current Python interpreter.

### With Arguments

You can pass arguments to your script:

```bash
pylon hello --name="World" --verbose
```

### User Scripts

You can store scripts in your user's `.pylon` directory (`~/.pylon`) to make them globally accessible:

1. Create a script file in `~/.pylon/myscript.py`
2. Run it from anywhere:

```bash
pylon myscript arg1 arg2
```

### Project-Based Scripts

For scripts with dependencies:

1. Create a directory in `~/.pylon/myproject/`
2. Add `pyproject.toml` with dependencies
3. Add your script `myscript.py` in the same directory
4. Run it:

```bash
pylon myscript
```

Pylon will automatically create a virtual environment and install dependencies.

### Example Script

Create a file called `greet.py` in your current directory:

```python
import sys

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(f"Hello, {name}!")
    
if __name__ == "__main__":
    main()
```

Then run it with:

```bash
pylon greet Alice
# Output: Hello, Alice!
```

## Available Scripts

When you run `pylon` without any arguments, it will show you all available scripts in both the current directory and the user's `.pylon` directory, along with their type and location.

## Requirements

- Python 3.13 or higher

## License

This project is licensed under the Apache-2.0 license.