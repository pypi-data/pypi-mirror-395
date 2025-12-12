"""
Bark Message Module - Send notifications through Bark service
"""

from typing import Dict, Optional, Any
import requests
from loguru import logger
from pydantic import BaseModel, Field

from wicspy.config import get_config


class BarkResponse(BaseModel):
    """Bark response model"""
    code: int = Field(..., description="Response code")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


class BarkClient:
    """Bark client"""
    
    def __init__(self, bark_id: Optional[str] = None):
        """
        Initialize Bark client
        
        Args:
            bark_id: Bark ID, if None, will be retrieved from config
        """
        self.bark_id = bark_id or get_config("bark_id")
        if not self.bark_id:
            raise ValueError(
                "BARK_ID not set. Please set it via environment variable or config, "
                "e.g., 'export BARK_ID=your_bark_id'"
            )
        
        self.base_url = f"https://api.day.app/{self.bark_id}"
        
    def send_message(
        self, 
        title: str, 
        content: str, 
        group: Optional[str] = None,
        sound: Optional[str] = None,
        icon: Optional[str] = None,
        url: Optional[str] = None,
        level: Optional[str] = None,
    ) -> BarkResponse:
        """
        Send Bark message
        
        Args:
            title: Message title
            content: Message content
            group: Message group
            sound: Alert sound
            icon: Icon URL
            url: URL to open when clicking the message
            level: Message level (active, timeSensitive, passive)
            
        Returns:
            BarkResponse: Bark response object
        """
        endpoint = f"{self.base_url}/{title}/{content}"
        
        params: Dict[str, str] = {}
        if group:
            params["group"] = group
        if sound:
            params["sound"] = sound
        if icon:
            params["icon"] = icon
        if url:
            params["url"] = url
        if level:
            params["level"] = level
            
        try:
            logger.debug(f"Sending Bark message: {title} > {content}")
            response = requests.post(endpoint, params=params, timeout=get_config("timeout", 30))
            response.raise_for_status()
            
            logger.info(f"Bark message sent successfully: {title}")
            
            return BarkResponse(**response.json())
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Bark message: {title} > {content}, error: {e}")
            raise


# Create default client instance
_default_client: Optional[BarkClient] = None


def get_client() -> BarkClient:
    """
    Get default Bark client instance
    
    Returns:
        BarkClient: Bark client instance
    """
    global _default_client
    if _default_client is None:
        _default_client = BarkClient()
    return _default_client


def send_message(
    title: str, 
    content: str, 
    group: Optional[str] = None,
    sound: Optional[str] = None,
    icon: Optional[str] = None,
    url: Optional[str] = None,
    level: Optional[str] = None,
    client: Optional[BarkClient] = None,
) -> BarkResponse:
    """
    Send Bark message
    
    Args:
        title: Message title
        content: Message content
        group: Message group
        sound: Alert sound
        icon: Icon URL
        url: URL to open when clicking the message
        level: Message level (active, timeSensitive, passive)
        client: Custom Bark client, if None, use default client
        
    Returns:
        BarkResponse: Bark response object
    """
    if client is None:
        client = get_client()
    
    return client.send_message(
        title=title,
        content=content,
        group=group,
        sound=sound,
        icon=icon,
        url=url,
        level=level,
    ) 