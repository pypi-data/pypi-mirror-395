import sys
import platform
from setuptools import setup

def check_compatibility():
    # 1. 仅允许 Windows 系统（排除 Linux/macOS）
    if sys.platform != "win32":
        raise RuntimeError("该包依赖 Windows 专属 .pyd 扩展，仅支持 Windows 系统！")
    # 2. 仅允许 x64（64位）架构（.pyd 若为 64位编译，需拦截 32位系统）
    if platform.machine() != "AMD64":
        raise RuntimeError("该包仅支持 64位（x64）Windows 系统！")
    # 3. 仅允许 Windows 7 及以上版本
    win_version = float(platform.release())  # 处理 Win8.1（返回 8.1）
    if win_version < 6.1:
        raise RuntimeError("该包要求 Windows 7 及以上版本！")

# 安装前执行校验，失败则终止安装
check_compatibility()

# 读取 pyproject.toml 配置，无需重复写其他参数
setup()
