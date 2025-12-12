# soar/cli.py
import argparse
import os
import sys
import types
import time

from soar.encryptor import encrypt_file
from soar.loader import SoarLoader, SoarFinder
from soar import check_version

# ----------------------------- 颜色定义 -----------------------------
RED = "\033[91m"
GRN = "\033[92m"
YLW = "\033[93m"
BLU = "\033[94m"
RST = "\033[0m"
CYA = '\033[96m'
MAG = '\033[95m'
WHT = '\033[97m'

VERSION = "1.0"


import unicodedata

def _disp_len(s: str) -> int:
    """按终端显示宽度统计长度：全角/宽字符算 2，其它算 1"""
    l = 0
    for ch in s:
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            l += 2
        else:
            l += 1
    return l

def _pad_disp(s: str, width: int) -> str:
    """根据显示宽度右侧补空格"""
    cur = _disp_len(s)
    if cur >= width:
        return s
    return s + " " * (width - cur)

def print_warning():
    # 目标显示宽度（两栏各自宽度，包含内容不含边框）
    left_width = 38
    right_width = 40

    left_lines = [
        "[警告] SOAR 加密系统并非军事级或商业级保护系统",
        "",
        "适用于：",
        "- 基础代码混淆",
        "- 防止随意复制",
        "- 绑定单台设备",
        "- 教学/轻量级保护",
        "",
        "限制：",
        "- 无法抵御专业逆向工程",
        "- 无法保护高价值算法",
        "- 无法防御强力攻击",
        "- 不应作为唯一商业保护方案",
        "",
        "商业级保护建议：",
        "- C/C++/Rust 加载器",
        "- 原生二进制加密",
        "- 硬件密钥存储",
        "- 专业混淆服务",
        "",
        "[SOAR] 使用代表风险自担",
    ]

    right_lines = [
        "[WARNING] SOAR is NOT a military /",
        "commercial-grade protection system.",
        "",
        "Intended for:",
        "- Simple code obfuscation",
        "- Preventing casual copying",
        "- Binding to one machine",
        "- Education / light protection",
        "",
        "Limitations:",
        "- Cannot resist professionals",
        "- Not for high-value algorithms",
        "- Cannot stop strong attackers",
        "- Not sole protection in products",
        "",
        "For real protection, consider:",
        "- C/C++/Rust loaders",
        "- Native binary encryption",
        "- Hardware key storage",
        "- Professional obfuscation",
        "",
        "[SOAR] Use at your own risk",
    ]

    # 行数对齐
    max_rows = max(len(left_lines), len(right_lines))
    left_lines += [""] * (max_rows - len(left_lines))
    right_lines += [""] * (max_rows - len(right_lines))

    top = f"{YLW}╔{'═' * (left_width + 2)}╦{'═' * (right_width + 2)}╗{RST}"
    bottom = f"{YLW}╚{'═' * (left_width + 2)}╩{'═' * (right_width + 2)}╝{RST}"
    print()
    print(top)
    for l, r in zip(left_lines, right_lines):
        l_p = _pad_disp(l, left_width)
        r_p = _pad_disp(r, right_width)
        print(f"{YLW}║ {l_p} ║ {r_p} ║{RST}")
    print(bottom)
    print()


# ----------------------------- Logo -----------------------------
def print_logo():
    logo = f"""
{BLU}    ╔═══════════════════════════════════════════════════════════╗
    ║  ███████╗ ██████╗  █████╗ ██████╗     {GRN}██████╗  █████╗ ██████╗  ║
    ║  ██╔════╝██╔═══██╗██╔══██╗██╔══██╗    {GRN}██╔══██╗██╔══██╗██╔══██╗ ║
    ║  ███████╗██║   ██║███████║██████╔╝    {GRN}██████╔╝███████║██████╔╝ ║
    ║  ╚════██║██║   ██║██╔══██║██╔══██╗    {GRN}██╔══██╗██╔══██║██╔══██╗ ║
    ║  ███████║╚██████╔╝██║  ██║██║  ██║    {GRN}██║  ██║██║  ██║██║  ██║ ║
    ║  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    {GRN}╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ║
    ╠═══════════════════════════════════════════════════════════╣
    ║  {CYA}Secure Obfuscated Archives Repository (SOAR) v{VERSION}  ║
    ╚═══════════════════════════════════════════════════════════╝{RST}
"""
    print(logo)


