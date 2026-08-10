"""The prose checker. Hard-fail where a violation is unambiguous, baselined ratchet everywhere else.

WHAT THIS EXISTS FOR. `docs/HOUSE-STYLE.md` states the writing rules and nothing enforced any of
them, so the only thing standing between the corpus and a slow drift back was whether a reviewer
happened to remember a rule identifier. This file enforces the subset that CAN be enforced and says
plainly which subset that is.

THE DESIGN RULE, taken from the writing plan and not negotiable here: hard-fail ONLY where a
violation is unambiguous and the current corpus is clean. A gate that reddens a legitimate editorial
choice is one people delete, and the repository already recorded that judgment once in
`test_docs_do_not_drift.TheBlufConventionHasOneSpelling`.

WHAT WAS MEASURED BEFORE CHOOSING, because the choice is the whole design. Every candidate pattern
was run over the corpus on 2026-08-08 and every hit was read:

  B-7  "cleanly", "elegantly", "robustly"      16 hits, ~0 genuine  -> NOT ENFORCED
  B-5  "in order to", "utilize", "leverage"    10 hits,  1 genuine  -> ENFORCED, narrowed
  B-3  "Importantly", "It is worth noting"      5 hits,  0 genuine  -> ENFORCED, narrowed
  B-10 a heading that is a question             1 hit,   0 genuine  -> NOT ENFORCED

B-7 IS THE INSTRUCTIVE ONE AND IT IS DELIBERATELY ABSENT. The rule bans those adverbs "describing
this project's own work". Measured, every single hit was standard technical vocabulary instead:
`git merges both cleanly`, `a session that exits cleanly`, `an execution-alias stub that resolves
cleanly`, `a transform producing valid-but-wrong output passes cleanly`. The distinction the rule
draws is about WHAT IS BEING DESCRIBED, and no pattern over the text can see that. Enforcing it would
redden sixteen correct sentences to catch nothing, so it stays a review item. The same reasoning
retires B-10: its one hit, `## The one question: does failing it stop the change?`, is a question the
section immediately answers, which is not the rhetorical opener the rule is about.

B-5 IS NARROWED TO THE UNAMBIGUOUS FORMS. Bare "leverage" is a noun as often as a verb here --
`ordered by its own leverage`, `the highest-leverage gate` -- so only the participles and the
unmistakable phrases are enforced. The one genuine violation the scan found, a cloud program that had
`begun leveraging an external framework`, was fixed in the same commit that added this file, because
a hard-fail rule whose corpus is already red is a rule that ships disabled.

THE RULE SHEET MUST BE ABLE TO QUOTE WHAT IT BANS. `docs/HOUSE-STYLE.md` lists every banned
construction verbatim in its own tables. The exemption is deliberately NARROW: a table row whose
first cell is a rule identifier, and nothing else. Exempting the whole file would leave the rule
sheet the only unchecked prose in the repository.

WHAT THE EXEMPTION ACTUALLY DOES, measured rather than assumed -- the sentence that used to sit here
credited it with the wrong job. Its live effect is on the FAT-CELL RATCHET. `scannable_lines` is read
by `_measure` and by nothing else, so what a rule row escapes is being counted against the 40-word
cell baseline, which matters because a definition row quotes several banned forms and their
replacements and runs long. The banned-construction scan never sees a table row at all: `paragraphs`
drops every line beginning with a pipe, so the rule sheet was never at risk from that half. Neither
is any other page, and that is a COVERAGE LIMIT rather than a feature -- a banned construction
written inside an ordinary table cell is caught by nothing here. It is recorded on the rule sheet and
left open, because closing it means judging a cell by a sentence rule, which is what PD-4 forbids.

THE CITATION USED TO DANGLE, AND IS NOW PINNED. This file named `docs/HOUSE-STYLE.md` in four
docstrings and in the failure message above, and `test_a_links_text_never_wraps.py` named it for
HS-16. No such file had ever existed in this repository: `git log --all --follow` over that path
returned nothing, because the rule sheet stayed in the toolkit repository when the standards split
out in 282a76c. Every gate stayed green, and the only person who could find out was one who tripped a
rule and went looking. `TheRuleSheetIsInThisRepository` below is what stops that recurring.

WHAT IS REPORTED RATHER THAN FAILED, and why each is not a hard fail:

  cross-file duplication   HS-3, but which of two copies should go is an editorial call
  table cell word counts   fourteen files exceed 40 words per cell, SECURE-DEVELOPMENT among them
  long sentences           a cap at 30 fires on 1,397 of 6,579; the long tail carries the warnings

Each is a RATCHET against a baseline measured from the corpus. It may not get worse. If it gets
better the test says so and asks for the baseline to be lowered, because a ratchet nobody tightens is
a number that stops meaning anything.

Run: python -m unittest discover -s tests
"""

