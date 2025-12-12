===========
Change logs
===========

v0.3.1
======

:Date: 2025-12-04 (Asia/Tokyo)

Fixes
-----

* Use future annotations

Others
------

* Update deps outside of uv.
* tests: Use pathlib instead of sphinx.testing.path
* Use ty for static check instead of mypy.
* Mark Python 3.14 is supported on classifier.

v0.3.0
======

:Date: 2025-10-26 (Asia/Tokyo)

Deps
----

* Update default Bulma version to 1.0.4.

Features
--------

* Support custom version of Blumaswatch. It set current latest version.

Fixes
-----

* Redesign section elements to render flatten.
* Add ``menu-list`` class into toc components of sidebar without JavaScript.

Others
------

* Update classifier to mark as "Beta" product.

v0.2.4
======

:Date: 2025-03-15 (Asia/Tokyo)

Fixes
-----

* Change CDN of Blumaswatch.

v0.2.3
======

:Date: 2025-03-15 (Asia/Tokyo)

Others
------

* search.html does not override 'body' block.

v0.2.2
======

:Date: 2025-03-05 (Asia/Tokyo)

Fixes
-----

* Explicit column of main contents to wrap code-block.
* Set alignment by doctree.

Others
------

* Python version of workspace is 3.12

  * This is minimum version supported as "bug-fix" status.
  * Required version is still >=3.9.

v0.2.1
======

:Date: 2025-01-12 (JST)

Fixes
-----

* Theme

  * Set pygments style.
  * Does not try import when ``bulmaswatch`` of html_theme_options is not set.

Others
------

* Document

  * Use confval.
  * Use navigation for scroll to top.

v0.2.0
======

:Date: 2025-01-02 (JST)

Breaking changes
----------------

* FEAT: Render custom sidebar.
* REFACTOR: Merge setup func.

Features
--------

* Update features of navbar.

  * Display search form on navbar.
  * Show external links on navbar.

* Added sidebar components.

  * sidebar/logo.html
  * sidebar/line.html
  * sidebar/globaltoc.html

* Added configurations. (You can docs to know more)

  * sidebar_size
  * logo_class
  * logo_description
  * navbar_search
  * navbar_links

v0.1.0
======

:Date: 2024-12-21 (JST)

Features
--------

* Add ``bulma-basic`` theme.

v0.0.0
======

:date: 2024-09-18 (JST)

Initial commit.
