"""Translation of menu items.

:ref: https://bulma.io/documentation/components/menu/
"""

from __future__ import annotations

from bs4 import BeautifulSoup, Tag


def append_style(html: str, tag: str = "ul") -> str:
    """Append class attribute to render as Bulma's menu list.

    :param html: HTML string to be modified.
    :param tag: Tag name to be searched for.
    :return: Modified HTML string.
    """
    soup = BeautifulSoup(html, "html.parser")
    elm = soup.find(tag)
    if isinstance(elm, Tag):
        elm.attrs.setdefault("class", [])
        if isinstance(elm.attrs["class"], str):
            elm.attrs["class"] = [elm.attrs["class"]]
        elm.attrs["class"].append("menu-list")
    return str(soup)
