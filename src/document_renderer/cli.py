"""Command-line entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .compiler import LatexCompilationError, LatexCompilerUnavailable, compile_latex
from .latex_renderer import render_document
from .markdown_parser import parse_markdown_file


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="document-renderer",
        description="Render a Markdown report to LaTeX and PDF.",
    )
    parser.add_argument("input", type=Path, help="Markdown file to render")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: directory containing the Markdown file)",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=project_root() / "templates" / "professional_report.tex.j2",
        help="Jinja2 LaTeX template",
    )
    parser.add_argument("--no-compile", action="store_true", help="Generate .tex without compiling PDF")
    parser.add_argument(
        "--keep-tex",
        action="store_true",
        help="Keep the generated .tex file after successful PDF compilation",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    input_path = args.input.resolve()

    if not input_path.is_file():
        print(f"error: input file not found: {input_path}", file=sys.stderr)
        return 2
    if not args.template.is_file():
        print(f"error: template not found: {args.template}", file=sys.stderr)
        return 2

    output_dir = (args.output_dir or input_path.parent).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    tex_path = output_dir / f"{input_path.stem}.tex"

    try:
        document = parse_markdown_file(input_path)
        for warning in document.warnings:
            print(f"warning: {warning}", file=sys.stderr)
        tex_path.write_text(render_document(document, args.template), encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"error: could not render document: {exc}", file=sys.stderr)
        return 1

    if args.no_compile:
        print(f"Generated {tex_path}")
        return 0

    try:
        pdf_path = compile_latex(tex_path)
    except LatexCompilerUnavailable as exc:
        print(f"Retained {tex_path}", file=sys.stderr)
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except LatexCompilationError as exc:
        print(f"Retained {tex_path}", file=sys.stderr)
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.keep_tex:
        print(f"Generated {tex_path}")
    else:
        try:
            tex_path.unlink()
        except OSError as exc:
            print(f"warning: could not remove generated LaTeX file: {exc}", file=sys.stderr)

    print(f"Generated {pdf_path}")
    return 0
