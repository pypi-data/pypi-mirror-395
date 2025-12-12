import os
from typing import Annotated, Any, TypedDict

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from trajectory.common.tracer import Tracer
from trajectory.integrations.langgraph import TrajectoryCallbackHandler

# -------- Tools --------


@tool
def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


@tool
def get_time() -> str:
    """Return current time as string."""
    import datetime

    return datetime.datetime.now().isoformat(timespec="seconds")


# -------- Graph state --------


class State(TypedDict):
    messages: Annotated[list[Any], add_messages]


# -------- Model (bind tools) --------

llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
tools = [add, get_time]
llm_with_tools = llm.bind_tools(tools)


# -------- Nodes --------


def chat_node(state: State, *, config=None) -> State:
    """Call the LLM; it may return tool calls."""
    resp: AIMessage = llm_with_tools.invoke(state["messages"], config=config)
    return {"messages": [resp]}


tool_node = ToolNode(tools)


# -------- Build graph --------

graph = StateGraph(State)
graph.add_node("chat", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat")
# If model requested tools => go to tools; else END
graph.add_conditional_edges("chat", tools_condition, {"tools": "tools", "__end__": END})
graph.add_edge("tools", "chat")

app = graph.compile(checkpointer=MemorySaver())


# -------- Trajectory tracer --------

tracer = Tracer(
    project_name="langgraph_example",
    enable_monitoring=True,
    enable_evaluations=False,
    api_key=os.getenv("TRAJECTORY_API_KEY"),
    organization_id=os.getenv("TRAJECTORY_ORG_ID"),
)

jv_cb = TrajectoryCallbackHandler(tracer)


# -------- Run --------


def main():
    # Make sure OPENAI_API_KEY is set in env
    prompt = "First add 2 and 3 using tools, then tell me the current time."
    state: State = {"messages": [HumanMessage(content=prompt)]}

    run_config = {
        "callbacks": [jv_cb],
        "configurable": {
            "thread_id": "123",
        },
    }
    print("Streaming events...")
    for event in app.stream(state, stream_mode="values", config=run_config):
        last = event.get("messages", [])[-1]
        role = "assistant" if isinstance(last, AIMessage) else "user"
        print(f"[{role}] {getattr(last, 'content', last)}")

    final = app.invoke(state, config=run_config)
    print("\nFinal assistant message:")
    print(final["messages"][-1].content)


if __name__ == "__main__":
    main()