from __future__ import annotations

import re
import subprocess
import unittest

import _ccxtest as t

# ---------------------------------------------------------------------------
# Corpus


def tracked_files() -> list[str]:
    """Every path git is tracking, as forward-slash repo-relative strings."""
    out = subprocess.run(
        ["git", "ls-files"],
        cwd=t.REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in out.stdout.splitlines() if line.strip()]


def prose_files() -> list[str]:
    """Tracked markdown that is prose. Word copies are generated and are not edited."""
    return [
        f
        for f in tracked_files()
        if f.endswith(".md")
        and (f.startswith(("docs/", "README", "INSTALL")))
        and "/word/" not in f
    ]


RULE_ROW = re.compile(r"^\|\s*`?(?:B|HS|PD|OPEN|SD|CP)-\d+`?\s*\|")
FENCE = re.compile(r"^\s*(```|~~~)")

# A list item's marker, including a task-list checkbox. Matched so that an item can START a unit of
# prose and so the marker itself is not counted as a word. See `paragraphs` for what this fixes.
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(?:\[[ xX]\]\s+)?")


def scannable_lines(text: str) -> list[tuple[int, str]]:
    """Prose lines only: no code fences, and no rule-definition rows.

    ONE CALLER, ONE EFFECT. `_measure` reads this and nothing else does, so the rule-row exemption
    buys exactly one thing: HOUSE-STYLE.md's definition rows stay off the 40-word fat-cell ratchet.
    They quote several banned forms and their replacements, so they run long by design. It matches
    ONLY a table row whose first cell is a rule identifier.

    It is NOT what keeps that page off the banned-construction scan, though it reads as if it were.
    `paragraphs` drops every line beginning with a pipe, so no table row reaches that scan at all.
    See the module docstring for why that distinction is worth writing down.
    """
    out: list[tuple[int, str]] = []
    inside = False
    for n, line in enumerate(text.split("\n"), 1):
        if FENCE.match(line):
            inside = not inside
            continue
        if inside or RULE_ROW.match(line):
            continue
        out.append((n, line))
    return out


