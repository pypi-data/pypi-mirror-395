"""
配置管理模块 - 处理应用程序的配置设置和环境变量
"""

import os
from typing import Any, Dict, Optional
from pathlib import Path
import json
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 全局配置字典
_config: Dict[str, Any] = {}

# 默认配置
DEFAULT_CONFIG = {
    "log_level": "INFO",
    "log_dir": "./logs",
    "bark_id": os.environ.get("BARK_ID", ""),
    "api_key": os.environ.get("API_KEY", ""),
    "timeout": 30,
    "max_retries": 3,
}

# 初始化配置
_config.update(DEFAULT_CONFIG)


def get_config(key: str, default: Any = None) -> Any:
    """
    获取配置值

    Args:
        key: 配置键名
        default: 如果键不存在，返回的默认值

    Returns:
        配置值或默认值
    """
    return _config.get(key, default)


def set_config(key: str, value: Any) -> None:
    """
    设置配置值

    Args:
        key: 配置键名
        value: 配置值
    """
    _config[key] = value


def load_config_file(config_path: str) -> Dict[str, Any]:
    """
    从文件加载配置

    Args:
        config_path: 配置文件路径

    Returns:
        加载的配置字典
    """
    path = Path(config_path)
    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
            _config.update(config)
            return config
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        return {}


def save_config_file(config_path: str, config: Optional[Dict[str, Any]] = None) -> bool:
    """
    保存配置到文件

    Args:
        config_path: 配置文件路径
        config: 要保存的配置字典，如果为None则保存全局配置

    Returns:
        是否保存成功
    """
    if config is None:
        config = _config

    path = Path(config_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"保存配置文件失败: {e}")
        return False
