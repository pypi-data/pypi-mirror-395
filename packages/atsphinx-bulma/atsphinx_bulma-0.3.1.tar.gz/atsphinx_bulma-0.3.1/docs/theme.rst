===========
Using theme
===========

Overview
========

This provides theme to display contents designed by Bulma.

Requirements
============

This does not have extra requirements.
You can use soon after install atsphinx-bulma.

Usage
=====

.. code-block:: python
   :caption: conf.py

   html_theme = "bulma-basic"

Options
=======

.. confval:: bulma_version
   :type: str
   :default: ``"1.0.4"``

   Version of bulma to fetch from CDN.

.. confval:: bulmaswatch
   :type: str
   :default: ``""``

   Theme name of `bulmaswatch <https://jenil.github.io/bulmaswatch/>`_ if it is set no-blank string.

.. confval:: bulmaswatch_version
   :type: str
   :default: ``"0.8.1"``

   Version of bulmaswatch to fetch from CDN.

.. confval:: color_mode
   :type: Literal["light", "dark", ""]
   :default: ``""``

   Using color mode.

.. confval:: logo_class
   :type: str
   :default: ``"is-128x128"``

   When you set ``html_logo`` into ``conf.py``, set class attributes.

.. confval:: logo_description
   :type: str
   :default: ``""``

   Description text under logo image on sideber.

.. confval:: sidebar_position
   :type: Literal["left", "right"]
   :default: ``"left"``

   Which sidebar renders on content. Set ``'left'`` or ``'right'``.

.. confval:: sideber_size
   :type: int
   :default: ``2``

   Column size of sidebar.

.. confval:: navbar_icons
   :type: list[dict]
   :default: ``[]``

   Configurations for icons on navbar (top of page).

.. confval:: navbar_search
   :type: bool
   :default: ``False``

   When this is set ``True``, display search input form on navbar.

.. confval:: navbar_links
   :type: list[dict]
   :default: ``[]``

   Addtional links on navbar.

.. confval:: show_theme_credit
   :type: bool
   :default: ``True``

   Please set ``False`` if you don't want to render credit of this extension.
