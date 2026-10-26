#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS301 机器学习导论 —— 实验环境自检脚本

用法：
    python check_env.py

功能：检查 Python 版本与课程所需第三方库是否已正确安装。
全部通过会输出 "环境检查通过"，有缺失则给出对应的安装命令。

说明：这是课程配套脚本，学生可直接运行；教师如需修改依赖版本，
请同时更新 COURSE_REQUIREMENTS 与 README 中的环境说明。
"""

import sys
import importlib

MIN_PYTHON = (3, 10)

# (导入名, 显示名, 最低版本, 是否必需)
COURSE_REQUIREMENTS = [
    ("numpy",      "NumPy",       "1.24", True),
    ("scipy",      "SciPy",       "1.10", True),
    ("sklearn",    "scikit-learn", "1.3", True),
    ("matplotlib", "Matplotlib",  "3.7",  True),
    ("pandas",     "pandas",      "2.0",  True),
    ("jupyter",    "Jupyter",     "1.0",  False),
    ("seaborn",    "Seaborn",     "0.12", False),
]


def parse_version(v):
    """把 '1.24.3' 转成 (1, 24, 3)，便于比较。"""
    parts = []
    for chunk in str(v).split(".")[:3]:
        digits = "".join(c for c in chunk if c.isdigit())
        parts.append(int(digits) if digits else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def check_package(import_name, display_name, min_version, required):
    try:
        module = importlib.import_module(import_name)
    except ImportError:
        return display_name, None, min_version, required, False

    installed = getattr(module, "__version__", "unknown")
    if installed == "unknown":
        return display_name, installed, min_version, required, True
    return display_name, installed, min_version, required, \
        parse_version(installed) >= parse_version(min_version)


def main():
    print("=" * 58)
    print("CS301 机器学习导论 · 实验环境自检")
    print("=" * 58)

    # 1. Python 版本
    py = sys.version_info[:2]
    py_ok = py >= MIN_PYTHON
    status = "OK  " if py_ok else "FAIL"
    print(f"\n[{status}] Python {sys.version.split()[0]}"
          f"  (要求 >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]})")

    # 2. 第三方库
    print(f"\n{'库':<14}{'已安装':<12}{'要求':<10}{'类型':<8}结果")
    print("-" * 58)

    missing = []
    for import_name, display, min_v, required in COURSE_REQUIREMENTS:
        name, installed, min_v, required, ok = check_package(
            import_name, display, min_v, required)
        kind = "必需" if required else "可选"
        mark = "OK" if ok else ("缺失" if installed is None else "过旧")
        print(f"{name:<14}{str(installed or '-'):<12}{'>=' + min_v:<10}{kind:<8}{mark}")
        if not ok and required:
            missing.append(name)

    print("-" * 58)

    # 3. 结论
    if py_ok and not missing:
        print("\n环境检查通过，可以开始课程。\n")
        return 0

    print("\n环境检查未通过，请按下面的提示处理：")
    if not py_ok:
        print(f"  · Python 版本过低，请安装 {MIN_PYTHON[0]}.{MIN_PYTHON[1]} 或更高版本")
    if missing:
        print("  · 缺少或版本过旧的库：" + "、".join(missing))
        print("\n  推荐一次性安装（使用课程提供的 requirements.txt）：")
        print("      pip install -r requirements.txt")
        print("\n  或手动安装：")
        print("      pip install " + " ".join(missing))
    print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
