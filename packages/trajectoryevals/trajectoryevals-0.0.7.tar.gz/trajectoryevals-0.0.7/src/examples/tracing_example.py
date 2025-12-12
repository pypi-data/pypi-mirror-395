import json
import os
from typing import Any
from uuid import uuid4

from dotenv import load_dotenv
from openai import OpenAI

from trajectory import TrajectoryClient
from trajectory.common.tracer import Tracer, wrap
from trajectory.data import Example
from trajectory.scorers import ToolOrderScorer
from trajectory.verifiers.models import VerifierConfig, VerifierType

# Load environment variables
load_dotenv()

# Get API credentials from environment variables
api_key = os.getenv("TRAJECTORY_API_KEY")
org_id = os.getenv("TRAJECTORY_ORG_ID")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not api_key or not org_id:
    print("❌ Error: Missing required environment variables")
    print("Please set the following in your .env file or environment:")
    print("TRAJECTORY_API_KEY=your-api-key")
    print("TRAJECTORY_ORG_ID=your-org-id")
    print("OPENAI_API_KEY=your-openai-key")
    exit(1)

if not openai_api_key:
    print("❌ Error: OPENAI_API_KEY not found in environment variables")
    print("Please add OPENAI_API_KEY=your-openai-key to your .env file")
    exit(1)

# Initialize client with API credentials
client = TrajectoryClient(api_key=api_key, organization_id=org_id)

# Initialize the tracer
trajectory = Tracer(
    api_key=api_key,
    organization_id=org_id,
    project_name="tracing_example_project",
    enable_monitoring=True,
    enable_evaluations=False,
)

# Wrap the OpenAI client
openai_client = wrap(OpenAI(api_key=openai_api_key))


# Unified verifier functions
def weather_unified_verifier(inputs: dict, output: Any) -> dict[str, Any]:
    """Unified verifier for weather function"""
    scores = {}

    # Input validation
    input_valid = "city" in inputs and isinstance(inputs["city"], str)
    scores["input_validity"] = 1.0 if input_valid else 0.0

    # Output validation
    required_fields = ["temperature", "condition", "humidity"]
    output_valid = all(field in output for field in required_fields)
    scores["output_quality"] = 1.0 if output_valid else 0.0

    # Additional scoring
    if output_valid and "temperature" in output:
        temp = output["temperature"]
        if 0 <= temp <= 120:  # Reasonable temperature range
            scores["temperature_reasonableness"] = 1.0
        else:
            scores["temperature_reasonableness"] = 0.5

    # Overall score
    scores["overall_score"] = sum(scores.values()) / len(scores)

    return {
        "passed": scores["overall_score"] >= 0.8,
        "scores": scores,
        "details": f"Input valid: {input_valid}, Output valid: {output_valid}",
    }


def attractions_unified_verifier(inputs: dict, output: Any) -> dict[str, Any]:
    """Unified verifier for attractions function"""
    scores = {}

    # Input validation
    input_valid = "destination" in inputs and isinstance(inputs["destination"], str)
    scores["input_validity"] = 1.0 if input_valid else 0.0

    # Output validation
    output_valid = "attractions" in output and isinstance(output["attractions"], list)
    scores["output_quality"] = 1.0 if output_valid else 0.0

    # Additional scoring
    if output_valid and len(output["attractions"]) >= 3:
        scores["attraction_count"] = 1.0
    else:
        scores["attraction_count"] = 0.5

    # Overall score
    scores["overall_score"] = sum(scores.values()) / len(scores)

    return {
        "passed": scores["overall_score"] >= 0.8,
        "scores": scores,
        "details": f"Input valid: {input_valid}, Output valid: {output_valid}",
    }