def paragraphs(text: str) -> list[tuple[str, list[tuple[int, int]]]]:
    """Prose rejoined into paragraphs, each with an offset -> line map.

    THIS IS THE WHOLE REASON THE CHECKER WORKS. HS-14 wraps prose near 100 characters, so a sentence
    here is spread over three or four lines. Scanning line by line gets both halves wrong: no line
    ever reaches 30 words, so a sentence-length measure reports zero, and a line that happens to
    BEGIN with a wrapped "importantly" looks like a sentence opener when it is the middle of one.
    Both were observed before this was rewritten.

    A LIST ITEM STARTS ITS OWN UNIT, and that is the second half of the same defect. The rejoin above
    is indiscriminate, so a bullet list became ONE blob and the sentence split then read the run of
    items as a single enormous sentence. Measured before this was fixed: 60 of the 363 sentences over
    30 words were rejoined list runs, and 17 of the 64 over 43 words. The largest was 156 words and
    is five links in `SECURE-DEVELOPMENT.md`, each on its own line, each perfectly short.

    That is worse than a wrong number, because the fix the length reads as asking for is the fix that
    made it. Pulling a series out of a sentence into bullets is the standard remedy, and under the old
    rejoin it moved the words from one blob into the same blob and changed the count by nothing.

    Continuation lines still belong to their item -- HS-14 wraps at 100 characters and a long item
    wraps like anything else -- so only a line that BEGINS an item flushes. The marker is stripped
    because `"- a dependency".split()` counts the hyphen as a word, which inflates every item by one.

    Tables are excluded here and counted separately -- a table row is not prose and PD-4 protects it.
    """
    out: list[tuple[str, list[tuple[int, int]]]] = []
    current: list[tuple[int, str]] = []

    def flush() -> None:
        if not current:
            return
        parts: list[str] = []
        spans: list[tuple[int, int]] = []
        pos = 0
        for line_no, line in current:
            stripped = line.strip()
            if parts:
                pos += 1  # the space join() will insert
            spans.append((pos, line_no))
            parts.append(stripped)
            pos += len(stripped)
        out.append((" ".join(parts), spans))
        current.clear()

    inside = False
    for n, line in enumerate(text.split("\n"), 1):
        if FENCE.match(line):
            inside = not inside
            flush()
            continue
        stripped = line.strip()
        if inside or not stripped or stripped.startswith(("|", "#", ">")) or RULE_ROW.match(line):
            flush()
            continue
        if LIST_ITEM.match(line):
            flush()
            current.append((n, LIST_ITEM.sub("", line, count=1)))
            continue
        current.append((n, line))
    flush()
    return out


def line_at(spans: list[tuple[int, int]], offset: int) -> int:
    """Map a character offset inside a joined paragraph back to its source line."""
    line_no = spans[0][1]
    for start, n in spans:
        if start <= offset:
            line_no = n
        else:
            break
    return line_no


# ---------------------------------------------------------------------------
# Hard fail. Every pattern here fires zero times on the corpus as committed.

BANNED = [
    (
        "B-3",
        'an opener whose only work is to announce that what follows matters. Write the note.',
        re.compile(r"(?:\A|(?<=[.!?] ))(?:Importantly|Notably)\b|\bIt (?:is worth noting|should be noted)\b", re.I),
    ),
    (
        "B-5",
        'padding. Write "use", "to", or "can".',
        re.compile(r"\bin order to\b|\bprovides? the (?:capability|ability) to\b|\butili[sz](?:e|es|ed|ing)\b|\bleverag(?:ing|ed)\b", re.I),
    ),
    (
        "B-6",
        "a sentence asserting its own significance. State the fact that makes it significant.",
        re.compile(r"\bthis is (?:important|significant|critical)\b|\bthe key (?:point|thing) (?:is|here)\b|\bcannot be overstated\b|\bworth emphasi[sz]ing\b", re.I),
    ),
]


class BannedConstructionsAreAbsent(unittest.TestCase):
    def test_no_tracked_page_carries_a_banned_construction(self):
        offenders = []
        for relpath in prose_files():
            text = t.read(t.REPO_ROOT / relpath)
            for joined, spans in paragraphs(text):
                for rule_id, why, pattern in BANNED:
                    for m in pattern.finditer(joined):
                        line_no = line_at(spans, m.start())
                        offenders.append(f"{relpath}:{line_no}: {rule_id} {m.group(0).strip()!r} -- {why}")
        self.assertEqual(
            [],
            offenders,
            "these pages carry a construction docs/HOUSE-STYLE.md bans:\n  "
            + "\n  ".join(offenders)
            + "\nOnly the unambiguous rules are enforced here. If you believe one of these is a false "
            "positive, that is a reason to narrow the pattern in this file and say why in the commit "
            "-- not a reason to add an exemption for your page.",
        )

    def test_the_scan_actually_reads_the_corpus(self):
        """The empty-match guard. A scan for absences passes trivially against an empty corpus."""
        files = prose_files()
        self.assertGreaterEqual(
            len(files),
            12,
            f"the prose scan found only {len(files)} pages. The absence check above would pass "
            "against an empty corpus while measuring nothing, so this is what makes it mean "
            "anything. If the docs really did shrink this far, lower the number deliberately.",
        )
        words = sum(len(t.read(t.REPO_ROOT / f).split()) for f in files)
        self.assertGreater(words, 25_000, f"only {words} words scanned; the corpus is ~170,000.")


