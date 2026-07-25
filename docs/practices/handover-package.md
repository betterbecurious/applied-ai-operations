# The handover package

`Verb: Ship` · [← Index](../../README.md)

---

## What it is

The set of things you hand a person so that a working AI system becomes *theirs*: a runbook, an [eval sheet](../tools/eval-sheet.md) with real numbers in it, a named owner, an escalation path, and a written list of known limitations.

Five items. It fits in one document. [There's a template](../../templates/handover-package.md).

## Why it matters

**No vendor tool does this, which is exactly why it needs a page.**

Every platform in this space will help you build. None of them will help you leave. There is no button that transfers understanding, and no amount of product polish substitutes for a person knowing what to do when the output looks wrong on a Tuesday.

This is where AI projects actually die. Not at the model, not at the integration — at the moment the person who built it stops paying attention. The system keeps running. It keeps producing output. The output slowly stops being right, and because nobody was told what "right" looked like or who was supposed to check, nobody notices for four months.

The distinction the whole reference turns on applies here too. [An eval you run once tells you nothing](the-loop.md). An eval sheet you hand over with real numbers in it, to someone who knows they're expected to re-run it, is a control system that outlives you.

**A system without a handover package is not shipped. It's abandoned in production.**

## How to use it

Write it *before* you finish building. If you can't fill in a section, that's a design finding, not a paperwork problem — a system with no plausible owner should not be built, and you'd rather learn that in week one.

### 1. The runbook

What this does, how to run it, what normal looks like.

Written for someone who was not in any of the meetings. Include: what the system is for in two sentences, the actual steps to run it, an example of good output, and — the part people skip — **an example of bad output**, so the reader can recognise failure without having to define it themselves.

Length: two pages. If it needs more, the system is too big to hand over in one piece.

### 2. The eval sheet, with real numbers

Not a blank template. **The sheet you actually ran, with the scores you actually got, dated.**

This is the item most often omitted and the one that carries the most weight. A blank template says "you should test this." A filled sheet says "here is what this scored on 20 real cases on 12 March, this is the bar, re-run it when something changes." One is advice. The other is a baseline, and a baseline is the only thing that makes a regression visible.

Include the cases it *failed*. A sheet that's 20 out of 20 means the cases were too easy and tells the next owner nothing about where the edges are.

### 3. A named owner

**One person. A name, not a team.**

"The operations team owns it" means nobody owns it. The owner is the person who gets the question when output looks wrong, and who is expected to re-run the eval when the inputs change.

Get their agreement before you write their name down. An owner who learns about their ownership from a document is not an owner.

### 4. An escalation path

What the owner does when it's beyond them — with a name and a route, not a department.

Two branches, and they are different: **it's broken** (the system errors, produces nothing, or produces obvious nonsense), and **it's wrong** (the system produces confident, plausible, incorrect output). The second is more dangerous and more likely, and it needs a stated destination. Include what to do in the meantime: usually "stop using it and do it by hand," which needs saying out loud so it feels like a sanctioned option rather than a failure.

### 5. Known limitations

Everything you know it can't do, written down while you still remember.

This section buys you more credibility than the rest of the document combined, and it is the one people soften. Don't. "This has never been tested on multi-currency invoices" is worth more to the next person than any amount of confident description. Every limitation you leave out becomes a surprise that someone else pays for.

Include the ones that feel obvious to you. Obvious-to-you is precisely the category that doesn't transfer.

## Worked example

*(Invented. Thornbury Housing Trust is not a real organisation.)*

Thornbury Housing Trust built a system that reads inbound maintenance requests and drafts a triage summary: category, urgency band, the relevant policy clause, and a suggested response. It worked well in testing. The contractor who built it had two weeks left.

**What they handed over:**

- **Runbook** — 2 pages. What it does, how to run it, one good output, and one genuinely bad output: a damp complaint miscategorised as cosmetic because the tenant had described it politely.
- **Eval sheet** — 20 real anonymised requests, scored 1–3 on category accuracy, urgency accuracy, and clause correctness. Dated 4 March. Scored 17/20, 19/20, 20/20. **The three category failures were listed by name**, all of them understated urgency, all of them politely-worded.
- **Owner** — Priya, maintenance coordinator. Asked first, agreed, and sat in on the last two eval runs so the sheet wasn't a stranger.
- **Escalation** — *Broken:* Dan in IT. *Wrong:* Priya flags it, stops using it for that request type, triages by hand, and re-runs the eval sheet. If two consecutive runs drop below 16/20 on any column, the system comes out of service until reviewed.
- **Known limitations** — Never tested on requests over 400 words. Never tested on requests in any language but English. Systematically understates urgency when the tenant is polite. Has no access to the tenancy history system, so it cannot see repeat complaints — **a repeated request looks identical to a first one.**

That last limitation was the most valuable line in the document. It wasn't a bug and nothing could be done about it in two weeks. But because it was written down, Priya knew to check repeat-complaint history manually — and six weeks later, when a tenant's third damp report came in politely worded, it got escalated by a human who knew the system's blind spot.

The system didn't catch it. The handover package did.

## What goes wrong

**It gets written on the last day.** By then you've forgotten which decisions were deliberate and which were accidents, and the limitations section is empty because everything currently feels obvious.

**The owner is a team.** The single most common defect. Diffuse ownership performs exactly like no ownership, but looks better on a slide.

**The eval sheet is handed over blank.** Enormously common, and it silently converts a control system back into a suggestion. Without a baseline there is nothing to regress *from*.

**Limitations are softened into strengths.** "Works best with structured input" is a limitation wearing a suit. Say "fails on unstructured input, here's an example."

**Nobody re-runs anything.** The handover happens, everyone nods, and the eval sheet is never opened again. This is a management problem more than a documentation one — which is why the owner has to agree out loud, and why the escalation path needs a stated threshold that takes the system out of service.

**It's handed to someone who can't act on it.** Perfect package, recipient with no authority to take the system offline or change it. The package needs to reach someone who can actually pull the lever.

## When not to use it

Honestly: almost never. If a system is going to be used by someone other than you, it needs this.

The real judgement calls are about **scale**:

- **Personal tools that stay personal.** A Skill you use alone doesn't need a handover package. But be honest about "stays personal" — the moment a colleague asks you to run it for them, it has escaped, and this is the most common way an undocumented dependency gets created.
- **Genuine throwaways.** A one-week system for a one-week problem. Say so explicitly and put an end date on it, or it will still be running in a year, unowned.
- **Prototypes shown but not deployed.** No package needed — but say the word "prototype" out loud, in the room, every time. Demos get promoted to production by enthusiasm alone, and the [Process Filter](../../site/index.html)'s Axis B exists precisely to catch this.

Where the package genuinely scales down: a small system might handle all five items in half a page. **Half a page with all five beats six pages with four of them.** The item people drop is the eval sheet with real numbers, and that's the one that matters most.

---

`Last reviewed: 2026-07-25`
