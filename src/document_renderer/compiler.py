"""Compile generated LaTeX using latexmk when it is available."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class LatexCompilerUnavailable(RuntimeError):
    pass


class LatexCompilationError(RuntimeError):
    pass


def compile_latex(tex_path: Path) -> Path:
    tex_path = tex_path.resolve()
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        raise LatexCompilerUnavailable(
            "latexmk was not found. The .tex file was generated successfully; "
            "install a TeX distribution with latexmk to produce the PDF."
        )

    command = [
        latexmk,
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-outdir=.",
        tex_path.name,
    ]
    result = subprocess.run(
        command,
        cwd=tex_path.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        log_tail = "\n".join((result.stdout + "\n" + result.stderr).splitlines()[-30:])
        raise LatexCompilationError(f"LaTeX compilation failed:\n{log_tail}")

    subprocess.run(
        [latexmk, "-c", "-outdir=.", tex_path.name],
        cwd=tex_path.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    return tex_path.with_suffix(".pdf")
