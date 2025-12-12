from atsphinx import mini18n
from atsphinx.htmx_boost import __version__

# -- Project information
project = "atsphinx-htmx-boost"
copyright = "2024, Kazuya Takei"
author = "Kazuya Takei"
release = __version__

# -- General configuration
extensions = [
    "atsphinx.goto_top",
    "atsphinx.htmx_boost",
    "atsphinx.mini18n",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
]
templates_path = ["_templates", mini18n.get_template_dir()]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for i18n
gettext_compact = False
language = "en"
locale_dirs = ["_locales"]

# -- Options for HTML output
html_theme = "furo"
html_title = f"{project} v{release}"
html_static_path = ["_static"]
html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "mini18n/snippets/select-lang.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ]
}

# -- Options for extensions
# For sphinx.ext.intersphinx
intersphinx_mapping = {
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}
# For atsphinx.goto_top
goto_top_design = "image"
# For atsphinx.htmx_boost
htmx_boost_preload = "mouseover"
# For atsphinx.mini18n,
mini18n_default_language = "en"
mini18n_support_languages = ["en", "ja"]
mini18n_basepath = "/htmx-boost/"


def setup(app):
    app.add_object_type(
        "confval",
        "confval",
        objname="configuration value",
        indextemplate="pair: %s; configuration value",
    )
