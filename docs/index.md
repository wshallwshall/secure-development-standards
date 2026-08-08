# Security standards for teams building with AI coding assistants

## TLDR/BLUF

Standards you can adopt, fork, or hand to an auditor. Every one is written to be copied whole into
your own repository and edited, which is why each ships as markdown and as a Word file. They cover
what to require of a team writing code with an AI assistant, how deeply a human has to read what it
produces, what to do about dependencies you did not write, and what to ask a vendor before you buy.

**What it costs you.** Adoption is per document and each says its own price. Nothing here is a
product, a scanner, or a service, and nothing is sold. The expensive part is not reading these -- it
is that a control you claim has to be one you can show firing, and several of these documents exist
to make that difference visible.

**Not for you** if you want a certification, a compliance attestation, or a maturity score. None is
offered and none is implied: these set a bar to hold, not a badge to present. Also not for you if you
want a tool recommendation, because no scanner, format or assessor is named anywhere in the set.

**The honest limit, before you spend time here.** Whether any of this binds your organization is
decided by a clause number and by counsel, never by a web page. What these documents can do is tell
you which questions are real and what a good answer looks like.

**Start at** [which security standards actually apply to you](standards/WHICH-STANDARDS-APPLY.md),
which routes on your situation rather than on the documents. If you already know what you are looking
for, [the standards index](standards/OVERVIEW.md) has one row each. If you have ten minutes and an
executive to brief, [the CISO summary](standards/CISO-SUMMARY.md) is the whole argument in two pages.

---

## Where each reader goes

| You are | Start at |
|---|---|
| Deciding whether any of this reaches you | [Which security standards actually apply to you](standards/WHICH-STANDARDS-APPLY.md) |
| Briefing an executive, or asking for funding | [The CISO summary](standards/CISO-SUMMARY.md) |
| Writing or forking your own standard | [Secure development](standards/SECURE-DEVELOPMENT.md), the model, with stable rule identifiers |
| Deciding how much AI-written code a human reads | [Human review of code](standards/REVIEW-DEPTH.md) |
| Setting expectations for AI-assisted work | [AI-assisted development](standards/AI-ASSISTED-DEVELOPMENT.md) |
| Judging whether a body of code is any good | [Code quality](standards/CODE-QUALITY.md) |
| Managing code you did not write | [Dependency and artifact integrity](standards/DEPENDENCY-INTEGRITY.md) |
| Working out which rules a pipeline can enforce | [Automated compliance in CI](standards/CI-ENFORCEMENT.md) |
| Buying software, and asking for evidence | [What to ask a software vendor for](standards/DILIGENCE-PACKET.md) |
| Adopting any of it, in an order that works | [How to adopt these](standards/ADOPTING-THESE.md) |

---

## What makes these different from a checklist

One claim runs through every document: **a control that reports success is indistinguishable from a
control that never ran**, so a claim is worth what its receipt is worth and nothing more. That is why
[secure development](standards/SECURE-DEVELOPMENT.md) carries permanent rule identifiers you can cite
in your own deviations register, why every rule has an evidence column, and why
[automated compliance in CI](standards/CI-ENFORCEMENT.md) turns on one question -- does failing it
actually stop the change.

The set also publishes what did not survive checking. Widely repeated figures about machine-written
code are named in [code quality](standards/CODE-QUALITY.md) as claims to stop repeating, next to the
ones that held. A document that only published its wins would be asking for trust it had not earned.

---

## Running an assessment, and the pipeline it runs in

Two method documents sit beside the standards rather than inside them.
[Running a large security-standard assessment with AI agents](ASVS-ASSESSMENT.md) is what was learned
scoring several hundred requirements with agent sessions, and it is candid that the obvious way to
split that work is the wrong one. [CI and standards for agent-written code](CI-AND-STANDARDS.md)
covers getting parallel work through a pipeline without believing things that are not true.

---

## Where these came from

They were written alongside [claude-multisession](https://github.com/wshallwshall/claude-multisession),
a toolkit for running several agent sessions against one repository, and that toolkit remains their
worked demonstration: it applies the same claim to concurrency, where every control fires on purpose
and prints what it examined. The documents outgrew it and now live here.

Everything is MIT licensed. Copy it, fork it, put your own name on it.
