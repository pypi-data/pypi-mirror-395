# soar/encryptor.py
import os
import hashlib
from soar.fingerprint import get_fingerprint
from soar.utils import backup_file

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

MAGIC = b"SOAR0001"
FP_LEN = 64
IV_LEN = 16

# ==================================================
# 🔐 Rust derive_key() 的完全同步版本
# ==================================================
BASE_KEY = b"dawali-2025!@#-soar-locker-key"
SECRET_KEY = hashlib.sha256(BASE_KEY).digest()      # 32 bytes AES256 key
# ==================================================


def encrypt_bytes(data: bytes):
    """使用 AES-256-CBC + PKCS7 加密，与 Rust decrypt 完全对齐"""
    iv = os.urandom(IV_LEN)
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv)).encryptor()

    padder = PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()

    ciphertext = cipher.update(padded) + cipher.finalize()
    return iv, ciphertext


def encrypt_file(path: str):
    """加密单个 .py 文件并生成 .soa 文件"""
    if not path.endswith(".py"):
        return

    root = os.path.dirname(path)

    with open(path, "rb") as f:
        src = f.read()

    # 备份原始源码
    backup_file(path, root)

    iv, cipher = encrypt_bytes(src)

    # fingerprint: Rust verify_fingerprint() 校验
    fp = get_fingerprint().encode()  # 必须长度 = 64

    blob = MAGIC + fp + iv + cipher

    out = path[:-3] + ".soa"
    with open(out, "wb") as f:
        f.write(blob)

    print(f"Encrypted: {path} → {out}")
