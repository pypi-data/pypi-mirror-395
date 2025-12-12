# soar/fingerprint.py
import hashlib
import platform
import sys

# ---------------------------
# Windows machine GUID
# ---------------------------
def _machine_id_win():
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Cryptography"
        )
        val, _ = winreg.QueryValueEx(key, "MachineGuid")
        return val
    except:
        return "no-win-guid"

# ---------------------------
# Linux /etc/machine-id
# ---------------------------
def _machine_id_linux():
    try:
        with open("/etc/machine-id") as f:
            return f.read().strip()
    except:
        return "no-linux-mid"


def get_machine_id():
    if sys.platform.startswith("win"):
        return _machine_id_win()
    return _machine_id_linux()

# ---------------------------
# CPU Serial（完全对齐 Rust）
# ---------------------------
def get_cpu_serial():
    try:
        if sys.platform.startswith("linux"):
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "Serial" in line:
                        return line.split(":")[1].strip()
            return "no-serial"

        # Windows CPU Identifier
        cpu = platform.processor()
        if not cpu:
            return "no-win-cpu"
        return cpu
    except:
        return "cpu-unknown"

# ---------------------------
# FINAL FINGERPRINT
# ---------------------------
def get_fingerprint() -> str:
    raw = (get_machine_id() + get_cpu_serial()).encode()
    return hashlib.sha256(raw).hexdigest()
