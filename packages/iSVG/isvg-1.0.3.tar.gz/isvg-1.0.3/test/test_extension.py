"""
Test case for the Latex2MathML markdown extension.
"""

from typing import Union
from unittest import TestCase
from xml.etree.ElementTree import fromstring

from markdown import Markdown
from isvg import InlineSVGExtension

EQUALITY_ATTR = ["tag", "text", "tail", "attrib"]


class TestExtension(TestCase):
    """
    Tests for the Latex2MathML markdown extension.
    """

    def setUp(self):
        self.markdown = Markdown(extensions=[
            InlineSVGExtension(root="./svg/")
        ])
        self.markdown_attr_list = Markdown(extensions=[
            InlineSVGExtension(root="./svg/"),
            "attr_list"
        ])

    # pylint: disable=invalid-name
    def assertHTMLEqualsMarkdown(self, expected, actual):
        """
        Assert that the specified Markdown coverts to HTML identical to the
        specified HTML. Whitespace surrounding newlines in the specified
        HTML are discarded.
        """

        # wrap both in a div to make sure there's only one root element
        a = [fromstring(f"<div>{expected}</div>")]
        b = [fromstring(f"<div>{actual}</div>")]

        index = 0

        def normalize(value) -> Union[str, None]:
            if not isinstance(value, str):
                return value

            if value.isspace():
                return None

            return value.strip()

        while index < len(a) and index < len(b):
            element_a = a[index]
            element_b = b[index]

            self.assertEqual(
                len(element_a),
                len(element_b),
                f"{element_a} (a) and {element_b} (b) do not have the same "
                f"number of children"
            )

            for attr in ["tag", "text", "tail", "attrib"]:
                attribute_a = normalize(getattr(element_a, attr))
                attribute_b = normalize(getattr(element_b, attr))

                self.assertEqual(
                    attribute_a,
                    attribute_b,
                    f"{attr} of {element_a} (a) and {element_b} (b) are not "
                    f"equal"
                )

            for child_a, child_b in zip(element_a, element_b):
                a.append(child_a)
                b.append(child_b)

            index += 1

    def test_no_image(self):
        """
        Assert that markdown conversion still works as expected.
        """
        self.assertHTMLEqualsMarkdown(
            "<p>Spam, bacon, eggs.</p>",
            self.markdown.convert("Spam, bacon, eggs.")
        )

    def test_no_svg(self):
        """
        Assert that non-SVG images still work as expected.
        """
        self.assertHTMLEqualsMarkdown(
            """
            <p>
                <img alt=\"spam\" src=\"bacon.png\" />
            </p>
            """,
            self.markdown.convert("![spam](bacon.png)")
        )

    def test_svg_not_found(self):
        """
        Assert that non-existent SVG images are loaded as normal images.
        """
        self.assertHTMLEqualsMarkdown(
            """
            <p>
                <img alt=\"spam\" src=\"bacon.svg\" />
            </p>
            """,
            self.markdown.convert("![spam](bacon.svg)")
        )

    def test_svg_remote(self):
        """
        Assert that remote SVG images are loaded as normal images.
        """
        self.assertHTMLEqualsMarkdown(
            """
            <p>
                <img alt=\"spam\" src=\"https://example.com/bacon.svg\" />
            </p>
            """,
            self.markdown.convert("![spam](https://example.com/bacon.svg)")
        )

    def test_svg_no_caption(self):
        """
        Assert that SVG-images without caption are loaded inline.
        """
        self.assertHTMLEqualsMarkdown(
            """
            <p>
                <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
                    <circle cx="5" cy="5" r="3" fill="blue" stroke="red"/>
                </svg>
            </p>
            """,
            self.markdown.convert("!(test.svg)")
        )

    def test_svg_no_caption_multiple(self):
        """
        Assert that multiple SVG-images without captions are loaded inline.
        """
        self.assertHTMLEqualsMarkdown(
            """
            <p>
                <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
                    <circle cx="5" cy="5" r="3" fill="blue" stroke="red"/>
                </svg>
                <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
                    <circle cx="5" cy="5" r="3" fill="green" stroke="yellow"/>
                </svg>
            </p>
            """,
            self.markdown.convert("!(test.svg)\n!(test2.svg)")
        )

    def test_svg_caption(self):
        """
        Assert that SVG-image with caption are loaded inline as a figure.
        """
        self.assertHTMLEqualsMarkdown(
            """
            <p>
                <figure>
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
                        <circle cx="5" cy="5" r="3" fill="blue" stroke="red"/>
                    </svg>
                    <figcaption>
                        spam, bacon, eggs
                    </figcaption>
                </figure>
            </p>
            """,
            self.markdown.convert("![spam, bacon, eggs](test.svg)")
        )

    def test_svg_caption_multiple(self):
        """
        Assert that multiple SVG-images with captions are loaded inline as a
        figure.
        """
        self.assertHTMLEqualsMarkdown(
            """
            <p>
                <figure>
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
                        <circle cx="5" cy="5" r="3" fill="blue" stroke="red"/>
                    </svg>
                    <figcaption>
                        spam, bacon, eggs
                    </figcaption>
                </figure>
                <figure>
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
                        <circle cx="5" cy="5" r="3" fill="green" stroke="yellow"/>
                    </svg>
                    <figcaption>
                        ham, eggs, beans
                    </figcaption>
                </figure>
            </p>
            """,
            self.markdown.convert(
                "![spam, bacon, eggs](test.svg)\n"
                "![ham, eggs, beans](test2.svg)"
            )
        )

    def test_svg_caption_link(self):
        """
        Assert that SVG-image with caption are loaded inline as a figure.
        """
        self.assertHTMLEqualsMarkdown(
            """
            <p>
                <figure>
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
                        <circle cx="5" cy="5" r="3" fill="blue" stroke="red"/>
                    </svg>
                    <figcaption>
                        spam, <a href="/ham">bacon</a>, eggs
                    </figcaption>
                </figure>
            </p>
            """,
            self.markdown.convert("![spam, [bacon](/ham), eggs](test.svg)")
        )

    def test_svg_caption_attr_list(self):
        """
        Assert that SVG-image with caption are loaded inline as a figure,
        with the appropriate attributes when attr_list is enabled.
        """
        self.assertHTMLEqualsMarkdown(
            """
            <p>
                <figure id="spam-bacon-eggs">
                    <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
                        <circle cx="5" cy="5" r="3" fill="blue" stroke="red"/>
                    </svg>
                    <figcaption>
                        spam, bacon, eggs
                    </figcaption>
                </figure>
            </p>
            """,
            self.markdown_attr_list.convert(
                "![spam, bacon, eggs](test.svg){#spam-bacon-eggs}"
            )
        )
