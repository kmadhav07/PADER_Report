"""
Professional PDF Exporter Module (ReportLab Table Parser).

Author: Madhav Kumar
Module: exporters.pdf_exporter
"""

import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors


def parse_markdown_table(table_lines: list, styles) -> Table:
    """Parse Markdown table lines (| col1 | col2 |) into a styled ReportLab Table."""
    raw_rows = []
    for line in table_lines:
        if '| ---' in line or '|:---' in line:
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if cells and any(c for c in cells):
            raw_rows.append(cells)

    if not raw_rows:
        return None

    # Determine column widths dynamically based on max cols
    num_cols = max(len(r) for r in raw_rows)
    
    # Normalize rows
    table_data = []
    for i, row in enumerate(raw_rows):
        formatted_row = []
        is_header = (i == 0)
        for cell in row:
            # Clean Markdown bold/italics
            c_text = cell.replace('**', '<b>').replace('**', '</b>')
            c_text = c_text.replace('*', '<i>').replace('*', '</i>')
            style = styles['TableHeader'] if is_header else styles['TableCell']
            formatted_row.append(Paragraph(c_text, style))
        
        # Pad row if missing columns
        while len(formatted_row) < num_cols:
            formatted_row.append(Paragraph("", styles['TableCell']))
            
        table_data.append(formatted_row)

    # Calculate column widths to fit page width (540pt printable width)
    avail_width = 540.0
    col_w = avail_width / num_cols

    t = Table(table_data, colWidths=[col_w] * num_cols)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ]))
    return t


def export_to_pdf(markdown_text: str, output_path: str) -> str:
    """Export report to professionally styled PDF document using ReportLab."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    ))

    story = []
    lines = markdown_text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        if not line:
            story.append(Spacer(1, 4))
            i += 1
            continue

        # Detect Markdown Table
        if line.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            t_obj = parse_markdown_table(table_lines, styles)
            if t_obj:
                story.append(Spacer(1, 6))
                story.append(t_obj)
                story.append(Spacer(1, 8))
            continue

        # Headings
        if line.startswith('# '):
            story.append(Paragraph(f"<b><font size=16 color='#1e3a8a'>{line[2:]}</font></b>", styles['Heading1']))
            story.append(Spacer(1, 8))
        elif line.startswith('## '):
            story.append(Paragraph(f"<b><font size=13 color='#0f172a'>{line[3:]}</font></b>", styles['Heading2']))
            story.append(Spacer(1, 6))
        elif line.startswith('### '):
            story.append(Paragraph(f"<b><font size=11 color='#334155'>{line[4:]}</font></b>", styles['Heading3']))
            story.append(Spacer(1, 4))
        elif line.startswith('#### '):
            story.append(Paragraph(f"<b><font size=10 color='#475569'>{line[5:]}</font></b>", styles['Heading4']))
            story.append(Spacer(1, 4))
        elif line.startswith('##### '):
            story.append(Paragraph(f"<b><font size=9.5 color='#475569'>{line[6:]}</font></b>", styles['Heading4']))
            story.append(Spacer(1, 4))
        elif line == '---':
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e2e8f0'), spaceAfter=8, spaceBefore=8))
        else:
            # Inline bold / italic / code formatting
            text_clean = line.replace('**', '<b>', 1)
            text_clean = text_clean.replace('**', '</b>', 1)
            text_clean = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text_clean)
            text_clean = re.sub(r'`(.*?)`', r'<font face="Courier" color="#0369a1">\1</font>', text_clean)
            
            story.append(Paragraph(text_clean, styles['Normal']))
            story.append(Spacer(1, 3))
            
        i += 1

    doc.build(story)
    return output_path
