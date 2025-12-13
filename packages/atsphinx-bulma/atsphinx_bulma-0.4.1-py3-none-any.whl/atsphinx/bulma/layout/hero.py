"""Behavior about Hero.

:ref: https://bulma.io/documentation/layout/hero/
"""

from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING

import jinja2
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from .. import __version__

if TYPE_CHECKING:
    from typing import Any, Generator

    from sphinx.application import Sphinx
    from sphinx.writers.html import HTMLTranslator


logger = logging.getLogger(__name__)

template = jinja2.Template(
    textwrap.dedent("""
    <section class="{{ hero_classes }}">
      <div class="{{ body_classes }}">
        <p class="title">{{ title }}</p>
        <p class="subtitle">{{ subtitle }}</p>
      </div>
    </section>
""").strip()
)


class hero(nodes.General, nodes.Element):
    pass


class HeroDirective(SphinxDirective):
    """Hero directive to render fullwidth banner on top of page.

    When it is added on document,
    builder generates ``hero`` context value to inject upper of main section.
    This renders nothing on ``body`` variable.

    This directive must be only one on one document.
    """

    option_spec = {
        "title": directives.unchanged,
        "subtitle": directives.unchanged,
        "classes": directives.unchanged,
    }
    has_content = False

    def run(self) -> list[hero]:  # noqa: D102
        node = hero()
        node.attributes |= self.options
        return [
            node,
        ]


def skip_node(self: HTMLTranslator, node: hero):
    raise nodes.SkipNode


def register_hero_html(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: nodes.document | None = None,
) -> str | None:
    if not doctree:
        return
    hero_list: Generator[hero] = doctree.findall(hero)
    for node in hero_list:
        if "bulma_hero" in context:
            logger.warning("'hero' directives should be only one on one document.")
            continue
        hero_classes = "hero"
        if "classes" in node:
            hero_classes += f" {node['classes']}"
        body_classes = "hero-body"
        context["bulma_hero"] = template.render(
            {
                "title": node.get("title", ""),
                "subtitle": node.get("subtitle", ""),
                "hero_classes": hero_classes,
                "body_classes": body_classes,
            }
        )
    else:
        return


def setup(app: Sphinx):  # noqa: D103
    app.add_directive("bulma-hero", HeroDirective)
    app.add_node(hero, html=(skip_node, None))
    app.connect("html-page-context", register_hero_html)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
