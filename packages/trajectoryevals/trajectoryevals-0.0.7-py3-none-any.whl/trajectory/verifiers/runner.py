import asyncio
import json
import os
import threading
import time
from collections.abc import Callable
from typing import Any

from .models import VerifierConfig, VerifierType


class AsyncVerifierRunner:
    def __init__(self):
        # Remove llm_client parameter - we'll create clients dynamically
        self._llm_clients = {}  # Cache for created clients

    def _get_llm_client(self, model: str):
        """Get or create LLM client based on model name"""
        if model in self._llm_clients:
            return self._llm_clients[model]

        # Determine client type based on model name
        if model.startswith(("gpt-", "gpt-4", "gpt-3")):
            # OpenAI models
            try:
                from openai import OpenAI

                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError(f"OPENAI_API_KEY not found for model {model}")
                client = OpenAI(api_key=api_key)
                self._llm_clients[model] = client
                return client
            except ImportError:
                raise ImportError(
                    "OpenAI client not installed. Run: pip install openai"
                )

        elif model.startswith(("claude-", "claude")):
            # Anthropic models
            try:
                from anthropic import Anthropic

                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise ValueError(f"ANTHROPIC_API_KEY not found for model {model}")
                client = Anthropic(api_key=api_key)
                self._llm_clients[model] = client
                return client
            except ImportError:
                raise ImportError(
                    "Anthropic client not installed. Run: pip install anthropic"
                )

        elif model.startswith(("gemini-", "gemini")):
            # Google Gemini models
            try:
                import google.generativeai as genai

                api_key = os.getenv("GOOGLE_API_KEY")
                if not api_key:
                    raise ValueError(f"GOOGLE_API_KEY not found for model {model}")
                genai.configure(api_key=api_key)
                # For Gemini, we'll use the genai module directly
                self._llm_clients[model] = genai
                return genai
            except ImportError:
                raise ImportError(
                    "Google Generative AI not installed. Run: pip install google-generativeai"
                )

        else:
            # Default to OpenAI for unknown models
            try:
                from openai import OpenAI

                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError(f"OPENAI_API_KEY not found for model {model}")
                client = OpenAI(api_key=api_key)
                self._llm_clients[model] = client
                return client
            except ImportError:
                raise ImportError(
                    "OpenAI client not installed. Run: pip install openai"
                )

    def run_verifiers_async(
        self,
        verifiers: list[VerifierConfig],
        inputs: dict,
        output: Any,
        callback=None,
        trace_id: str = None,
        span_id: str = None,
    ) -> None:
        """Run verifiers asynchronously and call callback when done"""
        print("Running verifiers asynchronously")

        async def run_all_verifiers():
            # Create tasks for each verifier
            tasks = []
            for verifier in verifiers:
                print(f"Running verifier: {verifier.function_name}")
                task = self._run_single_verifier_async(verifier, inputs, output)
                tasks.append(task)

            # Wait for all verifiers to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Combine results
            combined_results = {}
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    combined_results[f"verifier_{i}_error"] = str(result)
                else:
                    combined_results[f"verifier_{i}"] = result

            # Call callback with results
            if callback:
                callback(trace_id, span_id, combined_results)

        # Run in thread
        def run_in_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(run_all_verifiers())
            finally:
                loop.close()

        thread = threading.Thread(target=run_in_thread, daemon=False)
        thread.start()

    async def _run_single_verifier_async(
        self, verifier: VerifierConfig, inputs: dict, output: Any
    ) -> dict[str, Any]:
        """Run a single verifier asynchronously"""
        start_time = time.time()

        # Check if using new unified verifier or legacy separate verifiers
        if hasattr(verifier, "verifier") and verifier.verifier:
            # New unified verifier approach
            if verifier.verifier_type == VerifierType.PROGRAMMATIC:
                result = await self._run_unified_programmatic_verifier_async(
                    verifier.verifier, inputs, output
                )
            else:
                result = await self._run_unified_llm_verifier_async(
                    verifier.verifier, inputs, output, verifier.llm_model
                )
        else:
            # Legacy approach - run separate input/output verifiers
            result = await self._run_legacy_verifier_async(verifier, inputs, output)

        result["execution_time_ms"] = (time.time() - start_time) * 1000
        return result

    async def _run_legacy_verifier_async(
        self, verifier: VerifierConfig, inputs: dict, output: Any
    ) -> dict[str, Any]:
        """Run a single legacy verifier asynchronously"""
        start_time = time.time()

        result = {
            "verifier_type": verifier.verifier_type.value,
            "input_verification": None,
            "output_verification": None,
            "overall_passed": True,
            "overall_score": 0.0,
        }
        print(f"Running verifier {verifier.function_name} inside")
        # Run input verification
        if verifier.input_verifier:
            if verifier.verifier_type == VerifierType.PROGRAMMATIC:
                input_result = await self._run_programmatic_verifier_async(
                    verifier.input_verifier, inputs, "input"
                )
            else:
                input_result = await self._run_llm_verifier_async(
                    verifier.input_verifier, inputs, "input", verifier.llm_model
                )

            result["input_verification"] = input_result
            if not input_result["passed"]:
                result["overall_passed"] = False

        # Run output verification
        if verifier.output_verifier:
            if verifier.verifier_type == VerifierType.PROGRAMMATIC:
                output_result = await self._run_programmatic_verifier_async(
                    verifier.output_verifier, output, "output"
                )
            else:
                output_result = await self._run_llm_verifier_async(
                    verifier.output_verifier, output, "output", verifier.llm_model
                )

            result["output_verification"] = output_result
            if not output_result["passed"]:
                result["overall_passed"] = False

        # Calculate overall score
        scores = []
        if result["input_verification"]:
            scores.append(result["input_verification"]["score"])
        if result["output_verification"]:
            scores.append(result["output_verification"]["score"])

        if scores:
            result["overall_score"] = sum(scores) / len(scores)

        result["execution_time_ms"] = (time.time() - start_time) * 1000
        print(f"Result: {result}")
        return result

    async def _run_programmatic_verifier_async(
        self, verifier_func: Callable, data: Any, verification_type: str
    ) -> dict[str, Any]:
        """Run programmatic verifier in thread pool"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._run_programmatic_verifier_sync,
            verifier_func,
            data,
            verification_type,
        )

    def _run_programmatic_verifier_sync(
        self, verifier_func: Callable, data: Any, verification_type: str
    ) -> dict[str, Any]:
        """Run programmatic verifier synchronously"""
        try:
            result = verifier_func(data)
            return {
                "type": f"programmatic_{verification_type}",
                "passed": bool(result),
                "score": float(result)
                if isinstance(result, (int, float))
                else (1.0 if result else 0.0),
                "details": str(result)
                if not isinstance(result, (bool, int, float))
                else None,
                "error": None,
            }
        except Exception as e:
            return {
                "type": f"programmatic_{verification_type}",
                "passed": False,
                "score": 0.0,
                "details": None,
                "error": str(e),
            }

    async def _run_llm_verifier_async(
        self, prompt: str, data: Any, verification_type: str, model: str
    ) -> dict[str, Any]:
        """Run legacy LLM verifier with dynamic client creation"""
        try:
            # Get the appropriate LLM client
            llm_client = self._get_llm_client(model)

            formatted_prompt = f"""
{prompt}

