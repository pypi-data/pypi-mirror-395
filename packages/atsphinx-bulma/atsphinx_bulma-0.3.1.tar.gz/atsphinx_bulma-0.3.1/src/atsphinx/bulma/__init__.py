"""Bluma using suite for Sphinx.."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .components.messages import DEFAULT_MESSAGE_CLASSES, MessageClassMap
from .translator import BulmaTranslator

if TYPE_CHECKING:
    from sphinx.application import Sphinx


__version__ = "0.3.1"


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value(
        "bulma_message_classes",
        DEFAULT_MESSAGE_CLASSES,
        "env",
        MessageClassMap,
    )
    app.add_config_value("bulma_message_fallback", "", "env", str)
    app.set_translator("html", BulmaTranslator)
    app.set_translator("dirhtml", BulmaTranslator)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
