"""
Prompt Assembly Engine.

Author: Madhav Kumar
Module: pipeline.prompt_builder
"""

import os
from typing import Dict, Any, Optional
from config.settings import PROMPTS_DIR


def load_prompt_template(filename: str) -> str:
    """Load system prompt template from file."""
    path = os.path.join(PROMPTS_DIR, os.path.basename(filename))
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Provide a concise, formal regulatory summary based strictly on the evidence packet."


def build_section_prompt(section_title: str, custom_instruction: Optional[str] = None) -> str:
    """Build user task prompt for section generation."""
    prompt = f"Compose formal regulatory narrative for section: '{section_title}'."
    if custom_instruction:
        prompt += f"\nAdditional Instruction: {custom_instruction}"
    return prompt
