"""Translator for messages (from admonition)."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from docutils import nodes
from sphinx.locale import admonitionlabels

if TYPE_CHECKING:
    from typing import Optional

    from sphinx.writers.html5 import HTML5Translator


class MessageClassMap(TypedDict):
    """Mappings definition for admonitions and color classes.

    :ref: https://www.docutils.org/docs/ref/rst/directives.html#specific-admonitions
    """

    # docutils admonition's types
    attention: str
    caution: str
    danger: str
    error: str
    hint: str
    important: str
    note: str
    tip: str
    warning: str
    # Sphinx extra admonitions
    Todo: str


DEFAULT_MESSAGE_CLASSES: MessageClassMap = {
    # docutils admonition's types
    "attention": "is-warning",
    "caution": "is-warning",
    "danger": "is-danger",
    "error": "is-danger",
    "hint": "is-info",
    "important": "is-info",
    "note": "is-info",
    "tip": "is-info",
    "warning": "is-warning",
    # Sphinx extra admonitions
    "Todo": "is-link",
}


def visit_admonition(  # noqa: D103
    self: HTML5Translator, node: nodes.admonition, name: str = ""
) -> None:
    message_classes: MessageClassMap = self.builder.app.config.bulma_message_classes
    fallback_class = self.builder.app.config.bulma_message_fallback
    if isinstance(node.children[0], nodes.title):
        msg_title = node.pop(0).astext()
        msg_class = message_classes.get(msg_title, fallback_class)
    else:
        msg_title = admonitionlabels[name]
        msg_class = message_classes.get(name, fallback_class)
    self.body.append(f'<article class="message {msg_class}">')
    self.body.append(f"""
      <div class="message-header">
        <p>{msg_title}</p>
      </div>
    """)
    self.body.append('  <div class="message-body">')


def depart_admonition(  # noqa: D103
    self: HTML5Translator, node: Optional[nodes.admonition] = None
) -> None:
    self.body.append("  </div>")
    self.body.append("</article>")
