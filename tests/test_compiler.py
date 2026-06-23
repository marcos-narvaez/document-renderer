import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from document_renderer.cli import main
from document_renderer.compiler import LatexCompilationError, compile_latex


UNICODE_MARKDOWN = """# Unicode Regression

Ordinary report text should render: − → ≈ ≥ ≤ × ÷ ² ³ · — – … • ° “curly quotes” á é í ó ú ñ ü.

| Symbol | Meaning |
| --- | --- |
| ≥ | greater than or equal |
| ≤ | less than or equal |
| ≈ | approximately |
"""


class CompilerRegressionTests(unittest.TestCase):
    @unittest.skipUnless(
        shutil.which("latexmk") and shutil.which("xelatex"),
        "latexmk and xelatex are required for integration compilation",
    )
    def test_unicode_markdown_builds_pdf_without_tex_retained(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            markdown_path = Path(directory) / "unicode.md"
            markdown_path.write_text(UNICODE_MARKDOWN, encoding="utf-8")

            self.assertEqual(main([str(markdown_path)]), 0)
            self.assertTrue(markdown_path.with_suffix(".pdf").is_file())
            self.assertFalse(markdown_path.with_suffix(".tex").exists())

    @patch("document_renderer.compiler.shutil.which", return_value="/usr/bin/latexmk")
    @patch("document_renderer.compiler.subprocess.run")
    def test_malformed_latex_output_reports_clean_error(self, run, _which) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tex_path = Path(directory) / "broken.tex"
            tex_path.write_text(r"\documentclass{article}\begin{document}\end{document}")
            tex_path.with_suffix(".log").write_bytes(
                b"! LaTeX Error: Unicode character \xe2\x88\n"
                b"l.12 Broken line with malformed byte \x80\n"
            )
            run.return_value = subprocess.CompletedProcess(
                args=["latexmk"],
                returncode=1,
                stdout=b"stdout before malformed byte \x80 after",
                stderr=b"stderr malformed \xff byte",
            )

            with self.assertRaises(LatexCompilationError) as context:
                compile_latex(tex_path)

        message = str(context.exception)
        self.assertIn("LaTeX compilation failed", message)
        self.assertIn("LaTeX diagnostic", message)
        self.assertIn("\ufffd", message)


if __name__ == "__main__":
    unittest.main()