# ----------------------------- 加载动画 -----------------------------
def loading_animation(duration, message="加载中 / Loading"):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start_time = time.time()
    idx = 0
    while time.time() - start_time < duration:
        print(f"\r{CYA}{message} {frames[idx]}{RST}", end="", flush=True)
        idx = (idx + 1) % len(frames)
        time.sleep(0.09)
    print(f"\r{GRN}{message} ✓{RST}")


# ----------------------------- loader 注入 -----------------------------
def enable_loader():
    if not any(isinstance(f, SoarFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, SoarFinder())

# ----------------------------- bak 检查 -----------------------------
def is_in_bak(path):
    p = os.path.abspath(path).lower()
    return "\\bak\\" in p or "/bak/" in p or p.endswith("\\bak") or p.endswith("/bak")

# ----------------------------- 主逻辑 -----------------------------
def cmd_auto(args):
    target = os.path.abspath(args.target)

    # -----------------------------
    # 执行 .soa → 纯净模式，无更新检查，无 logo
    # -----------------------------
    if os.path.isfile(target) and target.endswith(".soa"):
        enable_loader()

        current_dir = os.path.dirname(target)
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)

        module = types.ModuleType("__main__")
        module.__file__ = target
        module.__package__ = None
        loader = SoarLoader("__main__", target)
        loader.exec_module(module)
        return

    # -----------------------------
    # 其它情况 = 加密模式（需要显示 logo、检查更新）
    # ----------------------------- 
    print_logo()
    loading_animation(1.2, "检查环境 / Checking environment")
    print_warning()

    # -------------------------
    # 检查 bak 目录
    # -------------------------
    if is_in_bak(target):
        print(f"{RED}[SOAR] ERROR: 当前位于 bak 目录，不允许加密或执行。{RST}")
        return

    # -------------------------
    # 单文件 .py → 加密
    # -------------------------
    if os.path.isfile(target) and target.endswith(".py"):
        loading_animation(0.938, "生成密钥 / Deriving key")

        # 模拟复杂加密过程
        print(f"{BLU}[SOAR] Encrypting file...{RST}")
        import random
        steps = 20
        for i in range(steps):
            bar = "#" * (i+1) + "-" * (steps-i-1)
            percent = int((i+1)/steps*100)
            print(f"\r[{bar}] {percent}%", end="", flush=True)
            time.sleep(random.uniform(0.02, 0.09))
        print()

        encrypt_file(target)
        print(f"{GRN}[SOAR] Encryption complete.{RST}")
        return

    # -------------------------
    # 目录 → 批量加密
    # -------------------------
    if os.path.isdir(target):
        loading_animation(0.92, "生成密钥 / Deriving key")
        py_files = []
        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d.lower() != "bak"]
            for f in files:
                if f.endswith(".py"):
                    py_files.append(os.path.join(root, f))

        if not py_files:
            print(f"{YLW}[SOAR] No Python files found.{RST}")
            return

        print(f"{BLU}[SOAR] Encrypting {len(py_files)} files...{RST}")

        import random
        steps = 25
        for i in range(steps):
            bar = "#" * (i+1) + "-" * (steps-i-1)
            percent = int((i+1)/steps*100)
            print(f"\r[{bar}] {percent}%", end="", flush=True)
            time.sleep(random.uniform(0.03, 0.1))
        print()

        for f in py_files:
            encrypt_file(f)

        print(f"{GRN}[SOAR] Directory encryption complete.{RST}")
        check_version() 
        time.sleep(1)
        return

    print(f"{RED}[SOAR] Unsupported target:{RST}", target)


# ----------------------------- CLI -----------------------------
def build():
    parser = argparse.ArgumentParser(
        prog="soar",
        description=(
            "SOAR - Secure Obfuscated Archives Repository\n"
            "安全加密与设备绑定执行系统"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="输入文件或目录\nfile.py / file.soa / directory"
    )

    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="显示当前 SOAR 版本 / Show version"
    )

    # ❗ 不要添加 -h/--help，argparse 自动管理
    return parser


def main():
    parser = build()
    args = parser.parse_args()

    # -----------------------------
    # 版本输出
    # -----------------------------
    if args.version:
        print(f"SOAR version {VERSION}")
        print("Secure Obfuscated Archives Repository 加密执行框架")
        return

    cmd_auto(args)
