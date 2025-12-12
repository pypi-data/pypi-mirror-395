# soar/utils.py
import os
import shutil

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def backup_file(src, root):
    bak_dir = os.path.join(root, "bak")
    ensure_dir(bak_dir)
    shutil.copy2(src, bak_dir)
