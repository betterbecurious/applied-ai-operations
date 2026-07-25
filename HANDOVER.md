# 📦 Repo Handover Brief — applied-ai-operations

> 📦 **Handover brief for Claude Code.** Rewritten 25 Jul 2026 as a **standalone public asset** — all course dependencies removed. Read §12 first: five decisions need answering before website work starts.
>
> **Status note (2026-07-25):** §12 has been answered. Resolutions are recorded inline in §12 and in [`CHANGELOG.md`](CHANGELOG.md). This file is kept as the specification of record — the standard every page is checked against during review.

# 1. What this is

**Applied AI Operations** is a public, opinionated reference for putting AI systems inside an organisation and making them stay there.

It exists to be pointed at. When someone asks *"which tools should we actually use, and how do we use them well?"*, the answer is a link to this repo.

**The thesis it argues:** The bottleneck with AI is not the model. It's that almost nobody knows how to put one inside an organisation and make it stay there.

**The spine:** Design · Build · Evaluate · Ship — with a loop in the middle.

`Design → [ Build ⇄ Evaluate ] → Ship`

Evaluation is a control system, not a report card. An eval you run once tells you nothing; an eval you re-run makes regressions visible. That distinction is the most important idea in the repo and every page should be consistent with it.

**This repo is standalone.** It has no prerequisites, no curriculum, no cohort, no timeline. Other programs and workshops may link to it; it never references them. If a sentence only makes sense to someone enrolled in something, cut the sentence.

# 2. Audience

Anyone responsible for making AI produce real work in a real organisation. In practice:

- Operations and department leads evaluating whether this is worth their time
- Technically-minded non-developers who will build the thing themselves
- Developers who can build fine but have never had to hand something over
- Consultants and peers looking for a defensible position to argue with

**Write layered, not levelled.** A non-technical reader must never hit an unexplained term; a developer must never feel condescended to. The way to serve both is precision and brevity, not two versions of every page.

**Assume no facilitator.** There is nobody in the room to clarify, correct, or answer questions. Every page stands alone, states its own prerequisites, and links rather than assumes.

**Assume a paid Claude subscription**, but do not assert which plan unlocks which capability — plan boundaries change. Where a tool has plan requirements, instruct the reader to check current Anthropic documentation and link to it rather than hardcoding a claim that will go stale.

# 3. Editorial stance

**This is not documentation. It is a position.**

Anthropic's docs are complete, free, and better maintained than this repo will ever be. Competing on coverage is a losing game and produces something nobody needs. The value here is entirely in judgement: what matters, what doesn't, what order to learn it in, and what to deliberately ignore.

Practical consequences for every page:

- **Take a position.** "Use X, not Y, because Z" beats "there are several approaches."
- **Say what to skip and why.** The exclusions in §11 are content, not omissions. Publish them.
- **Link out for reference detail.** Explain *why* and *when*; link to Anthropic's docs for *how exactly*.
- **Every claim must survive a hostile reader.** This is public and it has an author's name on it.
- **No hedging filler.** No "it depends," no "as always, your mileage may vary."

# 4. What to build

Two surfaces, one body of content:

1. **`README.md` + `/docs`** — the written reference. **Canonical.**
2. **A single-page website** — the same content, browsable, plus one working interactive tool (§7).

The website must be generated from or deliberately synced with the docs. Two hand-maintained copies will diverge within a month. State in the repo which is canonical.

# 5. Repo structure

```
applied-ai-operations/
├── README.md              ← thesis, spine, index, last-reviewed date
├── HANDOVER.md            ← this file
├── CHANGELOG.md           ← what changed, when, why
├── docs/
│   ├── tools/             ← 5 pages
│   └── practices/         ← 6 pages
├── templates/
│   ├── eval-sheet.csv
│   ├── process-brief.md
│   └── handover-package.md
└── site/
    └── index.html         ← single file, no build step
```

# 6. Content spec

Every page follows the same shape:

**What it is → why it matters → how to use it → one worked example → what goes wrong → when not to use it.**

That last section is mandatory and is where most of the credibility lives. Tag each page with the verb it serves. Five-minute read maximum.

## The Tools (5) — what you use

| Tool | Must cover |
|---|---|
| **Project** | The container: instructions, knowledge, scope. Why the container is what makes a system transferable rather than personal. |
| **Skill** | The reusable unit, and the atom of this whole reference. Anatomy, when to write one, when a plain instruction is enough instead. |
| **Connectors** | Making a system touch real data instead of pasted text. The permission and data-exposure question belongs here, prominently. Argue for starting with exactly one. |
| **Claude Code** | For anything file-shaped, and for eval scripts. Framed as an assistant for people who don't write code — not a developer tool guide. |
| **Eval sheet** | A spreadsheet. Deliberately *not* a framework. Columns, how to choose ~20 cases, how to score, why crude beats absent. |

## The Practices (6) — how you use them well

