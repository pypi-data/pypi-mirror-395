from pathlib import Path


def create_from_tree(tree_text: str, root: str = ".", ignore_root_label: bool = True) -> None:
    root_path = Path(root).resolve()
    stack = [(-1, root_path)]
    first_dir_line_skipped = False

    for raw_line in tree_text.splitlines():
        line = raw_line.rstrip("\n\r")
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip(" "))
        name = line.strip()

        if name.endswith("/"):
            is_dir = True
            name = name[:-1]
        else:
            is_dir = False

        if ignore_root_label and is_dir and indent == 0 and not first_dir_line_skipped:
            first_dir_line_skipped = True
            continue

        while stack and indent <= stack[-1][0]:
            stack.pop()

        parent = stack[-1][1] if stack else root_path
        path = parent / name

        if is_dir:
            path.mkdir(parents=True, exist_ok=True)
            stack.append((indent, path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.touch()
