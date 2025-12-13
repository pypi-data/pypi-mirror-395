import platform
import sys
from typing import TypedDict

class SystemInfo(TypedDict):
    os: str
    arch: str
    runtime: str
    runtime_version: str

def get_system_info() -> SystemInfo:
    """Get system information for User-Agent header."""
    return {
        "os": platform.system().lower(),
        "arch": platform.machine().lower(),
        "runtime": "python",
        "runtime_version": platform.python_version(),
    }
