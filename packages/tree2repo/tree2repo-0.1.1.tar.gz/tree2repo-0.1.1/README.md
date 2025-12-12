# tree2repo

Create a project directory structure from a pasted tree printed by a tool, an editor, or an AI model.

Instead of clicking `New folder` fifty times, you paste a tree and let this tool create all folders and files for you.

---

## Features

- Paste a simple indented tree and turn it into real folders and files.
- Ignores the first top-level label by default, so you can paste from inside the project root without nesting.
- Optional flag to respect the top-level label and create that folder too.
- Tiny Python API if you want to generate structures programmatically.

---

## Installation

```bash
pip install tree2repo
```

---

## Basic usage

Assume you are inside a directory where you want to generate your project:

```bash
cd my_project_root

tree2repo << 'EOF'
my_project_root/
  src/
    my_package/
      __init__.py
      core.py
  tests/
    test_core.py
  README.md
  pyproject.toml
EOF
```

Result:

- The top-level label line `my_project_root/` is ignored by default.
- Inside `my_project_root` you will now have:

```python
src/
  my_package/
    __init__.py
    core.py
tests/
  test_core.py
README.md
pyproject.toml
```

This is ideal when you get a tree for a repository but you are already standing at the intended root.

---

## Respecting the top-level folder

If you actually want the top-level folder to be created, use `--respect-root`:

```bash
cd /tmp

tree2repo --respect-root << 'EOF'
my_project_root/
  src/
    my_package/
      __init__.py
      core.py
  tests/
    test_core.py
  README.md
  pyproject.toml
EOF
```

Now you get:

```bash
my_project_root/
  src/
    my_package/
      __init__.py
      core.py
  tests/
    test_core.py
  README.md
  pyproject.toml
```

---

## Choosing a different root directory

You can tell tree2repo to create the structure somewhere else using `--root`:

```bash
tree2repo --root /tmp/new_project << 'EOF'
my_project_root/
  src/
    my_package/
      __init__.py
      core.py
  README.md
EOF
```

With default settings, the top-level label is ignored, so the files end up directly under `/tmp/new_project`.

---

## Tree format

tree2repo expects a very simple, whitespace-indented format:

- Each line is a file or directory.
- Indentation is spaces only.
- Directories end with a forward slash `/`.
- Files have no trailing slash.

Example:

```bash
my_project_root/
  src/
    my_package/
      __init__.py
      core.py
  tests/
    test_core.py
  README.md
```

Notes:

- Indentation depth is determined by the number of leading spaces.
- You can paste from editors, terminals, or any tool that prints a similar tree, as long as the indentation and trailing slashes are preserved.
- Empty lines are ignored.

---

## Python API

You can also use tree2repo directly from Python.

```python
from tree2repo import create_from_tree

tree = """my_project_root/
  src/
    my_package/
      __init__.py
      core.py
  README.md
"""


# Create under "./generated" and ignore the top-level label "my-project/"
create_from_tree(tree_text=tree, root="./generated", ignore_root_label=True)
````

Arguments:

- `tree_text`: the indented tree as a single string.
- `root`: directory where the structure should be created.
- `ignore_root_label`: when true, skips the first top-level directory label.

---

## Behavior details

- Directories are created with `mkdir(parents=True, exist_ok=True)`, so existing directories are reused.
- Files are created empty with `touch` semantics (existing files are left as they are).
- The first top-level directory line (indentation zero and ending with `/`) is treated as a label and skipped when `ignore_root_label` is true.
- If you use `--respect-root` in the CLI, `ignore_root_label` is set to false and the top-level folder is created.

---

## Examples

### 1. Generate a simple package skeleton

```bash
cd my_package_root

tree2repo << 'EOF'
example-project/
  src/
    example_package/
      __init__.py
      cli.py
  tests/
    test_cli.py
  pyproject.toml
  README.md
EOF
```

You now have a ready-made layout to start turning into a real package.

### 2. Use from within a script

```python
from tree2repo import create_from_tree

skeleton = """example-project/
  src/
    example_package/
      __init__.py
      api.py
  tests/
    test_api.py
    

create_from_tree(skeleton, root=".", ignore_root_label=True)
```

---

## Development

If you want to work on tree2repo itself:

```bash
git clone https://github.com/akshan-main/tree2repo.git
cd tree2repo

python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

pip install -e .
```

Run tests (if you add or modify them):

```bash
pytest
```

---

## Limitations and ideas

Current focus is deliberately small:

- No parsing of complex tree outputs with extra characters (`├──`, `│`, and so on).
- No built-in support for templated file contents.
- No validation that filenames are valid on all platforms.

Potential future improvements:

- Optional support for common tree output formats.
- Allow specifying file contents inline with a simple syntax.
- Predefined skeletons for common layouts (libraries, apps, tooling).

For now, tree2repo is meant to solve a very specific irritation: turning a pasted tree into a real project skeleton in a single command.
