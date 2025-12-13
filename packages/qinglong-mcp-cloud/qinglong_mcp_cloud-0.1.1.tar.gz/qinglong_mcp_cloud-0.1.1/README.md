# 青龙面板 MCP Server (Cloud Version)

[![PyPI version](https://badge.fury.io/py/qinglong-mcp-cloud.svg)](https://badge.fury.io/py/qinglong-mcp-cloud)

这是青龙面板 MCP Server 的云部署版本，支持在每次调用时动态传递凭证参数，适合云端部署场景。

## 与标准版的区别

- **标准版** (`qinglong-mcp-server`): 从本地 `.env` 文件读取配置，适合本地部署
- **云版** (`qinglong-mcp-cloud`): 每次调用时传递凭证参数，无状态设计，适合云端部署

## 功能

- `list_qinglong_tasks`: 查询青龙面板中的所有定时任务列表
- `run_task`: 执行任务并等待完成，自动返回执行日志（最多等待30秒）
- `run_task_async`: 异步启动任务，不等待执行完成
- `get_task_logs`: 获取青龙面板中指定任务的执行日志
- `get_task_status`: 获取青龙面板中指定任务的执行状态

## 安装

使用 pip 安装：

```bash
pip install qinglong-mcp-cloud
```

或使用 uvx（推荐，无需安装）：

```bash
uvx qinglong-mcp-cloud
```

## 使用

### 在 MCP 客户端中使用

编辑 MCP 配置文件，添加以下内容：

```json
{
  "mcpServers": {
    "qinglong-cloud": {
      "command": "uvx",
      "args": ["qinglong-mcp-cloud"]
    }
  }
}
```

配置文件位置（以 Kiro CLI 为例）：
- `~/.kiro/settings/mcp.json`

### 参数说明

每次调用工具时需要提供以下参数：

- `qinglong_url`: 青龙面板的 URL（例如：https://your-qinglong-url.com）
- `client_id`: 青龙面板的 Client ID
- `client_secret`: 青龙面板的 Client Secret
- `task_id`: 任务 ID（部分操作需要）

### 使用示例

在对话中提供凭证信息：

```
帮我查询青龙面板的任务列表
URL: https://your-qinglong-url.com
Client ID: your_client_id
Client Secret: your_client_secret
```

AI 助手会自动调用相应的工具并传递这些参数。

## 安全建议

- 避免在公共频道或日志中暴露 Client Secret
- 建议配合会话级缓存或加密存储使用
- 定期轮换 Client ID 和 Client Secret

## 升级

```bash
pip install -U qinglong-mcp-cloud
```

## 项目地址

- PyPI: https://pypi.org/project/qinglong-mcp-cloud/
- GitHub: https://github.com/pholex/qinglong-mcp-cloud

## 联系方式

Email: pholex@gmail.com
