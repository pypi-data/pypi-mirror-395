# soar/walker.py
import os

IGNORE = {"__pycache__", ".git", ".idea", "venv", ".venv", "bak"}

def iter_py_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE]
        for f in filenames:
            if f.endswith(".py"):
                yield os.path.join(dirpath, f)
