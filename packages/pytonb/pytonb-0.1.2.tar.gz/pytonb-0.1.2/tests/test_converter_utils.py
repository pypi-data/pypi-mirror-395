import json
import textwrap
import time
import threading
from pathlib import Path

import pytest

from pytonb import write_notebook, write_script
from pytonb import _converter as converter


def test_get_files_filters_hidden_and_respects_patterns(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    nested = root / "nested"
    nested.mkdir()

    visible = nested / "note.ipynb"
    visible.write_text("{}", encoding="utf-8")

    # should be excluded due to pattern/hidden rules
    hidden_dir = root / ".hidden"
    hidden_dir.mkdir()
    (hidden_dir / "ignored.ipynb").write_text("{}", encoding="utf-8")
    (nested / "ignore.txt").write_text("{}", encoding="utf-8")

    files = converter._get_files(
        str(root), level=1, include="*.ipynb", exclude="ignored.ipynb"
    )
    files = {Path(f) for f in files}

    assert visible in files
    assert all("ignored" not in f.name for f in files)
    assert all(not f.name.startswith(".") for f in files)


def test_check_params_validation_paths(tmp_path, capsys):
    wrong_ext = tmp_path / "bad.txt"
    wrong_ext.write_text("content", encoding="utf-8")

    res = converter._check_params(str(wrong_ext), None, overwrite=True)
    assert res == (None, None, None)
    out = capsys.readouterr().out
    assert "expected nb_path to have ipynb extension" in out

    missing = tmp_path / "missing.ipynb"
    res = converter._check_params(str(missing), None, overwrite=True)
    assert res == (None, None, None)
    out = capsys.readouterr().out
    assert "not a file" in out

    nb_file = tmp_path / "good.ipynb"
    nb_file.write_text("{}", encoding="utf-8")
    py_file = tmp_path / "good.py"
    py_file.write_text("# existing", encoding="utf-8")

    res = converter._check_params(str(nb_file), str(py_file), overwrite=False)
    assert res == (None, None, None)
    out = capsys.readouterr().out
    assert "exists, set overwrite to True" in out

    res = converter._check_params(str(nb_file), None, overwrite=True)
    assert res == (str(nb_file), str(nb_file.with_suffix(".py")), True)


def test_parse_code_handles_blocks_and_invalid_indent():
    source = textwrap.dedent(
        """
        import os

        def top_level():
            return 1

        value = 3
        """
    ).strip()

    blocks = converter._parse_code(source)
    # verify we captured both function and assignment segments
    kinds = [b["type"] for b in blocks]
    assert "function" in kinds
    assert "assignment" in kinds

    bad_source = "  def not_allowed():\n        return 0\n"
    with pytest.raises(ValueError):
        converter._parse_code(bad_source)


def test_split_and_collapse_helpers():
    parts = converter._split_list(["a", "---", "b", "c", "---", "d"], "---")
    assert parts == [["a"], ["---"], ["b", "c"], ["---"], ["d"]]

    collapsed = converter._collapse_list(
        [{"source": ["line1", "line2"]}, {"source": ["line3"]}]
    )
    assert collapsed == "line1\nline2\nline3"


def test_get_blocks_detects_markdown_and_code():
    text = textwrap.dedent(
        """
        # # Heading
        # Some description
        print("hello")

        # # Follow up
        value = 42
        """
    ).strip()

    blocks = converter._get_blocks(text)
    kinds = [k for k, *_ in blocks]
    assert "markdown" in kinds
    assert "code" in kinds

    # markdown block should have stripped comment prefixes
    markdown_block = next(k for k in blocks if k[0] == "markdown")
    assert "Heading" in markdown_block[1]
    assert "Some description" in markdown_block[1]


def test_write_notebook_without_markers_returns_cells(tmp_path):
    script = tmp_path / "sample.py"
    script.write_text(
        textwrap.dedent(
            """
            #!/usr/bin/env python
            # coding: utf-8

            # # Title
            # intro text

            def add(a, b):
                return a + b

            class Greeter:
                pass
            """
        ),
        encoding="utf-8",
    )

    cells = write_notebook(
        str(script), save_name=None, write=False, return_cells=True, use_ast=False
    )
    assert any(cell["cell_type"] == "markdown" for cell in cells)
    assert any(cell["cell_type"] == "code" for cell in cells)

    # error paths: wrong extension and missing file
    bad_ext = script.with_suffix(".txt")
    bad_ext.write_text("print('bad extension')", encoding="utf-8")
    assert (
        write_notebook(str(bad_ext), write=False, return_cells=True) is None
    )
    assert (
        write_notebook(str(script.with_name("missing.py")), write=False, return_cells=True)
        is None
    )


def test_write_script_handles_string_sources(tmp_path):
    nb_path = tmp_path / "legacy.ipynb"
    py_path = tmp_path / "legacy.py"

    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "First line\\nSecond line",
            },
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": "print('hello world')\\n",
            },
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    with nb_path.open("w", encoding="utf-8") as handle:
        json.dump(notebook, handle)

    write_script(str(nb_path), save_name=str(py_path), overwrite=True, vb=2)

    content = py_path.read_text(encoding="utf-8")
    assert "# In[1]" in content
    assert "# First line" in content
    assert "print('hello world')" in content


