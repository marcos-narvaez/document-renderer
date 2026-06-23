"""Compile generated LaTeX using latexmk when it is available."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class LatexCompilerUnavailable(RuntimeError):
    pass


class LatexCompilationError(RuntimeError):
    pass


def _decode_process_output(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return value.decode("utf-8", errors="replace")


def _read_text_lossy(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8", errors="replace")
    except OSError:
        return ""


def _extract_latex_diagnostic(tex_path: Path) -> str:
    log_text = _read_text_lossy(tex_path.with_suffix(".log"))
    if not log_text:
        return ""

    lines = log_text.splitlines()
    diagnostics: list[str] = []
    for index, line in enumerate(lines):
        if line.startswith("! LaTeX Error: Unicode character "):
            diagnostics.append(line)
            for follow in lines[index + 1 : index + 8]:
                if follow.startswith("l."):
                    diagnostics.append(follow)
                    break
            break
        if line.startswith("! "):
            diagnostics.append(line)
            for follow in lines[index + 1 : index + 6]:
                if follow.startswith("l."):
                    diagnostics.append(follow)
                    break
            break

    if not diagnostics:
        return ""
    return "LaTeX diagnostic:\n" + "\n".join(diagnostics)


def _run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=False,
        check=False,
    )


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
        "-xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-outdir=.",
        tex_path.name,
    ]
    result = _run_command(command, tex_path.parent)
    if result.returncode != 0:
        output = _decode_process_output(result.stdout) + "\n" + _decode_process_output(result.stderr)
        log_tail = "\n".join(output.splitlines()[-30:])
        diagnostic = _extract_latex_diagnostic(tex_path)
        if diagnostic:
            log_tail = diagnostic + "\n\n" + log_tail
        raise LatexCompilationError(f"LaTeX compilation failed:\n{log_tail}")

    _run_command([latexmk, "-c", "-outdir=.", tex_path.name], tex_path.parent)
    return tex_path.with_suffix(".pdf")
