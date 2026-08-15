"""
Markdown Exporter Module.

Author: Madhav Kumar
Module: exporters.markdown_exporter
"""

import os


def export_to_markdown(markdown_text: str, output_path: str) -> str:
    """Save report as Markdown document."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    return output_path
