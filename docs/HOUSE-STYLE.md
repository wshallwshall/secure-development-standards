# House style for this documentation set

## TLDR/BLUF

The writing rules this repository holds its own pages to. Three are enforced by a test, one by a CI
gate, one by a link test. The rest are review items and say so.

**Every rule below states which it is.** A rule nothing can fire is a preference. Reading it as more
than that is how a review turns into an argument about taste.

**Where the authority sits.** For an enforced rule, the pattern in the test is what runs. This page
states the rule in words so a developer who trips one can read what it wants. If the two ever
disagree, the pattern is what stops the commit, and this page is the defect.

**This page is scanned like every other.** It is tracked markdown under `docs/`, so the prose checker
reads it. One narrow exemption exists so that it can quote what it bans, and that exemption is
described at the end rather than left for a reader to infer.

---

## What is enforced, and by what

The first column is what actually fires, because that is the thing a reader can go and run. Rule
identifiers are keyed to their definitions further down, one table per group.

| What fires | Rules | Result |
|---|---|---|
| [test_prose_rules_hold.py](https://github.com/wshallwshall/secure-development-standards/blob/main/tests/test_prose_rules_hold.py) | B-3, B-5, B-6 | hard fail |
| the ASCII gate in [gates.yml](https://github.com/wshallwshall/secure-development-standards/blob/main/.github/workflows/gates.yml) | HS-11 | hard fail |
| [test_a_links_text_never_wraps.py](https://github.com/wshallwshall/secure-development-standards/blob/main/tests/test_a_links_text_never_wraps.py) | HS-16 | hard fail |
| nothing directly. Both shape how the scanners read a page | HS-14, PD-4 | review |
| nothing. Each was measured against this corpus and rejected as a gate | B-7, B-10, HS-3 | review |

Two measured qualities are also ratcheted rather than capped: sentences over 30 words, and table
cells over 40 words. Neither may get worse than its recorded baseline. Neither is a limit you have to
write under, and the long tail of this corpus is where the engineering warnings live.

---

## The banned constructions

Each of these bans a SHAPE of sentence, not a subject. Each names a construction that carries no
information, and each says what to write in its place.

| Rule | Banned | Write instead | Enforced |
|---|---|---|---|
| `B-3` | an opener whose only work is to announce that what follows matters: "Importantly", "Notably", "It is worth noting that", "It should be noted that" | the note itself, with nothing announcing it | yes |
| `B-5` | padding that adds length without adding meaning: "in order to", "utilize" and "utilise" with all their inflections, "leveraging", "leveraged", "provides the capability to", "provides the ability to" | "to", "use", "can". The bare noun "leverage" is deliberately NOT banned: this corpus uses it correctly and often, as in "ordered by its own leverage" and "the highest-leverage gate", so only the participles and the unmistakable phrases are enforced | yes, narrowed |
| `B-6` | a sentence asserting its own significance: "this is important", and equally "significant" or "critical" in that frame, "the key point is", "the key thing here", "cannot be overstated", "worth emphasising" in either spelling | the fact that makes it significant, stated plainly and left to carry itself | yes |
| `B-7` | "cleanly", "elegantly", "robustly" describing this project's own work | the behaviour those words stand in for, in terms a reader can check | no, and see below |
| `B-10` | a heading written as a rhetorical question that the section then answers | a heading that states the answer | no, and see below |

---

## Rules about form

| Rule | The rule | Enforced |
|---|---|---|
| `HS-11` | prose is ASCII, absolutely. No smart quotes, no en dash, no non-breaking space. Write `--` where a dash is wanted. This is not a preference: pandoc renders a smart quote differently from the character an author meant, and the Word copies are compared against a rebuild | yes |
| `HS-14` | wrap prose near 100 characters | no |
| `HS-16` | a markdown link sits on ONE line, even where that pushes the line past HS-14's 100 characters. This is the stated exception to HS-14, and it is the only one | yes |
| `HS-3` | one fact lives in one place. A second copy is not redundancy, it is the place the two will silently disagree | no |

**Why HS-16 outranks HS-14.** The site is built by Jekyll, and `jekyll-relative-links` rewrites
relative links with a regular expression whose `.` excludes a newline. A link whose text wraps is
never rewritten. The raw `](FILE.md)` reaches the published HTML, and any `#fragment` on it addresses
nothing. There is no 404 for a reader to report, and github.com renders the same characters
correctly, which is the surface the change gets reviewed on.

---

## Rules about tables

| Rule | The rule | Enforced |
|---|---|---|
| `PD-4` | a table row is not prose. Do not convert a table to paragraphs to satisfy a length rule, and do not judge a cell against a sentence rule | no |

PD-4 is why the sentence-length measure excludes tables, headings and block quotes, and why the fat
cell count is kept as a separate number. A long cell and a long sentence are different problems. The
fix for one is not the fix for the other.

---

## What was measured and then rejected

Three rules are stated here and enforced by nobody. That is a decision with evidence behind it, not
an omission. The design rule for the whole set: hard-fail ONLY where a violation is unambiguous.

A gate that reddens a legitimate editorial choice is a gate people delete. Losing it also loses the
rules it was enforcing correctly, so the cost of a bad gate is not limited to the bad rule.

**B-7 is the instructive one.** Every candidate pattern was run over this corpus and every hit was
read. "cleanly" and its siblings fired 16 times, and not one was the self-praise the rule bans. The
hits were ordinary technical vocabulary: `git merges both cleanly`, `a session that exits cleanly`,
`an alias stub that resolves cleanly`. The rule turns on WHAT IS BEING DESCRIBED, which no pattern
over the text can see. Enforcing it would redden sixteen correct sentences to catch nothing.

**B-10 went the same way on its single hit.** That hit was `## The one question: does failing it stop
the change?`, which the section immediately answers. It is not the rhetorical opener the rule exists
for.

**HS-3 is rejected for a different reason.** Duplication across two files is detectable, but which of
the two copies should go is an editorial call. A test cannot make it. The duplication is reported and
left to a human.

---

## The rule sheet may quote what it bans

This page lists every banned construction verbatim, in tables. A naive scan would redden the one page
that defines the rules, so `test_prose_rules_hold.py` carries an exemption for a table row whose
first cell is a rule identifier. That row, and nothing more.

**What the exemption actually does, stated from measurement rather than from intent.** It does two
different jobs, and only one of them is the job its name suggests:

* **The fat-cell ratchet skips rule rows.** This is the exemption's live effect. A rule row here runs
  long, because it quotes several banned forms and their replacements. Without the exemption those
  rows would push the fat-cell count against its baseline, and this page would be paying a penalty
  for doing its job.
* **The banned-construction scan never sees ANY table row.** That protection comes from a wider rule
  and not from this exemption. The scanner rejoins prose into paragraphs before matching, and it
  drops every line beginning with a pipe while doing so. So a rule row is safe from it, and so is an
  ordinary row.

The second half is worth stating plainly because it is a coverage limit, not a feature: a banned
construction written inside an ordinary table cell is not caught anywhere. That is a known gap. It is
recorded here rather than closed, because closing it means scanning cells against sentence rules,
which is what PD-4 forbids.

Exempting the whole page was considered and rejected. It would leave the rule sheet as the only
unchecked prose in the repository, which is the wrong page to stop reading.

---

## Where these identifiers come from, and why they have gaps

The numbering is inherited. These documents were written alongside a toolkit repository and split out
of it, and the rule sheet stayed behind. What crossed the split was the enforcement: the tests, the
CI gate, and their citations.

**The identifiers are kept because they are cited.** They appear in CI comments, in test failure
messages, and in commit messages that are already written. Renumbering them would break every one of
those citations to buy a tidier sequence. This repository already recorded that judgment once, for
the `SD-<section>.<n>` identifiers in the secure development standard.

**The gaps are deliberate.** Only the rules this repository actually enforces or names are restated
here. The rules that did not come across are not reconstructed, because a rule sheet that invents its
own contents is worse than a short one. If a rule is missing and you need it, add it with the
evidence and give it the next free number in its series.

**This page is derived from the enforcement, not the other way round.** For B-3, B-5, B-6, HS-11 and
HS-16, the running check is the definition of record. The words here describe what those checks do.
