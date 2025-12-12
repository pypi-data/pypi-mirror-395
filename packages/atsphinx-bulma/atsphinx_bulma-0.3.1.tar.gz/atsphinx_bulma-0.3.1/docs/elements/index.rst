========
Elements
========

Documents are wrapped by ``content`` class of Bulma by ``bulma-basic`` theme.
Some elements render as Bulma designed style.

Definition lists
================

term (up to a line of text)
   Definition of the term, which must be indented

Table
=====

.. note:: Tables are translated to add ``table`` class for design.

.. csv-table::
   :header: Name,Description

   toybox, Misc items.
   bulma, Bulma components and theme.

Field lists
===========

:fieldname: Field content

Code block
==========

.. code-block:: console

   $ ogpy --format=json https://ogp.me
   {"title": "Open Graph protocol", "type": "website", "url": "https://ogp.me/", "images": [{"url": "https://ogp.me/logo.png", "secure_url": null, "type": "image/png", "width": 300, "height": 300, "alt": "The Open Graph logo"}], "audio": null, "description": "The Open Graph protocol enables any web page to become a rich object in a social graph.", "determiner": "", "locale": "en_US", "locale_alternates": [], "site_name": null, "video": null}

Images
======

.. image:: https://www.attakei.net/_static/images/icon-attakei@2x.png
   :align: center

Footnotes
=========

.. note:: Style of footnotes is updated to adjust for other elements.


Lorem ipsum [#f1]_ dolor sit amet ... [#f2]_

.. rubric:: Footnotes

.. [#f1] Text of the first footnote.
.. [#f2] Text of the second footnote.

