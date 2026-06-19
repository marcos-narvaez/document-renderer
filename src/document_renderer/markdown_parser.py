"""Parse a deliberately small Markdown subset into document blocks."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

from markdown_it import MarkdownIt
from markdown_it.token import Token

SUPPORTED_IMAGE_EXTENSIONS = {".jpeg", ".jpg", ".pdf", ".png"}


@dataclass
class Block:
    kind: str
    content: str = ""
    source: str = ""
    level: int = 0
    items: list[str] = field(default_factory=list)
    headers: list[str] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)
    language: str = ""


@dataclass
class Document:
    title: str
    blocks: list[Block]
    warnings: list[str] = field(default_factory=list)


def _inline_content(token: Token) -> str:
    """Preserve inline Markdown tokens for the LaTeX renderer."""
    return token.content


def _strip_explicit_heading_number(content: str) -> str:
    """Remove numbering that LaTeX will generate from a body heading."""
    return re.sub(r"^\s*\d+(?:\.\d+)*[.)]?\s+", "", content, count=1)


def parse_markdown(
    source: str,
    fallback_title: str = "Report",
    source_dir: Path | None = None,
) -> Document:
    parser = MarkdownIt("commonmark").enable("table")
    tokens = parser.parse(source)
    blocks: list[Block] = []
    title = fallback_title
    title_found = False
    last_heading_level: int | None = None
    warnings: list[str] = []
    index = 0

    while index < len(tokens):
        token = tokens[index]

        if token.type == "heading_open":
            level = int(token.tag[1])
            content = _inline_content(tokens[index + 1])
            if level == 1 and not title_found:
                title = content
                title_found = True
            else:
                level = max(level, 2)
                if last_heading_level is None:
                    level = 2
                elif level > last_heading_level + 1:
                    level = last_heading_level + 1
                blocks.append(
                    Block(
                        kind="heading",
                        content=_strip_explicit_heading_number(content),
                        level=level,
                    )
                )
                last_heading_level = level
            index += 3
            continue

        if token.type == "paragraph_open":
            inline = tokens[index + 1]
            children = inline.children or []
            if len(children) == 1 and children[0].type == "image":
                image = children[0]
                image_source = image.attrGet("src") or ""
                if image_source.startswith(("http://", "https://")):
                    warnings.append(
                        f"Remote image '{image_source}' is unsupported and will render as literal text."
                    )
                    blocks.append(Block(kind="paragraph", content=inline.content))
                else:
                    image_path = Path(unquote(image_source)).expanduser()
                    if not image_path.is_absolute():
                        image_path = (source_dir or Path.cwd()) / image_path
                    image_path = image_path.resolve()
                    if image_path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
                        warnings.append(
                            f"Unsupported image format '{image_path.suffix or '(none)'}': "
                            f"{image_path}. Supported formats: JPEG, PNG, PDF."
                        )
                        blocks.append(Block(kind="paragraph", content=inline.content))
                    elif image_path.is_file():
                        blocks.append(
                            Block(
                                kind="image",
                                content=image.content,
                                source=str(image_path),
                            )
                        )
                    else:
                        warnings.append(
                            f"Image not found: {image_path}. It will render as literal text."
                        )
                        blocks.append(Block(kind="paragraph", content=inline.content))
            else:
                for child in children:
                    if child.type == "image":
                        image_source = child.attrGet("src") or child.content
                        warnings.append(
                            f"Inline image '{image_source}' is unsupported and will render as literal text."
                        )
                blocks.append(Block(kind="paragraph", content=_inline_content(inline)))
            index += 3
            continue

        if token.type == "blockquote_open":
            quote_parts: list[str] = []
            depth = 1
            index += 1
            while index < len(tokens) and depth:
                current = tokens[index]
                if current.type == "blockquote_open":
                    depth += 1
                elif current.type == "blockquote_close":
                    depth -= 1
                elif current.type == "inline" and depth == 1:
                    quote_parts.append(_inline_content(current))
                index += 1
            blocks.append(Block(kind="blockquote", content="\n\n".join(quote_parts)))
            continue

        if token.type == "hr":
            blocks.append(Block(kind="horizontal_rule"))
            index += 1
            continue

        if token.type in {"bullet_list_open", "ordered_list_open"}:
            ordered = token.type == "ordered_list_open"
            items: list[str] = []
            index += 1
            while index < len(tokens) and tokens[index].type not in {
                "bullet_list_close",
                "ordered_list_close",
            }:
                if tokens[index].type == "inline":
                    items.append(_inline_content(tokens[index]))
                index += 1
            blocks.append(Block(kind="ordered_list" if ordered else "bullet_list", items=items))
            index += 1
            continue

        if token.type == "fence":
            blocks.append(
                Block(
                    kind="code",
                    content=token.content.rstrip("\n"),
                    language=token.info.strip(),
                )
            )
            index += 1
            continue

        if token.type == "table_open":
            headers: list[str] = []
            rows: list[list[str]] = []
            current_row: list[str] | None = None
            in_header = False
            index += 1
            while index < len(tokens) and tokens[index].type != "table_close":
                current = tokens[index]
                if current.type == "thead_open":
                    in_header = True
                elif current.type == "thead_close":
                    in_header = False
                elif current.type == "tr_open":
                    current_row = []
                elif current.type == "inline" and current_row is not None:
                    current_row.append(_inline_content(current))
                elif current.type == "tr_close" and current_row is not None:
                    if in_header:
                        headers = current_row
                    else:
                        rows.append(current_row)
                    current_row = None
                index += 1
            blocks.append(Block(kind="table", headers=headers, rows=rows))
            index += 1
            continue

        index += 1

    return Document(title=title, blocks=blocks, warnings=warnings)


def parse_markdown_file(path: Path) -> Document:
    return parse_markdown(
        path.read_text(encoding="utf-8"),
        fallback_title=path.stem.replace("_", " ").title(),
        source_dir=path.resolve().parent,
    )
