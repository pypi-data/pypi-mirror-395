"""This is root of package."""

from bs4 import BeautifulSoup
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.jinja2glue import BuiltinTemplateLoader

from atsphinx.helper.decorators import emit_only  # type: ignore[import-untyped]

__version__ = "0.3.0"


class WithHtmxTemplateLoader(BuiltinTemplateLoader):  # noqa: D101
    def render(self, template: str, context: dict) -> str:  # type: ignore[override]  # noqa: D102
        out = super().render(template, context)
        if not template.endswith(".html"):
            return out
        soup = BeautifulSoup(out, "lxml")
        # NOTE: Define as that it must convert only full-speced html (has head tag.)
        if not soup.head:
            return out
        preload = context.get("htmx_boost_preload", "")
        if preload:
            soup.body.attrs["hx-ext"] = "preload"  # type: ignore[union-attr]
        for a in soup.find_all("a", {"class": "internal"}):
            a["hx-boost"] = "true"
            a["preload"] = preload
        return str(soup)


@emit_only(formats=["html"])
def setup_custom_loader(app: Sphinx):
    """Inject extra values about htmx-boost into generated config."""
    app.config.template_bridge = "atsphinx.htmx_boost.WithHtmxTemplateLoader"  # type: ignore[attr-defined]
    app.builder.init()


def pass_extra_context(app: Sphinx, config: Config):  # noqa: D103
    config.html_js_files.append("https://unpkg.com/htmx.org@1.9.10")
    if app.config.htmx_boost_preload:
        config.html_js_files.append(
            "https://unpkg.com/htmx.org@1.9.10/dist/ext/preload.js"
        )
        config.html_context["htmx_boost_preload"] = app.config.htmx_boost_preload


def setup(app: Sphinx):
    """Load as Sphinx-extension."""
    app.connect("builder-inited", setup_custom_loader)
    app.connect("config-inited", pass_extra_context)
    app.add_config_value("htmx_boost_preload", "", "env", [str])
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