class TheBannedPatternsCatchWhatTheyExistToCatch(unittest.TestCase):
    """Prove each pattern on a planted example, and prove it declines the near-neighbour.

    Without the negative half this class would pass against a pattern that matches everything.
    """

    PLANTED = [
        ("B-3", "Importantly, the gate is advisory."),
        ("B-3", "It is worth noting that the hook is unwired."),
        ("B-5", "The installer exists in order to write a shim."),
        ("B-5", "The script will utilize the registry."),
        ("B-5", "One program has begun leveraging an external framework."),
        ("B-6", "This is important: the gate is advisory."),
    ]

    # Every one of these appears in the corpus today, or is the near-miss the pattern must decline.
    ACCEPTED = [
        "Git merges both cleanly, and nothing in the graph can see it.",
        "A session that exits cleanly unlinks its registry file.",
        "The rows are ordered by its own leverage.",
        "The highest-leverage gate to build first.",
        "A version pin does not satisfy it, and more importantly does not satisfy the property.",
        "The one question: does failing it stop the change?",
    ]

    def test_each_pattern_fires_on_its_planted_example(self):
        for rule_id, planted in self.PLANTED:
            pattern = next(p for r, _, p in BANNED if r == rule_id)
            self.assertTrue(
                pattern.search(planted),
                f"{rule_id} did not fire on {planted!r}; the rule is unenforced.",
            )

    def test_no_pattern_fires_on_prose_the_corpus_legitimately_uses(self):
        for accepted in self.ACCEPTED:
            for rule_id, _, pattern in BANNED:
                m = pattern.search(accepted)
                if m is not None:
                    self.fail(
                        f"{rule_id} fired on {accepted!r}, matching {m.group(0)!r}. That sentence is "
                        "correct prose from this corpus, so the pattern is too wide and would redden "
                        "a legitimate page."
                    )

    def test_a_rule_definition_row_is_exempt_but_the_rest_of_the_page_is_not(self):
        """HOUSE-STYLE.md must be able to name what it bans, without becoming unscannable.

        The planted half. `TheRuleSheetIsInThisRepository` is the corpus half, and it is the one
        that fails if the exemption stops having anything to exempt.
        """
        text = "| B-5 | \"in order to\", \"utilize\" | \"to\", \"use\" |\nThe installer runs in order to help."
        lines = scannable_lines(text)
        self.assertEqual(
            [2],
            [n for n, _ in lines],
            "the rule-row exemption should skip the table row and keep the prose line. Skipping "
            "more than the row would leave the rule sheet unchecked.",
        )


# ---------------------------------------------------------------------------
# The rule sheet the failure messages send people to.

HOUSE_STYLE = "docs/HOUSE-STYLE.md"

# What counts as DEFINING a rule: the identifier as the first cell of a table row. The summary table
# at the top of the rule sheet is deliberately keyed on what fires rather than on an identifier, so
# it cannot satisfy this by merely listing a rule it never defines.
DEFINITION = re.compile(r"^\|\s*`?((?:B|HS|PD)-\d+)`?\s*\|", re.M)

# What counts as CITING one: a rule identifier written at a reader, in a test, a failure message or a
# CI gate's comment. Read off the citing files rather than listed here, for the reason tests/README.md
# gives -- a hand-written list checked against a hand-written list only proves the two lists agree.
CITATION = re.compile(r"\b((?:B|HS|PD)-\d+)\b")
CITING_DIRS = ("tests/", ".github/workflows/")
CITING_SUFFIXES = (".py", ".md", ".yml")


