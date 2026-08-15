"""
HTML Exporter Module.

Author: Madhav Kumar
Module: exporters.html_exporter
"""

import os
import re


def export_to_html(markdown_text: str, output_path: str) -> str:
    """Export report to styled HTML document."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    body_html = markdown_text
    body_html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', body_html, flags=re.MULTILINE)
    body_html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', body_html, flags=re.MULTILINE)
    body_html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', body_html, flags=re.MULTILINE)
    body_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', body_html)
    body_html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', body_html)
    
    body_html = body_html.replace('Status: ✅ Approved', '<span class="badge badge-success">Approved</span>')
    body_html = body_html.replace('Status: ⏳ Pending Sign-off', '<span class="badge badge-warning">Pending Sign-off</span>')

    paragraphs = body_html.split('\n\n')
    formatted = []
    for p in paragraphs:
        p_str = p.strip()
        if p_str.startswith('<h') or p_str.startswith('<hr'):
            formatted.append(p_str)
        else:
            formatted.append(f'<p>{p_str.replace(chr(10), "<br>")}</p>')

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PADER Regulatory Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b; max-width: 900px; margin: 40px auto; padding: 20px; background-color: #f8fafc; }}
        .card {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }}
        h1 {{ color: #1e3a8a; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; }}
        h2 {{ color: #0f172a; border-bottom: 1px solid #cbd5e1; padding-bottom: 6px; margin-top: 30px; }}
        .badge {{ display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 0.85em; font-weight: 600; }}
        .badge-success {{ background: #dcfce7; color: #166534; }}
        .badge-warning {{ background: #fef3c7; color: #92400e; }}
        hr {{ border: 0; height: 1px; background: #e2e8f0; margin: 24px 0; }}
    </style>
</head>
<body>
    <div class="card">
        {"\n".join(formatted)}
    </div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
    return output_path
