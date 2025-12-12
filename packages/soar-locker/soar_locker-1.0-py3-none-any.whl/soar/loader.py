# soar/loader.py
import sys
import os
import importlib.abc
import importlib.util
from soar_core import verify_fingerprint, decrypt_blob

MAGIC = b"SOAR0001"
FP_LEN = 64
IV_LEN = 16

class SoarLoader(importlib.abc.Loader):
    def __init__(self, fullname, path):
        self.fullname = fullname
        self.path = path

    def _read_blob(self):
        with open(self.path, "rb") as f:
            data = f.read()

        if not data.startswith(MAGIC):
            raise RuntimeError("Invalid SOAR archive header")

        idx = len(MAGIC)
        fp = data[idx:idx + FP_LEN].decode()
        if len(fp) != 64:
            raise RuntimeError("Corrupted SOAR fingerprint")

        idx += FP_LEN
        iv = data[idx:idx + IV_LEN]
        if len(iv) != IV_LEN:
            raise RuntimeError("Corrupted SOAR IV")

        cipher = data[idx + IV_LEN:]
        if len(cipher) == 0:
            raise RuntimeError("Corrupted SOAR archive payload")

        return fp, iv, cipher

    def exec_module(self, module):
        fp, iv, cipher = self._read_blob()

        # 🔐 Rust-level verification
        verify_fingerprint(fp)

        # 🔐 Rust AES decrypt
        plain = decrypt_blob(cipher, iv)

        code = compile(plain.decode(), self.path, "exec")
        exec(code, module.__dict__)


class SoarFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if path is None:
            path = sys.path
        name = fullname.split(".")[-1]

        for base in path:
            p = os.path.join(base, name + ".soa")
            if os.path.exists(p):
                loader = SoarLoader(fullname, p)
                return importlib.util.spec_from_loader(fullname, loader)

        return None
