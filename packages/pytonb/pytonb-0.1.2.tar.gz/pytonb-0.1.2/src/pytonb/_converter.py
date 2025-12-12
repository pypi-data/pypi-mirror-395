#!/usr/bin/env python

# In[1]:


# imports
import ast
import json
import os
import re
import time
import types
from fnmatch import fnmatch

# In[2]:


# constants
ast_types = {
    ast.ImportFrom: "import",
    ast.Import: "import",
    ast.FunctionDef: "function",
    ast.Assign: "assignment",
    ast.Expr: "expression",
    ast.ClassDef: "class",
    ast.If: "if statement",
    ast.For: "for statement",
    ast.While: "while statement",
}
metadata = {
    "kernelspec": {
        "display_name": "Python 3 (ipykernel)",
        "language": "python",
        "name": "python3",
    },
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.13.0",
    },
}
NBFORMAT = 4
NBFORMAT_MINOR = 5
EXCLUDED = ["#!/usr/bin/env python", "# coding: utf-8"]


# In[3]:


# helpers


# In[4]:


def _get_files(
    folder: str,
    level: int = 0,
    exclude: str = None,
    include: str = None,
    ignore_hidden=True,
    vb=0,
):
    """recursively traverse subfolders and return files, ignoring hidden files"""
    if exclude is None:
        exclude = ""
    if include is None:
        include = "*"

    def __get_files(folder, level, current_level):
        if current_level > level:
            return []
        files = []
        try:
            for f in os.listdir(folder):
                if ignore_hidden and f.startswith("."):
                    continue
                fp = os.path.join(folder, f)
                if os.path.isdir(fp):
                    files.extend(__get_files(fp, level, current_level + 1))
                elif fnmatch(f, include) and not fnmatch(f, exclude):
                    files.append(fp)
        except PermissionError:
            pass
        return files

    return __get_files(folder, level, current_level=0)


# In[ ]:


# In[5]:


def _check_params(nb_path, py_path, overwrite):
    name, ext = os.path.splitext(nb_path)
    if not ext == ".ipynb":
        print(f"expected nb_path to have ipynb extension but got {ext}")
        return None, None, None
    if not os.path.isfile(nb_path):
        print(f"not a file: {nb_path}")
        return None, None, None
    if not py_path:
        py_path = name + ".py"
    if not overwrite and os.path.isfile(py_path):
        print(f"{py_path} exists, set overwrite to True to overwrite it")
        return None, None, None
    return nb_path, py_path, overwrite


# In[6]:


def _parse_code(t):
    """use ast to parse code into comments and code sections"""
    end = 0
    code = []
    try:
        tree = ast.parse(t)
    except (SyntaxError, IndentationError) as exc:
        raise ValueError(f"unable to parse source: {exc}") from exc
    for n in ast.iter_child_nodes(tree):
        if end != n.lineno - 1:
            c = t.splitlines()[end : n.lineno - 1]
            code.append({"source": c, "cell_type": "comment", "type": "comment"})
        c = t.splitlines()[n.lineno - 1 : n.end_lineno + 1]
        code.append(
            {
                "source": c,
                "cell_type": "code",
                "type": ast_types[n.__class__],
                "position": (n.lineno - 1, n.end_lineno + 1),
            }
        )
        end = n.end_lineno
        if n.col_offset != 0:
            raise ValueError(
                f"Expected top-level statement at line {n.lineno}, found column offset {n.col_offset}"
            )
    return code


# In[7]:


def _collapse_list(ls):
    """join the source value of a list of dicts"""
    return "\n".join(["\n".join(d["source"]) for d in ls])


# In[8]:


def _split_list(ls: list, dl: object | types.FunctionType) -> list[list]:
    """use a delimiter to split a list into sublists"""
    if not isinstance(dl, types.FunctionType):
        marker = dl
        dl = lambda x, target=marker: x == target
    res, b = [], []
    for el in ls:
        if dl(el) and b:
            res.append(b)
            res.append([el])  # keep delimiters in the list
            b = []
        else:
            b.append(el)
    if b:
        res.append(b)
    return res


# In[6]:


def _get_blocks(t: str) -> list[tuple]:
    """return list of ('code' or 'markdown', code block:str, (start, end))"""
    lines = t.splitlines()
    i, blocks, n = 0, [], len(lines)
    while i < n:
        md = False
        start = i
        while i < n and lines[i].strip().startswith("#"):  # comment
            if lines[i].strip().startswith("# #"):
                md = True
            i += 1
        if md:
            rt = lambda x: "#" if x.group() == "# #" else ""
            cb = [re.sub("^# #|^# ", rt, line, count=1) for line in lines[start:i]]
            blocks.append(("markdown", "\n".join(cb), (start, i)))
            start = i
        else:
            i = start
        while i < n and not lines[i].strip().startswith("# #"):
            i += 1
        if start < i:
            blocks.append(("code", "\n".join(lines[start:i]), (start, i)))
    blocks = blocks[1:] if blocks and not blocks[0][1] else blocks
    blocks = [(a, b.rstrip("\n\n"), c) for a, b, c in blocks]
    return blocks


# In[ ]:


# In[10]:


# main functions


# In[16]:


