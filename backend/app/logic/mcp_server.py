from mcp.server.fastmcp import FastMCP

mcp = FastMCP("web-mcp-server")


@mcp.tool(
    name = "click_element",
    description="Click an element on the page by its data-agent id."
)
def click_element(element_id: str) -> str:
    return f"ACTION:click:{element_id}"

@mcp.tool(
    name = "type_into",
    description="Type text into an input field by its data-agent id. "
)
def type_into(element_id: str, text: str) -> str:
    return f"ACTION:type:{element_id}:{text}"

@mcp.tool(
    name = "press_key",
    description = "Press key on a focused element"
)
def press_key(element_id: str, key: str) -> str:
    return f"ACTION:press_key:{element_id}:{key}"

@mcp.tool(
    name = "clear_input",
    description="Clear an input field by id"
)
def clear_input(element_id: str) -> str:
    return f"ACTION:clear:{element_id}"

if __name__ == "__main__":
    mcp.run(transport="stdio")