| Practice | Must cover |
|---|---|
| **Context engineering** | What belongs in Project instructions vs. the Skill vs. the message. This deliberately replaces "prompting best practices" — state that replacement openly and defend it. The minimal prompting core (explicit output format, worked examples, stating the actual task) is a short section, not a discipline. |
| **The loop** | Build ⇄ Evaluate. Why one eval run is worthless. How to tell when to stop looping. Why this is the difference between a demo and a system. |
| **Human checkpoints** | Where review gates go, and why "review everything" is operationally identical to reviewing nothing. Deliberate placement over blanket caution. |
| **Failure modes** | The short list, kept short: output that is wrong but looks right; systems following instructions found in untrusted documents; drift as inputs change. Include how to provoke each on purpose. |
| **Data hygiene** | What never enters a prompt, a repo, or a shared Project. Secrets, personal data, client-confidential material. Plainly, without a compliance lecture. |
| **The handover package** | What you actually give someone: runbook, eval sheet with real numbers, named owner, escalation path, known limitations. **No vendor tool does this, which is exactly why it needs a page.** This is the most differentiated page in the repo — weight it accordingly. |

# 7. The Process Filter (the one interactive tool)

A diagnostic for deciding whether a given process is a sensible target. Works standalone, shareable on its own, and is the single most linkable thing in the repo.

**Axis A — is this process a good target?** Score 1–3 each:

**Frequent** (daily or weekly, not annual) · **Boring** (repetitive, rule-ish) · **Text-shaped** (language and documents in, same out) · **Measurable** (countable before and after) · **Tolerant** (a wrong answer gets caught before it causes harm)

**Axis B — can this organisation receive it?** Score 1–3 each:

**Owned** (one identifiable person cares and will answer questions) · **Reviewable** (someone will actually look at the output) · **Operable** (someone can run it on Monday without you)

**Compute the axes separately and never sum them.** The entire diagnostic value is in the gap. High A with low B is the classic rotting demo — a well-chosen process in an organisation that cannot absorb it. The tool must name that pattern in words, not just return numbers. Write plain-language verdicts for each quadrant.

# 8. Website spec

**Single `index.html`. No build step, no npm, no framework.** Must work by double-clicking the file and deploy to GitHub Pages unchanged. People will fork this; a toolchain is a barrier and a maintenance liability.

Scroll-spy sidebar navigation, one section per tool and practice, verb tags visible, the Process Filter embedded and usable without scrolling past everything else.

**Do not fake interactivity.** Everything else is well-structured reading. Accordions that hide content from someone trying to learn are a net negative.

# 9. Freshness

This reference sits on a fast-moving product surface. A stale public reference is worse than none.

- **Visible `Last reviewed: YYYY-MM-DD`** in the README and in the site footer. Not "last updated" — reviewed.
- **`CHANGELOG.md`** with what changed and why.
- **A stated review cadence** in the README, and a documented routine: what to re-check, in what order.
- **Prefer linking to Anthropic docs over restating them.** Every restated product detail is a future correction.

Treat this as a living radar with a review routine, not a library.

# 10. Constraints

- **English throughout.** A German version may follow; never mix within a page.
- **No real company, client, or individual data. Anywhere.** This repo is public. Invented examples only.
- **No private infrastructure references or self-hosting assumptions.**
- **No course, cohort, curriculum, or programme language.**
- Every page maps to exactly one of the four verbs.
- Every product-specific claim either links to current documentation or is written to survive it changing.

# 11. Out of scope — publish these as exclusions

These are deliberate positions, not gaps. Put them in the README with one line of reasoning each:

- **Multi-agent orchestration and sub-agent architectures** — the most over-recommended pattern relative to how often it's the right answer
- **Model comparison and benchmarks** — stale on publication, and rarely the constraint
- **RAG theory** — the concept matters; the theory doesn't, for this audience
- **"Prompt engineering" as a discipline** — superseded by context engineering
- **A survey of the AI vendor landscape** — the most commoditised content in existence

> ⚠️ Publishing opinions invites argument, and the author's name is on it. Each exclusion needs a defensible one-liner — not a shrug.

# 12. Open decisions — needed before website work

**Resolved 2026-07-25.** Reasoning in [`CHANGELOG.md`](CHANGELOG.md).

1. **Brand and design tokens.** ⏳ **Still open.** Site stays on a neutral default until answered.
2. **Attribution and contact.** ✅ Published under **Billie Jeurink**. Contact: `billie@bjeurink.com`.
3. **License.** ✅ **CC BY 4.0.** Adaptable and teachable-from, with credit required.
4. **Contributions.** ✅ **Issues open, pull requests closed.** Staleness signal preserved; editorial voice stays with one person.
5. **Domain.** ✅ **GitHub Pages default.** Revisit if the reference is linked widely enough to earn a custom domain.

# 13. Build order

1. **`README.md`** — thesis, spine, index, exclusions with reasoning. Establishes voice and position.
2. **One tool page and one practice page**, complete, for review. **Do not write the remaining nine before the format is signed off.**
3. Remaining pages.
4. Templates.
5. Website last — content must be settled first.

> ⚠️ Step 2 is not optional. Format gets validated on one example before scaling.
