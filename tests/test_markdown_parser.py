import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from document_renderer.markdown_parser import parse_markdown


class HeadingNumberingTests(unittest.TestCase):
    def test_removes_explicit_body_heading_numbers(self) -> None:
        document = parse_markdown(
            "# Report\n\n"
            "## 1. Purpose\n\n"
            "### 2.1 Expected Value\n\n"
            "#### 3) Details\n"
        )

        self.assertEqual(
            [block.content for block in document.blocks if block.kind == "heading"],
            ["Purpose", "Expected Value", "Details"],
        )

    def test_preserves_semantic_identifiers(self) -> None:
        document = parse_markdown("# Report\n\n## H1 — First Hypothesis\n")

        self.assertEqual(document.blocks[0].content, "H1 — First Hypothesis")

    def test_promotes_heading_when_parent_level_is_missing(self) -> None:
        document = parse_markdown(
            "# Report\n\n"
            "### A Catalog Entry\n\n"
            "#### Detail\n\n"
            "## Main Section\n"
        )

        headings = [block for block in document.blocks if block.kind == "heading"]
        self.assertEqual(
            [(block.content, block.level) for block in headings],
            [("A Catalog Entry", 2), ("Detail", 3), ("Main Section", 2)],
        )

    def test_parses_existing_standalone_image(self) -> None:
        with TemporaryDirectory() as directory:
            image_path = Path(directory) / "plate.jpg"
            image_path.write_bytes(b"test")
            document = parse_markdown(
                "# Report\n\n![Plate](plate.jpg)\n",
                source_dir=Path(directory),
            )

        self.assertEqual(document.warnings, [])
        self.assertEqual(document.blocks[0].kind, "image")
        self.assertEqual(document.blocks[0].content, "Plate")
        self.assertEqual(document.blocks[0].source, str(image_path.resolve()))

    def test_warns_about_missing_image(self) -> None:
        with TemporaryDirectory() as directory:
            document = parse_markdown(
                "# Report\n\n![Plate](missing.jpg)\n",
                source_dir=Path(directory),
            )

        self.assertIn("Image not found:", document.warnings[0])
        self.assertEqual(document.blocks[0].kind, "paragraph")

    def test_warns_about_unsupported_image_format(self) -> None:
        with TemporaryDirectory() as directory:
            image_path = Path(directory) / "plate.heic"
            image_path.write_bytes(b"test")
            document = parse_markdown(
                "# Report\n\n![Plate](plate.heic)\n",
                source_dir=Path(directory),
            )

        self.assertIn("Unsupported image format '.heic'", document.warnings[0])
        self.assertEqual(document.blocks[0].kind, "paragraph")

    def test_parses_blockquote_and_horizontal_rule(self) -> None:
        document = parse_markdown(
            "# Report\n\n"
            "> First paragraph.\n>\n> Second **paragraph**.\n\n"
            "---\n"
        )

        self.assertEqual(
            [(block.kind, block.content) for block in document.blocks],
            [
                ("blockquote", "First paragraph.\n\nSecond **paragraph**."),
                ("horizontal_rule", ""),
            ],
        )


if __name__ == "__main__":
    unittest.main()
