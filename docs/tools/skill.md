# Skill

`Verb: Build` · [← Index](../../README.md)

---

## What it is

A Skill is a folder containing a markdown file of instructions, plus any files those instructions need. You write it once. It loads when the task calls for it, and stays out of the way when it doesn't.

That's the whole mechanism. The interesting part is what it lets you stop doing.

For the current file format, folder layout, and how Skills load across Claude apps and Claude Code, see [Anthropic's Agent Skills documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview). This page is about when to write one and how to write a good one — not the syntax.

## Why it matters

**A Skill is the atom of this entire reference.** Everything else is context around it: the [Project](project.md) is the container a Skill lives in, [connectors](connectors.md) are the data it reaches, the [eval sheet](eval-sheet.md) is how you know it works, and the [handover package](../practices/handover-package.md) is how someone else inherits it.

The reason it earns that position: a Skill is the smallest unit of work that survives leaving your head.

An instruction you type into a chat produces one good output and disappears. A Skill produces the same output next week, for a colleague, on a Monday you're not there. It is the difference between being good at using AI and having built something.

It is also the smallest unit you can *test*. You cannot run an eval against a habit. You can run an eval against a Skill, change one line, and re-run it — which is the loop, and the loop is where quality comes from.

## How to use it

**Write a Skill when all three are true:**

1. **The task recurs.** Not necessarily often — quarterly is fine — but it comes back.
2. **The output has a shape.** There's a right format, a required section, an established tone, a checklist that must be covered.
3. **You would have to re-explain it.** If handing the task to a new colleague would take a paragraph of context, that paragraph is the Skill.

**The anatomy that works:**

| Part | What goes in it |
|---|---|
| **Name and description** | The description is load-bearing — it's what determines whether the Skill fires at the right moment. Describe the *situation*, not the capability. "When drafting a supplier response to a delivery complaint" beats "Supplier communication helper." |
| **The task** | What this produces, in one or two sentences. Written for someone who has never seen it. |
| **Required inputs** | What you must supply, and what to do when it's missing. A Skill that silently invents a missing input is a [failure mode](../practices/failure-modes.md), not a convenience. |
| **The procedure** | Numbered steps. Short. If a step needs three paragraphs of explanation, it's probably two steps. |
| **Output format** | Explicit and exact. Section headings, field order, length. This is the single highest-leverage part of most Skills. |
| **One worked example** | Real input, real output, end to end. Worth more than any amount of describing. |
| **Refusal conditions** | When to stop and ask instead of proceeding. Most Skills need this and most Skills don't have it. |

**Keep it under two pages.** A Skill that sprawls is two Skills, or it's a [Project instruction](project.md) that wandered into the wrong place.

**Write the output format before the procedure.** Deciding what comes out clarifies what has to happen, and it's the part you'll tune most during the loop.

### When a plain instruction is enough instead

Most tasks do not need a Skill, and this is the mistake people make in their first enthusiastic week.

Skip the Skill and just ask when:

- **It's a one-off.** A Skill you use once cost more than it saved.
- **The task is fully specified by the request itself.** "Summarise this in five bullets" needs no scaffolding. You just said the whole thing.
- **You don't yet know what good looks like.** Write the Skill *after* you've done the task by hand three or four times and can point at what you want. Skills written before you have taste encode the wrong thing, then defend it.
- **The stable part belongs to every task, not this one.** Tone of voice, house style, "always use British English" — those go in Project instructions, once, rather than being copy-pasted into eleven Skills where they will drift apart.

## Worked example

*(Invented. Meridian Freight is not a real company.)*

Meridian Freight's operations team answers roughly forty delivery-delay complaints a week. Every reply needs the same things: an acknowledgement, the actual revised ETA from the tracking system, a specific reason, and a compensation offer that follows a fixed policy band. The replies are inconsistent, and the inconsistent ones generate follow-up complaints.

**The Skill — `delay-complaint-reply`**

> **Description:** When drafting a customer reply about a delayed or missed delivery for Meridian Freight operations.
>
> **Task:** Produce a ready-to-send email replying to a delivery-delay complaint.
>
> **Required inputs:** consignment number, customer's message, current tracking status, delay cause code.
> If the delay cause code is missing, stop and ask. Do not infer a cause from the tracking status.
>
> **Procedure:**
> 1. Open with a direct acknowledgement of the specific delay. No "we apologise for any inconvenience."
> 2. State the revised ETA as a date, not a duration.
> 3. Give the cause in one plain sentence, mapped from the cause code table below.
> 4. Apply the compensation band: <24h → none, 24–72h → 15% refund, >72h → full refund plus a named contact.
> 5. Close with what happens next and who owns it.
>
> **Output format:** Subject line, then body under 150 words. No bullet points — this is a customer email. Sign off with the handler's name.
>
> **Refuse if:** the customer has mentioned legal action, injury, or perishable/pharmaceutical goods. Escalate to the duty manager instead.
>
> **Example:** *[full input → full output pair]*

What changed: replies went out in the same shape every time, the compensation policy stopped being applied from memory, and the escalation cases got routed instead of answered. The team still reads every reply before it sends — that's the [checkpoint](../practices/human-checkpoints.md), and it stays.

Note what the refusal condition is doing. It's not a safety disclaimer. It's the recognition that the two-percent of cases where this Skill is wrong are exactly the cases where being wrong is expensive.

## What goes wrong

**The description is too vague to fire.** By far the most common failure, and it looks like the Skill "not working." If the description says what the Skill *is* rather than *when it applies*, it loads at the wrong moments or not at all. Fix the description first, always, before touching the body.

**It grows into a manual.** A Skill accumulates edge cases until it's six pages and nobody can tell which instructions are still live. Split it, or move the general parts up into the Project.

**It encodes a preference nobody agreed to.** You wrote what *you* think a good handover email looks like. Three people now send emails in your voice. Sometimes that's the goal; make sure it's a decision.

**No refusal conditions.** The Skill handles the ninety-percent case beautifully and handles the dangerous ten-percent case beautifully too — confidently, in the same tone, wrongly. Write down where it should stop.

**It was never evaluated.** You tested it on the three examples you had in mind while writing it, which is not a test — those examples are what you designed against. Build the [eval sheet](eval-sheet.md) from cases you did not have in mind.

## When not to use it

- **When you can't yet describe what good output looks like.** Do the task by hand until you can. A premature Skill locks in a guess.
- **When the task is genuinely judgement-heavy every time.** If the "procedure" is a paragraph of caveats and the real answer is "it depends on the situation," you're trying to systematise something that isn't a system yet.
- **When the instruction is universal.** Belongs in [Project instructions](project.md). One place, not eleven.
- **When nobody will own it.** A Skill with no named owner is a Skill that will be wrong in six months and nobody will notice. That's a [handover](../practices/handover-package.md) problem, and it will sink a technically perfect Skill.

---

`Last reviewed: 2026-07-25`