class TheRuleSheetIsInThisRepository(unittest.TestCase):
    """The dangling citation this class exists for, and it is not hypothetical.

    This file named `docs/HOUSE-STYLE.md` in four docstrings and in the message a developer sees when
    B-3, B-5 or B-6 fires; `test_a_links_text_never_wraps.py` named it for HS-16; tests/README.md
    described its role at length. No such file had ever existed here. It stayed in the toolkit
    repository when the standards split out, and nothing noticed, because a citation in a failure
    message is prose to every checker in this suite. The reader who found out was one who tripped a
    rule and went looking for the sheet.

    A test that cites a rule sheet is making a promise about a file. These cases keep it, in both
    directions: the file is here, and it defines every rule this suite sends anyone to read.
    """

    def _sheet(self) -> str:
        return t.read(t.REPO_ROOT / HOUSE_STYLE)

    def test_the_rule_sheet_exists(self):
        self.assertTrue(
            (t.REPO_ROOT / HOUSE_STYLE).is_file(),
            f"{HOUSE_STYLE} is missing. The failure messages in this file and in "
            "test_a_links_text_never_wraps.py send a developer there to read the rule they just "
            "tripped, so restore it or repoint every citation in the same commit. A message naming "
            "a file nobody can open is worse than no message: it reads like the reader's mistake.",
        )

    def test_every_rule_the_suite_cites_has_a_definition_row(self):
        defined = set(DEFINITION.findall(self._sheet()))
        self.assertTrue(
            defined,
            f"{HOUSE_STYLE} carries no rule-definition rows at all. Either the tables were reshaped "
            "or DEFINITION stopped matching them -- and an empty set would satisfy the comparison "
            "below by having nothing to disagree with, so this raises first.",
        )

        cited: dict[str, set[str]] = {}
        for relpath in tracked_files():
            if not relpath.startswith(CITING_DIRS) or not relpath.endswith(CITING_SUFFIXES):
                continue
            for rule_id in CITATION.findall(t.read(t.REPO_ROOT / relpath)):
                cited.setdefault(rule_id, set()).add(relpath)

        self.assertTrue(
            cited,
            "no rule identifier was found in tests/ or .github/workflows/ at all. This scan has "
            "gone blind, and a blind scan reports agreement with everything.",
        )

        undefined = sorted(set(cited) - defined)
        self.assertEqual(
            [],
            undefined,
            "these rules are cited at a reader but defined nowhere in "
            f"{HOUSE_STYLE}:\n  "
            + "\n  ".join(f"{r} cited by {', '.join(sorted(cited[r]))}" for r in undefined)
            + f"\nAdd a definition row keyed on the identifier, or stop citing it. Sending someone "
            "to a rule sheet that does not carry the rule is the same defect as sending them to a "
            "file that does not exist -- it just fails one step later.",
        )

    def test_the_exemption_has_something_real_to_exempt(self):
        """Without this, the exemption is a branch that runs on every line and protects nothing.

        That was its exact state while the rule sheet was missing: measured over all 17 tracked
        prose pages, RULE_ROW matched zero lines. The planted case above still passed, because it
        builds its own two-line fixture, so nothing in the suite could tell the difference.
        """
        sheet = self._sheet()
        exempted = [line for line in sheet.split("\n") if RULE_ROW.match(line)]
        self.assertGreaterEqual(
            len(exempted),
            5,
            f"RULE_ROW matches {len(exempted)} lines in {HOUSE_STYLE}. The exemption is then a "
            "branch that costs a comparison per line and buys nothing, and the planted case above "
            "would keep passing against its own fixture while this was true.",
        )

        # The exemption is only load-bearing if removing it would change a number. It does: a
        # definition row quotes several banned forms and their replacements, which is what makes it
        # exceed the same 40-word cell limit the ratchet counts.
        would_count = [
            line
            for line in exempted
            if any(len(cell.split()) > 40 for cell in line.strip().strip("|").split("|"))
        ]
        self.assertTrue(
            would_count,
            f"no rule row in {HOUSE_STYLE} exceeds 40 words in a cell, so dropping the exemption "
            "would change nothing measurable and it should be dropped. Keep it only while a "
            "definition row genuinely needs the room to quote what it bans.",
        )


