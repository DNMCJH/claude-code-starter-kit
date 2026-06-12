# HTML Presentation Deck Generator

Generate single-file HTML horizontal-swipe presentation decks with magazine-quality design. Opens directly in browser, no build step needed.

Based on [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) (MIT License).

## Two Visual Systems

### Style A: Editorial Magazine × E-Ink
- Serif titles (Noto Serif SC + Playfair Display), WebGL fluid backgrounds, warm tones
- Inspired by *Monocle* magazine
- 10 layout types, 5 theme presets
- Template: `~/.claude/html-deck/assets/template.html`

### Style B: Swiss International Style
- All sans-serif (Inter + Noto Sans SC), extreme font-size contrast (weight 200 for large text)
- Single high-saturation accent color, 16-column grid, hairline rules
- No shadows, no gradients, no rounded corners
- Inspired by Massimo Vignelli / Josef Müller-Brockmann
- 22 locked layouts (S01-S22), 4 theme presets
- Template: `~/.claude/html-deck/assets/template-swiss.html`

## Workflow

### Step 1: Requirements Clarification
Ask these 7 questions (skip if user already provided):
1. Style choice: A (Magazine) or B (Swiss)?
2. Target audience and context?
3. Approximate duration / slide count?
4. Source material (outline, doc, notes)?
5. Image needs (screenshots, illustrations, photos)?
6. Theme color preference? (must use presets, no custom hex)
7. Hard constraints (branding, format, deadline)?

If user has no outline, help build a narrative arc:
- Hook → Problem → Insight → Evidence → Solution → Call-to-Action

### Step 2: Copy Template
1. Copy the appropriate template to the user's target directory
2. Replace placeholder title text
3. Select theme colors from presets (see references/themes.md or themes-swiss.md)

### Step 3: Fill Content
Pre-flight checks:
- Verify all CSS class names exist in the template's `<style>` block before using them
- Plan theme rhythm: hero dark → hero light → light → dark (alternate)
- Pick layouts from references (Style B: every page MUST use a registered layout S01-S22 with `data-layout` attribute)

Content rules:
- No emoji anywhere — use Lucide icons via CDN
- Chinese large titles: apply font-size tier table (see below)
- Images: standard aspect ratios only, fit designated slots
- Style A and B CANNOT be mixed in one deck

### Step 4: Self-Check
Run against checklist (see references/checklist.md):
- P0: Layout registration, canvas alignment, font constraints, image handling
- P1: Hero/non-hero alternation, dense/sparse rhythm
- P2: Visual polish, spacing, Chinese title sizing
- P3: Relative paths, navigation preservation

For Style B: also run `node ~/.claude/html-deck/scripts/validate-swiss-deck.mjs <file.html>`

### Step 5: Local Preview
Open the HTML file directly in browser. Press B for static mode (disables WebGL).

### Step 6: Iterate
90% of adjustments are inline style tweaks (font-size, height, gap).

## Chinese Title Font-Size Tiers

| Characters | Max font-size |
|-----------|---------------|
| 2-4 chars | 4.8rem |
| 5-6 chars | 4rem |
| 7-8 chars | 3.2rem |
| 9-12 chars | 2.6rem |
| 13+ chars | 2rem (or split into two lines) |

## Key Constraints
- Styles A and B cannot coexist in one deck
- Style B: ONLY 22 registered layouts allowed, no inventing new ones
- No custom colors — only theme presets
- Font roles are strict: serif for titles (A), sans-serif everywhere (B), monospace for metadata
- WebGL/animation must degrade gracefully (press B for static mode)
- Navigation: keyboard arrows + touch swipe + mouse wheel

## Reference Files
All in `~/.claude/html-deck/references/`:
- `checklist.md` — Quality checklist (P0-P3 graded)
- `components.md` — Component manual (fonts, colors, grid, icons, motion)
- `layouts.md` — Style A: 10 layout skeletons
- `layouts-swiss.md` — Style B: 22 locked layouts
- `themes.md` — Style A: 5 theme presets
- `themes-swiss.md` — Style B: 4 accent presets
- `swiss-layout-lock.md` — Layout registration rules
- `image-prompts.md` — Image generation guidance