def write_notebook(
    path: str, save_name=None, write=True, return_cells=False, use_ast=False, vb=0
) -> dict:
    """get notebook dict from .py code string"""
    name, ext = os.path.splitext(path)
    if not os.path.isfile(path):
        print(f"not a file: {path}")
        return
    if not path.endswith(".py"):
        print(f"expected path to have .py extension but got {ext}")
        return

    try:
        with open(path) as f:
            t = f.read()
    except Exception as e:
        print(f"error opening {path}: {str(e)}")
        return
    if write and not save_name:
        save_name = name + ".ipynb"

    cells = []
    cs = re.split(r"# In\[(\d+| )\]:\s+\n", t)
    if len(cs) > 1 and not use_ast:  # we have markers
        # interpret each section as either comment or code
        for c1, c2 in zip(
            cs[1::2], cs[2::2]
        ):  # we ignore the first section (shebang line or empty)
            ex = None if not c1.strip() else int(c1)
            c2 = c2.strip("\n")
            c2 = _get_blocks(c2)
            # a marker is always followed by a cell, even if its empty
            c2 = c2 if c2 else [["code", "", ""]]
            for t, c, p in c2:
                c1 = c.splitlines()
                c = [
                    line + "\n" if i + 1 < len(c1) else line
                    for i, line in enumerate(c1)
                ]
                if vb > 3:
                    print(c)
                if t == "markdown":
                    cell = {
                        "source": c,
                        "cell_type": t,
                        "id": "00000000-0000-0000-0000-000000000000",
                        "metadata": {},
                    }
                else:
                    cell = {
                        "source": c,
                        "cell_type": t,
                        "execution_count": 0 if t == "markdown" else ex,
                        "id": "00000000-0000-0000-0000-000000000000",
                        "metadata": {},
                        "outputs": [],
                    }
                cells.append(cell)
    else:  # no markers, try to put each function into a separate cell
        t = "\n".join([line for line in t.splitlines() if line not in EXCLUDED])
        # get blocks
        bls = _get_blocks(t)
        for bl in bls:
            k, s, p = bl
            if k == "markdown":
                cell = {
                    "source": s,
                    "cell_type": k,
                    "id": "00000000-0000-0000-0000-000000000000",
                    "metadata": {},
                }
                cells.append(cell)
                continue
            # parse, split functions
            pc = _parse_code(s)
            sl = _split_list(pc, dl=lambda x: x["type"] == "function")
            for cl in sl:
                # normalize blocks for collapse helper
                normalized = []
                for block in cl:
                    if isinstance(block, dict):
                        normalized.append(block)
                    else:
                        normalized.append({"source": [str(block)]})
                if vb > 3:
                    print(normalized)
                try:
                    c = _collapse_list(normalized).strip("\n\n")
                    t = "code"
                    cell = {
                        "source": c,
                        "cell_type": t,
                        "execution_count": 0,
                        "id": "00000000-0000-0000-0000-000000000000",
                        "metadata": {},
                        "outputs": [],
                    }
                    cells.append(cell)
                except Exception as e:
                    print(cl)
                    print(e)
    if return_cells:
        return cells
    jsn = {
        "cells": cells,
        "metadata": metadata,
        "nbformat": NBFORMAT,
        "nbformat_minor": NBFORMAT_MINOR,
    }
    if write:
        json.dump(jsn, open(save_name, "w"))
    return {
        "cells": cells,
        "metadata": metadata,
        "nbformat": NBFORMAT,
        "nbformat_minor": NBFORMAT_MINOR,
    }


# In[22]:


def write_script(nb_path, save_name=None, overwrite=True, vb=0):
    """save notebook as python script"""
    nb_path, py_path, overwrite = _check_params(nb_path, save_name, overwrite)
    if nb_path is None:
        return
    with open(nb_path) as f:
        c = json.load(f)
    ret = []
    ret.append("\n".join(EXCLUDED))
    for cell in c["cells"]:
        ex = cell.get("execution_count", " ")
        ex = ex if ex else " "
        k = cell["cell_type"]
        s = cell["source"]
        if isinstance(s, str):
            if vb > 1:
                print("legacy cell: creating list from string")
            s = s.split("\n")
            if s:
                s = [f + "\n" for f in s[:-1]] + [s[-1]]
        if k == "markdown":
            s = ["# " + line for line in s]
        elif k == "code":
            s = [f"# In[{ex}]:\n\n\n"] + s + ["\n"]
        b = "".join(s)
        ret.append("\n" + b)  # .strip('\n'))
    code = "\n".join(ret) + "\n"
    with open(py_path, "w") as f:
        f.write(code)


# In[13]:


def sync_folder(
    folder: str,
    recursion_level: int = 0,
    include="*.ipynb",
    exclude=None,
    ignore_hidden=True,
    delay=3,
    vb=0,
):
    import threading

    nbs = _get_files(
        folder, level=recursion_level, exclude=exclude, include=include, vb=vb
    )
    e = threading.Event()
    for file in nbs:
        sync(nb_path=file, event=e, delay=delay, vb=vb)
    return e


# In[ ]:


# In[14]:


def sync(nb_path, py_path=None, delay=3, event=None, ignore_hidden=True, vb=0):
    """keep py file synced with nb file (one way nb->py)"""
    nb_path, py_path, _ = _check_params(nb_path, py_path, True)
    if not nb_path:
        return
    import threading

    def st(nb_path, py_path, delay, event, vb):
        name = os.path.relpath(nb_path)
        lt = os.path.getmtime(nb_path)
        if vb:
            print(f"syncing {name}")
        while not event.is_set():
            if vb > 2:
                print("sleeping")
            time.sleep(delay)
            if vb > 2:
                print("comparing...")
            ct = os.path.getmtime(nb_path)
            if ct != lt:
                if vb > 1:
                    print(f"writing {nb_path}...")
                write_script(nb_path, py_path, overwrite=True)
                lt = ct
        else:
            if vb:
                print(f"sync stopped for {name}")

    event = event if event else threading.Event()
    t = threading.Thread(target=st, args=(nb_path, py_path, delay, event, vb))
    t.daemon = True  # exit thread when main program exits
    t.start()
    return event


# In[ ]:
