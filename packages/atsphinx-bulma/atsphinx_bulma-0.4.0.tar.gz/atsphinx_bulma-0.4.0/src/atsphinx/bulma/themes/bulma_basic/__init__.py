"""Entrypoint of theme."""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path
from typing import TYPE_CHECKING, Union

from bs4 import BeautifulSoup, Tag
from docutils import nodes
from sphinx.application import Sphinx

from ... import __version__
from ...components import menu
from ...components.navbar import register_root_toctree_dict

if TYPE_CHECKING:
    from typing import Any


here = Path(__file__).parent


def append_styling_filters(app: Sphinx):
    """Append custom filters to update content for enabling Bulma styles."""
    app.builder.templates.environment.filters["set_menu_list"] = menu.append_style


def select_layout(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: nodes.document | None = None,
):
    """Pick layout of target page."""
    # TODO: Test it!!
    DEFAULT_LAYOUT = {
        "**": [
            {"type": "sidebar", "size": 2},
            {"type": "main", "size": 10},
        ]
    }
    layouts = app.config.html_theme_options.get("layout", DEFAULT_LAYOUT)
    for key, settings in layouts.items():
        regex = re.compile(fnmatch.translate(key))
        if regex.match(pagename):
            context["bulma_layout"] = settings
            break


def setup(app: Sphinx):  # noqa: D103
    app.add_html_theme("bulma-basic", str(here))
    app.connect("builder-inited", append_styling_filters)
    app.connect("html-page-context", register_root_toctree_dict)
    app.connect("html-page-context", select_layout)
    app.setup_extension("atsphinx.bulma")
    app.setup_extension("atsphinx.bulma.layout.hero")
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
