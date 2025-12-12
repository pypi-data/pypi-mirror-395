import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

# Trajectory tracing
from trajectory import Tracer, wrap

# --- Setup --------------------------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TRAJECTORY_API_KEY = os.getenv("TRAJECTORY_API_KEY")
TRAJECTORY_ORG_ID = os.getenv("TRAJECTORY_ORG_ID")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

judgment = Tracer(
    api_key=TRAJECTORY_API_KEY,
    organization_id=TRAJECTORY_ORG_ID,
    project_name="simple_agent_project",
    enable_monitoring=True,
    enable_evaluations=False,
)

client = OpenAI(api_key=OPENAI_API_KEY)
traced_client = wrap(client)


# --- Tool(s) ------------------------------------------------------------------


@judgment.observe(span_type="tool")
def lookup_attractions(city: str) -> str:
    attractions = {
        "paris": [
            "Eiffel Tower",
            "Louvre Museum",
            "Notre-Dame Cathedral",
            "Arc de Triomphe",
            "Sacré-Cœur",
        ],
        "london": [
            "British Museum",
            "Tower of London",
            "London Eye",
            "Buckingham Palace",
        ],
    }
    items = attractions.get(city.lower().strip(), [])
    return json.dumps({"city": city, "attractions": items or ["No data"]})


# --- Agent Orchestration (Responses API with function calling) ---------------

TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "lookup_attractions",
            "description": "Return a JSON list of popular attractions for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                },
                "required": ["city"],
            },
        },
    }
]


def _execute_tool_call(name: str, args_json: str) -> str:
    try:
        args = (
            json.loads(args_json) if isinstance(args_json, str) else (args_json or {})
        )
    except Exception:
        args = {}
    if name == "lookup_attractions":
        city = str((args or {}).get("city") or "")
        return lookup_attractions(city)
    return json.dumps({"error": f"unknown tool {name}"})


def run_simple_agent(user_input: str) -> str:
    with judgment.trace("simple_agent_run") as trace:
        # Start a Responses session with function calling enabled
        resp = traced_client.responses.create(
            model="gpt-4o-mini",
            input=f"User: {user_input}",
            tools=TOOLS_SPEC,
            tool_choice="auto",
            temperature=0.3,
            agent_name="executor",
        )

        # Handle required tool calls until the model finalizes an answer
        while True:
            required = getattr(resp, "required_action", None)
            if required and getattr(required, "type", None) == "submit_tool_outputs":
                tool_calls = (
                    required.submit_tool_outputs.tool_calls
                )  # list of {id, name, arguments}
                outputs = []
                for tc in tool_calls:
                    name = tc.name
                    args = tc.arguments
                    result = _execute_tool_call(name, args)
                    outputs.append({"tool_call_id": tc.id, "output": result})

                resp = traced_client.responses.submit_tool_outputs(
                    response_id=resp.id,
                    tool_outputs=outputs,
                    agent_name="executor",
                )
                continue

            # No tool submission required – try to read final text
            text = getattr(resp, "output_text", None)
            if isinstance(text, str) and text:
                trace.save(final_save=True)
                return text

            # Fallback structured extraction
            try:
                output = getattr(resp, "output", None) or []
                if output and isinstance(output, list):
                    content = (
                        output[0].get("content")
                        if isinstance(output[0], dict)
                        else None
                    )
                    if (
                        isinstance(content, list)
                        and content
                        and isinstance(content[0], dict)
                    ):
                        t = content[0].get("text")
                        if isinstance(t, str):
                            trace.save(final_save=True)
                            return t
            except Exception:
                pass

            # If nothing parsable, break with empty answer
            trace.save(final_save=True)
            return ""


if __name__ == "__main__":
    print("Simple Trajectory Agent (LLM -> Tool -> LLM)")
    query = "What are top attractions in Paris?"
    answer = run_simple_agent(query)
    print("\nFinal Answer:\n", answer)