class AListIsNotOneLongSentence(unittest.TestCase):
    """The rejoin defect this suite already recorded once, in its other half.

    `paragraphs` exists because a line-based scan reported ZERO sentences over 30 words: HS-14 wraps
    prose, so no LINE is ever long. The rejoin fixed that and introduced the mirror defect, which
    stood for two months. Rejoining indiscriminately turns a bullet list into one blob, and the
    sentence split then reads a run of items as one sentence. It reported 156 words for five links
    that sit on five lines.

    Both halves fail the same way from the outside -- a number that looks measured and is not -- and
    a corpus check cannot tell the difference, because the corpus is where the wrong number came
    from. So these are planted.
    """

    def test_each_item_in_a_list_is_measured_on_its_own(self):
        text = "- the first item\n- the second item\n- the third item"
        units = [joined for joined, _ in paragraphs(text)]
        self.assertEqual(
            ["the first item", "the second item", "the third item"],
            units,
            "a bullet list rejoined into one unit is what made 60 of the old 371 long sentences. "
            "Each item is prose on its own and is measured on its own.",
        )

    def test_a_wrapped_item_stays_one_unit(self):
        """The half that must NOT split, or the fix trades one wrong number for another."""
        text = "- an item long enough that HS-14 wraps it near a hundred\n  characters, as it does here"
        units = [joined for joined, _ in paragraphs(text)]
        self.assertEqual(1, len(units), f"a wrapped item split into {len(units)} units: {units}")
        self.assertIn("characters, as it does here", units[0])

    def test_the_marker_is_not_counted_as_a_word(self):
        joined = paragraphs("- a dependency inventory")[0][0]
        self.assertEqual(
            3,
            len(joined.split()),
            f"{joined!r} counts the list marker as a word, which inflates every item by one.",
        )

    def test_a_run_of_short_items_is_not_a_long_sentence(self):
        """The end-to-end shape, written the way the corpus writes it."""
        text = "\n".join(f"- item number {n} carrying six words" for n in range(1, 9))
        longest = max(
            len(sentence.split())
            for joined, _ in paragraphs(text)
            for sentence in SENTENCE_SPLIT.split(joined)
        )
        self.assertLess(
            longest,
            31,
            f"eight six-word items measured as a {longest}-word sentence. That is the artifact, and "
            "it punishes the page that already extracted its list.",
        )

    def test_a_checkbox_item_is_a_list_item(self):
        """ASVS-ASSESSMENT.md is largely task lists, so this is corpus shape, not a curiosity."""
        units = [joined for joined, _ in paragraphs("- [ ] the first check\n- [x] the second check")]
        self.assertEqual(["the first check", "the second check"], units)


class ABoldLedeEndsASentence(unittest.TestCase):
    """The third instrument defect in the same family, and the largest of them.

    This set writes a paragraph as `**A claim.** The evidence for it.` -- 587 times, `**Rule.**`
    alone 115 of them. The stop sits INSIDE the emphasis, so the character before the space is `*`
    and a naive split never fired. Every one of those paragraphs measured its lede and its next
    sentence as a single sentence, and 77 of the 339 long sentences were that.

    PLANTED, for the reason the class above gives: the corpus produced the wrong number, so it
    cannot be the thing that detects the wrong number. The negative cases matter as much as the
    positive ones -- widening a split is how a measure starts reporting improvement it did not earn.
    """

    def test_a_bold_lede_and_its_sentence_are_two_sentences(self):
        got = SENTENCE_SPLIT.split("**Rule.** Pick the source of record for each fact.")
        self.assertEqual(["**Rule.**", "Pick the source of record for each fact."], got)

    def test_a_whole_sentence_in_italic_ends_where_it_ends(self):
        got = SENTENCE_SPLIT.split("*Revised.* The source material said otherwise.")
        self.assertEqual(["*Revised.*", "The source material said otherwise."], got)

    def test_a_colon_lede_is_not_a_sentence_boundary(self):
        """38 of these exist. A colon lede introduces what follows rather than closing a thought."""
        text = "**Control not met:** independent review of every change."
        self.assertEqual([text], SENTENCE_SPLIT.split(text))

    def test_an_ordinary_sentence_still_splits(self):
        got = SENTENCE_SPLIT.split("The gate is advisory. Nothing stops the commit.")
        self.assertEqual(["The gate is advisory.", "Nothing stops the commit."], got)

    def test_emphasis_inside_a_sentence_is_not_a_boundary(self):
        text = "A rule the **prose checker** enforces is one a developer can read."
        self.assertEqual([text], SENTENCE_SPLIT.split(text))

    def test_the_fused_pair_is_no_longer_measured_as_one_sentence(self):
        """End to end, at the length the ratchet actually counts."""
        lede = "**A claim stated in a lede that runs to a dozen words or so here.**"
        rest = "The evidence for it, which also runs to about a dozen words here."
        longest = max(len(s.split()) for s in SENTENCE_SPLIT.split(f"{lede} {rest}"))
        self.assertLess(
            longest,
            31,
            f"a lede plus its sentence measured as {longest} words. That is the artifact: neither "
            "half is long and the pair is only long because the split could not see the stop.",
        )


