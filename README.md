# Applied AI Operations

**The bottleneck with AI is not the model. It's that almost nobody knows how to put one inside an organisation and make it stay there.**

This is an opinionated reference for closing that gap: which tools to use, how to use them well, and what to deliberately ignore.

`Last reviewed: 2026-07-25`

---

## The spine

```
Design → [ Build ⇄ Evaluate ] → Ship
```

Four verbs. Every page in this reference serves exactly one of them, and says which.

The loop in the middle is the point. **Evaluation is a control system, not a report card.** An eval you run once tells you nothing — it produces a number with nothing to compare it to. An eval you re-run makes regressions visible, which is the only way to change a working system without breaking it quietly.

If you take one idea from this reference, take that one. Everything else here is downstream of it.

## Who this is for

Anyone responsible for making AI produce real work in a real organisation:

- Operations and department leads deciding whether this is worth their time
- Technically-minded non-developers who will build the thing themselves
- Developers who can build fine but have never had to hand something over
- Consultants and peers looking for a defensible position to argue with

There are no prerequisites and no reading order beyond the one below. Every page stands alone and states what it assumes.

This reference assumes you have a paid Claude subscription. It deliberately does not claim which plan unlocks which capability — those boundaries change, and a reference that hardcodes them is wrong within a quarter. Where a plan matters, you'll be pointed at [Anthropic's current documentation](https://docs.claude.com/).

## This is not documentation

Anthropic's docs are complete, free, and better maintained than this repo will ever be. Competing on coverage is a losing game that produces something nobody needs.

The value here is entirely judgement: what matters, what doesn't, what order to learn it in, and what to skip. So every page takes a position, and links out for reference detail rather than restating it.

---

## The Tools — what you use

| Page | Verb | The position |
|---|---|---|
| [Project](docs/tools/project.md) | Design | The container is what makes a system transferable rather than personal. |
| [Skill](docs/tools/skill.md) | Build | The reusable unit, and the atom of this whole reference. |
| [Connectors](docs/tools/connectors.md) | Build | Start with exactly one. Permission and data exposure are the design question, not the plumbing. |
| [Claude Code](docs/tools/claude-code.md) | Build | For anything file-shaped, and for eval scripts. Not just for developers. |
| [Eval sheet](docs/tools/eval-sheet.md) | Evaluate | A spreadsheet. Deliberately not a framework. Crude beats absent. |

## The Practices — how you use them well

| Page | Verb | The position |
|---|---|---|
| [Context engineering](docs/practices/context-engineering.md) | Build | What goes in the Project vs. the Skill vs. the message. This replaces "prompting best practices." |
| [The loop](docs/practices/the-loop.md) | Evaluate | Build ⇄ Evaluate. Why one eval run is worthless, and how to tell when to stop. |
| [Human checkpoints](docs/practices/human-checkpoints.md) | Ship | "Review everything" is operationally identical to reviewing nothing. |
| [Failure modes](docs/practices/failure-modes.md) | Evaluate | Three that matter, and how to provoke each on purpose. |
| [Data hygiene](docs/practices/data-hygiene.md) | Design | What never enters a prompt, a repo, or a shared Project. |
| [The handover package](docs/practices/handover-package.md) | Ship | What you actually give someone. No vendor tool does this. |

## The Process Filter

A diagnostic for deciding whether a given process is a sensible target — before you build anything.

It scores two axes separately and **never sums them**. Axis A asks whether the process is a good target. Axis B asks whether the organisation can receive it. All of the diagnostic value is in the gap between them: a high-A, low-B score is the classic rotting demo — a well-chosen process in an organisation that cannot absorb it.

→ **[Run it in the browser](site/index.html)** · [Paper version](templates/process-brief.md)

## Templates

| File | What it's for |
|---|---|
| [`templates/eval-sheet.csv`](templates/eval-sheet.csv) | The eval sheet, with columns and a worked row. Open it in anything. |
| [`templates/process-brief.md`](templates/process-brief.md) | The Process Filter as a fillable page, for when you're away from a browser. |
| [`templates/handover-package.md`](templates/handover-package.md) | The document you hand over. Fill every section or don't hand over. |

## The website

[`site/index.html`](site/index.html) is the whole site: one file, no build step, no npm, no framework. Open it by double-clicking it. Deploy it to GitHub Pages unchanged. Fork it without installing anything.

**`docs/` is canonical.** The site is generated from it — it is never a second copy to keep in step by hand. After editing any page, regenerate:

```bash
python3 build-site.py
```

That script is a maintenance tool for whoever edits this repo, not a build step for whoever reads it. `site/index.html` is committed. Where the site and the docs ever disagree, the docs are right.

---

## Deliberately out of scope

These are positions, not gaps.

**Multi-agent orchestration and sub-agent architectures.** The most over-recommended pattern relative to how often it is the right answer. Nearly every problem presented as needing a fleet of coordinating agents is one badly-scoped Skill and a checkpoint. Orchestration multiplies the failure surface and the debugging cost while the underlying task stays the same size.

**Model comparison and benchmarks.** Stale on publication, and rarely the constraint. If your system is failing, the cause is almost never that you picked the wrong frontier model — it's context, scope, or the absence of an eval. Use the newest capable model available to you and spend the saved attention on the loop.

**RAG theory.** The concept matters and is covered where it belongs, in [Connectors](docs/tools/connectors.md). The theory — chunking strategies, embedding model selection, retrieval metrics — is a research literature for people building retrieval systems. You are not building one. You are pointing a system at data that already exists.

**"Prompt engineering" as a discipline.** Superseded by [context engineering](docs/practices/context-engineering.md), and this reference says so openly. Treating phrasing as a craft with its own body of technique made sense when models were brittle. The durable questions are about what information reaches the model and from where — not how you word the ask.

**A survey of the AI vendor landscape.** The most commoditised content in existence, and obsolete faster than anything else here. Comparison tables are written by people who have not deployed any of the options.

---

## Freshness

This reference sits on a fast-moving product surface. A stale public reference is worse than none, so this one carries a **reviewed** date rather than an updated one — the claim is that someone checked, not that someone edited.

**Review cadence: monthly**, and immediately after any significant Claude platform release.

The review routine, in order:

1. **Check every outbound link resolves.** Anthropic's docs reorganise. Dead links are the first visible sign of rot.
2. **Re-read the five tool pages against current product behaviour.** These carry the most product-specific surface and go stale first.
3. **Check for hardcoded plan or capability claims** that have crept in. Replace with a link.
4. **Re-read the exclusions.** An exclusion that is no longer defensible is a page that needs writing.
5. **Update the `Last reviewed` date** here and in `LAST_REVIEWED` in `build-site.py`, then run `python3 build-site.py` so the site footer matches.
6. **Add a `CHANGELOG.md` entry** — even when nothing changed. "Reviewed, no changes" is information.

## Contributing

**Issues, yes. Pull requests, no.**

An opinionated reference and an open contribution model pull against each other — merged prose from many hands converges on the hedged, comprehensive, position-free thing this repo exists not to be.

But the failure mode of a solo-authored public reference is silent staleness, and that is the worse risk. So: [open an issue](../../issues) if something is out of date, if a link is dead, or if you think a position here is wrong. Arguments are welcome and get read. The editing stays with one person.

## License

[CC BY 4.0](LICENSE). Adapt it, teach from it, fork it, translate it — credit **Billie Jeurink** and link back.

## Author

Written and maintained by **Billie Jeurink**.

If you're trying to do this inside your own organisation and want a second pair of eyes on it: **billie@bjeurink.com**. Whether that turns into work is a separate question — a specific question about something on these pages gets a specific answer either way.
