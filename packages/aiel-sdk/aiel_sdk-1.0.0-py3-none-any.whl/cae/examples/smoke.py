from cae.sdk import StateGraph, START, END, tools_condition, tool, mcp_server, http, ChatPromptTemplate

@tool("fetch_profile")
def fetch_profile(ctx, payload):
    return {"ok": True}

mcp = mcp_server("user_support")

@mcp.tool()
async def create_user(ctx, name: str, email: str) -> dict:
    return {"id": "u1"}

@http.post("/test")
def handler(ctx, body: dict):
    return {"received": body}

g = StateGraph(dict).add_node("x", lambda s: s).add_edge(START, END)
app = g.compile()

print("OK", tools_condition({}), app.invoke({"hello": "world"}), ChatPromptTemplate.from_messages([]))
