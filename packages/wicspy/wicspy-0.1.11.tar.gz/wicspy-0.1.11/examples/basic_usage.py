#!/usr/bin/env python3
"""
wicspy 工具库基本用法示例
"""

import os
import sys
from rich.console import Console
from rich.table import Table

# 添加包目录到路径中，仅在本地运行示例时需要
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 导入 wicspy 模块
from wicspy.config import get_config, set_config
from wicspy.messaging import send_bark_message
from wicspy.web import fetch_page, extract_text
from wicspy.server import get_system_info, get_memory_usage, get_cpu_usage, list_processes


def config_example():
    """配置模块示例"""
    console = Console()
    console.print("[bold green]配置模块示例[/bold green]")
    
    # 设置配置
    set_config("api_key", "test_api_key")
    set_config("app_name", "wicspy_demo")
    
    # 获取配置
    console.print(f"API Key: {get_config('api_key')}")
    console.print(f"Bark ID: {get_config('bark_id')}")
    console.print(f"App Name: {get_config('app_name')}")
    console.print(f"超时时间: {get_config('timeout')} 秒")
    console.print()


def messaging_example():
    """消息模块示例"""
    console = Console()
    console.print("[bold green]消息模块示例[/bold green]")
    
    # 检查是否有 Bark ID
    bark_id = get_config("bark_id")
    if not bark_id:
        console.print("[bold red]未设置 Bark ID，将跳过消息示例[/bold red]")
        console.print("可以设置环境变量: export BARK_ID=your_bark_id")
        return
    
    try:
        # 发送 Bark 消息
        response = send_bark_message(
            title="wicspy 测试",
            content="这是一条测试消息",
            group="示例"
        )
        console.print(f"消息发送状态: {response.code}")
        console.print(f"消息响应: {response.message}")
    except Exception as e:
        console.print(f"[bold red]发送消息失败: {e}[/bold red]")
    
    console.print()


def web_example():
    """网页模块示例"""
    console = Console()
    console.print("[bold green]网页模块示例[/bold green]")
    
    try:
        # 抓取网页
        url = "https://example.com"
        console.print(f"抓取网页: {url}")
        
        page = fetch_page(url)
        
        console.print(f"页面标题: {page.title}")
        console.print(f"链接数量: {len(page.links)}")
        
        # 显示一些元数据
        if page.metadata:
            table = Table(title="页面元数据")
            table.add_column("Name", style="cyan")
            table.add_column("Content", style="green")
            
            for name, content in list(page.metadata.items())[:5]:  # 只显示前5项
                table.add_row(name, content)
                
            console.print(table)
            
        # 提取文本
        text = extract_text(page.html)
        console.print(f"页面文本 (前100字符): {text[:100]}...")
    
    except Exception as e:
        console.print(f"[bold red]抓取网页失败: {e}[/bold red]")
    
    console.print()


def server_example():
    """服务器信息示例"""
    console = Console()
    console.print("[bold green]服务器信息示例[/bold green]")
    
    # 系统信息
    try:
        info = get_system_info()
        
        table = Table(title="系统信息")
        table.add_column("项目", style="cyan")
        table.add_column("值", style="green")
        
        table.add_row("主机名", info.hostname)
        table.add_row("平台", info.platform)
        table.add_row("版本", info.platform_version)
        table.add_row("架构", info.architecture)
        table.add_row("处理器", info.processor)
        table.add_row("IP地址", info.ip_address)
        table.add_row("Python版本", info.python_version)
        table.add_row("当前时间", str(info.current_time))
        if info.uptime:
            table.add_row("运行时间", info.uptime)
            
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]获取系统信息失败: {e}[/bold red]")
    
    # 内存使用情况
    try:
        memory = get_memory_usage()
        
        table = Table(title="内存使用情况")
        table.add_column("项目", style="cyan")
        table.add_column("值", style="green")
        
        table.add_row("总内存", f"{memory.total / (1024**3):.2f} GB")
        table.add_row("可用内存", f"{memory.available / (1024**3):.2f} GB")
        table.add_row("已用内存", f"{memory.used / (1024**3):.2f} GB")
        table.add_row("使用百分比", f"{memory.percent:.1f}%")
            
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]获取内存信息失败: {e}[/bold red]")
    
    # CPU使用情况
    try:
        cpu = get_cpu_usage()
        
        table = Table(title="CPU使用情况")
        table.add_column("项目", style="cyan")
        table.add_column("值", style="green")
        
        table.add_row("CPU使用率", f"{cpu.percent:.1f}%")
        table.add_row("核心数", str(len(cpu.cores)))
        table.add_row("负载平均值", f"{cpu.load_avg[0]:.2f}, {cpu.load_avg[1]:.2f}, {cpu.load_avg[2]:.2f}")
            
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]获取CPU信息失败: {e}[/bold red]")
    
    # 进程信息
    try:
        processes = list_processes()
        
        # 按CPU使用率排序并显示前5个
        top_processes = sorted(processes, key=lambda p: p.cpu_percent, reverse=True)[:5]
        
        table = Table(title="CPU使用率最高的5个进程")
        table.add_column("PID", style="cyan")
        table.add_column("名称", style="green")
        table.add_column("CPU%", style="magenta")
        table.add_column("内存%", style="yellow")
        table.add_column("用户", style="blue")
        
        for proc in top_processes:
            table.add_row(
                str(proc.pid),
                proc.name,
                f"{proc.cpu_percent:.1f}%",
                f"{proc.memory_percent:.1f}%",
                proc.user
            )
            
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]获取进程信息失败: {e}[/bold red]")
    
    console.print()


def main():
    """运行所有示例"""
    console = Console()
    console.print("[bold blue]wicspy 工具库示例[/bold blue]")
    console.print("=" * 50)
    
    # 运行示例
    config_example()
    messaging_example()
    web_example()
    server_example()
    
    console.print("[bold blue]示例运行完毕[/bold blue]")


if __name__ == "__main__":
    main() 