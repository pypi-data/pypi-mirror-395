"""
Bark CLI tool for sending notifications
"""

import argparse
from wicspy.messaging.bark import send_message
from loguru import logger


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Send notifications via Bark service")
    parser.add_argument("title", help="Message title")
    parser.add_argument("content", help="Message content")
    parser.add_argument("--group", "-g", help="Message group")
    parser.add_argument("--sound", "-s", help="Alert sound")
    parser.add_argument("--icon", "-i", help="Icon URL")
    parser.add_argument("--url", "-u", help="URL to open when clicking the message")
    parser.add_argument(
        "--level", 
        "-l",
        choices=["active", "timeSensitive", "passive"],
        help="Message level"
    )
    return parser


def bark():
    """Bark CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        response = send_message(
            title=args.title,
            content=args.content,
            group=args.group,
            sound=args.sound,
            icon=args.icon,
            url=args.url,
            level=args.level,
        )
        if response.code == 200:
            logger.info("Message sent successfully")
        else:
            logger.error(f"Failed to send message: {response.message}")
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    bark()
