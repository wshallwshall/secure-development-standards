"""Generate the forwarding site that replaces the old GitHub Pages content.

WHO THIS SERVES, AND WHO IT CANNOT. Read this before describing it as a mitigation, because the two
audiences are easy to confuse and only one of them is helped.

These stubs are hosted ON GITHUB PAGES. The reader this whole move was made for -- the one whose
network blocks GitHub -- CANNOT LOAD THEM. For that reader an old link fails exactly as it did
before: no redirect, no explanation, and not even the page that would have told them where the site
went. This forwarder is worth building for everyone else holding an old URL, and it is not a fix for
the blocked reader. Nothing hosted on the blocked host can be.

What does reach the blocked reader is the new site itself, which serves the markdown sources and the
Word copies beside the rendered pages on its own origin. That is where a "take a copy" link has to
point; a raw.githubusercontent URL is unreachable for exactly the audience most likely to want it.

WHY THIS EXISTS AS A GENERATOR AND NOT AS COMMITTED HTML. Old URLs are in circulation -- in Word
copies people have downloaded, in other repositories, in anything anyone bookmarked -- and a bare 404
tells that reader nothing. So the old address keeps serving, and every page forwards to its
counterpart.

The destination host is read from docs/_config.yml rather than typed here, for the same reason
tests/test_internal_links_resolve.py reads it: a second copy of an address is the place the two
silently disagree, and this address is expected to move again if *.pages.dev is blocked too.

THE PAGE LIST IS DERIVED FROM THE TREE, never curated. A curated list is complete on the day it is
written; a document added later would have no stub and its old URL would 404 with nothing saying so.

USAGE. This writes a directory; it publishes nothing and changes no setting.

    python scripts/site/build_redirects.py _redirects_site

Then push that directory as the root of the `gh-pages` branch and point GitHub Pages at it. Until
that setting changes, running this is inert.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS = REPO_ROOT / "docs"
CONFIG = DOCS / "_config.yml"


def site_url() -> str:
    """The destination host, out of docs/_config.yml.

    Raises rather than defaulting. A wrong or empty value here generates a site that forwards
    everything to nowhere, which looks exactly like a working forwarding site until someone clicks.
    """
    text = CONFIG.read_text(encoding="utf-8")
    m = re.search(r"^url:[ \t]*(.*?)[ \t]*$", text, re.M)
    if m is None:
        raise SystemExit(f"{CONFIG} has no top-level `url:`; refusing to guess the destination.")
    url = m.group(1).strip().strip('"').strip("'").rstrip("/")
    if not url.startswith("https://"):
        raise SystemExit(f"`url:` in {CONFIG} is {url!r}, which is not an https destination.")
    return url


def pages() -> list[str]:
    """Every served page path, derived from the markdown that builds the real site.

    docs/ is the Jekyll source root and no permalink style is configured, so docs/a/b.md is served
    at /a/b.html, and docs/index.md is served at /.
    """
    out = []
    for md in sorted(DOCS.rglob("*.md")):
        rel = md.relative_to(DOCS).as_posix()
        out.append("index.html" if rel == "index.md" else rel[: -len(".md")] + ".html")
    if not out:
        raise SystemExit(f"no markdown found under {DOCS}; refusing to write an empty stub set.")
    return out


STUB = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved -- {title}</title>
<link rel="canonical" href="{dest}">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={dest}">
<script>
// Runs ahead of the meta refresh and keeps any #fragment and query, which the refresh alone drops.
// A reader following a deep link into a section lands on that section rather than the page top.
// The meta refresh remains the fallback for anyone with scripting disabled.
location.replace({dest_js} + location.hash + location.search);
</script>
</head>
<body>
<h1>This page has moved</h1>
<p>These documents are no longer served from github.io, which is blocked on some corporate
networks. The new address is:</p>
<p><a href="{dest}">{dest}</a></p>
<p>If you are not redirected automatically, follow the link above.</p>
</body>
</html>
"""


def stub(dest: str, title: str) -> str:
    """One forwarding page. `dest` is trusted repository configuration, not reader input.

    It is still escaped for the attribute contexts and JSON-quoted for the script context, because
    "the input is trusted" is a claim about today and the escaping costs nothing.
    """
    return STUB.format(
        dest=html.escape(dest, quote=True),
        dest_js=json.dumps(dest),
        title=html.escape(title),
    )


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    out = Path(sys.argv[1])
    dest_root = site_url()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # Tells GitHub Pages not to run Jekyll over this tree. Without it a path beginning with an
    # underscore would be dropped silently, which is a class of missing page nothing would report.
    (out / ".nojekyll").write_text("", encoding="utf-8")

    written = 0
    for page in pages():
        dest = f"{dest_root}/{page}" if page != "index.html" else f"{dest_root}/"
        target = out / page
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(stub(dest, page), encoding="utf-8")
        print(f"  {page:<48} -> {dest}")
        written += 1

    # THE CATCH-ALL, and it covers more old URLs than the enumerated stubs do.
    #
    # GitHub Pages serves 404.html for any path it does not recognise, so this single file answers
    # the entire long tail: renamed pages, deep links, anything anyone ever typed wrong. Without it
    # an unknown old address got GitHub's generic "Page not found" with no mention that the site
    # moved -- measured on the live forwarder before this existed.
    #
    # IT POINTS AT THE NEW SITE'S 404, NOT THE ROOT. Sending an unknown address to a home page that
    # returns 200 tells the reader the page exists. It does not. The destination has to be a page
    # that says so.
    catch_all = f"{dest_root}/404.html"
    (out / "404.html").write_text(stub(catch_all, "404.html"), encoding="utf-8")
    print(f"  {'404.html (catch-all)':<48} -> {catch_all}")
    written += 1

    print(f"\nwrote {written} forwarding pages into {out}")
    print(f"destination host read from {CONFIG.relative_to(REPO_ROOT).as_posix()}: {dest_root}")
    print("\nThis published nothing and changed no setting. To cut over:")
    print(f"  push the contents of {out} as the root of the gh-pages branch")
    print("  then set GitHub Pages source to gh-pages / (root)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
