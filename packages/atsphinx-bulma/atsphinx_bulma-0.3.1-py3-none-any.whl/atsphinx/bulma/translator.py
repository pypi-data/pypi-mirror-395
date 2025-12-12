"""Collection of translators for Bluma components."""

from __future__ import annotations

from sphinx.writers.html5 import HTML5Translator
from typing_extensions import override

from .components import messages


class BulmaTranslator(HTML5Translator):  # noqa: D101
    def visit_table(self, node):
        """Append ``table`` class of Bulma."""
        node.set_class("table")
        super().visit_table(node)

    @override
    def visit_admonition(self, node, name=""):
        messages.visit_admonition(self, node, name)

    @override
    def depart_admonition(self, node=None):
        messages.depart_admonition(self, node)
