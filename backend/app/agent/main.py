from pathlib import Path
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from backend.app.agent import config
from langgraph.graph import MessagesState, END, StateGraph, START
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph
from langchain_core.runnables import RunnableConfig

SKILLS_DIRECTORY = Path(__file__).parent / "skills"

SKILL_CATALOG = {
    "web_navigation_skill": "Guidance for navigating and interacting with web forms and page elements in the marketplace.",
}


def read_skill_file(name: str) -> str:
    return (SKILLS_DIRECTORY / f"{name}.md").read_text(encoding="utf-8").strip()


@tool
def load_skill(skill_name: str) -> str:
    """Load the full instructions for a named skill from the catalog"""
    if skill_name not in SKILL_CATALOG:
        raise ValueError(f"Unknown skill: {skill_name}. Available: {list(SKILL_CATALOG)}")
    return read_skill_file(skill_name)


@tool
def click_element(element_id: str) -> str:
    """Click an element on the page by its data-agent id."""
    return f"ACTION:click:{element_id}"


@tool
def type_into(element_id: str, text: str) -> str:
    """Type text into an input field by its data-agent id."""
    return f"ACTION:type:{element_id}:{text}"


@tool
def press_key(element_id: str, key: str) -> str:
    """Press key on a focused element"""
    return f"ACTION:press_key:{element_id}:{key}"


@tool
def clear_input(element_id: str) -> str:
    """Clear an input field by id"""
    return f"ACTION:clear:{element_id}"


skill_tools = [load_skill]
automation_tools = [click_element, type_into, press_key, clear_input]
all_tools = skill_tools + automation_tools

llm = ChatOpenAI(
    model=config.MODEL_NAME,
    base_url=config.OPENROUTER_BASE_URL,
    api_key=config.require_api_key(),
    temperature=config.TEMPERATURE,
    max_completion_tokens=config.MAX_TOKENS,
).bind_tools(all_tools)

catalog_lines = "\n".join(f"- {name}: {desc}" for name, desc in SKILL_CATALOG.items())

SYSTEM_PROMPT = (
    "You are a webpage automation assistant for the NaijaMarketAgent marketplace. "
    "Use click_element, type_into, press_key, and clear_input to interact with UI elements. "
    "If a tool call fails, acknowledge the error and ask the user to try again.\n\n"
    "You have access to skills with more detailed guidance. Call load_skill "
    "with the skill name if one looks relevant before proceeding. Available skills:\n"
    f"{catalog_lines}\n\n"
    "RULES:\n"
    "1. One tool call per turn. Always wait for the result.\n"
    "2. After searching for anything, click the associated search button to complete the request.\n"
)


async def call_model(state: MessagesState):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    try:
        response = await llm.ainvoke(messages)
    except Exception as exc:
        return {"messages": [AIMessage(content=f"Sorry, I encountered an error calling the model: {exc}")]}
    
    if hasattr(response, "tool_calls") and len(response.tool_calls) > 1:
        response.tool_calls = [response.tool_calls[0]]
    
    return {"messages": [response]}


def route_after_agent(state: MessagesState):
    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return END

    requested_tool_name = last_message.tool_calls[0]["name"]

    if requested_tool_name == "load_skill":
        return "skill_tools"

    if requested_tool_name in {t.name for t in automation_tools}:
        return "automation_tools"

    raise ValueError(f"Unsupported tool requested: {requested_tool_name}")


original_tool_node = ToolNode(automation_tools)


async def tool_node_with_logging(state: MessagesState, config: RunnableConfig):
    result = await original_tool_node.ainvoke(state, config)
    for msg in result["messages"]:
        preview = str(msg.content)[:120].replace('\n', ' ')
        print(f"  ✅ {msg.name}: {preview}")
    return result


def build_graph() -> CompiledStateGraph:
    graph = StateGraph(MessagesState)

    graph.add_node("agent", call_model)
    graph.add_node("automation_tools", tool_node_with_logging)
    graph.add_node("skill_tools", ToolNode(skill_tools, handle_tool_errors=True))

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", route_after_agent)
    graph.add_edge("automation_tools", "agent")
    graph.add_edge("skill_tools", "agent")

    return graph.compile(checkpointer=InMemorySaver())


class WebAgentApp:
    """Web navigation agent app using LangGraph and skill-based tools."""

    def __init__(self):
        self.agent: CompiledStateGraph = None
        self.checkpointer = InMemorySaver()

    async def initialize(self):
        print("=" * 60)
        print("Web Navigation Agent (LangGraph + OpenRouter)")
        print("=" * 60)
        print(f"\nConnecting to {config.MODEL_NAME} via OpenRouter...")
        self.agent = build_graph()
        print("Agent ready. Ready to navigate the marketplace.\n")

    async def shutdown(self):
        pass
