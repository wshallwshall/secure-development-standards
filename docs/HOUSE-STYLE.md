# House style

These are the writing rules for this repository's prose. `tests/test_prose_rules_hold.py` enforces
the subset that can be matched without judgment, and names the subset it cannot. Everything else on
this page is a review item. A rule no pattern can see is still a rule. It is just not a gate.

**Every rule here was measured against the corpus before it was written.** The counts are in *What
the corpus measured*. That order is deliberate, and it is the whole design. A hard-fail rule whose
corpus is already red ships disabled. A rule that reddens correct prose is one people delete.

## The three states a rule can be in

| State | What it means | Where it lives |
| --- | --- | --- |
| **Enforced** | A pattern matches it, and the corpus is at zero | `test_prose_rules_hold.py`, hard fail |
| **Reported** | Measurable, but the right count is not zero | Same file, ratcheted against a baseline |
| **Review** | No pattern can decide it | This page only |

A rule moves from Review to Enforced by measurement, never by assertion. Run the candidate over the
corpus, read every hit, and enforce only if the hits are all genuine violations and there are none
left. The rules below record what that measurement found, including for the ones it rejected.

## Enforced: constructions

Each of these fires zero times on the corpus as committed. Examples sit in rule rows and fenced
blocks, the two things the scanner skips, so this page can name what it bans.

| Rule | Do not write | Write instead |
| --- | --- | --- |
| `B-3` | "Importantly", "Notably", "It is worth noting", "It should be noted" | The note itself |
| `B-5` | "in order to", "utilize", "leveraging", "provides the capability to" | "to", "use", "can" |
| `B-6` | "this is important", "the key point is", "cannot be overstated" | The fact that makes it so |
| `B-11` | "delve", "intricate", "meticulously", "garner", "showcase", "groundbreaking" | Plain equivalents |
| `B-12` | "tapestry", "camaraderie", "solace", "palpable", "fleeting", "amidst", "unravel" | Plain equivalents |
| `B-13` | "truly", "vastly", "incredibly", "remarkably", "profoundly", "undoubtedly" | Nothing, or a number |

`B-11` is the measured marker set. Every word in it carries a published post-2022 frequency rise in
academic prose, and every one of them is absent here. `B-12` is the ornamental register the same
research found. Those words belong in fiction, and a security standard is not fiction.

`B-11` bans "underscore" only as a verb. The character keeps its name, because a filename rule may
need it. The enforced form requires a following determiner, which separates the two cases:

```text
underscores the risk          caught, the verb
underscores in the filename   allowed, the character
```

`B-13` deliberately omits **"genuinely"**. See *What review has to catch* for the measurement.

## Enforced: mechanics

| Rule | Requirement |
| --- | --- |
| `HS-16` | A line may pass HS-14's width when reflowing it would wrap a relative link |
| `HS-17` | ASCII punctuation only. Write ` -- ` for a parenthetical break, `"` for quotes |

`HS-17` is the best-evidenced marker on this page and the cheapest to keep. The corpus holds 1,175
double-hyphens and zero em-dashes, zero en-dashes, zero curly quotes and zero ellipsis characters.
The rule costs nothing because the house already writes this way, and that is the only reason it is
a hard fail rather than a ratchet. The reasoning is narrower than the rule looks: see *What the
evidence does not support*.

## Conventions, not gates

| Rule | Requirement | Why it is not enforced |
| --- | --- | --- |
| `HS-3` | Do not carry the same passage in two files | Which copy should go is an editorial call |
| `HS-14` | Wrap prose near 100 characters | `HS-16` is a standing exception |
| `PD-4` | A table row is not a sentence | Shortening one is not an improvement |

`PD-4` exists to block a specific bad fix. When a length measure reports a fat table cell, converting
the table to prose satisfies the number and harms the reader. The cell count is reported for that
reason and never hard-failed.

## What review has to catch, because no pattern can

This is the half that matters most, and the half a linter will quietly convince you it has covered.

| Rule | What to look for | Why no pattern can decide it |
| --- | --- | --- |
| `B-7` | "cleanly", "elegantly", "robustly" praising this project's own work | Turns on what is described |
| `B-10` | A heading that is a rhetorical question | A question the text answers is fine |
| `B-14` | "not just X but Y", and the three-part list used for rhythm | Both are ordinary prose here |
| `B-15` | "genuinely", "actually", "simply" used as filler | All are load-bearing in this corpus |
| `B-16` | Noun-heavy phrasing and stacked participial clauses | Needs a parser, not a regex |
| `PD-5` | Filler sections, redundant closing summaries, boilerplate | No test knows what a page needed |
| `HS-18` | Never treat a lint hit as evidence of who wrote a page | Detectors cannot support that claim |

`B-7` and `B-10` were measured and rejected, and they are the instructive pair. "cleanly" fires 16
times and not one is self-praise: `git merges both cleanly`, `a session that exits cleanly`, `a
transform producing valid-but-wrong output passes cleanly`. The rule turns on **what is being
described**, and no pattern over the text can see that. `B-10` went the same way on its single hit.

`B-15` is the same shape, found the same way. "genuinely" appears 11 times and every one is doing
real work. Each separates a real thing from an apparent one: `a package that genuinely exists`, `a
run that genuinely processed 461 mutants`, `genuinely contested cells`. Banning it would redden
eleven correct sentences to catch nothing.

