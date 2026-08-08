# secure-development-standards

Security standards for teams building with AI coding assistants. Written to be copied whole into your
own repository and edited, which is why each one ships as markdown and as a Word file.

**Read them on the site:**
<https://wshallwshall.github.io/secure-development-standards/>

## TLDR/BLUF

Standards you can adopt, fork, or hand to an auditor. They cover what to require of a team writing
code with an AI assistant, how deeply a human has to read what it produces, what to do about
dependencies you did not write, which rules a pipeline can actually enforce, and what to ask a vendor
before you buy.

**Not for you** if you want a certification, a maturity score, or a tool recommendation. None is
offered and none is implied: these set a bar to hold, not a badge to present. No scanner, format or
assessor is named anywhere in the set.

**Start at** [which security standards actually apply to you](docs/standards/WHICH-STANDARDS-APPLY.md),
which routes on your situation rather than on the documents. If you already know what you want,
[the standards index](docs/standards/OVERVIEW.md) has one row each and links every file in both
formats. For an executive, [the CISO summary](docs/standards/CISO-SUMMARY.md) is the argument in two
pages.

## The claim these share

**A control that reports success is indistinguishable from a control that never ran.** So a claim is
worth what its receipt is worth and nothing more. That is why
[secure development](docs/standards/SECURE-DEVELOPMENT.md) carries permanent `SD-` rule identifiers
you can cite in your own deviations register, why every rule has an evidence column, and why
[automated compliance in CI](docs/standards/CI-ENFORCEMENT.md) turns on one question: does failing it
actually stop the change.

The set also publishes what did not survive checking. Widely repeated figures about machine-written
code are named in [code quality](docs/standards/CODE-QUALITY.md) as claims to stop repeating, beside
the ones that held.

## What runs here

This repository applies its own rules to itself, which is the only reason to believe them.

| Gate | What it proves |
|---|---|
| `tests/` | Rule identifiers are stable across history, every internal link and anchor resolves, the Word copies are rebuilt and compared rather than assumed current, and the writing rules that can be enforced are |
| ASCII gate | No non-ASCII byte reaches a document, because pandoc renders a smart quote differently from the character an author meant |
| pandoc, pinned by digest | The Word copies were produced by one converter. An unpinned one would redden every document at once on a commit that changed nothing |

Run them:

```bash
cd tests && python -m unittest discover -s . -q
```

Tests run **from inside `tests/`**. A root-level run finds nothing and exits without testing.

Editing any document under `docs/standards/` means rebuilding its Word copy in the same commit, on
pandoc 3.10. The recipe is in the docstring of `tests/test_word_copies_track_the_markdown.py`, which
parses its own block so it cannot drift from what the tests build with.

## Where these came from

Written alongside [claude-multisession](https://github.com/wshallwshall/claude-multisession), a
toolkit for running several agent sessions against one repository, which remains their worked
demonstration: it applies the same claim to concurrency, where every control fires on purpose and
prints what it examined. The documents outgrew it and now live here.

MIT licensed. Copy it, fork it, put your own name on it.
