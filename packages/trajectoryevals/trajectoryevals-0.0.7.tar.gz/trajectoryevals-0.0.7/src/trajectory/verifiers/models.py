# File: judgeval/src/judgeval/verifiers/models.py
from collections.abc import Callable
from enum import Enum
from typing import Union

from pydantic import BaseModel


class VerifierType(Enum):
    PROGRAMMATIC = "programmatic"
    LLM_JUDGE = "llm_judge"


class VerifierConfig(BaseModel):
    function_name: str
    verifier_type: VerifierType
    # Replace separate verifiers with single unified verifier
    verifier: Union[Callable, str]  # Function or LLM prompt
    llm_model: str = "gpt-4o-mini"

    # Optional: For backward compatibility during transition
    input_verifier: Union[Callable, str] | None = None
    output_verifier: Union[Callable, str] | None = None
