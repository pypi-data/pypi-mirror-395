"""Standard tests."""

from io import StringIO

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html", confoverrides={"html_theme": "bulma-basic"})
def test__render_hero(app: SphinxTestApp, warning: StringIO):
    """Test to pass."""
    app.build()
    soup = BeautifulSoup((app.outdir / "hero.html").read_text(), "html.parser")
    assert soup.find("section", class_="hero")


@pytest.mark.sphinx(
    "html", testroot="multiple-hero", confoverrides={"html_theme": "bulma-basic"}
)
def test__display_warning(app: SphinxTestApp, warning: StringIO):
    """Test to pass."""
    app.build()
    assert "'hero' directives should be only one on one document." in warning.getvalue()