# Define tool functions with tracing
@trajectory.observe(span_type="tool")
def get_weather(city: str, start_date: str = None, end_date: str = None) -> dict:
    """Get current weather for a city using a mock API"""
    print(f"🌤️  Tool: Getting weather for {city}")
    if start_date and end_date:
        print(f"🌤️  Date range: {start_date} to {end_date}")

    # Mock weather data
    weather_data = {
        "San Francisco": {"temperature": 68, "condition": "Sunny", "humidity": 65},
        "New York": {"temperature": 45, "condition": "Cloudy", "humidity": 80},
        "London": {"temperature": 52, "condition": "Rainy", "humidity": 85},
        "Tokyo": {"temperature": 72, "condition": "Clear", "humidity": 60},
        "Paris": {"temperature": 75, "condition": "Partly Cloudy", "humidity": 70},
    }

    result = weather_data.get(
        city,
        {
            "temperature": 70,
            "condition": "Unknown",
            "humidity": 50,
            "note": f"No data for {city}, showing default",
        },
    )

    if start_date and end_date:
        result["forecast_period"] = f"{start_date} to {end_date}"

    print(f"🌤️  Weather result: {result}")
    return result


@trajectory.observe(span_type="tool")
def get_attractions(destination: str) -> dict:
    """Get popular attractions for a destination"""
    print(f"🏛️  Tool: Getting attractions for {destination}")

    # Mock attractions data
    attractions_data = {
        "Paris": {
            "attractions": [
                "Eiffel Tower",
                "Louvre Museum",
                "Notre-Dame Cathedral",
                "Arc de Triomphe",
                "Sacré-Cœur",
            ],
            "description": "Top attractions in the City of Light",
        },
        "London": {
            "attractions": [
                "Big Ben",
                "Tower Bridge",
                "British Museum",
                "London Eye",
                "Buckingham Palace",
            ],
            "description": "Must-see sights in London",
        },
        "Tokyo": {
            "attractions": [
                "Tokyo Tower",
                "Senso-ji Temple",
                "Shibuya Crossing",
                "Meiji Shrine",
                "Tokyo Skytree",
            ],
            "description": "Popular Tokyo destinations",
        },
    }

    result = attractions_data.get(
        destination,
        {
            "attractions": ["Generic attraction 1", "Generic attraction 2"],
            "description": f"Popular attractions in {destination}",
            "note": f"Limited data available for {destination}",
        },
    )

    print(f"🏛️  Attractions result: {result}")
    return result


@trajectory.observe(span_type="tool")
def calculate(expression: str) -> dict:
    """Safely evaluate mathematical expressions"""
    print(f"🧮 Tool: Calculating {expression}")

    try:
        # Only allow basic math operations for security
        allowed_chars = set("0123456789+-*/.()")
        if not all(c in allowed_chars or c.isspace() for c in expression):
            result = {"error": "Invalid characters in expression"}
        else:
            calculated_result = eval(expression)
            result = {"expression": expression, "result": calculated_result}
    except Exception as e:
        result = {"error": f"Calculation error: {e!s}"}

    print(f"🧮 Calculation result: {result}")
    return result


@trajectory.observe(span_type="handle_tool_calls")
def handle_tool_calls(tool_calls):
    """Execute tool calls and return results"""
    print(f"🔧 Handling {len(tool_calls)} tool call(s)")
    tool_results = []

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        print(f"🔧 Calling tool: {function_name} with args: {function_args}")

        # Call the appropriate function
        if function_name == "get_weather":
            result = get_weather(**function_args)
        elif function_name == "get_attractions":
            result = get_attractions(**function_args)
        elif function_name == "calculate":
            result = calculate(function_args["expression"])
        else:
            result = {"error": f"Unknown function: {function_name}"}

        tool_results.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(result),
            }
        )

    return tool_results


