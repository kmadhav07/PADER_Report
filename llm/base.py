"""
Base Interface for LLM Providers.

Author: Madhav Kumar
Module: llm.base
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseLLMProvider(ABC):
    """Abstract Base Class for Large Language Model Providers."""

    @abstractmethod
    def generate_section_text(self, prompt: str, system_instruction: str, evidence_packet: Dict[str, Any]) -> str:
        """Generate narrative text based on evidence packet and system prompt."""
        pass
