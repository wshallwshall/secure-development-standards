# Security standards for teams building with AI coding assistants

## TLDR/BLUF

**What this is.** Standards you can adopt, fork, or hand to an auditor. Each ships as markdown and
as a Word file, written to be copied whole into your own repository and edited.

**Why it matters.** A control you claim has to be one you can show firing. Several of these
documents exist to make that difference visible.

**What it costs you.** Adoption is per document and each says its own price. Nothing here is a
product, a scanner, or a service, and nothing is sold.

**Not for you** if you want a certification, an attestation, a maturity score or a tool
recommendation. [What these are not](#what-these-are-not) says why none is offered.

**Where to start.** [Which security standards actually apply to you](standards/WHICH-STANDARDS-APPLY.md)
routes on your situation rather than on the documents. [The standards index](standards/OVERVIEW.md)
has one row each. [The CISO summary](standards/CISO-SUMMARY.md) is the argument in two pages.

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
| Selling software, and being asked for evidence | [What to have ready when a buyer asks](standards/DILIGENCE-PACKET.md) |
| Adopting any of it, in an order that works | [How to adopt these](standards/ADOPTING-THESE.md) |

---

## What these are not

**No certification, and no attestation.** None is offered and none is implied. These set a bar to
hold, not a badge to present, and no maturity score comes with them.

**No tool recommendation.** No scanner, format or assessor is recommended anywhere in the set.

**No legal force.** Whether any of this binds your organization is decided by a clause number and by
counsel, never by a web page. What these documents do is tell you which questions are real and what
a good answer looks like.

---

## What makes these different from a checklist

One claim runs through every document: **a control that reports success is indistinguishable from a
control that never ran**, so a claim is worth what its receipt is worth and nothing more. That is why:

* [secure development](standards/SECURE-DEVELOPMENT.md) carries permanent rule identifiers you can
  cite in your own deviations register
* every rule has an evidence column
* [automated compliance in CI](standards/CI-ENFORCEMENT.md) turns on one question -- does failing it
  actually stop the change

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

They were written alongside [claude-multisession](https://claude-multisession.pages.dev),
a toolkit for running several agent sessions against one repository, and that toolkit remains their
worked demonstration: it applies the same claim to concurrency, where every control fires on purpose
and prints what it examined. The documents outgrew it and now live here.

Everything is MIT licensed. Copy it, fork it, put your own name on it.
