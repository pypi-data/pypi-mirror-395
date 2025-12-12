"""
企业微信群机器人 SDK
功能完善版：重试机制、日志记录、异步支持、消息模板、批量发送
"""

import os
import time
import asyncio
import logging
import requests
import hashlib
import base64
from pathlib import Path
from typing import List, Dict, Optional, Union, Callable, Any, TypedDict
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def setup_logger(name: str = "WeChatBot", level: int = logging.INFO) -> logging.Logger:
    """配置日志"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


class ArticleDict(TypedDict, total=False):
    title: str
    url: str
    description: str
    picurl: str


@dataclass
class BotResponse:
    """机器人响应"""
    success: bool
    errcode: int
    errmsg: str
    data: dict
    elapsed: float = 0.0
    retries: int = 0
    
    @classmethod
    def from_dict(cls, data: dict, elapsed: float = 0, retries: int = 0) -> "BotResponse":
        return cls(
            success=data.get("errcode", -1) == 0,
            errcode=data.get("errcode", -1),
            errmsg=data.get("errmsg", ""),
            data=data,
            elapsed=elapsed,
            retries=retries
        )
    
    @classmethod
    def error(cls, message: str) -> "BotResponse":
        return cls(success=False, errcode=-1, errmsg=message, data={})
    
    def __bool__(self):
        return self.success
    
    def __repr__(self):
        status = "✓" if self.success else "✗"
        return f"[{status}] {self.errmsg} ({self.elapsed:.2f}s)"


class WeChatBot:
    """
    企业微信群机器人 SDK
    
    Args:
        key: Webhook key，不传则从环境变量 WECHAT_WEBHOOK_KEY 读取
        max_retries: 最大重试次数，默认 3
        retry_delay: 重试间隔(秒)，默认 1.0
        timeout: 请求超时时间(秒)，默认 10
        log_level: 日志级别，默认 logging.INFO
        enable_log: 是否启用日志，默认 True
    
    Examples:
        >>> from gwozai_wechat_bot import WeChatBot
        >>> bot = WeChatBot(key="your-key")
        >>> bot.text("Hello World")
    """
    
    BASE_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook"
    RATE_LIMIT = 20
    
    def __init__(
        self, 
        key: str = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 10,
        log_level: int = logging.INFO,
        enable_log: bool = True
    ):
        self.key = key or os.getenv("WECHAT_WEBHOOK_KEY")
        if not self.key:
            raise ValueError(
                "未配置 Webhook Key，请通过参数传入或设置环境变量 WECHAT_WEBHOOK_KEY"
            )
        
        self.send_url = f"{self.BASE_URL}/send?key={self.key}"
        self.upload_url = f"{self.BASE_URL}/upload_media?key={self.key}&type=file"
        
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        
        self.logger = setup_logger(level=log_level) if enable_log else logging.getLogger("null")
        self._message_times: List[float] = []
        self._executor = ThreadPoolExecutor(max_workers=5)
        
        self.logger.info(f"WeChatBot 初始化完成 (retries={max_retries}, timeout={timeout}s)")
    
    def _post(self, data: dict, _retry_attempt: int = 0) -> BotResponse:
        start_time = time.time()
        last_error = None
        
        for attempt in range(_retry_attempt, self.max_retries + 1):
            try:
                self._check_rate_limit()
                resp = requests.post(self.send_url, json=data, timeout=self.timeout)
                elapsed = time.time() - start_time
                result = BotResponse.from_dict(resp.json(), elapsed=elapsed, retries=attempt)
                
                if result.success:
                    self.logger.info(f"发送成功: {data.get('msgtype')} {result}")
                    return result
                else:
                    self.logger.warning(f"发送失败: {result.errmsg}")
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay * (attempt + 1))
                    last_error = result
                    
            except requests.exceptions.Timeout:
                self.logger.warning(f"请求超时 (attempt {attempt + 1}/{self.max_retries + 1})")
                last_error = BotResponse.error("请求超时")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (attempt + 1))
            except Exception as e:
                self.logger.error(f"请求异常: {e}")
                last_error = BotResponse.error(str(e))
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (attempt + 1))
        
        return last_error or BotResponse.error("未知错误")
    
    def _check_rate_limit(self):
        now = time.time()
        self._message_times = [t for t in self._message_times if now - t < 60]
        if len(self._message_times) >= self.RATE_LIMIT:
            wait_time = 60 - (now - self._message_times[0])
            if wait_time > 0:
                self.logger.warning(f"触发频率限制，等待 {wait_time:.1f}s")
                time.sleep(wait_time)
        self._message_times.append(now)
    
    # 异步方法
    async def _async_post(self, data: dict) -> BotResponse:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._post, data)
    
    async def async_text(self, content: str, **kwargs) -> BotResponse:
        return await self._async_post(self._build_text_payload(content, **kwargs))
    
    async def async_markdown(self, content: str) -> BotResponse:
        return await self._async_post({"msgtype": "markdown", "markdown": {"content": content}})
    
    async def async_image(self, source: Union[str, bytes]) -> BotResponse:
        return await self._async_post(self._build_image_payload(source))
    
    # 构建 Payload
    def _build_text_payload(self, content: str, mentioned: List[str] = None,
                            mentioned_mobile: List[str] = None, at_all: bool = False) -> dict:
        payload = {"msgtype": "text", "text": {"content": content}}
        mention_list = list(mentioned) if mentioned else []
        if at_all and "@all" not in mention_list:
            mention_list.append("@all")
        if mention_list:
            payload["text"]["mentioned_list"] = mention_list
        if mentioned_mobile:
            payload["text"]["mentioned_mobile_list"] = mentioned_mobile
        return payload
    
    def _build_image_payload(self, source: Union[str, bytes]) -> dict:
        if isinstance(source, bytes):
            image_data = source
        elif source.startswith(("http://", "https://")):
            resp = requests.get(source, timeout=30)
            resp.raise_for_status()
            image_data = resp.content
        else:
            with open(source, "rb") as f:
                image_data = f.read()
        return {
            "msgtype": "image",
            "image": {
                "base64": base64.b64encode(image_data).decode(),
                "md5": hashlib.md5(image_data).hexdigest()
            }
        }
    
    # 基础消息
    def text(self, content: str, mentioned: List[str] = None,
             mentioned_mobile: List[str] = None, at_all: bool = False) -> BotResponse:
        """发送文本消息"""
        return self._post(self._build_text_payload(content, mentioned, mentioned_mobile, at_all))
    
    def markdown(self, content: str) -> BotResponse:
        """发送 Markdown 消息"""
        return self._post({"msgtype": "markdown", "markdown": {"content": content}})
    
    def image(self, source: Union[str, bytes]) -> BotResponse:
        """发送图片（路径/URL/字节）"""
        return self._post(self._build_image_payload(source))
    
    def news(self, articles: List[ArticleDict]) -> BotResponse:
        """发送图文消息"""
        return self._post({"msgtype": "news", "news": {"articles": articles}})
    
    def news_single(self, title: str, url: str, description: str = "", picurl: str = "") -> BotResponse:
        """发送单条图文"""
        return self.news([{"title": title, "url": url, "description": description, "picurl": picurl}])
    
    def file(self, file_path: str) -> BotResponse:
        """发送文件"""
        try:
            with open(file_path, "rb") as f:
                files = {"media": (Path(file_path).name, f)}
                resp = requests.post(self.upload_url, files=files, timeout=60)
            result = resp.json()
            if result.get("errcode") != 0:
                return BotResponse.error(f"上传失败: {result.get('errmsg')}")
            return self._post({"msgtype": "file", "file": {"media_id": result["media_id"]}})
        except Exception as e:
            return BotResponse.error(str(e))
    
    # 卡片消息
    def card(self, title: str, desc: str = "", emphasis: tuple = None, sub_title: str = None,
             fields: List[tuple] = None, buttons: List[tuple] = None, url: str = None) -> BotResponse:
        """发送文本通知卡片"""
        card_data = {"card_type": "text_notice", "main_title": {"title": title, "desc": desc}}
        if emphasis:
            card_data["emphasis_content"] = {"title": str(emphasis[0]), "desc": emphasis[1] if len(emphasis) > 1 else ""}
        if sub_title:
            card_data["sub_title_text"] = sub_title
        if fields:
            card_data["horizontal_content_list"] = [{"keyname": k, "value": v} for k, v in fields]
        if buttons:
            card_data["jump_list"] = [{"type": 1, "title": t, "url": u} for t, u in buttons]
        if url:
            card_data["card_action"] = {"type": 1, "url": url}
        return self._post({"msgtype": "template_card", "template_card": card_data})
    
    def card_with_image(self, title: str, desc: str = "", image_url: str = None, items: List[tuple] = None,
                        fields: List[tuple] = None, buttons: List[tuple] = None, url: str = None) -> BotResponse:
        """发送图文展示卡片"""
        card_data = {"card_type": "news_notice", "main_title": {"title": title, "desc": desc}}
        if image_url:
            card_data["card_image"] = {"url": image_url, "aspect_ratio": 1.3}
        if items:
            card_data["vertical_content_list"] = [{"title": t, "desc": d} for t, d in items]
        if fields:
            card_data["horizontal_content_list"] = [{"keyname": k, "value": v} for k, v in fields]
        if buttons:
            card_data["jump_list"] = [{"type": 1, "title": t, "url": u} for t, u in buttons]
        if url:
            card_data["card_action"] = {"type": 1, "url": url}
        return self._post({"msgtype": "template_card", "template_card": card_data})
    
    # 消息模板
    def alert(self, message: str, level: str = "warning", source: str = None,
              details: Dict[str, str] = None, at_all: bool = False) -> BotResponse:
        """告警消息模板"""
        level_config = {
            "info": ("ℹ️", "info"), "warning": ("⚠️", "warning"),
            "error": ("❌", "warning"), "critical": ("🚨", "warning")
        }
        icon, color = level_config.get(level, ("⚠️", "warning"))
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"""{icon} **告警通知**

