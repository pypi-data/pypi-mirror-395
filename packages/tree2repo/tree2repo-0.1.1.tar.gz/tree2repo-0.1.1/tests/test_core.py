import shutil
from pathlib import Path

from tree2repo import create_from_tree


def test_create_from_tree(tmp_path: Path) -> None:
    tree = """project-root/
  src/
    package/
      __init__.py
  README.md
"""
    root = tmp_path / "work"
    root.mkdir()
    create_from_tree(tree, root=str(root))

    assert (root / "src" / "package" / "__init__.py").exists()
    assert (root / "README.md").exists()

    shutil.rmtree(root)
