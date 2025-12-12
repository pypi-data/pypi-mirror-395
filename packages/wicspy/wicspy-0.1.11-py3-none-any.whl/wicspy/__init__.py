"""
wicspy - 一个全面的 Python 工具库，提供各种实用功能和工具集合
"""

__version__ = "0.1.0"


from importlib.metadata import version, PackageNotFoundError


try:
    __version__ = version("wicspy")
except PackageNotFoundError:
    # 包未安装，使用默认版本号
    pass

# 为方便使用，导入常用的子模块
from wicspy.config import get_config, set_config

from wicspy.messaging.bark import send_message as bark

__all__ = ["bark", "get_config", "set_config"]

def hello() -> str:
    return "Hello from wicspy!"