# Define the main agent function with tracing
@trajectory.observe(span_type="function")
def run_agent(prompt) -> str:
    """Main agent function that uses tools and makes LLM calls"""
    # Handle both string and dict inputs
    if isinstance(prompt, dict):
        prompt_text = prompt.get("prompt", str(prompt))
    else:
        prompt_text = str(prompt)

    print(f"🤖 Agent: Processing prompt: {prompt_text}")

    # Define the tools available to the LLM
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather for a specific city with optional date range",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The city name to get weather for",
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date for weather forecast (YYYY-MM-DD format)",
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date for weather forecast (YYYY-MM-DD format)",
                        },
                    },
                    "required": ["city"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_attractions",
                "description": "Get popular attractions for a destination",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "destination": {
                            "type": "string",
                            "description": "The destination city or location",
                        }
                    },
                    "required": ["destination"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Perform mathematical calculations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to evaluate (e.g., '2+2', '10*5')",
                        }
                    },
                    "required": ["expression"],
                },
            },
        },
    ]

    # Make LLM call (this will be automatically traced by the wrapped client)
    print("🤖 Making LLM call...")
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_text}],
        tools=tools,
        tool_choice="auto",
        max_tokens=200,
    )

    response_message = response.choices[0].message
    print(f"💬 LLM Response: {response_message}")

    # Check if the model wants to call tools
    if response_message.tool_calls:
        print(f"🤖 Assistant wants to use {len(response_message.tool_calls)} tool(s)")

        # Execute tool calls
        tool_results = handle_tool_calls(response_message.tool_calls)

        # Make a second API call with tool results
        print("🤖 Making second LLM call with tool results...")
        messages = [
            {"role": "user", "content": prompt_text},
            response_message,
            *tool_results,
        ]

        final_response = openai_client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, max_tokens=200
        )

        final_message = final_response.choices[0].message.content
        print(f"🤖 Final response: {final_message}")
        return final_message
    else:
        # No tool calls needed
        result = response_message.content
        print(f"💬 Direct response: {result}")
        return result


# Define a conversation handler
@trajectory.observe(span_type="conversation")
def run_conversation(user_message):
    """Run a complete conversation with tool calling"""
    print(f"\n💬 Conversation: {user_message}")

    # Run the agent which handles tool calls
    response = run_agent(user_message)
    return response


