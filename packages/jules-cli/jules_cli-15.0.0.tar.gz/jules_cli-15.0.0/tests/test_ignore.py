import os
import pytest
from jules_cli.utils.ignore import ContextFilter, collect_context_files

def test_context_filter_respects_ignore_file(tmp_path):
    # Setup
    (tmp_path / ".julesignore").write_text("*.log\nnode_modules/\nsecret.txt\nbuild/output/")
    (tmp_path / "app.py").write_text("print('hello')")
    (tmp_path / "error.log").write_text("error")
    (tmp_path / "secret.txt").write_text("secret")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "pkg.json").write_text("{}")

    (tmp_path / "build").mkdir()
    (tmp_path / "build" / "output").mkdir()
    (tmp_path / "build" / "output" / "bin").write_text("binary")

    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "node_modules").mkdir() # Should be ignored because "node_modules/" matches anywhere
    (tmp_path / "src" / "node_modules" / "inner.txt").write_text("inner")

    # Execution using collect_context_files to test integration
    # We pass str(tmp_path) as root
    files = collect_context_files(root_path=str(tmp_path))

    # Assertion
    # files should already be relative paths

    assert "app.py" in files
    assert "error.log" not in files
    assert "secret.txt" not in files
    assert "node_modules/pkg.json" not in files

    # Nested dir check
    assert "build/output/bin" not in files

    # Recursive dir check
    assert "src/node_modules/inner.txt" not in files
