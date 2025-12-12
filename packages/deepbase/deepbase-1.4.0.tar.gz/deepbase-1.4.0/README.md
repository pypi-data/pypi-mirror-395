# DeepBase

**DeepBase** is a command-line tool that analyzes a project directory, extracts the folder structure and the content of all significant code files, and consolidates them into a single text/markdown file.

This unified "context" is perfect for providing to a Large Language Model (LLM) to enable it to deeply understand the entire codebase.

## Features

- **Project Structure**: Generates a tree view of the folder and file structure.
- **Smart Filtering**: Automatically ignores common unnecessary directories (e.g., `.git`, `venv`, `node_modules`).
- **Token Optimization (TOON)**: Capable of generating "Semantic Skeletons" (class definitions, function signatures, docstrings) instead of full code to save up to 90% of tokens.
- **Hybrid Focus Mode**: Combine lightweight context for the whole project with full content only for specific files or folders.
- **Configurable**: Customize ignored directories and included extensions via a `.deepbase.toml` file.
- **Unified Output**: Combines everything into a single file, easy to copy and paste.
- **PyPI Ready**: Easy to install via `pip`.

## Installation

You can install DeepBase directly from PyPI:

```sh
pip install deepbase
```

## How to Use

Once installed, use the `deepbase` command followed by the target (directory or file).

### 1. Basic Project Analysis

**Structure Only (Default)**
Quickly generate a tree view of your project folders and files. No code content is included.

```sh
deepbase .
```

**Include All Content**
To generate the full context including the code of all significant files, use the `--all` (or `-a`) flag.
*Warning: use this only for small projects.*

```sh
deepbase . --all
```

### 2. Smart Token Optimization (TOON)

For large projects, sending all code to an LLM is expensive and inefficient. **TOON (Token Oriented Object Notation)** extracts only the semantic "skeleton" of your code (classes, signatures, docstrings), ignoring implementations.

```sh
deepbase . --toon
# or
deepbase . -t
```
*Result: LLMs understand your architecture using minimal tokens.*

### 3. Hybrid Mode (Focus)

This is the power user feature. You can provide the TOON skeleton for the entire project (background context) while focusing on specific files (full content).

**Focus via CLI:**
Use `-f` or `--focus` with glob patterns (e.g., `*auth*`, `src/utils/*`).

```sh
deepbase . --toon --focus "server/controllers/*" --focus "client/src/login.js"
```

**Focus via File:**
Instead of typing patterns every time, create a text file (e.g., `context_task.txt`) with the list of files/folders you are working on.

*content of `context_task.txt`:*
```text
server/routes/auth.js
server/models/User.js
client/src/components/LoginForm.jsx
```

Run deepbase loading the file:
```sh
deepbase . --toon --focus-file context_task.txt
```

### 4. Single File Analysis

DeepBase supports analyzing a single specific file.

**Structure Only (Default)**
Extracts only the outline/headers. Useful for large documentation files.

```sh
deepbase README.md
```

**Structure + Content**
Appends the full content after the structure.

```sh
deepbase README.md --all
```

### Configuration (.deepbase.toml)

You can customize behavior by creating a `.deepbase.toml` file in your project root:

```toml
ignore_dirs = ["my_assets", "experimental"]
significant_extensions = [".cfg", "Makefile", ".tsx"]
```

## Development Workflow

If you want to contribute or test the tool locally:

```sh
# Install in editable mode
pip install -e ".[dev]"

# Run tests
pytest
```

## License

This project is released under the GPL 3 license. See the `LICENSE` file for details.
```