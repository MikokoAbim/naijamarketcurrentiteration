from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.agent.main import WebAgentApp
from langchain_core.messages import HumanMessage
import os 
from typing import Any

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    thread_id: str
    page_elements: list[dict[str, Any]] = [] # every chat request needs the current page elements

_chat_app: WebAgentApp | None = None

def get_chat_app() -> WebAgentApp:
    return _chat_app

async def initialize_agent():
    global _chat_app
    _chat_app = WebAgentApp()
    await _chat_app.initialize()

async def shutdown_agent():
    if _chat_app:
        await _chat_app.shutdown()

@router.post("/chat")
async def api_agent_control(request: ChatRequest):
    elements_text = "\n".join(
        f"{el.get('tag', 'element')} '{el.get("text", '')}' id = {el.get("id", '')}"
        for el in request.page_elements
    )
    enriched_message = f"{request.message}\n\nCurrent page elements:\n{elements_text}"

    print(f"\nYou> {request.message}")

    response = await _chat_app.agent.ainvoke(
        {"messages": [HumanMessage(content=enriched_message)]},
        {"configurable": {"thread_id": request.thread_id}},
    )

    actions = []
    for msg in response["messages"]:
        if hasattr(msg, "name") and isinstance(msg.content, str) and msg.content.startswith("ACTION:"):
            parts = msg.content.split(":")

            # ACTION:click:element-id
            if parts[1] == "click":
                actions.append({"type": "click", "id": parts[2]})

            # Action:type:element-id:text
            elif parts[1] == "type":
                actions.append({"type": "type", "id": parts[2], "text": parts[3]})

            # ACTION:press_key:element-id:Enter
            elif parts[1] == "press_key":
                actions.append({"type": "press_key", "id": parts[2], "text": parts[3]})

    response_text = response["messages"][-1].content
    print(f"\nAssistant> {response_text}\n")
    return {
        "response": response_text,
        "actions": actions
    }

