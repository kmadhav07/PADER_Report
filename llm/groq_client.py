"""
Groq API Provider Implementation.

Author: Madhav Kumar
Module: llm.groq_client
"""

import os
import json
import time
from typing import Dict, Any, Optional
from llm.base import BaseLLMProvider


class GroqSafetyClient(BaseLLMProvider):
    """Groq LPU Acceleration Client using Llama 3.3 70B."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY", "")
        self.model_name = model_name
        self.client = None

        if self.api_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"[GroqSafetyClient Warning] Groq client initialization failed: {e}")

    def generate_section_text(self, prompt: str, system_instruction: str, evidence_packet: Dict[str, Any]) -> str:
        """Generate narrative text using Groq LPU API."""
        if not self.client:
            raise RuntimeError("Groq API key not configured or client initialization failed.")

        context_str = json.dumps(evidence_packet, indent=2)
        full_system_prompt = f"{system_instruction}\n\nEVIDENCE DATASET (STRICT GROUND TRUTH):\n{context_str}\n\nSTRICT INSTRUCTION: Do NOT invent or alter numerical values."

        messages = [
            {"role": "system", "content": full_system_prompt},
            {"role": "user", "content": prompt}
        ]

        max_retries = 3
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.15,
                    max_tokens=1500
                )
                return completion.choices[0].message.content
            except Exception as e:
                print(f"[GroqSafetyClient Warning] Attempt {attempt+1} failed: {e}. Retrying in 2 seconds...")
                time.sleep(2.0)

        raise RuntimeError("Groq API calls failed after retries.")
