def test_menu_list():
    from atsphinx.bulma.components import menu

    src = "<ul><li>Item 1</li><li>Item 2</li></ul>"
    dest = menu.append_style(src, "ul")
    assert dest == '<ul class="menu-list"><li>Item 1</li><li>Item 2</li></ul>'
