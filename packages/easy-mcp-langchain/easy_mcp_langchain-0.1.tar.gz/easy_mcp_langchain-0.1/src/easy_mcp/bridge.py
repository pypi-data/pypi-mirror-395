from contextlib import AsyncExitStack
from typing import Dict,Any,Type
from langchain_core.tools import StructuredTool
from .client import MCPClient
from pydantic import Field,create_model
from typing import List
import logging

logger = logging.getLogger(__name__) # 初始化logger


# ===MCP适配器实现===
class LangChainMCPAdapter:
    """
    MCP适配器：将MCP客户端无缝转换为LangChain可用的工具集。
    实现了上下文管理器协议，
    """
    def __init__(self,mcp_client:MCPClient):
        self.client = mcp_client

    async def __aenter__(self):
        """进入上下文，自动建立连接"""
        await self.client.connect()
        return self

    async def __aexit__(self,exc_type,exc_value,exc_tb):
        """退出上下文，自动清理资源"""
        await self.client.cleanup()

    @staticmethod
    def _schema_to_pydantic(name:str,schema:Dict[str,Any]):
        """
        将MCP的JSON Schema动态转换为Pydantic模型
        这是让LLM理解参数要求的关键
        """
        # print(f"🔧 调试: 工具 '{name}' 的 inputSchema = {schema}") # 查看 MCP 返回的原始 inputSchema

        # 所有参数定义
        properties = schema.get("properties",{}) # 允许为空
        # 必需字段
        required = schema.get("required",[]) # 允许为空

        # 初始空字典
        fields = {}

        # 类型映射表：将JSON类型映射为Python类型
        type_map = {
            "string":str,
            "integer":int,
            "number":float,
            "boolean":bool,
            "array":list,
            "object":dict
        }

        for field_name,field_info in properties.items():
            # 1.获取字段类型
            json_type = field_info.get("type","string")
            python_type = type_map.get(json_type,Any)

            # 2.获取描述
            description = field_info.get("description","")

            # 3.是否为必需项
            # 如果是必填，默认值为 ... (Ellipsis): 否则为None
            if field_name in required:
                default_value = ...
            else:
                default_value = None

            # 4.构建Pydantic字段定义
            fields[field_name] = (python_type,Field(default=default_value,description=description))

        # 动态创建一个Pydantic模型类
        return create_model(f"{name}Schema",**fields)

    async def get_tools(self):
        """
        核心方法：获取并转换工具
        返回的是标准的LangChain Tool列表，可以直接喂给bind_tools
        """
        # 从MCP Server 获取原始工具列表
        mcp_tools = await self.client.list_tools()
        langchain_tools = []


        for tool_info in mcp_tools:
            # 1.动态生成参数模型 -- 要处理schema为空的情况
            # inputSchema一般会放好MCP各种工具/参数的介绍
            raw_schema = tool_info.get("input_schema",{})
            args_model = self._schema_to_pydantic(tool_info["name"],raw_schema)
            # 2.定义执行函数
            async def _dynamic_tool_func(tool_name=tool_info["name"],**kwargs):
                # ⚠️:必须绑定 tool_name 默认参数，否则循环会覆盖 tool_name
                return await self.client.call_tool(tool_name,kwargs)

            # 3.包装成llm可调用的工具(注入args_schema)
            tool = StructuredTool.from_function(
                coroutine=_dynamic_tool_func,
                name=tool_info["name"],
                description=tool_info["description"],
                args_schema=args_model # 把说明书传给 LangChain
            )
            langchain_tools.append(tool)
        return langchain_tools

# ===MCP工具批量初始化===
async def _load_mcp_tools(stack: AsyncExitStack, configs: list):
    """
    遍历配置，批量建立 MCP 连接并收集工具。
    要求外部传入 AsyncExit 以托管生命周期
    """
    all_tools = []
    for conf in configs:
        logger.info(f"🔌 Connecting to MCP Server: {conf['name']}...")
        # 初始化 Client
        client = MCPClient(
            command=conf["command"],
            args=conf["args"],
            env=conf.get("env")  # 可选参数
        )
        # 🔥:enter_async_context 替代了async with 缩进
        # 这样无论有多少个MCP，代码层级都不会变深
        adapter = await stack.enter_async_context(LangChainMCPAdapter(client))
        # 批量获取一个MCP下的所有工具
        tools = await adapter.get_tools()
        logger.debug(f"    ✅ Loaded tools: {[t.name for t in tools]}")
        all_tools.extend(tools)

    return all_tools

# ===高层API:安全的上下文管理器===
class MCPToolLoader:
    """
    用户友好的MCP 工具加载器

    ✅️ 自动管理子进程生命周期
    ✅️ 确保工具在使用期间服务不退出
    ✅️ 兼容高级用户 (仍可直接使用_load_mcp_tools)

    用法:
        async with MCPToolLoader() as tools:
        app = build_graph(tools)
        await run_agent(app,"query...")
    """
    def __init__(self,configs:List[Dict[str,Any]]):
        self.configs = configs
        self._stack = None
        self._tools = None

    async def __aenter__(self):
        self._stack = AsyncExitStack() # 创建清理栈
        await self._stack.__aenter__() # 激活清理栈
        self._tools = await _load_mcp_tools(self._stack,self.configs) # 加载工具并登记到栈
        return self._tools

    async def __aexit__(self,*exc_type):
        await self._stack.__aexit__(*exc_type) # 触发栈中所有清理操作(无论有无异常)





















