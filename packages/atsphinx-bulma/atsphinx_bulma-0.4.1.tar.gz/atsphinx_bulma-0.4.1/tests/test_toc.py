"""Standard tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from io import StringIO

    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html", confoverrides={"html_theme": "bulma-basic"})
def test__added_attr_in_toc(app: SphinxTestApp, status: StringIO, warning: StringIO):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "html.parser")
    toc_h3 = soup.find(lambda tag: tag.name == "h3" and tag.text == "Table of Contents")  # type: ignore[union-attr]
    assert "menu-list" in toc_h3.parent.find("ul").attrs["class"]  # type: ignore[union-attr]


@pytest.mark.sphinx(
    "html",
    confoverrides={
        "html_theme": "bulma-basic",
        "html_sidebars": {
            "**": ["sidebar/globaltoc.html"],
        },
    },
    testroot="toc",
)
def test__added_attr_in_globaltoc(
    app: SphinxTestApp, status: StringIO, warning: StringIO
):
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "html.parser")
    toc_h3 = soup.find(lambda tag: tag.name == "h3" and tag.text == "Table of Contents")  # type: ignore[union-attr]
    assert "menu-list" in toc_h3.parent.find("ul").attrs["class"]  # type: ignore[union-attr]
