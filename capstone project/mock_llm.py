from typing import Any, List, Optional
import json
from crewai.llms.base_llm import BaseLLM

class DeterministicMockLLM(BaseLLM):
    def __init__(self, **kwargs: Any):
        # Enforce the required model parameter dynamically to satisfy Pydantic validations
        if "model" not in kwargs:
            kwargs["model"] = "mock-lending-operations-model"
        super().__init__(**kwargs)

    def call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        return self._generate_response(prompt)

    def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Any = None, **kwargs: Any) -> str:
        return self._generate_response(prompt)

    def _generate_response(self, prompt: str) -> str:
        # Avoid built-in silent parsing pitfalls from standard ReAct templates
        if "Action:" in prompt:
            if "rag_tool" in prompt or "policy" in prompt:
                return 'Thought: I need to fetch the relevant loan policy parameters.\nAction: rag_tool\nAction Input: {"query": "What are the KYC document requirements?"}\n'
            elif "lookup_tool" in prompt or "status" in prompt:
                return 'Thought: I need to verify the application record indices.\nAction: lookup_tool\nAction Input: {"record_id": "CRED-LN-1005"}\n'
        
        # Formulate a clean, compact dictionary matching the StructuredCrewResponse schema fields
        mock_response_dict = {
            "policy_response": "Processed successfully. Minimum balance requirements state that premium savings accounts must maintain a monthly average balance of 10000 INR. Failure to maintain this baseline triggers a non-maintenance charge of 250 INR per month.",
            "record_status": "Under Review",
            "escalation_required": False
        }
        
        # Return ONLY the clean stringified dictionary representation with no conversational padding
        # This allows CrewAI's to_pydantic parser to convert the model string seamlessly
        return json.dumps(mock_response_dict, ensure_ascii=False).strip()

    @property
    def _llm_type(self) -> str:
        return "deterministic_mock_llm"