{verification_type.title()} to verify:
{json.dumps(data, indent=2) if isinstance(data, (dict, list)) else str(data)}

Please evaluate this {verification_type} and respond with a JSON object containing:
- "passed": boolean (true if {verification_type} is valid/acceptable)
- "score": float (0.0 to 1.0, where 1.0 is perfect)
- "reasoning": string (explanation of your evaluation)

Response (JSON only):
"""

            # Handle different client types - use sync methods since we're already in a separate thread
            if hasattr(llm_client, "chat"):  # OpenAI/Anthropic style
                response = llm_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": formatted_prompt}],
                    max_tokens=200,
                )
                result_text = response.choices[0].message.content

            elif hasattr(llm_client, "generate_content"):  # Google Gemini style
                response = llm_client.generate_content(
                    formatted_prompt, generation_config={"max_output_tokens": 200}
                )
                result_text = response.text

            else:
                raise ValueError(f"Unsupported LLM client type for model {model}")

            # Handle empty or invalid response
            if not result_text or not result_text.strip():
                return {
                    "type": f"llm_judge_{verification_type}",
                    "passed": False,
                    "score": 0.0,
                    "details": "Empty response from LLM",
                    "error": "Empty response",
                }

            # Try to parse JSON with better error handling
            try:
                result = json.loads(result_text.strip())
            except json.JSONDecodeError as json_error:
                # Try to extract JSON from the response if it's wrapped in text
                import re

                json_match = re.search(r"\{.*\}", result_text, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                    except json.JSONDecodeError:
                        return {
                            "type": f"llm_judge_{verification_type}",
                            "passed": False,
                            "score": 0.0,
                            "details": f"Invalid JSON response: {result_text[:200]}...",
                            "error": f"JSON decode error: {json_error}",
                        }
                else:
                    return {
                        "type": f"llm_judge_{verification_type}",
                        "passed": False,
                        "score": 0.0,
                        "details": f"Invalid JSON response: {result_text[:200]}...",
                        "error": f"JSON decode error: {json_error}",
                    }

            return {
                "type": f"llm_judge_{verification_type}",
                "passed": result.get("passed", False),
                "score": result.get("score", 0.0),
                "details": result.get("reasoning", ""),
                "error": None,
            }

        except Exception as e:
            return {
                "type": f"llm_judge_{verification_type}",
                "passed": False,
                "score": 0.0,
                "details": None,
                "error": str(e),
            }

    async def _run_unified_programmatic_verifier_async(
        self, verifier_func: Callable, inputs: dict, output: Any
    ) -> dict[str, Any]:
        """Run unified programmatic verifier"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._run_unified_programmatic_verifier_sync,
            verifier_func,
            inputs,
            output,
        )

    def _run_unified_programmatic_verifier_sync(
        self, verifier_func: Callable, inputs: dict, output: Any
    ) -> dict[str, Any]:
        """Run unified programmatic verifier synchronously"""
        try:
            result = verifier_func(inputs, output)

            # Handle different return types
            if isinstance(result, dict):
                return {
                    "type": "unified_programmatic",
                    "passed": result.get("passed", True),
                    "scores": result,
                    "error": None,
                }
            elif isinstance(result, (bool, int, float)):
                return {
                    "type": "unified_programmatic",
                    "passed": bool(result),
                    "scores": {"overall_score": float(result)},
                    "error": None,
                }
            else:
                return {
                    "type": "unified_programmatic",
                    "passed": True,
                    "scores": {"overall_score": 1.0, "details": str(result)},
                    "error": None,
                }
        except Exception as e:
            return {
                "type": "unified_programmatic",
                "passed": False,
                "scores": {"overall_score": 0.0},
                "error": str(e),
            }

    async def _run_unified_llm_verifier_async(
        self, prompt: str, inputs: dict, output: Any, model: str
    ) -> dict[str, Any]:
        """Run unified LLM verifier with dynamic client creation"""
        try:
            # Get the appropriate LLM client
            llm_client = self._get_llm_client(model)

            formatted_prompt = f"""
{prompt}

Input to verify:
{json.dumps(inputs, indent=2)}

Output to verify:
{json.dumps(output, indent=2) if isinstance(output, (dict, list)) else str(output)}

Please evaluate both the input and output and respond with a JSON object containing:
- "passed": boolean (true if overall verification passes)
- "scores": object with multiple score fields (e.g., "input_validity", "output_quality", "overall_score")
- "details": string (explanation of your evaluation)

Response (JSON only):
"""

            # Handle different client types - use sync methods since we're already in a separate thread
            if hasattr(llm_client, "chat"):  # OpenAI/Anthropic style
                response = llm_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": formatted_prompt}],
                    max_tokens=300,
                )
                result_text = response.choices[0].message.content

            elif hasattr(llm_client, "generate_content"):  # Google Gemini style
                response = llm_client.generate_content(
                    formatted_prompt, generation_config={"max_output_tokens": 300}
                )
                result_text = response.text

            else:
                raise ValueError(f"Unsupported LLM client type for model {model}")

            # Handle empty or invalid response
            if not result_text or not result_text.strip():
                return {
                    "type": "unified_llm_judge",
                    "passed": False,
                    "scores": {"overall_score": 0.0},
                    "details": "Empty response from LLM",
                    "error": "Empty response",
                }

            # Try to parse JSON with better error handling
            try:
                result = json.loads(result_text.strip())
            except json.JSONDecodeError as json_error:
                # Try to extract JSON from the response if it's wrapped in text
                import re

                json_match = re.search(r"\{.*\}", result_text, re.DOTALL)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                    except json.JSONDecodeError:
                        return {
                            "type": "unified_llm_judge",
                            "passed": False,
                            "scores": {"overall_score": 0.0},
                            "details": f"Invalid JSON response: {result_text[:200]}...",
                            "error": f"JSON decode error: {json_error}",
                        }
                else:
                    return {
                        "type": "unified_llm_judge",
                        "passed": False,
                        "scores": {"overall_score": 0.0},
                        "details": f"Invalid JSON response: {result_text[:200]}...",
                        "error": f"JSON decode error: {json_error}",
                    }

            return {
                "type": "unified_llm_judge",
                "passed": result.get("passed", False),
                "scores": result.get("scores", {"overall_score": 0.0}),
                "details": result.get("details", ""),
                "error": None,
            }

        except Exception as e:
            return {
                "type": "unified_llm_judge",
                "passed": False,
                "scores": {"overall_score": 0.0},
                "error": str(e),
            }