`B-14` failed on both tests a rule has to pass. Its one corpus hit is correct prose, and no measured
source for it survived verification. It stays here as a thing to notice, labelled as opinion.

`B-16` is not a judgment call. It is a tooling limit. The measured features are nominalization
density and present participial clauses, counted with a parser against a published human baseline. A
regex cannot see either. A rough suffix count puts this corpus at 34.8 nominalizations per 1,000
words, which is a proxy and not the published measure.

`HS-18` is a process rule and the one with the sharpest evidence behind it. A flagged phrase is a
prompt to a human reader. It is never a finding about authorship, and this page must not be cited to
support one.

## What the corpus measured

Measured on 2026-08-08 over 17 tracked files: 89,123 words whole-file, 54,422 words of prose
paragraphs. Every candidate was run and every hit was read before the rule above was chosen.

| Candidate | Hits | Genuine | Outcome |
| --- | --- | --- | --- |
| em-dash, en-dash, curly quotes, ellipsis | 0 | -- | `HS-17`, enforced |
| delve, intricate, meticulously, garner, showcase, groundbreaking | 0 | -- | `B-11`, enforced |
| underscore, any form | 0 | -- | `B-11`, enforced narrowed to the verb |
| tapestry, camaraderie, solace, palpable, fleeting, amidst, unravel | 0 | -- | `B-12`, enforced |
| truly, vastly, incredibly, remarkably, profoundly, undoubtedly | 0 | -- | `B-13`, enforced |
| genuinely | 11 | 0 | `B-15`, review only |
| "not just X but Y" | 1 | 0 | `B-14`, review only |
| cleanly, elegantly, robustly | 16 | 0 | `B-7`, review only |
| a heading that is a question | 1 | 0 | `B-10`, review only |

The pattern in that table is the argument of this page. Every rule with an outside evidence base
scores zero here, and every rule that fires scores zero genuine violations.

## Writing with an assistant

Claude Opus 5 runs longer than earlier Opus models by default, on Anthropic's own account, and files
it writes to disk run longer still. The `effort` parameter does not fix this. Anthropic documents
that effort controls how much the model thinks rather than how much it says, so length has to be
asked for directly.

Ask for length explicitly, and prefer showing the style you want over listing what to avoid.
Anthropic's guidance for this model is that positive examples work better than prohibitions. The
measured evidence agrees that a style instruction alone is weak. Models given a human sample, and
told to match its style, still produced the same noun-heavy prose.

The practical split follows from that. Steer generation with a positive exemplar, and keep the banned
list where it works, in a check that runs after the text exists.

```text
Match the length of written documents to what the task needs: cover the substance,
but do not pad with filler sections, redundant summaries, or boilerplate.
```

Revise rather than regenerate. A regenerated draft resets every judgment already made about it. This
page's own history is the argument: the rules that survived are the ones a human read the hits for.

## Where the evidence comes from

| Source | What it establishes |
| --- | --- |
| Kobak et al., *Science Advances* 11(27):eadt3813 | The LLM signal is style, not subject matter |
| Reinhart et al., *PNAS* 122:e2422455122 | Grammatical habits, with human baselines |
| Czuma, arXiv 2606.29540 | Em-dash rise, pre-registered, with falsification tests |
| Liang et al., *Patterns* 4:100779 | Detectors misfire on non-native writers |
| Anthropic, prompting guide for Claude Opus 5 | Length behaviour, and exemplars over prohibitions |

### What the evidence does not support

Four limits, recorded because a rule sheet that cites research should also cite what the research
refuses to say.

**No study here measured a Claude model.** Every frequency figure comes from GPT-4o, Llama 3, or
2024-era corpora. Applying them to Opus 5 is an argument from mechanism, not a measurement. The one
Opus 5 source is Anthropic's own documentation, which covers length and says nothing about any word.

**No marker decides anything about one document.** The em-dash source says so in terms: the mark
"decides nothing about any single manuscript". Its own pre-LLM baseline is about 4%, so the honest
reading of a single em-dash is that a person wrote a dash. `HS-17` is a consistency rule for a corpus
that already had zero. It is not a detector, and it must never be read as one.

**Word lists have low recall.** The most inflated word in the largest study still appears in under 5%
of post-2022 abstracts. Every rule in `B-11` and `B-12` will miss far more than it catches. They are
cheap and worth keeping, and they are not coverage.

**Detectors are unreliable, and unreliable unevenly.** Seven tools misclassified 61% of essays by
non-native English writers as machine-written, against near-perfect accuracy on native writers. That
figure is from 2023 and a 2026 re-run puts a modern tool at 23%, so the number has moved and the
finding has not. Those authors recommend against evaluative use outright, which is what `HS-18`
records.

One claim was checked and failed: there is no verified evidence that prompt-level bans suppress these
markers in Claude. Assertions that a prose-only instruction removes them did not survive
verification. Treat generation-time suppression as unproven, which is why every enforced rule on this
page runs after the text exists.

## Identifier policy

A rule identifier is a permanent name, not a position. It is the same promise `SECURE-DEVELOPMENT.md`
makes for its own scheme, for the same reason: a citation that silently repoints is worse than one
that breaks.

Numbers not listed on this page are **unassigned**. Do not fill the gaps. A retired rule keeps its
number and gains a note saying what replaced it, and a new rule takes the next free number in its
series. The series are `B-` for constructions, `HS-` for mechanics, and `PD-` for page design.
