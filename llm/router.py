"""
LLM Provider Router Facade.

Author: Madhav Kumar
Module: llm.router
"""

from typing import Dict, Any, Optional
from llm.base import BaseLLMProvider
from llm.groq_client import GroqSafetyClient
from llm.providers import OfflineFallbackProvider, GeminiProvider, HuggingFaceProvider


class LLMRouter(BaseLLMProvider):
    """Router Facade managing active LLM provider selection and fallback."""

    def __init__(self, provider_type: str = "groq", api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.provider_type = provider_type.lower()
        self.api_key = api_key
        self.model_name = model_name or "llama-3.3-70b-versatile"
        self.provider = self._select_provider()

    def _select_provider(self) -> BaseLLMProvider:
        if self.provider_type == "groq":
            try:
                return GroqSafetyClient(api_key=self.api_key, model_name=self.model_name)
            except Exception as e:
                print(f"[LLMRouter Warning] Groq provider selection failed ({e}). Falling back to Offline Provider.")
                return OfflineFallbackProvider()
        elif self.provider_type == "gemini":
            return GeminiProvider()
        elif self.provider_type == "huggingface":
            return HuggingFaceProvider()
        else:
            return OfflineFallbackProvider()

    def generate_section_text(self, prompt: str, system_instruction: str, evidence_packet: Dict[str, Any]) -> str:
        """Route generation request to active provider with fallback protection."""
        try:
            return self.provider.generate_section_text(prompt, system_instruction, evidence_packet)
        except Exception as e:
            print(f"[LLMRouter Warning] Primary provider failed: {e}. Executing offline fallback...")
            fallback = OfflineFallbackProvider()
            return fallback.generate_section_text(prompt, system_instruction, evidence_packet)
