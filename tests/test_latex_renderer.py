import unittest

from document_renderer.latex_renderer import render_block
from document_renderer.markdown_parser import Block


class BlockRenderingTests(unittest.TestCase):
    def test_renders_image_with_caption(self) -> None:
        rendered = render_block(
            Block(
                kind="image",
                content="Plate I — Cover",
                source="/tmp/plate one.jpg",
            )
        )

        self.assertIn(r"\includegraphics", rendered)
        self.assertIn(r"\detokenize{/tmp/plate one.jpg}", rendered)
        self.assertIn(r"\caption{Plate I — Cover}", rendered)

    def test_renders_blockquote(self) -> None:
        rendered = render_block(
            Block(kind="blockquote", content="First.\n\nSecond **bold**.")
        )

        self.assertIn(r"\begin{quote}", rendered)
        self.assertIn(r"\textbf{bold}", rendered)

    def test_renders_horizontal_rule(self) -> None:
        self.assertIn(r"\rule", render_block(Block(kind="horizontal_rule")))


if __name__ == "__main__":
    unittest.main()
