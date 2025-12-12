"""
网页抓取模块 - 提供网页内容抓取和解析功能
"""

try:
    import httpx
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError(
        "To use the web module, you need to install the wicspy[web] extra.\n"
    )
import re
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field
from loguru import logger

from wicspy.config import get_config


class PageContent(BaseModel):
    """网页内容模型"""
    url: str = Field(..., description="网页 URL")
    title: str = Field("", description="网页标题")
    html: str = Field(..., description="原始 HTML")
    text: str = Field("", description="提取的文本内容")
    links: List[str] = Field(default_factory=list, description="页面中的链接")
    metadata: Dict[str, str] = Field(default_factory=dict, description="页面元数据")


async def fetch_page_async(url: str, headers: Optional[Dict[str, str]] = None) -> PageContent:
    """
    异步抓取网页内容
    
    Args:
        url: 要抓取的网页 URL
        headers: 请求头
        
    Returns:
        PageContent: 网页内容对象
    """
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
    timeout = get_config("timeout", 30)
    max_retries = get_config("max_retries", 3)
    
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                logger.debug(f"抓取网页: {url}")
                response = await client.get(url, headers=headers, follow_redirects=True)
                response.raise_for_status()
                
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                
                # 提取标题
                title = soup.title.text.strip() if soup.title else ""
                
                # 提取链接
                links = [a.get("href", "") for a in soup.find_all("a", href=True)]
                
                # 提取元数据
                metadata = {
                    meta.get("name", meta.get("property", "unknown")): meta.get("content", "")
                    for meta in soup.find_all("meta")
                    if meta.get("name") or meta.get("property")
                }
                
                # 提取文本
                text = soup.get_text(separator="\n", strip=True)
                
                return PageContent(
                    url=url,
                    title=title,
                    html=html,
                    text=text,
                    links=links,
                    metadata=metadata
                )
                
        except Exception as e:
            logger.warning(f"抓取网页失败 (尝试 {attempt+1}/{max_retries}): {url}, 异常: {e}")
            if attempt == max_retries - 1:
                logger.error(f"抓取网页最终失败: {url}")
                raise
    
    # 不应该到达这里，但为了类型检查
    raise Exception("无法抓取网页")


def fetch_page(url: str, headers: Optional[Dict[str, str]] = None) -> PageContent:
    """
    同步抓取网页内容
    
    Args:
        url: 要抓取的网页 URL
        headers: 请求头
        
    Returns:
        PageContent: 网页内容对象
    """
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
    timeout = get_config("timeout", 30)
    max_retries = get_config("max_retries", 3)
    
    for attempt in range(max_retries):
        try:
            logger.debug(f"抓取网页: {url}")
            response = httpx.get(url, headers=headers, timeout=timeout, follow_redirects=True)
            response.raise_for_status()
            
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            
            # 提取标题
            title = soup.title.text.strip() if soup.title else ""
            
            # 提取链接
            links = [a.get("href", "") for a in soup.find_all("a", href=True)]
            
            # 提取元数据
            metadata = {
                meta.get("name", meta.get("property", "unknown")): meta.get("content", "")
                for meta in soup.find_all("meta")
                if meta.get("name") or meta.get("property")
            }
            
            # 提取文本
            text = soup.get_text(separator="\n", strip=True)
            
            return PageContent(
                url=url,
                title=title,
                html=html,
                text=text,
                links=links,
                metadata=metadata
            )
            
        except Exception as e:
            logger.warning(f"抓取网页失败 (尝试 {attempt+1}/{max_retries}): {url}, 异常: {e}")
            if attempt == max_retries - 1:
                logger.error(f"抓取网页最终失败: {url}")
                raise
    
    # 不应该到达这里，但为了类型检查
    raise Exception("无法抓取网页")


def extract_text(html: str, selector: Optional[str] = None) -> str:
    """
    从 HTML 中提取文本
    
    Args:
        html: HTML 内容
        selector: CSS 选择器，如果指定则只提取匹配元素的文本
        
    Returns:
        str: 提取的文本
    """
    soup = BeautifulSoup(html, "html.parser")
    
    if selector:
        elements = soup.select(selector)
        return "\n".join(element.get_text(strip=True) for element in elements)
    else:
        return soup.get_text(separator="\n", strip=True)


def extract_with_pattern(text: str, pattern: str) -> List[str]:
    """
    使用正则表达式从文本中提取内容
    
    Args:
        text: 要搜索的文本
        pattern: 正则表达式模式
        
    Returns:
        List[str]: 匹配的结果列表
    """
    try:
        return re.findall(pattern, text)
    except Exception as e:
        logger.error(f"正则表达式匹配失败: {pattern}, 异常: {e}")
        return [] 