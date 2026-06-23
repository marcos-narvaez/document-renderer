"""Render parsed Markdown blocks through a Jinja2 LaTeX template."""

from __future__ import annotations

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from .markdown_parser import Block, Document


LATEX_REPLACEMENTS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

UNICODE_LATEX_REPLACEMENTS = {
    "−": "-",
    "→": r"$\rightarrow$",
    "←": r"$\leftarrow$",
    "↔": r"$\leftrightarrow$",
    "⇒": r"$\Rightarrow$",
    "≈": r"$\approx$",
    "≥": r"$\geq$",
    "≤": r"$\leq$",
    "×": r"$\times$",
    "÷": r"$\div$",
    "·": r"$\cdot$",
    "²": r"$^{2}$",
    "³": r"$^{3}$",
    "°": r"$^\circ$",
    "•": r"\textbullet{}",
    "…": r"\ldots{}",
    "“": "``",
    "”": "''",
    "‘": "`",
    "’": "'",
    "–": "--",
    "—": "---",
}


def escape_latex(value: str) -> str:
    return "".join(LATEX_REPLACEMENTS.get(char, char) for char in value)


def render_inline(value: str) -> str:
    """Render basic inline Markdown while escaping all ordinary text."""
    placeholders: list[str] = []

    def stash(latex: str) -> str:
        placeholders.append(latex)
        return f"\x00{len(placeholders) - 1}\x00"

    value = "".join(
        stash(replacement) if (replacement := UNICODE_LATEX_REPLACEMENTS.get(char)) else char
        for char in value
    )

    value = re.sub(
        r"`([^`\n]+)`",
        lambda match: stash(r"\texttt{" + escape_latex(match.group(1)) + "}"),
        value,
    )
    value = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: stash(
            r"\href{" + escape_latex(match.group(2)) + "}{" + escape_latex(match.group(1)) + "}"
        ),
        value,
    )
    value = re.sub(
        r"\*\*([^*\n]+)\*\*|__([^_\n]+)__",
        lambda match: stash(r"\textbf{" + escape_latex(match.group(1) or match.group(2)) + "}"),
        value,
    )
    value = re.sub(
        r"(?<!\*)\*([^*\n]+)\*(?!\*)|(?<!_)_([^_\n]+)_(?!_)",
        lambda match: stash(r"\emph{" + escape_latex(match.group(1) or match.group(2)) + "}"),
        value,
    )
    rendered = escape_latex(value)
    for index, placeholder in enumerate(placeholders):
        rendered = rendered.replace(escape_latex(f"\x00{index}\x00"), placeholder)
    return rendered


def render_block(block: Block) -> str:
    if block.kind == "heading":
        commands = {1: "section", 2: "section", 3: "subsection", 4: "subsubsection"}
        command = commands.get(block.level, "paragraph")
        return rf"\{command}{{{render_inline(block.content)}}}"

    if block.kind == "paragraph":
        return render_inline(block.content)

    if block.kind == "blockquote":
        paragraphs = "\n\n".join(
            render_inline(paragraph) for paragraph in block.content.split("\n\n")
        )
        return "\\begin{quote}\n" + paragraphs + "\n\\end{quote}"

    if block.kind == "horizontal_rule":
        return r"\begin{center}\rule{0.35\textwidth}{0.4pt}\end{center}"

    if block.kind == "image":
        lines = [
            r"\begin{figure}[htbp]",
            r"\centering",
            (
                r"\includegraphics[width=\textwidth,height=0.78\textheight,"
                r"keepaspectratio]{\detokenize{" + block.source + "}}"
            ),
        ]
        if block.content:
            lines.append(r"\caption{" + render_inline(block.content) + "}")
        lines.append(r"\end{figure}")
        return "\n".join(lines)

    if block.kind in {"bullet_list", "ordered_list"}:
        environment = "enumerate" if block.kind == "ordered_list" else "itemize"
        items = "\n".join(r"\item " + render_inline(item) for item in block.items)
        return f"\\begin{{{environment}}}\n{items}\n\\end{{{environment}}}"

    if block.kind == "code":
        return "\\begin{Verbatim}[fontsize=\\small,breaklines=true]\n" + block.content + "\n\\end{Verbatim}"

    if block.kind == "table":
        column_count = max(len(block.headers), *(len(row) for row in block.rows), 1)
        column_spec = "@{}" + "X" * column_count + "@{}"
        lines = [rf"\begin{{tabularx}}{{\textwidth}}{{{column_spec}}}", r"\toprule"]
        if block.headers:
            lines.extend([" & ".join(render_inline(cell) for cell in block.headers) + r" \\", r"\midrule"])
        for row in block.rows:
            padded = row + [""] * (column_count - len(row))
            lines.append(" & ".join(render_inline(cell) for cell in padded) + r" \\")
        lines.extend([r"\bottomrule", r"\end{tabularx}"])
        return "\n".join(lines)

    raise ValueError(f"Unsupported block type: {block.kind}")


def render_document(document: Document, template_path: Path) -> str:
    environment = Environment(
        loader=FileSystemLoader(template_path.parent),
        undefined=StrictUndefined,
        autoescape=False,
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="<<",
        variable_end_string=">>",
    )
    template = environment.get_template(template_path.name)
    return template.render(
        title=render_inline(document.title),
        body="\n\n".join(render_block(block) for block in document.blocks),
    )
