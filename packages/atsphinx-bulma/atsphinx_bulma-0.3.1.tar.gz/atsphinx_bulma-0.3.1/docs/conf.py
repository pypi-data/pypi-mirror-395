"""Configuration for documents."""

import os

from atsphinx.bulma import __version__ as version

# -- Project information
project = "atsphinx-bulma"
copyright = "2024, Kazuya Takei"
author = "Kazuya Takei"
release = version

# -- General configuration
extensions = [
    # Bundled extensions
    "sphinx.ext.githubpages",
    "sphinx.ext.todo",
    # Third-party extensions
    "sphinx_toolbox.confval",
    # My extensions
    "atsphinx.goto_top",
    "atsphinx.mini18n",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for i18n
gettext_compact = False
locale_dirs = ["_locales"]

# -- Options for HTML output
html_logo = "https://attakei.net/_static/images/icon-attakei@2x.png"
html_theme = "bulma-basic"
html_theme_options = {
    "color_mode": "light",
    "bulmaswatch": "pulse",
    "logo_description": "This is documentation of atsphinx-bulma.",
    "sidebar_position": "right",
    "sidebar_size": 3,
    "navbar_icons": [
        {
            "label": "",
            "icon": "fa-brands fa-solid fa-github fa-2x",
            "url": "https://github.com/atsphinx/bulma",
        }
    ],
}
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]
html_title = f"{project} v{release}"
html_static_path = ["_static"]
html_sidebars = {
    "**": [
        "sidebar/logo.html",
        "sidebar/line.html",
        "select-lang.html",
        "sidebar/searchbox.html",
        "sidebar/localtoc.html",
        "navigation.html",
    ]
}

# -- Options for extensions
# sphinx.ext.todo
todo_include_todos = True
# atsphinx.mini18n
mini18n_default_language = "en"
mini18n_support_languages = ["en", "ja"]
mini18n_select_lang_label = "Languages"
mini18n_basepath = "/bulma/" if os.environ.get("GITHUB_PAGES") else "/"
