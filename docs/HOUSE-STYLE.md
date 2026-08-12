# House style for this documentation set

## TLDR/BLUF

**What this is.** The writing rules this repository holds its own pages to. Seven are enforced by
tests, one by a CI gate, and one is half-covered by tests written for other purposes. The rest are
review items or recorded, and every row says which. The table below is what fires; this sentence
summarises it and loses to it.

**Why it matters.** Every rule below states which it is. A rule nothing can fire is a preference,
and reading it as more than that is how a review turns into an argument about taste.

**Not for you** as evidence about who wrote a page. HS-18 forbids citing any rule here to support a
claim about authorship, and the measurement behind that rule is the strongest on this page.

**Where to start.** [What is enforced, and by what](#what-is-enforced-and-by-what), which is keyed
on what actually fires rather than on a rule identifier.

---

## Where the authority sits

For an enforced rule, the pattern in the test is what runs. This page states the rule in words so a
developer who trips one can read what it wants. If the two ever disagree, the pattern is what stops
the commit, and this page is the defect.

**This page is scanned like every other.** It is tracked markdown under `docs/`, so the prose checker
reads it. One narrow exemption exists so that it can quote what it bans, and that exemption is
described at the end rather than left for a reader to infer.

---

## What is enforced, and by what

The first column is what actually fires, because that is the thing a reader can go and run. Rule
identifiers are keyed to their definitions further down, one table per group.

| What fires | Rules | Result |
|---|---|---|
| [test_prose_rules_hold.py](https://github.com/wshallwshall/secure-development-standards/blob/main/tests/test_prose_rules_hold.py) | B-3, B-5, B-6, HS-20 | hard fail |
| the ASCII gate in [gates.yml](https://github.com/wshallwshall/secure-development-standards/blob/main/.github/workflows/gates.yml) | HS-11 | hard fail |
| [test_a_links_text_never_wraps.py](https://github.com/wshallwshall/secure-development-standards/blob/main/tests/test_a_links_text_never_wraps.py) | HS-16 | hard fail |
| [test_docs_do_not_drift.py](https://github.com/wshallwshall/secure-development-standards/blob/main/tests/test_docs_do_not_drift.py) | PD-10 | hard fail |
| [test_prose_rules_hold.py](https://github.com/wshallwshall/secure-development-standards/blob/main/tests/test_prose_rules_hold.py), for the census only | PD-12 | hard fail |
| [test_rule_ids_are_stable.py](https://github.com/wshallwshall/secure-development-standards/blob/main/tests/test_rule_ids_are_stable.py) and [test_the_selector_matches_the_routing_table.py](https://github.com/wshallwshall/secure-development-standards/blob/main/tests/test_the_selector_matches_the_routing_table.py), for two of the four sections it names | PD-8 | hard fail, on those two |
| nothing directly. Both shape how the scanners read a page | HS-14, PD-4 | review |
| nothing. Each was measured against this corpus and rejected as a gate | B-7, B-10, HS-3, HS-19, PD-11 | review |
| nothing. Each names a defect a reviewer can see and no pattern can | HS-18, PD-9 | review |
| nothing, and no review item either. Each was measured against this model's own prose and found nothing to catch | B-11, B-12, B-13, B-14, B-15, B-16 | recorded |
| nothing, and no review item either. Measured against this corpus rather than that one, with the same result | B-17 | recorded |

A third result appears in that table. **Recorded** means the rule was measured and then dropped as
both a gate and a review item, and its identifier is spent so nobody reissues it. The evidence sits
in the section that records what was rejected.

**The Result column says what happens when a rule fires, never how wide the rule is.** PD-12 is the
case that settles it: its gate hard-fails, and it covers exactly one count on this page. It is a
`hard fail` row and it counts toward the census, because a reader asking "what stops my commit"
wants the first fact. Scope belongs in the rule's own text, and PD-12's says "at one point".

Read the other way, PD-12 would join PD-8 as half-covered and the census would read six. That is
defensible and it is not what this page does. The next narrowly scoped gate lands on the same fork,
which is why the answer is written here rather than left to be re-derived from the numbers.

Two measured qualities are also ratcheted rather than capped: sentences over 30 words, and table
cells over 40 words. Neither may get worse than its recorded baseline. Neither is a limit you have to
write under, and the long tail of this corpus is where the engineering warnings live.

**The sentence baseline fell by 109 and no sentence was edited.** Both moves were defects in the
instrument rather than improvements to the writing. 137 of the 371 it started at were miscounted,
and correcting them removed 109 -- the two differ because splitting a rejoined list still leaves
some of its items long. The current figure is the one the test holds, not one restated here.

The first was the rejoin. The checker joins wrapped lines before measuring, and it used to join a
bullet list too, so a run of items measured as one enormous sentence. 60 of the 371 were that. The
largest read as 156 words and is five links, each on its own line, each short.

The second was emphasis. A stop inside bold is still a stop, and the split could not see one, so
`**Rule.** Pick the source` measured as a single sentence rather than two. This set writes that way
587 times. 77 of the remaining 339 were that.

Neither is a curiosity, because of which fix each punished. Pulling a series into bullets is the
ordinary remedy for length, and under the first defect it changed the count by nothing. Splitting a
claim off as its own lede is the ordinary remedy for a fused sentence, and under the second it made
the number worse. A measure that reddens the fix it exists to ask for is worse than no measure.

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

**What a corpus of this model's own prose says about B-3.** The openers in B-3's row run at 0.05 per
1,000 words across 6.98 million words of assistant chat. In 1.6 million words of markdown the model
wrote to disk they run at 0.01 per 1,000, which is nine hits. The construction barely reaches a
written file, which is why B-3 is cheap to enforce.

It also says the risk is text pasted in from a chat window rather than text composed in one. Read
that as a statement about where to look, never about who wrote a page.

---

## Rules about form

| Rule | The rule | Enforced |
|---|---|---|
| `HS-11` | prose is ASCII, absolutely. No smart quotes, no en dash, no non-breaking space. Write `--` where a dash is wanted. This is not a preference: pandoc renders a smart quote differently from the character an author meant, and the Word copies are compared against a rebuild | yes |
| `HS-14` | wrap prose near 100 characters | no |
| `HS-16` | a markdown link sits on ONE line, even where that pushes the line past HS-14's 100 characters. This is the stated exception to HS-14, and it is the only one | yes |
| `HS-3` | one fact lives in one place. A second copy is not redundancy, it is the place the two will silently disagree | no |
| `HS-18` | a lint hit is a prompt to a human reader, never evidence of who wrote a page. No rule on this page may be cited to support a claim about authorship | no |
| `HS-20` | no sentence runs past 300 characters AS A READER SEES IT. A link's target does not count, because nobody reads it. This is a cap and not a ratchet, and it is the only length rule here that hard-fails | yes |
| `HS-19` | where a sentence has an actor, put the actor at the front. The case this rule is about is a passive that names its own actor in a trailing "by" phrase, because that one can always be turned round. A passive with no actor to name is not a violation and is often the accurate form | no, and see below |

**Why HS-20 caps where every other length measure here ratchets.** The 30-word figure is ratcheted
because the long tail of this corpus is where the engineering warnings live. 300 rendered characters
is roughly twice that, and it stopped being about pace. At the site's 66-character measure it is a
paragraph-shaped block presented as one sentence, and a reader tracking back to the next line lost
the subject four lines ago.

**The measure ignores a link's target, and that distinction is the whole rule.** 24 sentences
exceeded 300 characters of markdown. Only 9 exceeded it as rendered. The other 15 are ordinary
sentences of thirty-odd words carrying two hundred characters of URL. Failing those would ask an
author to shorten prose that is already short, or to drop a citation.

All nine real ones were rewritten rather than split: each was a list wearing semicolons, a citation
swallowed into the claim it supports, or a subject carrying six items.

**Why HS-16 outranks HS-14.** The site is built by Jekyll, and `jekyll-relative-links` rewrites
relative links with a regular expression whose `.` excludes a newline. A link whose text wraps is
never rewritten. The raw `](FILE.md)` reaches the published HTML, and any `#fragment` on it addresses
nothing. There is no 404 for a reader to report, and github.com renders the same characters
correctly, which is the surface the change gets reviewed on.

**What the measurement adds to HS-11, and what it does not.** The reason stays the rendering one
above. The numbers only say the gate is cheap and still has work to do. This corpus holds 1,175
double hyphens and no em dash at all, and 253 distinct prose blobs across this repository's history
carry zero non-ASCII bytes. Against that, the em dash runs at 12.51 per 1,000 words in 1.6 million
words of markdown this model wrote to disk.

So the gate costs the house nothing and still catches pasted-in text. It is not a detector, and
HS-18 forbids reading it as one.

**Why HS-18 is a rule and not a footnote.** The evidence for it is the strongest on this page, and
it cuts against the page itself. The control corpus behind every ratio measured here turned out to
be 94% prompts written by another instance of the same model. Cleaning the control did not rescue
it. The turns a person actually typed are terse instructions rather than prose, so the comparison
never had a matched register to begin with.

Published detector work fails the same way. Seven tools once flagged 61% of essays by non-native
English writers as machine-written, and a 2026 re-run of a modern tool still reports 23%. A pattern
on this page can tell a writer that a sentence is padded. It can never tell a reader who typed it.

---

## Rules about tables

| Rule | The rule | Enforced |
|---|---|---|
| `PD-4` | a table row is not prose. Do not convert a table to paragraphs to satisfy a length rule, and do not judge a cell against a sentence rule | no |
| `PD-11` | where the motive is length, extract a series into a LIST. A table is for data with more than one dimension, and a one-dimensional series put in one is a long sentence wearing pipes: it leaves the sentence measure for the cell measure and PD-4 then forbids the way back | no |

PD-4 is why the sentence-length measure excludes tables, headings and block quotes, and why the fat
cell count is kept as a separate number. A long cell and a long sentence are different problems. The
fix for one is not the fix for the other.

**PD-11 exists because the two rules looked like they contradicted each other, and the measurement
says they do not.** The ordinary advice for a long sentence carrying three or more items is to pull
the series out. That fix has two destinations and they behave differently here, which is the whole
of the apparent conflict:

* **A list is safe, and only became so recently.** Each item is measured as its own unit, so the
  extraction lands where a writer expects. Before that fix the items were rejoined into one blob and
  the count did not move at all, which is recorded above with the baseline it cost.
* **A table is the trap.** The words leave the sentence measure and arrive at the 40-word cell
  ratchet, and PD-4 forbids converting back to paragraphs to escape it. A writer who reaches for a
  table to shorten a sentence can end up with nowhere legal to go.

**Measured, nobody has fallen in.** All 30 cells over 40 words were read. Every one is a genuine
row: a document name against its description, or a reference row of five columns. Not one is a
series that should have been a list. So PD-11 is a review item and not a gate, on the same ground as
B-7 -- no pattern can tell a series in a cell from a description in a cell, and the corpus gives it
nothing to catch.

**The finding worth more than the rule.** A loose proxy put the long sentences carrying a series at
110. Read, only 50 carry a real three-item series and 20 of those were worth extracting. Doing so
produced the first fall in the long-sentence figure earned by editing rather than by fixing the
instrument. A sweep run on the proxy alone would have damaged 90 sentences to improve 20.

---

## Sections that look like filler and are not

| Rule | The rule | Enforced |
|---|---|---|
| `PD-8` | four named sections read like the padding the `B` rules order deleted, and each carries something its document has nowhere else. Do not trim one to satisfy a length or opener rule | two of four |

Each is named by path, because none of them looks load-bearing from the inside. The last column is
what actually fails, which for half of them is nothing.

| Section | What it carries | What fails if it goes |
|---|---|---|
| `docs/standards/SECURE-DEVELOPMENT.md`, `## Retired rules` | An empty table, where the emptiness is the artifact: it is where a retired identifier is recorded instead of being reused | `test_rule_ids_are_stable.py`, which raises by name when the heading is absent |
| `docs/standards/WHICH-STANDARDS-APPLY.md`, the selector sentinel comment | The line the layout splits on to place the selector, so reformatting it drops the app off the page silently | `test_the_selector_matches_the_routing_table.py`, which pins the string on both sides |
| `docs/standards/STANDARDS-REFERENCE.md`, the line carrying the status-check date | The one date every status in that table is scoped to, stated once there rather than repeated in every cell | nothing |
| `docs/ASVS-ASSESSMENT.md`, `## Handing this to Claude Code` | The only marker that Part 1 ends, and the paste-ready command that starts the assessment | nothing |

**The two that are pinned are not pinned by a rule about editing them.** `test_rule_ids_are_stable.py`
needs the `## Retired rules` heading because it parses retirements out of that section. The selector
test pins the sentinel because the layout splits on it. Both fail on a deletion, and neither tells an
editor why the section reads thin.

**The other two fail nothing, which is what this rule is for.** The status-check line is one sentence
that looks like a stray note and scopes an entire table. The ASVS section is the sharper case. It is
short and transitional in shape, and it is the only place the document says that everything after it
is addressed to an agent. An editor cutting it as a throat-clear takes the boundary with it.

**Why PD-8 and not the next free number.** The identifier is inherited, like the rest of the numbering
here, and it was written for these four sections. It is cited in the toolkit's sheet, where it is now
a tombstone recording that they left. Issuing PD-8 to a different rule later would break that citation
to buy a tidier sequence, which this page already declines to do.

---

## Notation that looks like emphasis and is not

| Rule | The rule | Enforced |
|---|---|---|
| `PD-9` | bold that a document defines in its own legend is notation, not emphasis. Do not unbold it to satisfy a style rule, and do not count it when measuring emphasis | no |

Two of these exist today, and both were counted before the rule was written.
`docs/standards/SECURE-DEVELOPMENT.md` gives the RFC 2119 keywords their force in a legend near the
top of the file, and then uses them 139 times. Every one is bold and none is left plain, so the
convention is the only thing telling a reader a requirement from a recommendation. The second is the
bolded `Rule.` label, 115 uses across four standards, which is how a reader scanning a page finds the
normative sentence inside it.

**PD-9 exists because these are the cheapest bold to delete.** A rule capping bold would count all
254 as hits. Stripping them is one mechanical pass with no judgment in it. That is the same trap PD-8
records for whole sections, one level down. The measurement that produced PD-9 is in
[what was measured and then rejected](#what-was-measured-and-then-rejected), and it was rejected as
a gate partly for this reason.

---

## A count stated in prose

| Rule | The rule | Enforced |
|---|---|---|
| `PD-12` | a count stated in prose must match the thing it counts. Enforced at ONE point, where both sides are structured: this page's own enforcement census against the table beneath it. The general form was measured and rejected, and the measurement is below | at one point |

**This rule exists because the defect escaped everything else here.** An adversarial audit of the
work that produced HS-20 and PD-10 found four counts that had drifted from what they counted. The
worst was this page's own summary saying three rules were enforced by a test while the table under
it listed six. It had been wrong across two merges. A sentence describing a table is prose to every
checker in this repository, so nothing could see it.

**The general form was measured and does not survive.** "A count in a lead-in must match the list
under it" fires on 46 lead-ins across this corpus, and 37 already agree. All 9 that disagree are
false positives, and every one was read. They include `recurred twice inside one week`, `Every one
of these`, and `This section and the three after it are the argument`.

A cardinal in a lead-in usually counts something other than the list beneath it. That is B-7's shape
at nine hits and zero precision, so the wide rule is rejected on the same ground.

**What makes the census checkable is that both sides are structured.** The sentence names a number
and a route. The table names routes and rules. Nothing has to infer what the number refers to, which
is the whole of the difference.

Where a future count sits against something equally structured, gate it and say so in this row.
Where it does not, this rule is a review item and reads as one.

**The four that were found are recorded rather than left implicit.** Three were written by the
session that then falsified them:

* a baseline restated as a fall
* a proxy figure quoted after it had been read down
* a per-1,000 rate over a page whose length then grew by half
* this census

Only the last is gated. The other three are why the page now says the current figure is the one the
test holds.

---

## The summary section has a fixed vocabulary

| Rule | The rule | Enforced |
|---|---|---|
| `PD-10` | a `## TLDR/BLUF` section labels its blocks from a fixed, ordered vocabulary: "What this is", "Why it matters", "Benefits", "Costs", "Not for you", "Where to start". The first and last are required and the middle four are optional. A block that is none of these is not a summary, and belongs below the section under its own heading | yes |

**This is the heading rule one level down, and the drift had already happened.** Fifteen pages
answered the same five questions in three vocabularies. SECURE-DEVELOPMENT said "What it demands"
and "Where it does not apply", the landing page said "What it costs you" and "Start at", ASVS said
"Why you should care" and "How to use it". Every page was internally consistent, so nothing could
see it. The only instrument that could was a reader who had read all fifteen.

**Nothing here requires a page to have a BLUF.** Three do not, and that restraint belongs to
`TheBlufConventionHasOneSpelling`, which records why a test is the wrong place to make that call.
PD-10 governs the labels of a section that exists, never whether it exists.

**`Benefits` and `Costs` are two blocks, and benefits leads.** The slot was "What it costs you"
until 2026-08-11, then briefly "Cost/Benefit", and is now split. A reader scanning for what a
document gives them finds it under its own label rather than inside a clause. Each block states
the document's own claim rather than restating "Why it matters" -- if they say the same thing, the
second is padding -- and `Costs` keeps every concrete price the combined block named. A split is
not permission to soften the half that was harder to write.

**Benefits before costs inverts the order this set used before, and the objection is recorded here
rather than answered.** Benefit-then-price is the shape of a pitch followed by fine print, and this
corpus is built to read as the opposite. Nothing measured decides the order. What holds it honest
is `Not for you`, which still follows both and disqualifies the reader outright.

**The prose inside a block is not checked, and that is PD-4's reasoning.** A rule that could not
tell a good block from a merely short one would be a rule about taste. What is checkable is whether
the label is one of six strings and whether the six are in order, which is all this fires on.

---

## What was measured and then rejected

Five rules are stated here and enforced by nobody. That is a decision with evidence behind it, not
an omission. The design rule for the whole set: hard-fail ONLY where a violation is unambiguous.

A gate that reddens a legitimate editorial choice is a gate people delete. Losing it also loses the
rules it was enforcing correctly, so the cost of a bad gate is not limited to the bad rule.

**B-7 is the instructive one.** Every candidate pattern was run over this corpus and every hit was
read. "cleanly" and its siblings fired 16 times, and not one was the self-praise the rule bans. The
hits were ordinary technical vocabulary: `git merges both cleanly`, `a session that exits cleanly`,
`an alias stub that resolves cleanly`.

The rule turns on WHAT IS BEING DESCRIBED, which no pattern over the text can see. Enforcing it
would redden sixteen correct sentences to catch nothing.

**B-10 went the same way on its single hit.** That hit was `## The one question: does failing it stop
the change?`, which the section immediately answers. It is not the rhetorical opener the rule exists
for.

**HS-3 is rejected for a different reason.** Duplication across two files is detectable, but which of
the two copies should go is an editorial call. A test cannot make it. The duplication is reported and
left to a human.

**HS-19 arrived from an outside checklist and lands where B-7 landed.** Passive constructions run to
656 here, or 10.89 per 1,000 words. Only 37 name their actor in a trailing "by" phrase, which is the
subset a pattern could turn round without judgment. All 37 were read. Two would read better
inverted.

The rest already put the right thing first. One reads `a codebase is judged by the composite`,
another `an advisory measurement that prints to a job log is read by nobody`. The remaining 619 have
no actor available to front, and inventing one would be a fabrication. `No scanner, format or
assessor is recommended anywhere in the set` names nobody, because nobody is recommended. So the
wide pattern is wrong 619 times, and the narrow one is wrong 35 times out of 37.

**The rule sheet was the second-heaviest page on that measure when HS-19 was written**, at 64 hits.
No rate is restated here. This page has grown by half since that measurement and a per-1,000 figure
would decay into a false claim, which is the same trap the baseline sentence above refuses. This is
recorded rather than fixed. HS-19 is a review item, and a page that measures itself and then quietly
edits to a better number is doing the thing PD-8 warns about.

**The candidates below failed a different test.** B-7, B-10, HS-19 and PD-11 were rejected because
no pattern can see the distinction they draw. HS-3 was rejected because the fix is an editorial
call. Each of those is an invitation to write a better pattern. The ones below are not.

They were measured against a corpus of this model's own output and found to describe nothing that
happens here, so a better detector would still be detecting nothing wrong. They are recorded rather
than reviewed, because a review item a reviewer would be wrong to raise is the argument about taste
this page opens by refusing.

**B-17 is the exception to that sourcing, and it reached the same place.** It came from an outside
editing checklist rather than this model's habits, and was measured here. The same checklist named
two forms already held here: one is B-5 and enforced, the other is B-15 and already recorded.

| Rule | The candidate | What the measurement found |
|---|---|---|
| `B-11` | "delve", "intricate", "meticulous", "garner", "showcase", "groundbreaking", "underscores" as a verb | 0 hits here, and 0 in every prose file this repository has ever committed. "intricate" and "meticulous" account for 20 of the 22 legitimate hits in this model's chat |
| `B-12` | "tapestry", "camaraderie", "solace", "palpable", "fleeting", "unspoken", "amidst", "unravel" | 0 hits here and 0 in the history. Its 2 chat hits are "unspoken" and "unravel", both correct. 11 of the 15 words in these two rows have no genuine use in 34 million words |
| `B-13` | "truly", "vastly", "incredibly", "remarkably", "profoundly", "undoubtedly" | 0 hits here and 0 in the history. 195 hits in chat and 20 in written files, none of them read, so precision is unmeasured. "truly random" is a term of art in this subject |
| `B-14` | "not just X but Y", and the three-part list used for rhythm | 1 hit here, 0 genuine. The outside source for it did not survive verification |
| `B-15` | "genuinely", "actually", "simply" used as filler | "genuinely" fires 11 times here and every one is doing work, as in `a package that genuinely exists` |
| `B-16` | noun-heavy phrasing and stacked participial clauses | needs a parser. A suffix proxy puts this corpus at 34.8 nominalizations per 1,000 words, against a baseline never measured for this model |
| `B-17` | "very", "just" and "really" deleted as filler, and "that" deleted wherever it can go | the first three fire 18 times across 60,831 words. Every hit was read and every one is load-bearing, as in `the very next re-run passed` and `not just the pointer`. The third has no hits at all. "that" fires 992 times. 12 have the shape of a deletable complementizer, and reading those 12 leaves 4: the rest are demonstratives and subject relatives the proxy miscaught, as in `recorded that judgment once` |

**Why the vocabulary rules were dropped rather than narrowed.** The cost case for them is real: they
fire on nothing, so a gate would be free. The design rule above says hard-fail ONLY where a
violation is unambiguous, which is a filter on gates and not a warrant for one. Cleanliness alone
does not earn enforcement, and treating it as if it did is how those six rules came to be written.

The reading settles it. In 1.6 million words of markdown this model wrote to disk, these patterns
fire 28 times. 27 of those are the draft sheet quoting its own ban list, and the 28th is correct
prose.

B-7 is the same shape and it fires 1,462 times in chat, the highest rate of any candidate here. Base
rate is not what separates a good gate from a bad one. Precision when it fires is, and these measure
zero.

**The record above is a table for a reason.** An evidence paragraph naming those words in prose takes
13 hits from the patterns proposed for them. Backticks do not help, because the scanner strips fences
and pipe rows and never touches inline code. The same content in rule rows takes none. A page that
cannot state its own finding in words is a page arguing with itself, and that is a second reason
those rules are not here as gates.

**The false positive B-11 can produce is one nobody may fix.** A link in this corpus can carry a
banned word inside its URL, and one on-topic certification announcement does. HS-16 forbids wrapping
a link, and the scanner rejoins wrapped lines anyway, so the only remedy is deleting the citation.
Quoted standard text has the same problem: B-5's own hits in this model's files include ASVS wording
a writer is not free to reword.

**Bold density was measured and carries no identifier.** It is a measure and not a construction, and
the two ratchets this page already names carry no identifier either. A number in the `B` series says
a construction is banned somewhere, which invites a later reader to finish the job.

The corpus held 1,544 bold spans over 18 files and 90,923 words before this section was added, which
is 16.98 per 1,000. Every file carries some, and the per-file spread runs from 6.69 to 24.38 per
1,000. The tightest cap that is clean today is 24.39, which sits above the rate of the register it
would exist to detect. A hard fail is closed on the same ground that closed B-7, at ninety-six times
the scale.

**A ratchet was the serious proposal, and this history refuses it.** Take the baseline at the commit
that added the prose checker. That is where a baseline would have been taken.

Every one of the eight commits after it is above that line, on all bold and on the narrow
in-sentence count alike. The sentence ratchet held green across the same eight commits. One of the
reddened commits is the one that landed this page.

Over 120 commits the in-sentence count rose 21 times, and all 21 are ordinary authoring work. The
rate fell from 14.15 to 6.60 per 1,000 over that span with nothing enforcing it. There is no drift
here to arrest. 79 of every 100 spans are structure rather than emphasis: 467 table cells, 361 list
ledes, 360 paragraph ledes and 26 block quotes, PD-9's 254 among them. The remaining 330 were read,
and they are contrast markers and term definitions in normative sentences.

**That breakdown is re-derived, because the one that stood here did not add up.** Its four components
summed to 1,196 while the remainder and the ratio beside them both required 1,176. At least one was
wrong and nothing said which.

Re-measured against the same tree, three figures reproduce exactly: the 1,544 total, the 467 table
cells and the 26 block quotes. That is what makes the method trustworthy enough to correct the other
two. A span may wrap across lines, and a lede counts once per paragraph or item, with any further
span in that unit falling to the remainder.

The gap that made a ratchet tempting is stated here without a claim attached. Markdown this model
writes to disk runs at 29.18 per 1,000 in the same page-size band, against 16.98 here. Nothing in
that says 17 is better than 29 for a reader, and this page does not enforce a preference under a
measurement's colours.

**The word "honest" was measured and left alone.** It fires 31 times across 9 of the 18 files, and
83 times across this repository's history. Every hit is load-bearing in a document set whose subject
is stating limits truthfully, as in `an honest scorecard says so out loud`.

It also runs at 0.35 per 1,000 in this model's chat and 0.44 in the files it writes, so the file
register is the higher one. That is B-7's case at twice the scale. It is recorded so the next reader
who finds the word on an imported list does not measure it again.

**One number this section does not print.** Every candidate above was first scored as a ratio
against a control corpus of user turns. That control was 94% prompts written by another instance of
the same model, because the scan never filtered the flag that marks them. Removing them leaves 1.67
million words against 26.7 million, and what remains is terse instruction rather than prose.

The ratios are withdrawn and only absolute counts are quoted above. The finding is worth more than
the ratios were, and HS-18 is where it is written as a rule.

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

**The gaps were checked against the toolkit, and they are occupied.** The toolkit repository this
numbering came from was read directly rather than inferred from this page. Its sheet issues B-1 to
B-10, HS-1 to HS-16, PD-1 to PD-8 and OPEN-1 to OPEN-6, with no gaps of its own.

So the next free number is the one above the highest issued, never the lowest unused. The gaps here
are inherited names rather than vacancies. Its PD-6 states the rule this page follows: reword a rule
freely under the same identifier, and allocate a new one when you change what it demands.

**HS-17 is spent and must not be issued.** A superseded branch defines it as the ASCII punctuation
rule, which is what HS-11 already demands and what the gate already runs. Two names for one rule
split its citations, which is the defect HS-3 describes. PD-5 is spent the same way: the toolkit
issues it for something else, and the rule that draft gave it is PD-8 pointing the other way. After
this page, the next free numbers are B-18, HS-21 and PD-13.
