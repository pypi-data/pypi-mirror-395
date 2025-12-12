"""
进程管理模块 - 提供进程查询、管理等功能
"""

import os
import platform
import subprocess
import signal
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from loguru import logger


class Process(BaseModel):
    """进程信息模型"""
    pid: int = Field(..., description="进程ID")
    name: str = Field("", description="进程名称")
    cmd: str = Field("", description="命令行")
    cpu_percent: float = Field(0.0, description="CPU使用百分比")
    memory_percent: float = Field(0.0, description="内存使用百分比")
    status: str = Field("", description="进程状态")
    user: str = Field("", description="用户")
    created: Optional[str] = Field(None, description="创建时间")


def list_processes() -> List[Process]:
    """
    列出系统进程
    
    Returns:
        List[Process]: 进程信息列表
    """
    result = []
    
    try:
        if platform.system() == "Linux":
            # 使用 ps 命令获取进程信息
            output = subprocess.run(
                ["ps", "aux"], 
                capture_output=True, 
                text=True
            )
            if output.returncode == 0:
                lines = output.stdout.strip().split("\n")
                # 跳过标题行
                for line in lines[1:]:
                    parts = line.split(None, 10)
                    if len(parts) >= 11:
                        user = parts[0]
                        pid = int(parts[1])
                        cpu = float(parts[2])
                        mem = float(parts[3])
                        status = parts[7]
                        created = parts[8]
                        cmd = parts[10]
                        name = cmd.split()[0] if cmd else ""
                        
                        result.append(Process(
                            pid=pid,
                            name=name,
                            cmd=cmd,
                            cpu_percent=cpu,
                            memory_percent=mem,
                            status=status,
                            user=user,
                            created=created
                        ))
                        
        elif platform.system() == "Darwin":  # macOS
            # 使用 ps 命令获取进程信息
            output = subprocess.run(
                ["ps", "-eo", "user,pid,pcpu,pmem,state,start,comm,command"], 
                capture_output=True, 
                text=True
            )
            if output.returncode == 0:
                lines = output.stdout.strip().split("\n")
                # 跳过标题行
                for line in lines[1:]:
                    parts = line.split(None, 7)
                    if len(parts) >= 8:
                        user = parts[0]
                        pid = int(parts[1])
                        cpu = float(parts[2])
                        mem = float(parts[3])
                        status = parts[4]
                        created = parts[5]
                        name = parts[6]
                        cmd = parts[7]
                        
                        result.append(Process(
                            pid=pid,
                            name=name,
                            cmd=cmd,
                            cpu_percent=cpu,
                            memory_percent=mem,
                            status=status,
                            user=user,
                            created=created
                        ))
    except Exception as e:
        logger.error(f"获取进程信息失败: {e}")
    
    return result


def find_process(name: str) -> List[Process]:
    """
    根据进程名查找进程
    
    Args:
        name: 进程名称（部分匹配）
        
    Returns:
        List[Process]: 匹配的进程列表
    """
    processes = list_processes()
    return [p for p in processes if name.lower() in p.name.lower() or name.lower() in p.cmd.lower()]


def kill_process(pid: int, force: bool = False) -> bool:
    """
    终止进程
    
    Args:
        pid: 进程ID
        force: 是否强制终止
        
    Returns:
        bool: 是否成功终止
    """
    try:
        sig = signal.SIGKILL if force else signal.SIGTERM
        os.kill(pid, sig)
        logger.info(f"已终止进程 {pid} (强制: {force})")
        return True
    except ProcessLookupError:
        logger.warning(f"进程 {pid} 不存在")
        return False
    except PermissionError:
        logger.error(f"没有权限终止进程 {pid}")
        return False
    except Exception as e:
        logger.error(f"终止进程 {pid} 失败: {e}")
        return False 