> 级别：<font color="{color}">{level.upper()}</font>

**告警内容：** {message}
**告警时间：** {now}"""
        if source:
            content += f"\n**告警来源：** {source}"
        if details:
            content += "\n\n---\n**详细信息：**"
            for k, v in details.items():
                content += f"\n- {k}：{v}"
        if at_all:
            content += "\n\n<@all>"
        return self.markdown(content)
    
    def build_notify(self, project: str = "Unknown", status: str = "success", branch: str = "master",
                     commit: str = None, author: str = None, duration: str = None, url: str = None) -> BotResponse:
        """构建通知模板"""
        status_config = {
            "success": ("✅", "info", "成功"), "failed": ("❌", "warning", "失败"),
            "running": ("🔄", "comment", "进行中")
        }
        icon, color, text = status_config.get(status, ("❓", "comment", status))
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"""# {icon} 构建通知

> 状态：<font color="{color}">{text}</font>

**项目：** {project}
**分支：** {branch}
**时间：** {now}"""
        if author:
            content += f"\n**提交者：** {author}"
        if commit:
            content += f"\n**提交信息：** {commit}"
        if duration:
            content += f"\n**构建耗时：** {duration}"
        if url:
            content += f"\n\n[查看详情]({url})"
        return self.markdown(content)
    
    def deploy_notify(self, project: str, env: str = "production", version: str = None,
                      status: str = "success", changes: List[str] = None, url: str = None) -> BotResponse:
        """部署通知模板"""
        status_icon = "🚀" if status == "success" else "❌"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"""# {status_icon} 部署通知

