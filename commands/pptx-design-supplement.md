# PPTX Design Supplement — Swiss & Chinese Typography Principles

Supplementary design reference for the built-in `document-skills:pptx` skill. Read this when creating presentations that need:
- Swiss International Style (极简、网格、大字重对比)
- Chinese typography optimization
- High-end minimalist aesthetics

Source: [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) (MIT)

---

## Swiss International Style Principles (for .pptx)

### Core Rules
1. **One accent color only** — pick a single high-saturation color, everything else is grayscale
2. **No shadows, no gradients, no rounded corners** — flat, geometric, honest
3. **Extreme font-size contrast** — titles 60-80pt thin weight, body 14-16pt regular
4. **Grid system** — align everything to an invisible 12 or 16-column grid
5. **Hairline rules** — 0.5pt lines as dividers, never thick borders
6. **Whitespace is content** — 40%+ of slide area should be empty

### Typography Pairing (Swiss)
| Role | Font | Weight | Notes |
|------|------|--------|-------|
| Display (EN) | Inter / Helvetica Neue | 200 (Thin) | Very large, very light |
| Display (CN) | Noto Sans SC | 300 (Light) | Large Chinese titles |
| Body (EN) | Inter | 400 | Clean, neutral |
| Body (CN) | Noto Sans SC | 400 | |
| Metadata | IBM Plex Mono | 400 | Page numbers, dates, labels |

### Swiss Color Presets (for PptxGenJS)
| Name | Accent | Use Case |
|------|--------|----------|
| IKB | `002FA7` | Tech, authority, trust |
| Cadmium Yellow | `FFD500` | Energy, creativity, attention |
| Highlighter Green | `C5E803` | Fresh, modern, startup |
| Safety Orange | `FF6B35` | Bold, warm, action |

Grey scale (shared): paper `FAFAF8`, ink `0A0A0A`, grey-1 `F0F0EE`, grey-2 `D4D4D2`, grey-3 `737373`

### Swiss Layout Patterns (adapt to PptxGenJS)
- **Statement slide**: One sentence, centered, 60pt+ thin weight, no other elements
- **Data grid**: 2x2 or 3x2 cards with hairline borders, large numbers top-left
- **Split**: 50/50 image + text, no overlap, clean edge
- **Timeline**: Horizontal line with numbered nodes, minimal labels below
- **Evidence**: Full-width image with small caption bottom-left

---

## Chinese Title Font-Size Tiers

When using Chinese characters as slide titles, longer text needs smaller sizes to maintain visual balance:

| Characters | PptxGenJS fontSize | Notes |
|-----------|-------------------|-------|
| 2-4 chars | 60-72pt | Maximum impact |
| 5-6 chars | 48-54pt | Still dominant |
| 7-8 chars | 40-44pt | Standard title |
| 9-12 chars | 32-36pt | Needs breathing room |
| 13+ chars | 24-28pt | Consider splitting into two lines |

### Chinese Typography Rules
- Chinese body text: minimum 14pt (smaller is unreadable on projection)
- Line height for Chinese: 1.8-2.0x (wider than English 1.4-1.6x)
- Mixed CN/EN: keep English slightly smaller than Chinese in same line
- Never use bold for Chinese body text (strokes become muddy) — use weight 500 max
- Punctuation: use full-width Chinese punctuation（，。；：）not half-width

---

## Structured Workflow (6 Steps)

Apply this workflow when creating any presentation:

1. **Clarify** — Audience, duration, source material, visual style, constraints
2. **Structure** — Build narrative arc: Hook → Problem → Insight → Evidence → Solution → CTA
3. **Layout Plan** — Map content to slide types, plan dark/light rhythm (sandwich: dark title → light content → dark closing)
4. **Fill** — One visual element per slide minimum; vary layouts across slides
5. **Self-Check** — Run visual QA (use subagent), check Chinese sizing, verify contrast
6. **Iterate** — Fix issues, re-verify, repeat until clean pass

---

## Theme Rhythm

Alternate slide backgrounds for visual interest:
- Title/Closing: dark background, light text
- Content: light background, dark text
- Emphasis: accent color background (use sparingly, 1-2 slides max)
- Never use more than 3 consecutive same-background slides

---

## Quick Reference: What NOT to Do

| Bad | Good |
|-----|------|
| All colors equal weight | 60% dominant + 30% secondary + 10% accent |
| Centered body text | Left-aligned body, centered only for statements |
| Same layout every slide | Vary: split, grid, statement, data, image |
| Decorative gradients | Flat colors, hairline rules |
| Emoji as icons | Lucide/Feather icon set (or no icons) |
| Text-only slides | Every slide has a visual element |
| Generic blue theme | Topic-specific color choice |
