"""Groq Provider - LLM API integration"""

import os
import requests
from typing import List, Dict, Any, Optional

from ..provider import Provider, LLMResponse


class GroqProvider(Provider):
    """Groq API implementation with cost tracking."""

    API_URL = "https://api.groq.com/openai/v1/chat/completions"

    COSTS = {
        "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
        "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
        "llama-4-scout": {"input": 0.11, "output": 0.34},
    }

    def __init__(self, model: str = "llama-3.1-8b-instant",
                 system_instruction: str = None,
                 temperature: float = 0.5,
                 top_p: float = 0.65):
        self.model = model
        self.api_key = self._get_api_key()
        self.system_message = self._create_system_message(system_instruction)
        self.temperature = temperature
        self.top_p = top_p

    def chat(self, messages: List[Dict], tools: List = None) -> LLMResponse:
        payload = self._build_payload(messages, tools)
        response = self._call_api(payload)
        return self._parse_response(response)

    def get_cost(self, usage: Dict) -> float:
        if not usage or self.model not in self.COSTS:
            return 0.0

        costs = self.COSTS[self.model]
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        input_cost = self._calculate_token_cost(prompt_tokens, costs["input"])
        output_cost = self._calculate_token_cost(
            completion_tokens, costs["output"]
        )
        return input_cost + output_cost

    def _get_api_key(self) -> str:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable required")
        return api_key

    def _create_system_message(self, instruction: Optional[str]) -> Optional[Dict]:
        if not instruction:
            return None
        return {"role": "system", "content": instruction}

    def _build_payload(self, messages: List[Dict], tools: List) -> Dict:
        full_messages = self._add_system_message(messages)
        payload = {
            "model": self.model,
            "messages": full_messages,
            "temperature": self.temperature,
            "top_p": self.top_p
        }

        if tools:
            payload["tools"] = tools

        return payload

    def _add_system_message(self, messages: List[Dict]) -> List[Dict]:
        if self.system_message:
            return [self.system_message] + messages
        return messages

    def _call_api(self, payload: Dict) -> Dict:
        response = requests.post(
            self.API_URL,
            headers=self._build_headers(),
            json=payload,
        )

        if not response.ok:
            error_data = response.json() if response.text else {}

            # Enhanced error handling for tool_use_failed (400 errors)
            if response.status_code == 400:
                error_obj = error_data.get("error", {})
                error_message = error_obj.get("message", "Unknown error")

                # Check for tool use failures - show what the model generated
                is_tool_failure = (
                    "tool_use_failed" in error_message.lower() or
                    error_obj.get("failed_generation")
                )
                if is_tool_failure:
                    failed_gen = error_obj.get("failed_generation", "Not provided")
                    hint_msg = (
                        "Some models (especially 8b) may wrap JSON in XML tags."
                    )
                    recommendation = (
                        "Try 'llama-3.3-70b-versatile' "
                        "for more reliable tool calling."
                    )
                    raise RuntimeError(
                        f"Groq API error (400): tool_use_failed\n"
                        f"Model '{self.model}' generated "
                        f"malformed tool call format.\n"
                        f"Generated: {failed_gen}\n"
                        f"Hint: {hint_msg}\n"
                        f"      {recommendation}"
                    )

            # Generic error fallback
            raise RuntimeError(f"Groq API error ({response.status_code}): {error_data}")

        return response.json()

    def _build_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _parse_response(self, data: Dict) -> LLMResponse:
        message = data["choices"][0]["message"]
        return LLMResponse(
            text=message.get("content", ""),
            tool_calls=message.get("tool_calls"),
            usage=data.get("usage"),
        )

    def _calculate_token_cost(self, tokens: int, cost_per_million: float) -> float:
        return (tokens / 1_000_000) * cost_per_million
