# Pylon CLI

Pylon is a simple command-line tool that allows you to run Python scripts from either your current project directory or your user's `.pylon` directory. It searches for Python scripts by name and executes them with the specified arguments.

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

Pylon looks for Python files with the `.py` extension that match the name you provide. For example, if you run `pylon myscript`, it will look for a file named `myscript.py` in the current directory and in your user's `.pylon` directory.

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

When you run `pylon` without any arguments, it will show you all available scripts in both the current directory and the user's `.pylon` directory.

## Requirements

- Python 3.13 or higher

## License

This project is licensed under the Apache-2.0 license.