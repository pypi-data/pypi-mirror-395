"""
Markdown Extension: Inline SVG Embedding

This extension allows users to embed local SVG files into Markdown
using a syntax similar to image embedding:

    ![caption](path/to/image.svg)

or:

    !(path/to/image.svg)

If a caption is provided, the resulting HTML is wrapped in a <figure>
element with <figcaption>. Otherwise, the raw inline SVG is inserted.

Example:
    ![A diagram](images/example.svg)
"""

from __future__ import annotations

import os
import re
from typing import Optional
from xml.etree.ElementTree import register_namespace, parse, Element, \
    SubElement, tostring, ParseError

from markdown import Extension, Markdown, util
from markdown.extensions.attr_list import AttrListTreeprocessor
from markdown.inlinepatterns import InlineProcessor
from markdown.postprocessors import Postprocessor

# accepts:
#   ![caption](file.svg)
#   !(file.svg)
RE_SVG_CAPTIONED = r"\!(?:\[([^\]]+)\])?\(([^)]+)\)"

# ensure default namespace applied only once
register_namespace("", "http://www.w3.org/2000/svg")

_CACHE = {}


def _placeholder(path: str) -> str:
    """
    Generate a Markdown-safe placeholder for later replacement.
    """
    return util.STX + path + util.ETX


class SVGInlineProcessor(InlineProcessor):
    """
    InlineProcessor that replaces Markdown-style inline SVG references
    with placeholder tokens to be replaced later by SVGPostprocessor.

    This prevents the Markdown parser from escaping or altering the inline
    SVG due to namespacing.
    """

    def __init__(self,
                 pattern: str,
                 md: Optional[Markdown] = None,
                 **kwargs):
        super().__init__(pattern, md)
        self._root = kwargs.get("root", None)
        self._remove_prefix = kwargs.get("remove_prefix", None)

    def handleMatch(self, m, data):
        caption = m.group(1)
        href = m.group(2).strip()

        if self._remove_prefix:
            href = href.removeprefix(self._remove_prefix)

        # skip urls or non-svg type files
        if (href.lower().startswith(("http://", "https://", "//"))
                or not href.lower().endswith(".svg")):
            return None, None, None

        if self._root:
            # resolve the relative path
            path = os.path.abspath(os.path.join(self._root, href))
        else:
            path = os.path.abspath(href)

        if not os.path.exists(path):
            return None, None, None

        if path not in _CACHE:
            try:
                svg = parse(path).getroot()
            except ParseError:
                return None, None, None

            _CACHE[path] = svg

        placeholder = _placeholder(path)

        # no caption, return placeholder
        if not caption or caption.isspace():
            return placeholder, m.start(), m.end()

        # captioned svg, wrap in figure with caption
        fig = Element("figure")
        fig.text = placeholder

        cap = SubElement(fig, "figcaption")
        cap.text = caption.strip()

        index = m.end()

        if "attr_list" in self.md.treeprocessors:
            attributes = re.match(AttrListTreeprocessor.BASE_RE, data[index:])

            if attributes:
                fig[-1].tail = f"\n{attributes.group()}"
                index += attributes.end()

        return fig, m.start(), index


# pylint: disable=too-few-public-methods
class SVGPostprocessor(Postprocessor):
    """
    Postprocessor that replaces placeholder tokens with real SVG markup.

    The placeholders prevent Markdown from escaping inline XML prematurely,
    especially in relation to namespaces.
    """

    def run(self, text):
        for path, svg in _CACHE.items():
            placeholder = _placeholder(path)

            # skip unnecessary replacements
            if placeholder not in text:
                continue

            svg_str = tostring(svg, encoding="unicode")
            text = text.replace(placeholder, svg_str)
        return text


# pylint: disable=too-few-public-methods
class InlineSVGExtension(Extension):
    """
    Markdown Extension: Inline SVG Embedding.

    Configuration:
        root: str = "./"
            Root directory from which relative SVG paths will be resolved.
    """

    def __init__(self, **kwargs):
        self.config = {
            "root": ["", "Root directory for SVG files"],
            "remove_prefix": ["", "Prefix to remove from matched HREFs"]
        }

        super().__init__(**kwargs)

    # pylint: disable=invalid-name
    def extendMarkdown(self, md):
        root = self.getConfig("root")
        remove_prefix = self.getConfig("remove_prefix")

        md.inlinePatterns.register(
            SVGInlineProcessor(RE_SVG_CAPTIONED, md,
                               root=root,
                               remove_prefix=remove_prefix),
            "inline-svg",
            200
        )

        md.postprocessors.register(
            SVGPostprocessor(),
            "inline-svg",
            200
        )
