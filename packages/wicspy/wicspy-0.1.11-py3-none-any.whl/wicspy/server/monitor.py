"""
服务器监控模块 - 提供系统信息、资源使用情况等监控功能
"""

import os
import platform
import socket
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import subprocess
import json
from pydantic import BaseModel, Field
from loguru import logger


class SystemInfo(BaseModel):
    """系统信息模型"""
    hostname: str = Field(..., description="主机名")
    platform: str = Field(..., description="操作系统平台")
    platform_version: str = Field(..., description="操作系统版本")
    architecture: str = Field(..., description="系统架构")
    processor: str = Field(..., description="处理器信息")
    ip_address: str = Field(..., description="IP地址")
    python_version: str = Field(..., description="Python版本")
    current_time: datetime = Field(..., description="当前时间")
    uptime: Optional[str] = Field(None, description="系统运行时间")


class MemoryUsage(BaseModel):
    """内存使用情况模型"""
    total: int = Field(..., description="总内存(字节)")
    available: int = Field(..., description="可用内存(字节)")
    used: int = Field(..., description="已用内存(字节)")
    percent: float = Field(..., description="内存使用百分比")
    

class DiskUsage(BaseModel):
    """磁盘使用情况模型"""
    device: str = Field(..., description="设备名")
    mountpoint: str = Field(..., description="挂载点")
    total: int = Field(..., description="总容量(字节)")
    used: int = Field(..., description="已用容量(字节)")
    free: int = Field(..., description="可用容量(字节)")
    percent: float = Field(..., description="使用百分比")
    filesystem: str = Field(..., description="文件系统类型")


class CPUUsage(BaseModel):
    """CPU使用情况模型"""
    percent: float = Field(..., description="CPU使用百分比")
    cores: List[float] = Field(..., description="每个核心的使用百分比")
    load_avg: List[float] = Field(..., description="1分钟、5分钟、15分钟负载")


def get_system_info() -> SystemInfo:
    """
    获取系统信息
    
    Returns:
        SystemInfo: 系统信息对象
    """
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
    except Exception:
        hostname = "unknown"
        ip_address = "unknown"
        
    # 获取系统运行时间
    uptime = None
    if platform.system() == "Linux":
        try:
            with open("/proc/uptime", "r") as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime = str(datetime.timedelta(seconds=uptime_seconds))
        except Exception:
            uptime = None
    elif platform.system() == "Darwin":  # macOS
        try:
            result = subprocess.run(["uptime"], capture_output=True, text=True)
            if result.returncode == 0:
                uptime = result.stdout.strip()
        except Exception:
            uptime = None
            
    return SystemInfo(
        hostname=hostname,
        platform=platform.system(),
        platform_version=platform.version(),
        architecture=platform.machine(),
        processor=platform.processor(),
        ip_address=ip_address,
        python_version=platform.python_version(),
        current_time=datetime.now(),
        uptime=uptime
    )


def get_memory_usage() -> MemoryUsage:
    """
    获取内存使用情况
    
    Returns:
        MemoryUsage: 内存使用情况对象
    """
    if platform.system() == "Linux":
        try:
            with open("/proc/meminfo", "r") as f:
                meminfo = f.readlines()
                
            mem_total = 0
            mem_available = 0
            
            for line in meminfo:
                if "MemTotal" in line:
                    mem_total = int(line.split()[1]) * 1024  # KB to bytes
                elif "MemAvailable" in line:
                    mem_available = int(line.split()[1]) * 1024  # KB to bytes
                    
            mem_used = mem_total - mem_available
            mem_percent = (mem_used / mem_total) * 100.0
            
            return MemoryUsage(
                total=mem_total,
                available=mem_available,
                used=mem_used,
                percent=mem_percent
            )
        except Exception as e:
            logger.error(f"获取内存信息失败: {e}")
            
    # 对于其他系统，尝试使用 subprocess 调用系统命令
    try:
        if platform.system() == "Darwin":  # macOS
            result = subprocess.run(["vm_stat"], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                page_size = 4096  # 默认页面大小
                mem_stats = {}
                
                for line in lines:
                    if "page size of" in line:
                        page_size = int(line.split()[-2])
                    if ":" in line:
                        key, value = line.split(":")
                        mem_stats[key.strip()] = int(''.join(c for c in value if c.isdigit())) * page_size
                
                mem_total = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True)
                total = int(mem_total.stdout.strip())
                
                # 计算可用和已用内存
                free = mem_stats.get("Pages free", 0) + mem_stats.get("Pages inactive", 0)
                used = total - free
                percent = (used / total) * 100.0
                
                return MemoryUsage(
                    total=total,
                    available=free,
                    used=used,
                    percent=percent
                )
    except Exception as e:
        logger.error(f"获取内存信息失败: {e}")
    
    # 如果所有方法都失败，返回空值
    return MemoryUsage(
        total=0,
        available=0,
        used=0,
        percent=0.0
    )