def test_get_files_handles_permission_error(monkeypatch, tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    blocked = root / "blocked"
    blocked.mkdir()
    allowed = root / "allowed"
    allowed.mkdir()
    allowed_file = allowed / "file.ipynb"
    allowed_file.write_text("{}", encoding="utf-8")

    original_listdir = converter.os.listdir

    def fake_listdir(path):
        if path == str(blocked):
            raise PermissionError("blocked")
        return original_listdir(path)

    monkeypatch.setattr(converter.os, "listdir", fake_listdir)

    files = converter._get_files(str(root), level=2, include=None, exclude=None)
    assert Path(allowed_file) in {Path(f) for f in files}


def test_parse_code_rejects_offset(monkeypatch):
    class FakeNode:
        lineno = 1
        end_lineno = 1
        col_offset = 1

    fake_node = FakeNode()

    monkeypatch.setattr(converter.ast, "iter_child_nodes", lambda tree: [fake_node])
    converter.ast_types[FakeNode] = "fake"
    try:
        with pytest.raises(ValueError, match="Expected top-level statement"):
            converter._parse_code("value = 1")
    finally:
        converter.ast_types.pop(FakeNode, None)


def test_write_notebook_handles_open_error(monkeypatch, tmp_path, capsys):
    script = tmp_path / "problem.py"
    script.write_text("print('hi')\n", encoding="utf-8")

    import builtins

    real_open = builtins.open

    def fake_open(path, *args, **kwargs):
        if path == str(script):
            raise OSError("boom")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", fake_open)

    assert write_notebook(str(script)) is None
    out = capsys.readouterr().out
    assert "error opening" in out


def test_write_notebook_sets_default_save_name(tmp_path):
    script = tmp_path / "fresh.py"
    script.write_text("# In[1]:\n\nprint('ok')\n", encoding="utf-8")

    write_notebook(str(script))

    created = tmp_path / "fresh.ipynb"
    assert created.exists()


def test_write_notebook_verbose_with_markers(tmp_path, capsys):
    script = tmp_path / "verbose_markers.py"
    script.write_text("# In[1]:\n\nprint('marker')\n", encoding="utf-8")

    write_notebook(str(script), write=False, vb=4)
    out = capsys.readouterr().out
    assert "marker" in out


def test_write_notebook_verbose_ast_path(tmp_path, capsys):
    script = tmp_path / "verbose_ast.py"
    script.write_text(
        textwrap.dedent(
            """
            #!/usr/bin/env python
            # coding: utf-8

            def hello():
                return 'hello'
            """
        ),
        encoding="utf-8",
    )

    write_notebook(str(script), write=False, vb=4, use_ast=False)
    out = capsys.readouterr().out
    assert "hello" in out


def test_write_notebook_handles_collapse_failure(monkeypatch, tmp_path, capsys):
    script = tmp_path / "collapse.py"
    script.write_text(
        textwrap.dedent(
            """
            def foo():
                return 1
            """
        ),
        encoding="utf-8",
    )

    def raising_collapse(*_args, **_kwargs):
        raise RuntimeError("collapse failure")

    monkeypatch.setattr(converter, "_collapse_list", raising_collapse)

    write_notebook(str(script), write=False, use_ast=False, vb=0)
    out = capsys.readouterr().out
    assert "collapse failure" in out


def test_write_notebook_normalizes_non_dict_blocks(monkeypatch, tmp_path):
    script = tmp_path / "normalize.py"
    script.write_text(
        textwrap.dedent(
            """
            def foo():
                return 1
            """
        ),
        encoding="utf-8",
    )

    def fake_split_list(ls, dl):
        return [[{"source": ["def foo():", "    return 1"]}], ["notadict"]]

    monkeypatch.setattr(converter, "_split_list", fake_split_list)
    cells = write_notebook(
        str(script), save_name=None, write=False, return_cells=True, use_ast=False
    )
    assert any("foo" in "".join(cell["source"]) for cell in cells)


def test_write_script_returns_when_invalid_path(capsys):
    write_script("invalid.txt")
    out = capsys.readouterr().out
    assert "expected nb_path" in out


def test_sync_verbose_reports_changes(tmp_path, capsys):
    nb_path = tmp_path / "sync.ipynb"
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": ["print('sync')\n"],
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    with nb_path.open("w", encoding="utf-8") as handle:
        json.dump(notebook, handle)

    event = threading.Event()
    converter.sync(str(nb_path), delay=0.05, event=event, vb=3)

    time.sleep(0.1)

    notebook["cells"][0]["source"] = ["print('changed')\n"]
    with nb_path.open("w", encoding="utf-8") as handle:
        json.dump(notebook, handle)

    time.sleep(0.1)
    event.set()
    time.sleep(0.1)

    out = capsys.readouterr().out
    assert "sleeping" in out
    assert "writing" in out
