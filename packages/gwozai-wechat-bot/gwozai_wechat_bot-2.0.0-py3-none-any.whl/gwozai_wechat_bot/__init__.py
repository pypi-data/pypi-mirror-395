"""
gwozai-wechat-bot - 企业微信群机器人 SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

简单易用的企业微信群机器人 Python SDK

基本用法:
    >>> from gwozai_wechat_bot import WeChatBot
    >>> bot = WeChatBot(key="your-key")
    >>> bot.text("Hello World")

环境变量配置:
    >>> # .env 文件中设置 WECHAT_WEBHOOK_KEY=your-key
    >>> bot = WeChatBot()  # 自动读取

GitHub: https://github.com/gwozai/gwozai-wechat-bot
"""

from .bot import (
    WeChatBot,
    BotResponse,
    send_text,
    send_markdown,
    send_image,
    send_file,
    send_alert,
    get_bot,
)

__title__ = "gwozai-wechat-bot"
__version__ = "2.0.0"
__author__ = "gwozai"
__license__ = "MIT"
__all__ = [
    "WeChatBot",
    "BotResponse",
    "send_text",
    "send_markdown",
    "send_image",
    "send_file",
    "send_alert",
    "get_bot",
]