# ---------------------------------------------------------------------------
# Reported, and ratcheted. These may not get worse.

# Measured on 2026-08-08 against this repository's corpus: 54,310 words of prose in 17 files.
#
# MEASURE WITH THE FILES TRACKED. `prose_files()` reads `git ls-files`, so a baseline taken while a
# new page is still untracked is a baseline that has not seen it. That happened here: the first
# figure was 362, taken before README.md and docs/index.md were committed, and CI reported 371 on
# the same corpus. Nine sentences, and the ratchet caught it rather than the reviewer.
# To change one, run the test: it names the current figure and which direction it moved.
#
# These are lower than the figures in the writing plan (which counted 1,397 long sentences) because
# that count included headings, table rows and block quotes. This one is prose only, for the same
# reason PD-4 exists: a table row is not a sentence and shortening it is not an improvement.
#
# 371 -> 339 -> 262 on 2026-08-10, AND NOT ONE SENTENCE WAS EDITED TO EARN EITHER MOVE. Both were
# defects in this file rather than improvements to the corpus, and both inflated the same number:
#
#   371 -> 339   `paragraphs` rejoined a bullet list into one blob, so the split read a run of
#                items as a single long sentence. 60 of the 371 were that.
#   339 -> 262   `SENTENCE_SPLIT` could not see a stop inside emphasis, so `**Rule.** Pick the
#                source` measured as one sentence rather than two. 77 of the 339 were that.
#
# Together they were 137 of the original 371, so more than a third of the baseline was instrument
# error. Each is lowered here rather than banked as headroom: slack bought by fixing the measurement
# is slack a future page spends with nothing reporting it. That both survived the first review is
# the argument for AListIsNotOneLongSentence and ABoldLedeEndsASentence being planted cases -- a
# corpus check cannot find them, because the corpus is where the wrong number came from.
#
# 262 -> 263 on the rebase onto #23. The extra sentence is not from this branch: four commits landed
# on main while this was in flight, and they were reviewed against an instrument that could not see
# a stop inside emphasis. This is what the corrected measure reports on the corpus as it now stands,
# which is the only number a ratchet can honestly hold.
BASELINE_LONG_SENTENCES = 263       # sentences over 30 words
BASELINE_FAT_TABLE_CELLS = 30       # table cells over 40 words

# How far below baseline a metric may drift before the test asks for the baseline to be lowered.
# Sized to each metric rather than shared: 40 is noise against 833 and most of the way to zero
# against 49.
LONG_SENTENCE_SLACK = 25
FAT_CELL_SLACK = 6

