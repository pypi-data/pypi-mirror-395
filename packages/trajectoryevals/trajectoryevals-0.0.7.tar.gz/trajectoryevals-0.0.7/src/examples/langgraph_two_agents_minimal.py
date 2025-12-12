# Save as: trajectory/src/judgeval/examples/langgraph_two_agents_minimal.py

import json
import operator
import os
from typing import Annotated

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from trajectory import Tracer
from trajectory.integrations.langgraph import (
    JudgevalCallbackHandler,  # single callback at invoke
)


# Graph state
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]


# Tools (one per agent)
@tool
def get_current_time() -> str:
    """Return current time as string."""
    import datetime

    return datetime.utcnow().isoformat() + "Z"


@tool
def add_numbers(a: float, b: float) -> str:
    """Add two numbers."""
    return str(a + b)


TOOLS_PLANNER = [get_current_time]
TOOLS_EXECUTOR = [add_numbers]

TOOL_REGISTRY = {
    "get_current_time": get_current_time,
    "add_numbers": add_numbers,
}


def _execute_tools(ai_msg: AIMessage) -> list[ToolMessage]:
    results: list[ToolMessage] = []
    tool_calls = getattr(ai_msg, "tool_calls", None) or []
    for tc in tool_calls:
        name = tc.get("name")
        args = tc.get("args") or {}
        call_id = tc.get("id")

        # normalize args
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                args = {}

        fn = TOOL_REGISTRY.get(name)
        if not fn:
            result = f"ERROR: unknown tool '{name}'"
        else:
            try:
                if hasattr(fn, "invoke"):
                    tool_input = (
                        None
                        if (args is None or (isinstance(args, dict) and not args))
                        else args
                    )
                    result = fn.invoke(tool_input)
                else:
                    # raw function
                    if isinstance(args, dict) and not args:
                        result = fn()
                    elif isinstance(args, dict):
                        result = fn(**args)
                    else:
                        result = fn(args)
            except TypeError:
                result = f"ERROR: bad args for '{name}': {args}"
            except Exception as e:
                result = f"ERROR: tool '{name}' failed: {e}"

        results.append(ToolMessage(content=str(result), tool_call_id=call_id))
    return results


# Agent nodes (no per-node callbacks; single callback at graph.invoke)
def planner_node(state: AgentState) -> AgentState:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are Planner. Decide the next step and call your tool if needed.",
            ),
            ("placeholder", "{messages}"),
        ]
    )
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0).bind_tools(TOOLS_PLANNER)
    ai = (prompt | model).invoke({"messages": state["messages"]})
    out: list[BaseMessage] = [ai]
    if getattr(ai, "tool_calls", None):
        out += _execute_tools(ai)
    return {"messages": out}


def executor_node(state: AgentState) -> AgentState:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are Executor. Complete tasks and call your tool if needed.",
            ),
            ("placeholder", "{messages}"),
        ]
    )
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0).bind_tools(TOOLS_EXECUTOR)
    ai = (prompt | model).invoke({"messages": state["messages"]})
    out: list[BaseMessage] = [ai]
    if getattr(ai, "tool_calls", None):
        out += _execute_tools(ai)
    return {"messages": out}


# Build graph
wf = StateGraph(AgentState)
wf.add_node("planner", planner_node)
wf.add_node("executor", executor_node)
wf.add_edge(START, "planner")
wf.add_edge("planner", "executor")
wf.add_edge("executor", END)
graph = wf.compile()


if __name__ == "__main__":
    tracer = Tracer(
        project_name="langgraph_two_agents_demo",
        enable_monitoring=True,
        enable_evaluations=False,
        trace_across_async_contexts=True,
        api_key=os.getenv("TRAJECTORY_API_KEY"),
        organization_id=os.getenv("TRAJECTORY_ORG_ID"),
    )
    cb = JudgevalCallbackHandler(tracer)

    # Single callback at invoke; pass agent mapping once.
    # JudgevalCallbackHandler will map node -> agent_name using this.
    run_config = {
        "callbacks": [cb],
        "metadata": {
            "agent_map": {
                "planner": "planner",
                "executor": "executor",
            }
        },
        "tags": ["graph:two_agents"],
        "configurable": {"thread_id": "demo_thread_1"},
    }

    initial: AgentState = {
        "messages": [
            HumanMessage(content="Add 2 and 3, then tell me the current UTC time.")
        ]
    }

    result = graph.invoke(initial, config=run_config)
    print("Final:", result["messages"][-1].content)
