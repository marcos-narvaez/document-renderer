# Document Renderer

A minimal, deterministic Markdown-to-LaTeX/PDF renderer. It keeps report content in Markdown and owns presentation locally through one reusable Jinja2 LaTeX template.

## Install

Requirements:

- Python 3.10+
- `latexmk` and a working LaTeX distribution for PDF output
- Git

First, check what is already installed:

```bash
python3 --version
latexmk --version
git --version
```

Only install missing prerequisites. On macOS with Homebrew:

```bash
# Only if python3 is missing or older than 3.10:
brew install python

# Only if latexmk is missing:
brew install --cask mactex-no-gui

# Only if git is missing:
brew install git
```

Then clone and install:

```bash
git clone https://github.com/marcos-narvaez/document-renderer.git
cd document-renderer
./install.sh
```

The installer creates an isolated virtual environment and exposes
`document-renderer` through `~/.local/bin`.

To update:

```bash
cd document-renderer
git pull
./install.sh
```

Verify:

```bash
document-renderer examples/sample_report.md
```

The generated PDF will be written beside `examples/sample_report.md`.

### Claude Code and Codex

Add this stable pointer to `~/.claude/CLAUDE.md`, replacing the path with the
actual clone location:

```markdown
## Formal PDF Reports

When asked to create or render a formal PDF report, read:
`/absolute/path/to/document-renderer/TOOLING.md`

Follow those instructions for that report. Do not apply them to unrelated
writing, coding, or local-tool workflows.
```

Add the same scoped pointer to `~/.codex/AGENTS.md`:

```markdown
## Formal PDF Reports

When asked to create or render a formal PDF report, read:
`/absolute/path/to/document-renderer/TOOLING.md`

Apply those instructions only to that report. Do not apply them to unrelated
writing, coding, or local-tool workflows.
```

## Usage

```bash
document-renderer examples/sample_report.md
```

By default, a successful build retains only the PDF:

```text
examples/sample_report.pdf
```

The PDF is written beside the source Markdown file. Use `-o` only to override that location.

Keep the intermediate LaTeX when needed:

```bash
python -m document_renderer examples/sample_report.md --keep-tex
```

Generate only LaTeX without compiling:

```bash
python -m document_renderer examples/sample_report.md --no-compile
```

Choose another output directory or template:

```bash
python -m document_renderer report.md -o build --template templates/professional_report.tex.j2
```

If compilation fails or `latexmk` is unavailable, the renderer retains the `.tex` file for debugging and exits with a clear message.

## Supported Markdown

- First level-one heading as the document title
- Headings
- Paragraphs
- Bullet and numbered lists
- Fenced code blocks
- Simple tables
- Blockquotes
- Horizontal rules
- Standalone local images with optional captions
- Basic inline bold, emphasis, code, and links

Image paths are resolved relative to the Markdown file; JPEG, PNG, and PDF are supported. Missing,
remote, inline, and unsupported-format images produce clear warnings instead of failing silently.
Heading levels that skip a required parent are promoted to prevent invalid numbering such as `0.1`.

The parser remains intentionally small. Nested lists and complex Markdown extensions are outside
v1.

## Style references

Place example LaTeX reports in `reference/`. They are inputs for future template refinement only. The renderer should borrow general visual choices—margins, typography, spacing, title treatment, headers, footers, and tables—without copying report content or hardcoding a single document.

The v1 template reflects the preferred conventions in the Historian, Rush Chair, and Okavango references:

- Letter paper with approximately one-inch margins
- 11pt Latin-style serif body typography
- Okavango-style centered, regular-weight report masthead
- Rush/Historian-style bold article headings and readable list spacing
- Minimal chrome with page number only
- Booktabs tables and compact page numbering

## Architecture

The pipeline has four direct stages:

1. `markdown_parser.py` converts Markdown tokens into a small document model.
2. `latex_renderer.py` escapes content and renders LaTeX blocks.
3. `professional_report.tex.j2` owns reusable document styling.
4. `compiler.py` invokes `latexmk`.