# A BOLD LEDE ENDS A SENTENCE, and the naive form of this could not see that. `**Rule.** Pick the
# source` puts the stop INSIDE the emphasis, so the character before the space is `*` and the split
# never fired. The lede fused to the sentence after it and the pair was measured as one. That shape
# is not a curiosity here: `**Rule.**` alone appears 115 times, and 587 bold ledes end in a stop.
#
# The italic branch is separate and earns its place at 16 hits -- `*Revised.*`, `*This is not a
# pass.*` -- each a whole sentence in italic. There is NO underscore branch, because `__bold__` and
# `_italic_` fire zero times here and a branch that protects nothing is one this suite deletes.
#
# A COLON LEDE MUST NOT SPLIT, and 38 of them would be wrong to: `**Control not met:** independent`
# introduces what follows rather than closing a thought. Splitting only on `.!?` declines them for
# free. The other near-neighbour is an abbreviation inside emphasis -- a bold `**e.g.**` would split
# mid-sentence -- so every emphasis run of three words or fewer ending in a stop was read before
# this widened. All 57 distinct forms are lede labels. The corpus has no such abbreviation today.
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|(?<=[.!?]\*)\s+|(?<=[.!?]\*\*)\s+")


def _measure() -> tuple[int, int, int]:
    """(sentences over 30 words, table cells over 40 words, words examined)."""
    long_sentences = 0
    fat_cells = 0
    words = 0
    for relpath in prose_files():
        text = t.read(t.REPO_ROOT / relpath)
        for joined, _ in paragraphs(text):
            words += len(joined.split())
            for sentence in SENTENCE_SPLIT.split(joined):
                if len(sentence.split()) > 30:
                    long_sentences += 1
        for line_no, line in scannable_lines(text):
            stripped = line.strip()
            if not stripped.startswith("|"):
                continue
            for cell in stripped.strip("|").split("|"):
                if len(cell.split()) > 40:
                    fat_cells += 1
    return long_sentences, fat_cells, words


class TheReportedMetricsDoNotRegress(unittest.TestCase):
    """A ratchet, not a cap. The plan rejected all three as hard fails, with the measurement."""

    def test_it_reports_what_it_examined(self):
        long_sentences, fat_cells, words = _measure()
        self.assertGreater(
            words,
            25_000,
            f"the metric pass examined {words} words of prose, which is too few to have read the "
            "corpus. A measurement over nothing reports zero and reads like a pass.",
        )
        self.assertGreater(
            long_sentences,
            0,
            "zero sentences over 30 words is not credible for this corpus and means the paragraph "
            "rejoin has broken. It reported exactly this before the line-based scan was replaced.",
        )

    def test_long_sentences_do_not_increase(self):
        long_sentences, _, _ = _measure()
        self.assertLessEqual(
            long_sentences,
            BASELINE_LONG_SENTENCES,
            f"{long_sentences} sentences now exceed 30 words, against a baseline of "
            f"{BASELINE_LONG_SENTENCES}. This is not a cap -- the long tail of this corpus is where "
            "the engineering warnings live -- but it may not grow.",
        )
        self.assertGreater(
            long_sentences,
            BASELINE_LONG_SENTENCES - LONG_SENTENCE_SLACK,
            f"only {long_sentences} long sentences remain, against a baseline of "
            f"{BASELINE_LONG_SENTENCES}. Lower BASELINE_LONG_SENTENCES to {long_sentences} in this "
            "file. A ratchet nobody tightens stops measuring anything.",
        )

    def test_fat_table_cells_do_not_increase(self):
        _, fat_cells, _ = _measure()
        self.assertLessEqual(
            fat_cells,
            BASELINE_FAT_TABLE_CELLS,
            f"{fat_cells} table cells now exceed 40 words, against a baseline of "
            f"{BASELINE_FAT_TABLE_CELLS}. PD-4 forbids solving this by converting a table to prose.",
        )
        self.assertGreater(
            fat_cells,
            BASELINE_FAT_TABLE_CELLS - FAT_CELL_SLACK,
            f"only {fat_cells} fat table cells remain, against a baseline of "
            f"{BASELINE_FAT_TABLE_CELLS}. Lower BASELINE_FAT_TABLE_CELLS to {fat_cells}.",
        )


if __name__ == "__main__":
    unittest.main()
