# Context engineering

`Verb: Build` · [← Index](../../README.md)

---

## What it is

Deciding what information reaches the model, and from where.

Three places it can come from: the [Project](../tools/project.md) (true for everything in this container), the [Skill](../tools/skill.md) (true for this kind of task), and the message (true right now). Context engineering is the discipline of putting each thing in exactly one of them.

## Why it matters

**This deliberately replaces "prompting best practices," and the replacement is the position of the page.**

Prompt engineering made sense when models were brittle. Phrasing genuinely moved results, so people accumulated technique — role-play openers, threats and inducements, incantations about taking a deep breath. That body of technique was real, and it has been largely obsoleted by models that are simply better at understanding what you meant.

What has *not* been obsoleted, and has become more important, is the structural question: **what does the system know, where does it live, and who maintains it?**

The reason this matters more than phrasing is durability. A cleverly-worded prompt is a personal artifact — it lives in your chat history and dies with your memory of it. A correctly-placed instruction is an organisational one: it applies every time, someone else can read it, and when it's wrong you can find it and fix it in a single place.

Put bluntly: prompting is about how you ask. Context engineering is about what the system already knows before you ask. Only the second one survives you leaving.

**The minimal prompting core is a short section, not a discipline** — see below. It's about five things long, all of them obvious, and once you've internalised them there is nothing else in that field you need.

## How to use it

**The placement test.** For every piece of information, ask: *how often is this true?*

| True... | Goes in | Example |
|---|---|---|
| Every time, in this container | **Project instructions** | "British English. Never name a client in external text." |
| Every time we do *this task* | **Skill** | "Delay replies open with the specific delay, then the revised ETA as a date." |
| Only right now | **The message** | "This one's from a customer we've already compensated twice." |

**One thing, one place.** The rule that does the most work. Duplication is not redundancy — it's two copies that will disagree, and when they do you won't be able to tell which one is being followed.

**Move things up when you notice repetition.** Typing the same clarification in the third message of every conversation means it belongs in the Project. This is the main way a container gets good: not by design, but by promotion.

**Move things down when they're not universal.** An instruction in the Project that's only true half the time is worse than nothing, because it trains everyone — including the model — to treat the instructions as approximate.

**Less context beats more.** Every irrelevant document in the knowledge slot competes with the relevant one. The instinct to add everything "just in case" reliably makes output worse, and reliably feels like diligence.

### The minimal prompting core

The whole of it:

1. **State the actual task.** Not the topic. "Summarise this for a committee that hasn't read it" beats "summarise this."
2. **Specify the output format explicitly.** Sections, length, order. The single highest-leverage sentence in most requests.
3. **Give one worked example.** Worth more than three paragraphs of description, every time.
4. **Say what to do when something's missing.** Otherwise the gap gets filled plausibly and silently.
5. **Put the long reference material before your question, not after.**

That's the list. It is not a discipline. If you find yourself reading a fifth article about prompting technique, the thing you're actually missing is an [eval sheet](../tools/eval-sheet.md).

## Worked example

*(Invented. Northfield Care Group is not a real organisation.)*

Seven residential homes, one central team writing incident reports for the regulator. Reports were inconsistent between homes. The team's fix had been an increasingly elaborate prompt — by the time anyone looked at it, roughly 600 words, pasted from a document at the start of every conversation, with three people maintaining slightly different copies.

**What the 600 words turned out to be, once sorted:**

- **Project instructions** — regulator's terminology, British English, factual register, never name a resident, never speculate on cause. *True in every report.*
- **Skill: `medication-incident`** — the five mandatory fields, the escalation threshold, the specific refusal case. *True for one report type.*
- **Skill: `fall-incident`** — a different five fields, a different threshold. *True for a different report type.*
- **The message** — this resident, this date, these observations. *True once.*
- **Deleted outright** — about 150 words of "be thorough," "use professional language," "think carefully." Doing nothing, taking up room.

<details>
<summary><strong>Expand: the two instructions that were quietly contradicting each other</strong></summary>

The 600-word prompt contained both of these, about 200 words apart:

> *"Report objectively and factually. Do not speculate about causes."*

and, in the section on medication errors:

> *"Where possible, indicate the likely point of failure in the administration process to support the home's improvement planning."*

Those are in direct conflict, and nobody had noticed in fourteen months — because nobody had ever read the prompt top to bottom. It had been appended to, never reviewed. Each addition was sensible when it was written.

The result was reports that were inconsistent *in a way that looked like inconsistency between homes*, and was actually the same document contradicting itself depending on which instruction happened to dominate. The team had spent months trying to fix it by standardising practice between homes.

**How the placement test resolved it:** "do not speculate" is true of every report → Project. "Indicate the likely point of failure" is true only for medication incidents, where the regulator specifically asks for it → the `medication-incident` Skill, reworded to name the exception explicitly: *"This report type requires a stated likely point of failure, as an exception to the standing instruction against speculation. Base it only on the recorded sequence."*

Two things happened. The reports became consistent. And the *exception became visible* — a thing the organisation could look at and decide about, rather than an inconsistency it kept trying to train out of its staff.

That's the real argument for this practice. Well-placed context isn't just more reliable. It's legible: you can read it and find the contradiction.

</details>

## What goes wrong

**Everything lives in one giant prompt.** Pasted at the start of every conversation, maintained by nobody, contradicting itself in the middle. Extremely common. Always contains dead instructions and usually at least one contradiction.

**The same instruction lives in three places.** They drift. Debugging becomes impossible because you can't tell which copy won.

**Project instructions that are only sometimes true.** Teaches everyone to treat the instructions as suggestions.

**Adding context to fix a quality problem.** The instinctive response to a bad output is to add another sentence. Twenty bad outputs later you have a 600-word prompt. Often the fix is deletion.

**Politeness and motivation filler.** "Be thorough," "this is very important," "take your time." It's inherited from an earlier era and it's now just tokens.

**Nobody reads it end to end.** Prompts get appended to, never reviewed. Read yours top to bottom once a quarter and delete on sight.

**Reaching for phrasing when the problem is knowledge.** No wording fixes a system that can't see the document it needs. That's a [connector](../tools/connectors.md) question.

## When not to use it

This one isn't optional — any system with more than one instruction is doing context engineering, well or badly. But don't over-apply it:

- **On a one-off conversation.** Just ask. Placement discipline is for things that repeat.
- **Before you know what's invariant.** You can't sort instructions by "how often is this true" until you've done the task enough times to know. Work by hand first, then sort.
- **As a substitute for evaluation.** Perfectly-placed context, never tested, is a tidy system of unknown quality. Placement makes it maintainable; only [the loop](the-loop.md) makes it good.
- **When the real problem is scope.** If instructions can't be sorted because the container does five unrelated jobs, that's a [Project](../tools/project.md) problem. No amount of sorting fixes a container that shouldn't exist.

---

`Last reviewed: 2026-07-25`
