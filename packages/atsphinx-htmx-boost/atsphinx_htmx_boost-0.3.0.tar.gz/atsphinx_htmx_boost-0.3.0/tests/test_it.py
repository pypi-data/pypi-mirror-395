"""Standard integration tests."""

import shutil
from io import StringIO
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html")
def test__it(app: SphinxTestApp, status: StringIO, warning: StringIO):
    """Test to pass."""
    app.build()


@pytest.mark.parametrize(
    "theme", ["alabaster", "haiku", "nonav", "furo", "sphinx_rtd_theme"]
)
def test__work_on_theme(
    sphinx_test_tempdir: Path, rootdir: Path, make_app: callable, theme: str
):
    testroot = "root"
    srcdir = sphinx_test_tempdir / testroot
    if not srcdir.exists():
        testroot_path = rootdir / f"test-{testroot}"
        shutil.copytree(testroot_path, srcdir)

    app: SphinxTestApp = make_app(
        "html", srcdir=srcdir, confoverrides={"html_theme": theme}
    )
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "html.parser")
    for a in soup.find_all("a"):
        if "internal" in a.attrs.get("class", []):
            assert "hx-boost" in a.attrs
        if "internal" not in a.attrs.get("class", []):
            assert "hx-boost" not in a.attrs


@pytest.mark.parametrize(
    "theme", ["alabaster", "haiku", "nonav", "furo", "sphinx_rtd_theme"]
)
def test__work_with_preload(
    sphinx_test_tempdir: Path, rootdir: Path, make_app: callable, theme: str
):
    testroot = "root"
    srcdir = sphinx_test_tempdir / testroot
    if not srcdir.exists():
        testroot_path = rootdir / f"test-{testroot}"
        shutil.copytree(testroot_path, srcdir)

    app: SphinxTestApp = make_app(
        "html",
        srcdir=srcdir,
        confoverrides={"html_theme": theme, "htmx_boost_preload": True},
    )
    app.build()
    soup = BeautifulSoup((app.outdir / "index.html").read_text(), "html.parser")
    scripts = [s["src"] for s in soup.find_all("script") if "src" in s.attrs]
    assert "https://unpkg.com/htmx.org@1.9.10/dist/ext/preload.js" in scripts
    for a in soup.find_all("a"):
        if "internal" in a.attrs.get("class", []):
            assert "hx-boost" in a.attrs
            assert "preload" in a.attrs
        if "internal" not in a.attrs.get("class", []):
            assert "hx-boost" not in a.attrs


@pytest.mark.sphinx("html", confoverrides={"html_use_opensearch": True})
def test__with_opensearch(app: SphinxTestApp, status: StringIO, warning: StringIO):
    app.build()


@pytest.mark.sphinx("html")
def test__inline_code(app: SphinxTestApp):
    app.build()
    html = (app.outdir / "index.html").read_text()
    assert "</span></code>" in html


@pytest.mark.sphinx("html", testroot="parallel", parallel=2)
def test__build_parallel(app: SphinxTestApp, status: StringIO, warning: StringIO):
    """Test to pass."""
    for idx in range(1, 10):
        shutil.copy(
            (app.srcdir / "sub-0.rst"),
            (app.srcdir / f"sub-{idx}.rst"),
        )
    app.build()
