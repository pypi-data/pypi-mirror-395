# generate_and_run_scorer_agent_selfcontained.py
import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from trajectory.common.tracer import Tracer, wrap
from trajectory.data import Example, Trace
from trajectory.scorers.scorer_codegen import ScorerCodeGenerator

load_dotenv()


def ensure_env():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY in your environment")
    if not os.getenv("TRAJECTORY_API_KEY") or not os.getenv("TRAJECTORY_ORG_ID"):
        raise RuntimeError("Set TRAJECTORY_API_KEY and TRAJECTORY_ORG_ID")


# Initialize tracer and OpenAI client (wrapped for tracing)
trajectory_client = Tracer(
    api_key=os.getenv("TRAJECTORY_API_KEY"),
    organization_id=os.getenv("TRAJECTORY_ORG_ID"),
    project_name="nl_scorer_demo_project",
    enable_monitoring=True,
    enable_evaluations=False,
)
openai_client = wrap(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))


# -------------------- Tools (traced) --------------------
@trajectory_client.observe(span_type="tool")
def get_weather(city: str, start_date: str = None, end_date: str = None) -> dict:
    # Minimal mock for demo; ensures a deterministic tool output
    data = {
        "Paris": {"temperature": 72, "condition": "Clear", "humidity": 60},
        "Tokyo": {"temperature": 70, "condition": "Sunny", "humidity": 55},
        "London": {"temperature": 58, "condition": "Cloudy", "humidity": 70},
    }
    res = data.get(city, {"temperature": 70, "condition": "Unknown", "humidity": 50})
    if start_date and end_date:
        res["forecast_period"] = f"{start_date} to {end_date}"
    return res


@trajectory_client.observe(span_type="tool")
def get_attractions(destination: str) -> dict:
    data = {
        "Paris": {
            "attractions": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral"]
        },
        "Tokyo": {
            "attractions": ["Senso-ji Temple", "Shibuya Crossing", "Meiji Shrine"]
        },
        "London": {"attractions": ["Big Ben", "Tower Bridge", "British Museum"]},
    }
    return data.get(destination, {"attractions": ["Main Square", "Old Town"]})


@trajectory_client.observe(span_type="handle_tool_calls")
def handle_tool_calls(tool_calls):
    tool_results = []
    for tc in tool_calls:
        name = tc.function.name
        args = json.loads(tc.function.arguments or "{}")
        if name == "get_weather":
            out = get_weather(**args)
        elif name == "get_attractions":
            out = get_attractions(**args)
        else:
            out = {"error": f"Unknown tool: {name}"}
        tool_results.append(
            {
                "tool_call_id": tc.id,
                "role": "tool",
                "name": name,
                "content": json.dumps(out),
            }
        )
    return tool_results


# -------------------- Agent (traced) --------------------
@trajectory_client.observe(span_type="function")
def run_agent(user_prompt: str) -> str:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "start_date": {"type": "string"},
                        "end_date": {"type": "string"},
                    },
                    "required": ["city"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_attractions",
                "description": "Get top attractions",
                "parameters": {
                    "type": "object",
                    "properties": {"destination": {"type": "string"}},
                    "required": ["destination"],
                },
            },
        },
    ]

    # First call (model may choose tools)
    resp = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_prompt}],
        tools=tools,
        tool_choice="auto",
        max_tokens=200,
    )
    msg = resp.choices[0].message

    if msg.tool_calls:
        # Execute tools
        tool_msgs = handle_tool_calls(msg.tool_calls)
        # Second call with tool results
        messages = [{"role": "user", "content": user_prompt}, msg, *tool_msgs]
        final = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=200,
        )
        return final.choices[0].message.content or ""
    else:
        return msg.content or ""


# -------------------- Runner --------------------
_TRACE_FIELDS = {
    "trace_id",
    "name",
    "created_at",
    "duration",
    "trace_spans",
    "overwrite",
    "offline_mode",
    "rules",
    "has_notification",
    "customer_id",
    "tags",
    "metadata",
    "update_id",
}


def _filter_trace_dict(d: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in (d or {}).items() if k in _TRACE_FIELDS}


def main():
    ensure_env()

    # 1) Run the real agent to produce a traced run (do NOT wrap in trajectory_client.trace, to let decorator create the root trace)
    prompt = "What's the weather in Paris and what are the top attractions?"
    _ = run_agent(prompt)

    # 2) Grab most recent recorded trace from tracer
    if not getattr(trajectory_client, "traces", None):
        raise RuntimeError(
            "No traces recorded; ensure tracing is enabled and the agent ran."
        )
    raw = trajectory_client.traces[-1]
    tr = Trace(**_filter_trace_dict(raw))
    print(f"🔍 Trace: {tr}")
    # 3) Example with expected tool order (LLM may vary; this is just for demo)
    ex = Example(
        input={"prompt": prompt},
        expected_tools=[
            {"tool_name": "get_weather", "parameters": {"city": "Paris"}},
            {"tool_name": "get_attractions", "parameters": {"destination": "Paris"}},
        ],
        expected_output="Paris weather and attractions summary",
    )

    # 4) Generate a simple scorer from natural language
    spec = """
    Create a scorer that checks tool call ordering. Score = fraction of matching
    positions between actual tool calls (from tool spans) and example.expected_tools.
    Name it ToolOrderingNLScorer, threshold 0.8, score_type "tool_ordering_nl".
    Return breakdown with actual and expected tool names.
    """
    gen = ScorerCodeGenerator(llm_model="gpt-4o-mini")
    code = gen.generate_code(spec, class_name="ToolOrderingNLScorer")

    print("\n=== Generated Scorer Code ===\n")
    print(code)

    # 5) Compile/load and score
    ScorerClass = gen.compile_and_load(
        code,
        module_name="generated_tool_order_scorer",
        class_name="ToolOrderingNLScorer",
    )
    scorer = ScorerClass()
    result = scorer.score_trajectory(tr, ex)

    print("\n=== Scoring Result ===")
    print(result)


if __name__ == "__main__":
    main()
