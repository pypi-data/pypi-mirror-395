# gwozai-wechat-bot

企业微信群机器人 Python SDK，简单易用，功能完善。

[![PyPI version](https://badge.fury.io/py/gwozai-wechat-bot.svg)](https://badge.fury.io/py/gwozai-wechat-bot)
[![Python](https://img.shields.io/pypi/pyversions/gwozai-wechat-bot.svg)](https://pypi.org/project/gwozai-wechat-bot/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 特性

- ✅ 支持所有消息类型（文本、Markdown、图片、图文、文件、卡片）
- ✅ 自动重试机制
- ✅ 异步发送支持
- ✅ 内置消息模板（告警、构建、部署、任务、日报）
- ✅ 批量发送（自动频率控制）
- ✅ 完善的类型提示
- ✅ 日志记录

## 安装

```bash
pip install gwozai-wechat-bot
```

如需支持 `.env` 文件配置：

```bash
pip install gwozai-wechat-bot[dotenv]
```

## 快速开始

```python
from gwozai_wechat_bot import WeChatBot

# 创建机器人
bot = WeChatBot(key="your-webhook-key")

# 发送文本
bot.text("Hello World")

# 发送 Markdown
bot.markdown("# 标题\n**加粗**")

# 发送图片
bot.image("/path/to/image.png")

# 发送文件
bot.file("/path/to/file.pdf")
```

## 环境变量配置

创建 `.env` 文件：

```env
WECHAT_WEBHOOK_KEY=your-webhook-key
```

然后直接使用：

```python
from gwozai_wechat_bot import WeChatBot

bot = WeChatBot()  # 自动读取环境变量
bot.text("Hello!")
```

## 消息类型

### 文本消息

```python
bot.text("Hello World")
bot.text("紧急通知！", at_all=True)
bot.text("提醒", mentioned=["zhangsan", "lisi"])
```

### Markdown 消息

```python
bot.markdown("""
# 标题
> 引用

**加粗** 普通文字

<font color="info">绿色</font>
<font color="warning">橙色</font>
""")
```

### 图片消息

```python
bot.image("/path/to/image.png")       # 本地文件
bot.image("https://example.com/a.png") # URL
bot.image(image_bytes)                 # 字节数据
```

### 图文消息

```python
bot.news_single(
    title="文章标题",
    url="https://example.com",
    description="文章描述",
    picurl="https://example.com/cover.png"
)
```

### 文件消息

```python
bot.file("/path/to/report.pdf")
```

### 卡片消息

```python
bot.card(
    title="审批通知",
    desc="您有待处理的审批",
    emphasis=("3", "待审批"),
    fields=[("申请人", "张三"), ("类型", "请假")],
    buttons=[("查看详情", "https://example.com")]
)
```

## 消息模板

```python
# 告警通知
bot.alert("服务器宕机", level="critical", source="订单服务")

# 构建通知
bot.build_notify(project="my-app", status="success", branch="main")

# 部署通知
bot.deploy_notify(project="my-app", env="production", version="v1.0.0")

# 任务通知
bot.task_notify(title="完成文档", assignee="张三", priority="high")

# 日报
bot.daily_report(title="系统日报", metrics={"请求量": "100万"})
```

## 异步发送

```python
import asyncio

async def main():
    bot = WeChatBot(key="your-key")
    await bot.async_text("异步消息")
    await bot.async_markdown("# 异步 Markdown")

asyncio.run(main())
```

## 批量发送

```python
bot.batch([
    ("text", "消息1"),
    ("text", "消息2"),
    ("markdown", "# 标题"),
])
```

## 便捷函数

```python
from gwozai_wechat_bot import send_text, send_markdown, send_alert

send_text("Hello")
send_markdown("# 标题")
send_alert("告警", level="error")
```

## License

MIT © gwozai
