"""The old address keeps serving, and every page it served forwards to the new one.

WHAT THIS EXISTS FOR. The site moved off github.io because that host is blocked on the readership's
network. Old URLs stay in circulation -- inside downloaded Word copies, in other repositories, in
bookmarks -- so the old address serves forwarding stubs rather than 404s.

THE FAILURE IT PREVENTS IS DRIFT, and it is silent in the direction that matters. Add a document to
docs/ and the real site grows a page. The forwarding site does not, unless someone regenerates it.
A reader on an old link then gets a 404 from a host that appears to be working, and nothing anywhere
reports it -- the new site is fine, the old site is fine, and the one path between them is missing.

So the stub set is DERIVED from the markdown tree rather than curated, and this pins that it is.
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import _ccxtest as t

GENERATOR = t.REPO_ROOT / "scripts" / "site" / "build_redirects.py"


def _load():
    spec = importlib.util.spec_from_file_location("build_redirects", GENERATOR)
    assert spec and spec.loader, f"cannot load {GENERATOR}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TheForwardingSiteCoversEveryPage(unittest.TestCase):
    def setUp(self):
        self.assertTrue(GENERATOR.exists(), f"{GENERATOR} is missing; the cutover has no mechanism")
        self.mod = _load()

    def test_every_served_page_gets_a_stub(self):
        """One stub per markdown document, derived rather than listed."""
        docs = t.REPO_ROOT / "docs"
        expected = {
            "index.html"
            if md.relative_to(docs).as_posix() == "index.md"
            else md.relative_to(docs).as_posix()[: -len(".md")] + ".html"
            for md in docs.rglob("*.md")
        }
        self.assertEqual(
            expected,
            set(self.mod.pages()),
            "the forwarding stub set does not match the documents the site serves. It is derived "
            "from the tree on purpose, so a mismatch here means the derivation broke -- not that a "
            "list needs updating.",
        )
        self.assertGreater(
            len(expected),
            10,
            f"only {len(expected)} pages found. A generator that walks an empty tree writes an "
            "empty forwarding site and exits 0, which is the shape of a cutover that quietly "
            "forwards nothing.",
        )

    def test_the_destination_is_read_from_the_site_config(self):
        """A typed-in destination is a second copy of an address expected to move again."""
        config = t.read(t.REPO_ROOT / "docs" / "_config.yml")
        self.assertIn(
            self.mod.site_url(),
            config,
            "the generator's destination does not appear in docs/_config.yml, so the two have "
            "drifted or the destination is hardcoded.",
        )

    def test_a_generated_stub_carries_the_destination_three_ways(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "site"
            import sys

            argv = sys.argv
            sys.argv = ["build_redirects.py", str(out)]
            try:
                self.assertEqual(0, self.mod.main())
            finally:
                sys.argv = argv

            dest = self.mod.site_url()
            page = out / "standards" / "CODE-QUALITY.html"
            self.assertTrue(page.exists(), "a known page produced no stub")
            html = page.read_text(encoding="utf-8")
            for form in (
                f'rel="canonical" href="{dest}/standards/CODE-QUALITY.html"',
                f'content="0; url={dest}/standards/CODE-QUALITY.html"',
                f'location.replace("{dest}/standards/CODE-QUALITY.html"',
            ):
                self.assertIn(form, html, f"the stub is missing this redirect route: {form}")

            self.assertTrue((out / ".nojekyll").exists(), ".nojekyll is what stops Jekyll eating it")

            # A reader with a deep link must land on the section, not the page top. The meta
            # refresh cannot do that, which is why the script carries hash and query.
            self.assertIn("location.hash", html)
            self.assertIn("location.search", html)

    def test_it_refuses_rather_than_guessing_a_destination(self):
        """A generator that defaults on a missing url writes a site forwarding everywhere to nothing.

        That failure is invisible from the outside: every stub renders, every link is clickable, and
        every one of them is wrong.
        """
        original = self.mod.CONFIG
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "_config.yml"
            empty.write_text("title: no url here\n", encoding="utf-8")
            self.mod.CONFIG = empty
            try:
                with self.assertRaises(SystemExit):
                    self.mod.site_url()
            finally:
                self.mod.CONFIG = original

        # And the positive control, so the case above cannot pass by raising for the wrong reason.
        self.assertTrue(self.mod.site_url().startswith("https://"))


if __name__ == "__main__":
    unittest.main()