def main():
    print("\n" + "=" * 60)
    print("🎯 RUNNING ENHANCED TRACING EXAMPLE WITH CONVERSATION TRACKING")
    print("=" * 60)

    # Create examples with component-level verifiers and trajectory-level scorers
    example1 = Example(
        input={
            "prompt": "What's the attraction and weather in Paris for early June 2025 (1st - 2nd)?"
        },
        expected_tools=[
            {"tool_name": "get_attractions", "parameters": {"destination": "Paris"}},
            {
                "tool_name": "get_weather",
                "parameters": {
                    "city": "Paris",
                    "start_date": "2025-06-01",
                    "end_date": "2025-06-02",
                },
            },
        ],
        expected_output="Paris attractions include Eiffel Tower, Louvre Museum... Weather: 75°F, Partly Cloudy",
        trajectory_scorers=[
            "RubricBasedScorer:gpt-4o-mini",
            "ToolCallOrderScorer:ordering_match",  # Add tool call order scorer
        ],
    )

    # Add component-specific verifiers to example1
    example1.add_component_verifier(
        "get_weather",
        VerifierConfig(
            function_name="get_weather",
            verifier_type=VerifierType.PROGRAMMATIC,
            verifier=weather_unified_verifier,
        ),
    )

    example1.add_component_verifier(
        "get_weather",
        VerifierConfig(
            function_name="get_weather",
            verifier_type=VerifierType.PROGRAMMATIC,
            verifier=weather_unified_verifier,
        ),
    )

    example1.add_component_verifier(
        "get_attractions",
        VerifierConfig(
            function_name="get_attractions",
            verifier_type=VerifierType.PROGRAMMATIC,
            verifier=attractions_unified_verifier,
        ),
    )

    # Create a second example with different verifiers
    example2 = Example(
        input={"prompt": "What's the weather in Tokyo and calculate 15 * 3?"},
        expected_tools=[
            {"tool_name": "get_weather", "parameters": {"city": "Tokyo"}},
            {"tool_name": "calculate", "parameters": {"expression": "15 * 3"}},
        ],
        expected_output="Tokyo weather: 72°F, Clear. Calculation: 15 * 3 = 45",
        trajectory_scorers=["RubricBasedScorer:gpt-4o-mini"],  # Add RubricBasedScorer
    )

    # Add different verifiers for example2
    example2.add_component_verifier(
        "get_weather",
        VerifierConfig(
            function_name="get_weather",
            verifier_type=VerifierType.LLM_JUDGE,
            verifier="""Verify that the weather data for Tokyo is reasonable and complete.
        Check that temperature is between 0-120°F and all required fields are present.""",
            llm_model="gpt-4o-mini",
        ),
    )

    print("📝 Example 1:")
    print(f"   Input: {example1.input}")
    print(f"   Expected Tools: {example1.expected_tools}")
    print(f"   Component Verifiers: {list(example1.component_verifiers.keys())}")
    print(f"   Trajectory Scorers: {example1.trajectory_scorers}")

    print("\n📝 Example 2:")
    print(f"   Input: {example2.input}")
    print(f"   Expected Tools: {example2.expected_tools}")
    print(f"   Component Verifiers: {list(example2.component_verifiers.keys())}")
    print(f"   Trajectory Scorers: {example2.trajectory_scorers}")

    # Test conversation tracking
    print("\n🧪 Testing conversation tracking...")

    # Conversation 1: Multiple turns with same conversation ID
    conversation_id_1 = str(uuid4())
    print(f"\n💬 Conversation 1 (ID: {conversation_id_1}):")

    with trajectory.conversation(conversation_id_1):
        print("Turn 1: What's the weather in Paris?")
        response1 = run_conversation("What's the weather in Paris?")
        print(f"Response: {response1}")

        print("\nTurn 2: What about the attractions there?")
        response2 = run_conversation("What about the attractions there?")
        print(f"Response: {response2}")

        print("\nTurn 3: Can you calculate 15 * 3?")
        response3 = run_conversation("Can you calculate 15 * 3?")
        print(f"Response: {response3}")

    # Conversation 2: Different conversation ID
    conversation_id_2 = str(uuid4())
    print(f"\n💬 Conversation 2 (ID: {conversation_id_2}):")

    with trajectory.conversation(conversation_id_2):
        print("Turn 1: What's the weather in Tokyo?")
        response4 = run_conversation("What's the weather in Tokyo?")
        print(f"Response: {response4}")

    # Conversation 3: Auto-generated conversation ID
    conversation_id_3 = uuid4().hex
    print(f"\n💬 Conversation 3 (Auto-generated ID: {conversation_id_3}):")

    with trajectory.conversation(conversation_id_3):
        print("Turn 1: What's the weather in London?")
        response5 = run_conversation("What's the weather in London?")
        print(f"Response: {response5}")

    # Optional: Only run assert_trace_test when explicitly enabled.
    # This prevents sending None traces to the backend if trace generation fails.
    if os.getenv("ENABLE_ASSERT_TRACE_TEST", "false").lower() == "true":
        try:
            print("\n🧪 Running enhanced assert_trace_test with multiple examples...")
            results = client.assert_trace_test(
                examples=[example1, example2],
                scorers=[ToolOrderScorer(exact_match=True)],
                function=run_agent,
                tracer=trajectory,
                project_name="tracing_example_project",
            )
            print("\n✅ Test completed successfully!")
            print(
                "🎉 All examples processed concurrently with component verifiers and trajectory scorers!"
            )
            print(f"📊 Results: {results}")
        except AssertionError as e:
            print("\n❌ Test failed!")
            print(f"💥 AssertionError: {e}")
            print("🔧 Some examples did not pass verification")
        except Exception as e:
            print(f"\n❌ Error running test: {e}")
            import traceback

            traceback.print_exc()
    else:
        print(
            "\nℹ️ Skipping assert_trace_test (set ENABLE_ASSERT_TRACE_TEST=true to enable)."
        )

    print("\n📊 Check your JudgEval dashboard for detailed results!")
    print("🔍 Component-level verifiers ran during execution")
    print("🎯 Trajectory-level scorers ran after trace completion")
    print(
        "💬 Conversation tracking: All traces within each conversation share the same conversation_id"
    )


if __name__ == "__main__":
    main()
