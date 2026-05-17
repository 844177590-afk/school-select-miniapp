from __future__ import annotations

import re
import sys
from pathlib import Path
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Preformatted,
)


def clean_inline(text: str) -> str:
    text = text.strip()
    parts: list[str] = []
    cursor = 0
    for match in re.finditer(r"`([^`]+)`", text):
        parts.append(escape(text[cursor : match.start()]))
        parts.append(f'<font color="#07999B">{escape(match.group(1))}</font>')
        cursor = match.end()
    parts.append(escape(text[cursor:]))
    text = "".join(parts)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    return bool(re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", line))


def build_story(markdown: str):
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

    styles = getSampleStyleSheet()
    base_font = "STSong-Light"
    styles.add(
        ParagraphStyle(
            name="CNBody",
            fontName=base_font,
            fontSize=9.6,
            leading=15,
            textColor=colors.HexColor("#172326"),
            spaceAfter=5,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNTitle",
            fontName=base_font,
            fontSize=24,
            leading=30,
            textColor=colors.HexColor("#07999B"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNH2",
            fontName=base_font,
            fontSize=15,
            leading=20,
            textColor=colors.HexColor("#07999B"),
            spaceBefore=12,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNH3",
            fontName=base_font,
            fontSize=12,
            leading=17,
            textColor=colors.HexColor("#172326"),
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNList",
            fontName=base_font,
            fontSize=9.5,
            leading=14,
            leftIndent=10,
            firstLineIndent=-6,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNCell",
            fontName=base_font,
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#172326"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNCode",
            fontName=base_font,
            fontSize=7.8,
            leading=10.5,
            textColor=colors.HexColor("#172326"),
        )
    )

    lines = markdown.splitlines()
    story = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            code = "\n".join(code_lines)
            story.append(
                Preformatted(
                    code,
                    styles["CNCode"],
                    maxLineLength=92,
                    newLineChars="\n",
                )
            )
            story.append(Spacer(1, 5))
            continue

        if stripped.startswith("# "):
            story.append(Paragraph(clean_inline(stripped[2:]), styles["CNTitle"]))
            i += 1
            continue

        if stripped.startswith("## "):
            story.append(Paragraph(clean_inline(stripped[3:]), styles["CNH2"]))
            i += 1
            continue

        if stripped.startswith("### "):
            story.append(Paragraph(clean_inline(stripped[4:]), styles["CNH3"]))
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            header = split_table_row(stripped)
            rows = [[Paragraph(clean_inline(cell), styles["CNCell"]) for cell in header]]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([Paragraph(clean_inline(cell), styles["CNCell"]) for cell in split_table_row(lines[i])])
                i += 1
            table = Table(rows, repeatRows=1, hAlign="LEFT")
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(20 / 255, 200 / 255, 200 / 255, alpha=0.10)),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#07999B")),
                        ("GRID", (0, 0), (-1, -1), 0.4, colors.Color(23 / 255, 35 / 255, 38 / 255, alpha=0.16)),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 5),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )
            story.append(table)
            story.append(Spacer(1, 7))
            continue

        if stripped.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            for item in items:
                story.append(Paragraph("• " + clean_inline(item), styles["CNList"]))
            story.append(Spacer(1, 2))
            continue

        para_lines = [stripped]
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if (
                not next_line
                or next_line.startswith("#")
                or next_line.startswith("- ")
                or next_line.startswith("```")
                or next_line.startswith("|")
            ):
                break
            para_lines.append(next_line)
            i += 1
        story.append(Paragraph(clean_inline(" ".join(para_lines)), styles["CNBody"]))

    return story


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("Usage: python md-to-pdf-reportlab.py <input.md> <output.pdf>")

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=input_path.stem,
        author="Codex",
    )
    story = build_story(input_path.read_text(encoding="utf-8"))
    doc.build(story)


if __name__ == "__main__":
    main()
