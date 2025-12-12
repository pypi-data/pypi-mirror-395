"""Entrypoint of theme."""

from pathlib import Path
from typing import Union

from bs4 import BeautifulSoup, Tag
from docutils import nodes
from sphinx.application import Sphinx

from ... import __version__
from ...components import menu
from ...components.navbar import register_root_toctree_dict

here = Path(__file__).parent


def append_styling_filters(app: Sphinx):
    """Append custom filters to update content for enabling Bulma styles."""
    app.builder.templates.environment.filters["set_menu_list"] = menu.append_style


def setup(app: Sphinx):  # noqa: D103
    app.add_html_theme("bulma-basic", str(here))
    app.connect("builder-inited", append_styling_filters)
    app.connect("html-page-context", register_root_toctree_dict)
    app.setup_extension("atsphinx.bulma")
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
