# DOCX Design Supplement — Chinese Business Document Typography

Supplementary design reference for the built-in `document-skills:docx` skill. Read this when creating Word documents that need:
- Chinese business/report typography (报告、方案、说明文档)
- Consistent heading and table conventions
- Professional bilingual (中英混排) layout

For academic papers (IEEE / SCI / 学报), use the dedicated **`paper` skill** instead — it enforces a stricter format than this general business style.

---

## Font Rules (字体规范)

| Role | Font | Notes |
|------|------|-------|
| Headings (all levels) | 黑体 (SimHei) | 所有标题统一用黑体,不分中英 |
| Body — Chinese | 等线 (DengXian) | 正文中文默认字体 |
| Body — English/digits | Times New Roman | 正文中英混排时英文与数字用此字体 |
| Code / monospace | Consolas | 代码块、命令、变量名 |

Apply per-run fonts in `python-docx`: set `run.font.name` for the Latin part and the `w:eastAsia` attribute for the CJK part, because Word tracks them separately:

```python
from docx.oxml.ns import qn

def set_run_fonts(run, latin="Times New Roman", cjk="等线"):
    run.font.name = latin
    run.element.rPr.rFonts.set(qn("w:eastAsia"), cjk)
```

---

## Heading Rules (标题规范)

- **一级标题 (Heading 1): 居中对齐** — `WD_ALIGN_PARAGRAPH.CENTER`
- 二级及以下标题: 左对齐
- All headings use 黑体, bold optional (黑体 already heavy — avoid double-bolding)
- Suggested sizes: H1 = 二号/22pt, H2 = 三号/16pt, H3 = 四号/14pt
- Keep heading numbering consistent (一、/ 1. / 1.1) — pick one scheme per document

```python
from docx.enum.text import WD_ALIGN_PARAGRAPH

h1 = doc.add_heading("第一章 概述", level=1)
h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in h1.runs:
    set_run_fonts(run, latin="SimHei", cjk="黑体")
```

---

## Table Rules (表格规范)

- **行标题 (row headers) 和列标题 (column headers): 居中对齐** — both horizontal and vertical center
- Header row: 黑体; body cells: 等线 / Times New Roman per content
- Body cell text: left-aligned for text, right-aligned for numbers, centered for short labels
- Use a clean single-line border (see [[feedback_word_table_formatting]] preferences); avoid heavy or doubled borders
- Header row may use light grey fill (`D9D9D9`) for separation — optional, keep subtle

```python
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH

def center_header_cell(cell):
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
```

---

## Chinese Typography Rules

- Body text: 小四 (12pt) standard, 五号 (10.5pt) for dense docs — not smaller
- Line spacing: 1.5x for reports, 1.15–1.3x for dense reference docs
- First-line indent: 2 characters (中文段落首行缩进 2 字符), not space-padded
- Punctuation: full-width Chinese punctuation（，。；：）, never half-width in CN body
- Mixed CN/EN: add no manual space around English words — Word handles 中英间距; if needed use the document's auto kerning, not literal spaces
- Never bold Chinese body text for emphasis — use a heading or 楷体 callout instead

---

## Structured Workflow (6 Steps)

1. **Clarify** — Document type (报告/方案/说明), audience, length, whether bilingual
2. **Outline** — Build heading tree first (H1/H2/H3), confirm numbering scheme
3. **Style setup** — Define fonts + heading alignment + table style ONCE at the top, reuse
4. **Fill** — Write content section by section, apply per-run fonts as you go
5. **Self-Check** — Verify H1 centered, table headers centered, fonts correct, no half-width CN punctuation
6. **Convert/Verify** — Open in Word (or LibreOffice headless) to confirm rendering, check fonts didn't fall back

---

## Quick Reference: What NOT to Do

| Bad | Good |
|-----|------|
| H1 left-aligned | H1 centered |
| Table headers left-aligned | Row + column headers centered |
| 宋体 headings | 黑体 headings (all levels) |
| Bold Chinese body for emphasis | Heading or 楷体 callout |
| Half-width punctuation in CN (,.;) | Full-width（，。；） |
| Space-padded first-line indent | Real 2-char indent property |
| Same font for code and prose | Consolas for code, 等线/Times for prose |
| Latin font only (CJK falls back) | Set both `font.name` and `w:eastAsia` |