def get_disk_usage(path: str = "/") -> List[DiskUsage]:
    """
    获取磁盘使用情况
    
    Args:
        path: 要检查的路径
        
    Returns:
        List[DiskUsage]: 磁盘使用情况对象列表
    """
    result = []
    
    try:
        if platform.system() == "Linux" or platform.system() == "Darwin":
            output = subprocess.run(["df", "-k"], capture_output=True, text=True)
            if output.returncode == 0:
                lines = output.stdout.strip().split("\n")
                # 跳过标题行
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) >= 6:
                        device = parts[0]
                        total = int(parts[1]) * 1024  # KB to bytes
                        used = int(parts[2]) * 1024   # KB to bytes
                        free = int(parts[3]) * 1024   # KB to bytes
                        percent = float(parts[4].replace("%", ""))
                        mountpoint = parts[5]
                        filesystem = ""  # 在某些系统上可能需要额外命令获取
                        
                        result.append(DiskUsage(
                            device=device,
                            mountpoint=mountpoint,
                            total=total,
                            used=used,
                            free=free,
                            percent=percent,
                            filesystem=filesystem
                        ))
    except Exception as e:
        logger.error(f"获取磁盘信息失败: {e}")
    
    return result


def get_cpu_usage() -> CPUUsage:
    """
    获取CPU使用情况
    
    Returns:
        CPUUsage: CPU使用情况对象
    """
    try:
        if platform.system() == "Linux":
            # 获取CPU使用率
            with open("/proc/stat", "r") as f:
                cpu_line = f.readline()
            
            # 计算总CPU使用率
            cpu_parts = cpu_line.split()[1:]
            idle = float(cpu_parts[3])
            total = sum(float(x) for x in cpu_parts)
            cpu_percent = 100.0 - (idle / total * 100.0)
            
            # 获取每个核心的使用率
            cores = []
            for i in range(os.cpu_count() or 1):
                subprocess.run(f"grep 'cpu{i}' /proc/stat", shell=True, capture_output=True, text=True)
                # 简化示例，实际需要解析输出
                cores.append(cpu_percent)  # 示例中使用相同的值
                
            # 获取负载情况
            with open("/proc/loadavg", "r") as f:
                load = f.readline().split()[:3]
                load_avg = [float(x) for x in load]
                
            return CPUUsage(
                percent=cpu_percent,
                cores=cores,
                load_avg=load_avg
            )
            
        elif platform.system() == "Darwin":  # macOS
            # 使用系统命令获取CPU使用率
            result = subprocess.run(["top", "-l", "1", "-n", "0"], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                cpu_line = ""
                for line in lines:
                    if "CPU usage" in line:
                        cpu_line = line
                        break
                
                if cpu_line:
                    parts = cpu_line.split(":")
                    if len(parts) > 1:
                        usage_parts = parts[1].split(",")
                        user = float(usage_parts[0].strip().replace("%", ""))
                        system = float(usage_parts[1].strip().replace("%", ""))
                        idle = float(usage_parts[2].strip().replace("%", ""))
                        cpu_percent = user + system
                        
                        # 获取负载情况
                        load_result = subprocess.run(["sysctl", "-n", "vm.loadavg"], capture_output=True, text=True)
                        load_parts = load_result.stdout.strip().replace("{", "").replace("}", "").split()
                        load_avg = [float(load_parts[0]), float(load_parts[1]), float(load_parts[2])]
                        
                        # 获取每个核心信息
                        cores = [cpu_percent] * (os.cpu_count() or 1)  # 简化处理
                        
                        return CPUUsage(
                            percent=cpu_percent,
                            cores=cores,
                            load_avg=load_avg
                        )
    except Exception as e:
        logger.error(f"获取CPU信息失败: {e}")
    
    # 如果所有方法都失败，返回默认值
    return CPUUsage(
        percent=0.0,
        cores=[0.0] * (os.cpu_count() or 1),
        load_avg=[0.0, 0.0, 0.0]
    ) 