from backend.app.agent import config
from backend.app.logic.mcp_client import SimpleMCPClient
from mcp import types

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from contextlib import AsyncExitStack
from typing import Any, Optional

from pydantic import create_model

import json

from langchain_core.tools import StructuredTool

from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph, MessagesState, START
from langchain_core.messages import SystemMessage

from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableConfig

from openai import RateLimitError
class MCPChatApp:
    def __init__(self, servers: list[dict]):
        self.clients = [
            SimpleMCPClient(command = s["command"], args=s["server_args"]) for s in servers
        ]

        self.mcp_tools: list[types.Tool] = []
        self.langchin_tools = []

        # self.llm = ChatOllama(
        #     model = "qwen2.5:7b",
        #     temperature=0.6,
        #     num_ctx=2048,
        # )

        self.llm = ChatOpenAI(
            model=config.MODEL_NAME,
            base_url=config.OPENROUTER_BASE_URL,
            api_key=config.require_api_key(),
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
        )

        self.checkpointer = InMemorySaver()
        self.agent = None

        # AsyncExitStack kept alive for the whole server lifetime
        # so MCP clients stay connected while FastAPI runs
        self._stack = AsyncExitStack()

    def _wrap_mcp_tool(self, client: SimpleMCPClient, mcp_tool: types.Tool) -> StructuredTool:
        """
        Wrap one MCP tool as a LangChain tool.
        """

        description = mcp_tool.description or f"Execute {mcp_tool.name}"

        if getattr(mcp_tool, "inputSchema", None):
            description += (
                "\nInput schema: "
                + json.dumps(mcp_tool.inputSchema, ensure_ascii=False)
            )

        # build a pydantic model from the real schema fields
        # so langchain knows exactly how to map args into the function

        properties = mcp_tool.inputSchema.get("properties", {}) if getattr(mcp_tool, "inputSchema", None) else {}

        # Create a dictionary where each property becomes a field definition:
        # Each field is defined as a tuple:
        #   (type, default_value)
        # Here:
        #   - type is Optional[Any], meaning the field can accept any value or None
        #   - default value is None, making the field optional
        fields = {name: (Optional[Any], None) for name in properties}

        DynamicSchema  = create_model(f"{mcp_tool.name}Input", **fields)

        tool_name = mcp_tool.name

        async def run_mcp_tool(**kwargs) -> str:
            args = {k: v for k, v in kwargs.items() if v is not None}
            result = await client.call_tool(tool_name, args)
            if getattr(result, "content", None):
                content = result.content

                if isinstance(content, list) and len(content) > 0:
                    return str(content[0].text) if hasattr(content[0], "text") else str(content)
                return str(content)
            return "Tool executed successfully"
        
        return StructuredTool.from_function(
            coroutine=run_mcp_tool,
            name=tool_name,
            description=description,
            args_schema=DynamicSchema
        )
    

    def _build_agent(self) -> CompiledStateGraph:
        """
        Custom LangGraph graph.
        Enforces one tool call at a time - no batch processing.
        """
        system_prompt = """You are a webpage automation assistant.

                        RULES — follow in strict order:
                        1. One tool call per turn. Always wait for the result.
                        2. After searching for anything ensure you click on the associated search button to compelete the user request
                        """
        llm_with_tools  = self.llm.bind_tools(self.langchin_tools)
        async def call_model(state: MessagesState):
            messages = [SystemMessage(content=system_prompt)] + state["messages"]

            try:
                response = await llm_with_tools.ainvoke(messages)
            except RateLimitError as e:
                print(f"Error message OpenRouter rate-limited; falling back to local Ollama {e}")
                return {"messages": []}

            # ── ENFORCE ONE TOOL AT A TIME ──────────────────────────
            # if model tries to call multiple tools at once restrict to one
            if hasattr(response, "tool_calls") and len(response.tool_calls) > 1:
                print(f"Model tried to call {len(response.tool_calls)} tools at once - trimming to one")
                response.tool_calls = [response.tool_calls[0]]
            # ────────────────────────────────────────────────────────

            usage = response.usage_metadata
            if usage:
                print(f"📊 tokens: {usage['input_tokens']} in / {usage['output_tokens']} out / {usage['total_tokens']}")
            
            return {"messages": [response]}
        
        def should_continue(state: MessagesState):
            last_message = state["messages"][-1]
            if last_message.tool_calls:
                return "tools"
            return "__end__"
        
        original_tool_node = ToolNode(self.langchin_tools)

        async def tool_node_with_logging(state: MessagesState, config: RunnableConfig):
            result = await original_tool_node.ainvoke(state, config)
            for msg in result["messages"]:
                preview = str(msg.content)[:120].replace('\n', ' ')
                print(f"  ✅ {msg.name}: {preview}")
            return result
        
        graph = StateGraph(MessagesState)
        
        # when graph arrives at "agent" node → automatically calls call_model(state)
        graph.add_node("agent", call_model)

        # when graph arrives at "tools" node → automatically calls tool_node_with_logging
        graph.add_node("tools", tool_node_with_logging)

        # When START is invoked ALWAYS go to agent node
        graph.add_edge(START, "agent")

        # FROM the agent node, run should_continue to decide where to go next
        # if should_continue returns "tools" → go to tools node
        # if should_continue returns "__end__" → stop
        graph.add_conditional_edges("agent", should_continue)

        # FROM the tools node, ALWAYS go back to agent node
        graph.add_edge("tools", "agent")

        return graph.compile(checkpointer=self.checkpointer)
    
    async def initialize(self):
        print("=" * 60)
        print("MCP Chat App (Web Mode — FastAPI + LangGraph + Ollama)")
        print("=" * 60)

        connected_clients = []
        for client in self.clients:
            connected = await self._stack.enter_async_context(client)
            connected_clients.append(connected)

        print("\nAll clients connected! Available tools:")

        for connected_client in connected_clients:
            mcp_tools = await connected_client.list_tools()

            for tool_def in mcp_tools:
                print(f"  • {tool_def.name}: {tool_def.description}")

                self.langchin_tools.append(self._wrap_mcp_tool(connected_client, tool_def))

        self.agent = self._build_agent()
        print("\nAgent ready. FastAPI listening on http://localhost:8000\n")

    async def shutdown(self):
        # cleanly close all MCP client connections when FastAPI shuts down
        await self._stack.aclose()