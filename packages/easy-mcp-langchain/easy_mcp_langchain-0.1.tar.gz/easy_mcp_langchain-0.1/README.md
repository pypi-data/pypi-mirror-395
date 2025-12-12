# 🚀 Easy MCP — 让 MCP 工具像本地函数一样简单

一行代码集成任意 MCP 服务
自动管理子进程生命周期 · 零配置接入 LangChain / LangGraph Agent

## ✨ 特性

- ✅ **自动资源管理**：无需手动启动/关闭 MCP 服务
- ✅ **零侵入集成**：返回标准 LangChain Tool 列表
- ✅ **多服务支持**：高德地图、天气、数据库 MCP 一次性接入
- ✅ **生产可用**：异常安全、子进程隔离、异步非阻塞

## 🚀 快速开始

### 1. 安装
```bash
pip install easy-mcp
```

### 2. 🧪「5 行代码」调用高德地图 MCP

```python
from src.easy_mcp import MCPToolLoader
import asyncio


async def main():
    async with MCPToolLoader([{
        "command": "npx",
        "args": ["-y", "@amap/amap-maps-mcp-server"],
        "env": {"AMAP_MAPS_API_KEY": "你的密钥"}
    }]) as tools:
        search = next(t for t in tools if t.name == "maps_text_search")
        print(await search.ainvoke({"keywords": "西湖", "city": "杭州"}))


asyncio.run(main())
```

### 输出示例
```json
{
  "pois": [
    {"name": "杭州西湖", "location": "120.1551,30.2741", ...}
  ]
}
```

## 🤖 构建 MCP-Powered Agent

```python
from langgraph.graph import StateGraph
from src.easy_mcp import MCPToolLoader

async with MCPToolLoader([高德配置]) as tools:
    graph = StateGraph(MessagesState)
    graph.add_node("agent", create_agent_node(tools))
    # ... 添加更多工具结点 ...
    app = graph.compile()
    await app.ainvoke({"messages": [("user", "西湖附近有什么酒店？")]})
```

👉 查看完整示例：`examples/full_agent_demo.py`

## 🔧 支持的 MCP 服务

| 服务 | 安装命令 | 必需环境变量 |
|------|----------|--------------|
| 高德地图 | `npx @amap/amap-maps-mcp-server` | `AMAP_MAPS_API_KEY` |
| 天气 API | `npx @weather/mcp-server` | `WEATHER_API_KEY` |
| 自定义 MCP | 任意符合 MCP 协议的进程 | - |

## 📂 项目结构

```
easy-mcp/
├── examples/
│   ├── quickstart.py          # 5 行上手示例
│   └── full_agent_demo.py     # 完整 LangGraph Agent 示例
├── src/easy_mcp/
│   ├── __init__.py            # 导出 MCPToolLoader
│   ├── bridge.py              # MCP ↔ LangChain 适配器
│   └── client.py              # MCP 客户端封装
└── README.md
```

## ❓ 常见问题（FAQ）

**Q: 如何添加新的 MCP 服务？**

只需在 MCPToolLoader([...]) 的列表中添加一个新的配置：

```json
{
    "command": "python",
    "args": ["my_mcp_server.py"],
    "env": {"API_KEY": "..."}
}
```

**Q: 子进程会残留吗？**

不会。
MCPToolLoader 使用 AsyncExitStack 和自动回收机制保证：
- MCP 子进程 100% 自动退出
- 不留下僵尸进程
- 异常情况下仍可安全清理