**项目：** {project}
**环境：** {env}
**时间：** {now}"""
        if version:
            content += f"\n**版本：** {version}"
        if changes:
            content += "\n\n**变更内容：**"
            for change in changes[:5]:
                content += f"\n- {change}"
        if url:
            content += f"\n\n[查看详情]({url})"
        return self.markdown(content)
    
    def daily_report(self, title: str, metrics: Dict[str, Union[str, int, float]],
                     summary: str = None, trend: str = None) -> BotResponse:
        """日报模板"""
        now = datetime.now().strftime("%Y-%m-%d")
        content = f"""# 📊 {title}

> 日期：{now}

**核心指标：**"""
        for k, v in metrics.items():
            content += f"\n- **{k}：** {v}"
        if summary:
            content += f"\n\n**总结：** {summary}"
        if trend:
            content += f"\n**趋势：** {trend}"
        return self.markdown(content)
    
    def task_notify(self, title: str, assignee: str = None, deadline: str = None,
                    priority: str = "normal", description: str = None, url: str = None) -> BotResponse:
        """任务通知模板"""
        priority_config = {"low": ("🟢", "低"), "normal": ("🟡", "中"), "high": ("🟠", "高"), "urgent": ("🔴", "紧急")}
        icon, text = priority_config.get(priority, ("🟡", "中"))
        fields = [("优先级", f"{icon} {text}")]
        if assignee:
            fields.append(("负责人", assignee))
        if deadline:
            fields.append(("截止时间", deadline))
        return self.card(title=f"📋 {title}", desc=description or "", fields=fields,
                        buttons=[("查看详情", url)] if url else None, url=url)
    
    # 批量发送
    def batch(self, messages: List[tuple], interval: float = 0.5) -> List[BotResponse]:
        """批量发送消息"""
        results = []
        method_map = {
            "text": self.text, "markdown": self.markdown, "image": self.image,
            "news": self.news, "file": self.file, "card": self.card, "alert": self.alert,
        }
        for i, msg in enumerate(messages):
            msg_type, content = msg[0], msg[1]
            kwargs = msg[2] if len(msg) > 2 else {}
            method = method_map.get(msg_type)
            if not method:
                results.append(BotResponse.error(f"未知消息类型: {msg_type}"))
                continue
            result = method(content, **kwargs) if kwargs else method(content)
            results.append(result)
            if i < len(messages) - 1:
                time.sleep(interval)
        self.logger.info(f"批量发送完成: {len(results)} 条消息")
        return results
    
    async def async_batch(self, messages: List[tuple], concurrency: int = 3) -> List[BotResponse]:
        """异步批量发送"""
        semaphore = asyncio.Semaphore(concurrency)
        async def send_one(msg):
            async with semaphore:
                msg_type, content = msg[0], msg[1]
                if msg_type == "text":
                    return await self.async_text(content)
                elif msg_type == "markdown":
                    return await self.async_markdown(content)
                elif msg_type == "image":
                    return await self.async_image(content)
                else:
                    loop = asyncio.get_event_loop()
                    method_map = {"news": self.news, "file": self.file, "card": self.card}
                    method = method_map.get(msg_type)
                    if method:
                        return await loop.run_in_executor(self._executor, method, content)
                    return BotResponse.error(f"未知消息类型: {msg_type}")
        return await asyncio.gather(*[send_one(msg) for msg in messages])
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._executor.shutdown(wait=False)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._executor.shutdown(wait=False)


# 便捷函数
_default_bot: WeChatBot = None

def get_bot(**kwargs) -> WeChatBot:
    global _default_bot
    if _default_bot is None:
        _default_bot = WeChatBot(**kwargs)
    return _default_bot

def send_text(content: str, **kwargs) -> BotResponse:
    return get_bot().text(content, **kwargs)

def send_markdown(content: str) -> BotResponse:
    return get_bot().markdown(content)

def send_image(source: Union[str, bytes]) -> BotResponse:
    return get_bot().image(source)

def send_file(file_path: str) -> BotResponse:
    return get_bot().file(file_path)

def send_alert(message: str, **kwargs) -> BotResponse:
    return get_bot().alert(message, **kwargs)
