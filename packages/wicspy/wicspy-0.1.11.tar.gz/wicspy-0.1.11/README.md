<!--
 * @Author: wicsp wicspa@gmail.com
 * @Date: 2024-08-26 17:01:30
 * @LastEditors: wicsp wicspa@gmail.com
 * @LastEditTime: 2024-08-26 17:03:45
 * @FilePath: /wicspy/README.md
 * @Description: 
 * 
 * Copyright (c) 2024 by wicsp, All Rights Reserved. 
-->
# wicspy

一个全面的 Python 工具库，提供各种实用功能和工具集合。

## 功能特点

- **消息通知模块**：支持 Bark 等多种通知渠道
- **服务器工具**：监控和收集服务器信息
- **网络工具**：网页抓取、API 客户端等
- **系统工具**：文件操作、日志管理等
- **安全工具**：加密解密、令牌管理等

## 安装

```bash
pip install wicspy
```

或者从源码安装：

```bash
git clone https://github.com/wicsp/wicspy.git
cd wicspy
pip install -e .
```

## 使用示例

### Bark 消息通知

```python
from wicspy.messaging import bark

# 发送 Bark 通知
bark.send_message("测试标题", "这是测试内容")
```

### 网页内容抓取

```python
from wicspy.web import scraper

# 抓取网页内容
content = scraper.fetch_page("https://example.com")
print(content.title)
```

## 环境变量配置

某些功能需要配置环境变量：

- `BARK_ID`: Bark 服务的 ID
- `API_KEY`: 用于 API 访问的密钥

推荐使用 `.env` 文件和 `python-dotenv` 进行管理。

## 开发说明

1. 克隆仓库
2. 安装开发依赖：`pip install -e ".[dev]"`
3. 运行测试：`pytest`

## 许可证

MIT 许可证
