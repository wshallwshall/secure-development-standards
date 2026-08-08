# What to have ready when a buyer asks, and what each artifact proves

**Every serious buyer asks for the same small, predictable set of documents. Have them on the shelf
before the first call, and know for each one the claim it carries and the claim it does not.**

> **Take a copy:**
> [markdown](https://raw.githubusercontent.com/wshallwshall/secure-development-standards/main/docs/standards/DILIGENCE-PACKET.md)
> or [Word document](https://raw.githubusercontent.com/wshallwshall/secure-development-standards/main/docs/standards/word/DILIGENCE-PACKET.docx).
> [Every file, both formats](OVERVIEW.md#the-files).

---

## TLDR/BLUF

**The commonest vendor mistake in diligence is offering an audit report or a certificate as an
answer about the product.** Those instruments examine how your company governs itself -- policies,
access reviews, change management. They never open your code. You can hold a clean twelve-month
report, ship software with an authorization flaw in it, and have said nothing false. Offer it as
product evidence and you have said something false -- the position that ends deals.

So sort your evidence by layer -- the company, the software, the contract -- and have three things
ready before the first call:

1. **The scope statement** of whatever organization-layer instrument you hold. Not the certificate,
   not the cover page. It alone decides whether the thing being bought was inside the examination,
   and for software you distribute rather than host, the answer is frequently no. Say so yourself: a
   paragraph now costs less than a deal later.
2. **An SBOM of what the buyer will actually run.** For an installed product that is the released
   artifact; for a hosted service, the runtime production environment. Generate it from the build --
   a hand-maintained list is a document about your intentions.
3. **Two dates and a name:** your last dynamic test, your last incident response exercise, and who
   ran the test. Both dates are trivial to supply if they happened and impossible to produce
   retrospectively, which is why they are asked for. The name decides whether you are offering an
   independent look or your own tooling's output.

Each is a document, a date or a name. None can be answered with an adjective, and a buyer who
accepts one is not the buyer whose approval is worth having.

---

## The organization layer is worth having; the failure is narrower

None of this is a reason to skip these instruments. That somebody outside the company examined how
you govern yourself, grant access and manage change is worth establishing, and a vendor holding none
is a different risk entirely. The failure is narrower: letting a program attestation stand as an
answer to "is this product secure", when no part of it asked that.

Statuses, versions and dates live on the reference page, each carrying the date it was checked. The
same cut, as a rule you can hold your own process to, is
[the organization layer is not the software layer](STANDARDS-REFERENCE.md#the-organization-layer-is-not-the-software-layer).

---

## Organization layer: evidence about your company

Procurement already knows how to ask for these. Most are issued by someone other than you, which is
where their weight comes from -- and none of that weight is about your product. One caveat governs
the group: an examination or a certification has a boundary, and software you distribute frequently
falls outside it. That boundary appears in the scope statement and nowhere else, so the scope
statement is the part to have ready.

| The item | What it proves for you | What it will not carry | What you must be able to say |
|---|---|---|---|
| **SOC 2 Type I** -- an examination report, point-in-time | A licensed firm's opinion that your controls were suitably designed as of one date | That any control ever operated. It observed a design, not a period of behavior, and it looked at your organization rather than your code | Why Type I rather than Type II, and the date the first Type II period ends |
| **SOC 2 Type II** -- an examination report over a period | A licensed firm's opinion on operating effectiveness across a period, typically six to twelve months, against the Trust Services Criteria you elected | That your distributed software was examined; it commonly sits outside the scope boundary. The report is an attestation, not a certificate -- there is no pass mark to claim | What the scope covered, and every exception the firm listed, offered rather than waited for |
| **ISO/IEC 27001** -- a management-system certificate | That an accredited certification body certified your information security management system for a stated scope | That your product was certified. It is not "the international SOC 2" -- that instrument is an opinion plus exceptions, this one a certificate plus a scope statement | The scope printed on the certificate, and who accredited the body that issued it |
| **HITRUST CSF** -- a validated assessment of controls and environment | A third-party validated result at one of three named tiers -- e1, i1 and r2 -- which are not interchangeable | That your distributable software was assessed. What is assessed is your controls and environment, which can include the environment operating the software | Which tier you hold and what the assessment took in, without leaning on the tier name alone |
| **Sector and program instruments** -- a PCI DSS validation document, a FedRAMP or StateRAMP authorization, a CJIS policy audit | That the operating environment for a named offering was assessed against that program's own rules | Anything about software a customer installs and runs themselves. Nor that a third party did the assessing: a PCI DSS self-assessment questionnaire is completed and signed by you | Which offering was in scope, whether it was independently assessed or self-assessed, and whether it is the offering being bought |

Three things that will be used against you if you leave them for the buyer to find:

- **An examination period that produced no exception at all invites a question of its own.** The
  scope passage and the exceptions passage are the report; the rest is structure. Be ready to explain
  a clean run.
- **A certificate scope of one office or one business unit is entirely ordinary,** and narrower than
  a reader takes it to be. Do not let them take it wider. The standards publisher issues nothing --
  the accredited body does.
- **HITRUST sits in the same set as the program instruments, and none outranks the others.** Its two
  lower tiers are fixed core control sets, the highest is tailored and risk-based, so a tier name
  alone says less than it sounds like: offer tier and scope. Never circulate control text, which is
  licensed. And the body that writes a program standard is often not the body that sets your
  customer's validation requirement.

---

## Software layer: evidence about the thing you are selling

Nothing above examined your code or your build. These four do, and for each the buyer's real
question is how it was produced. Three you write about your own system, so their weight comes from
the discipline behind them rather than from who issued them -- describe the discipline. Testing
evidence is the exception and the strongest item here, in one form only: an external assessment or a
penetration test, the one software-layer artifact a third party issues. Expect that request by name,
and expect it to test whether you offer your own tooling's output instead.

| The item | What it proves for you | What it will not carry | What you must be able to say |
|---|---|---|---|
| **A software bill of materials** | Which components are in the build | Whether any of it is exploitable in the configuration the buyer will run. A conforming SBOM can still be inaccurate | That it is generated by the build for the exact released artifact, rather than hand-maintained |
| **A data flow diagram** | Where data crosses a trust boundary -- which is where a control has to exist, and where a threat model becomes checkable | Anything at all, if the boundaries are not marked. Unmarked, it is a diagram rather than a security artifact | Which boundaries are marked, and which control sits on each one |
| **Cryptography documentation** | Which algorithms and modes you use, and where data is encrypted in transit and at rest | Key management. "AES-256" names an algorithm, not a key lifecycle | Who holds the keys, where they live, and what happens on rotation and on revocation |
| **Testing evidence** | That a named class of defect was looked for, by a named method, on a named date and against a named version | The absence of anything. Static analysis and dynamic testing find different classes of defect, and neither substitutes for the other | Who ran it, and whether they were independent of the team that wrote the code |

Two follow-ups you will be asked, so answer them unprompted:

- **For testing evidence:** what was in scope, which version was tested, and what triggers the next
  run -- a change, or a date on the calendar?
- **For a hosted platform's SBOM:** does it describe the runtime production environment, or a
  build-time source manifest? Those answer different questions, and only one describes what is
  running.

Three of these rows are outputs of a process rather than documents to write at diligence time.
[Secure development](SECURE-DEVELOPMENT.md) is where the data flow diagram and the testing regime
come from; [Dependency integrity](DEPENDENCY-INTEGRITY.md) is where the SBOM comes from, with the
dated citation behind the runtime-versus-build distinction. Build them there and diligence becomes a
retrieval task.

---

## Legal instruments: evidence about who pays when it goes wrong

These allocate liability. They do not establish security, and offering them as though they do is the
same overclaim in a third costume: a complete set says what happens after a failure, nothing about
its likelihood. They are read for their clock definitions and notification paths, which is where
they are weakest and always checkable.

| The item | What it proves for you | What it will not carry | What you must be able to say |
|---|---|---|---|
| **A vulnerability remediation commitment (the SLA)** | An agreed maximum elapsed time, and a contractual remedy if you miss it | That anything is fixed faster | When the clock starts, when it stops, and how a reporter reaches a human outside business hours |
| **An incident response plan** | That a written plan exists, with named roles and a notification path | That anyone has ever executed it | The date of your last exercise, and what changed as a result |
| **Data-handling agreements** -- a data processing agreement and its sector equivalents, such as a business associate agreement | Who may process the data, for what purpose, through which subprocessors, and who must notify whom within what time | That the processing is secure. It allocates duty and liability, which is a different thing | Your current subprocessor list, how customers are told when it changes, and where the breach-notification clock starts |

Two places these fail, both common and both yours to fix before anyone reads them:

- **An SLA fails at the clock's start point, not at the number.** A clock that starts when you accept
  triage is unbounded whatever the number on it, and a careful buyer will say so. "Patch released" is
  also not "patch deployed": for software the customer runs, deployment is their side of the line,
  and the agreement should say which side it means.
- **A plan with no exercise date is a document, not a capability.** Run one and date it.

[Secure development](SECURE-DEVELOPMENT.md) is where the disclosure path and the remediation clock
come from.

---

## What this page does not do

- **It lists at least the items a buyer commonly asks for, and is not a complete diligence list.**
  Holding everything here is not approval, and being asked for something not listed is ordinary.
- **Not legal advice.** What you are obliged to provide is decided by a contract clause, not by a web
  page. Nothing here has been reviewed by counsel.
- **No assessor, tool, format or vendor is named.** The rows describe instruments, not the market
  that sells them.
- **No status, version or edition claim appears here.** Those live on the reference page, each
  carrying the date it was checked, so a stale fact is visible as one.
- **A complete packet is not a secure product, and a thin packet is not an insecure one.** Both are
  evidence about what a buyer can check -- more modest than either side of a procurement
  conversation usually wants. Claiming more is the failure this page is about.

---

## Where to go next

| If you need | Read |
|---|---|
| Which of these reach your own organization | [Which standards apply to you](WHICH-STANDARDS-APPLY.md) |
| One row per document, as a lookup, with statuses and dates | [Security standards reference](STANDARDS-REFERENCE.md) |
| What to require of your own developers | [The CISO summary](CISO-SUMMARY.md) |
| The process a build must satisfy, including dynamic testing, the data flow diagram and disclosure | [Secure development](SECURE-DEVELOPMENT.md) |
| SBOM, provenance, and what gets published | [Dependency integrity](DEPENDENCY-INTEGRITY.md) |
| Whether a written rule can actually stop a change | [Automated compliance in CI](CI-ENFORCEMENT.md) |

**None of this certifies anything.** MIT licensed. Adapt it, put your own name on it, and delete
anything you cannot stand behind.
