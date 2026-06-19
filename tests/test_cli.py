import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from document_renderer.cli import main
from document_renderer.compiler import LatexCompilationError


TEMPLATE = r"""\documentclass{article}
\begin{document}
<< body >>
\end{document}
"""


class CliTexRetentionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.source = self.root / "report.md"
        self.template = self.root / "template.tex.j2"
        self.output = self.root / "output"
        self.source.write_text("# Report\n\nBody.\n", encoding="utf-8")
        self.template.write_text(TEMPLATE, encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def arguments(self, *extra: str) -> list[str]:
        return [
            str(self.source),
            "--template",
            str(self.template),
            "--output-dir",
            str(self.output),
            *extra,
        ]

    @patch("document_renderer.cli.compile_latex")
    def test_success_removes_tex_by_default(self, compile_latex) -> None:
        compile_latex.side_effect = lambda path: path.with_suffix(".pdf")

        self.assertEqual(main(self.arguments()), 0)
        self.assertFalse((self.output / "report.tex").exists())

    @patch("document_renderer.cli.compile_latex")
    def test_keep_tex_preserves_tex(self, compile_latex) -> None:
        def compile_in_selected_directory(path: Path) -> Path:
            pdf_path = path.with_suffix(".pdf")
            pdf_path.write_bytes(b"%PDF-test")
            return pdf_path

        compile_latex.side_effect = compile_in_selected_directory

        self.assertEqual(main(self.arguments("--keep-tex")), 0)
        self.assertTrue((self.output / "report.tex").exists())
        self.assertTrue((self.output / "report.pdf").exists())

    @patch("document_renderer.cli.compile_latex")
    def test_compilation_failure_preserves_tex(self, compile_latex) -> None:
        compile_latex.side_effect = LatexCompilationError("test failure")

        self.assertEqual(main(self.arguments()), 1)
        self.assertTrue((self.output / "report.tex").exists())

    def test_no_compile_preserves_tex(self) -> None:
        self.assertEqual(main(self.arguments("--no-compile")), 0)
        self.assertTrue((self.output / "report.tex").exists())

    def test_parser_marks_custom_output_directory(self) -> None:
        from document_renderer.cli import build_parser

        arguments = build_parser().parse_args(
            [str(self.source), "-o", str(self.output)]
        )
        self.assertEqual(arguments.output_dir, self.output)

    def test_image_warning_is_printed(self) -> None:
        self.source.write_text("# Report\n\n![Plate](plate.jpg)\n", encoding="utf-8")
        stderr = StringIO()

        with redirect_stderr(stderr):
            self.assertEqual(main(self.arguments("--no-compile")), 0)

        self.assertIn("warning: Image not found:", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
