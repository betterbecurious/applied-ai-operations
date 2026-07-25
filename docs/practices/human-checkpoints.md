# Human checkpoints

`Verb: Ship` · [← Index](../../README.md)

---

## What it is

The specific points where a person looks at the output before it goes anywhere, chosen deliberately rather than applied everywhere.

## Why it matters

**"Review everything" is operationally identical to reviewing nothing.**

This is the position of the page and it is worth being precise about *why*, because "a human reviews all output" sounds like the responsible answer and is usually the negligent one.

Attention is finite and it decays with use. Ask someone to check forty low-stakes drafts a day and by the second week they are scanning, by the fourth they are clicking. This is not a discipline problem — it is what happens to every human doing high-volume, low-yield checking. When almost everything you check is fine, you stop being someone who checks and become someone who approves.

So a blanket review policy produces the *worst* available arrangement: real cost, the appearance of control, and no actual inspection at the one moment it mattered. Worse, it moves accountability onto a person who was structurally set up to miss it.

**Deliberate placement beats blanket caution.** Three checkpoints on the three things that can actually hurt you get read properly, because they're rare enough to still feel like events. Forty checkpoints get skimmed.

The related trap: reviewing at the wrong *point*. A checkpoint after the irreversible step is not a checkpoint, it's a notification. Checkpoints belong where a decision can still change.

## How to use it

**Put a checkpoint where an error would be expensive and hard to reverse.** Two conditions, both required. Expensive-but-reversible usually needs a good undo, not a gate. Cheap-and-irreversible is fine. It's the intersection that needs a human.

Concretely, checkpoints go:

- **Before anything leaves the organisation.** External communication, filings, anything with your name on it going to a customer, a regulator, or the public.
- **Before anything is written to a system of record.** A bad draft is a nuisance. A bad record propagates and gets trusted later.
- **Where untrusted input first meets a system that acts.** See [connectors](../tools/connectors.md) and [failure modes](failure-modes.md).
- **On the cases your [eval sheet](../tools/eval-sheet.md) says the system is worst at.** This is the highest-value placement and almost nobody does it, because it requires having measured. A documented blind spot with a human in front of it is a solved problem.
- **Anywhere the cost of being wrong lands on someone who didn't choose the system** — a patient, a tenant, a claimant.

**And explicitly nowhere else.** Write down where checkpoints are *not*, so the absence reads as a decision rather than an oversight.

**Make the checkpoint answer a specific question.** "Review this" produces skimming. "Does every figure in this appear in the source document?" produces checking. A checkpoint with a question is a task; a checkpoint without one is a vibe.

**Give the reviewer the power to stop it.** A gate that can only be approved isn't a gate. Say out loud that rejecting, escalating, or doing it by hand are sanctioned outcomes — otherwise the path of least resistance is approval, and you've built a formality.

**Check the checkpoint.** Rubber-stamping is invisible unless you look for it. If nothing has been rejected in three months, either the system is flawless or the gate is decorative.

## Worked example

*(Invented. Bramfield District Council is not a real authority.)*

A housing benefit team introduced a system that drafted decision letters explaining entitlement calculations. The initial policy was "a caseworker reviews every letter" — around 90 letters a week.

**What went wrong, and what replaced it:**

- **Weeks 1–3** — genuine review. Caseworkers caught three real errors.
- **Week 6** — average review time had fallen from 4 minutes to under 40 seconds. Nothing rejected in ten days.
- **Week 8** — a letter went out stating an entitlement figure that didn't match the calculation. It had been "reviewed."
- **The replacement** — blanket review dropped, three named checkpoints instead.
- **Checkpoint 1** — any letter reducing or ending an existing entitlement. ~7 a week. Question: *does the stated figure match the calculation, and is the change reason cited from the schedule?*
- **Checkpoint 2** — any case flagged with a vulnerability marker. ~4 a week. Reviewed by a senior officer.
- **Checkpoint 3** — any case the system flags as outside its tested range. ~2 a week.
- **Everywhere else** — no review. Written down as a decision, with the eval numbers backing it.

<details>
<summary><strong>Expand: why those three, and what happened to the other 77 letters</strong></summary>

**Why the blanket policy failed, precisely.** It wasn't that caseworkers were careless. 90 letters a week, of which roughly 87 were routine and correct, is a task that trains you to approve. By week six the review had become a scroll to the bottom and a click — and the team was aware of it, which made it worse, because everyone assumed someone else was still reading properly.

**How the three were chosen — from the eval sheet, not from intuition.**

The system scored 54/60. The failures were not evenly spread:

- Entitlement *increases* and continuations: 30/30. Never wrong, across every run.
- Entitlement *reductions and terminations*: 15/20. Every failure in the whole eval was here — the calculation was right, but the cited reason for the change was sometimes generic rather than the specific schedule clause.
- Cases with a vulnerability marker: only 2 cases in the sheet, both fine, but **too few to have measured anything.** That checkpoint exists because of ignorance, not because of a known failure — which is a legitimate and underused reason for a gate.

So checkpoint 1 covers the measured weakness, checkpoint 2 covers the unmeasured population, and checkpoint 3 covers the system's own admission of unfamiliarity.

**What happened to the other 77 letters:** nothing. They went out unreviewed. This was the part that took a month to get agreed, and the argument that carried it was the eval sheet — 30/30 across four dated runs is a stronger claim about entitlement-increase letters than "a caseworker glanced at it for 38 seconds."

**Two things they added to stop it rotting:**

1. **A rejection log.** If a checkpoint rejects nothing for two months, it gets examined — either the gate is decorative or it's in the wrong place. Checkpoint 1 rejects something roughly monthly. It is working.
2. **The eval sheet re-runs quarterly**, and the checkpoint placement is reviewed against it. When the failure distribution moves, the gates move. Both are named in the [handover package](handover-package.md), owned by the team leader.

The letter volume being reviewed dropped by 85%, and the review that remained was real.

</details>

## What goes wrong

**Review everything.** Covered at length above. It is the default, it feels responsible, and it decays into clicking within weeks.

**The checkpoint is after the irreversible step.** Reviewing the sent email. Approving the filed record. Common when the gate is bolted on at the end rather than designed in.

**No specific question.** "Have a look at this" gets a look. It does not get a check.

**The reviewer can't say no.** No route to reject, no time budgeted, and rejecting makes them the person who slowed things down. Approval becomes structural.

**The reviewer can't tell.** They're shown output with no source to check it against. Being asked to verify a figure with no access to the calculation is theatre.

**Placement by intuition rather than measurement.** Gates end up on the scary-feeling cases rather than the failing ones. Those are frequently different, and the eval sheet is the only thing that tells you which is which.

**Nobody audits the gate.** Three months of unbroken approvals gets read as a well-performing system rather than an unread one.

## When not to use it

- **On cases the eval sheet shows are reliably correct**, where the output is reversible and low-stakes. Say so explicitly, with the numbers attached — an undefended absence looks like an oversight.
- **When the reviewer has no context to judge with.** Fix the context or move the gate. A checkpoint someone can't actually perform is worse than none, because it launders responsibility.
- **As a substitute for [the loop](the-loop.md).** Checkpoints catch individual bad outputs. They do not tell you the system is getting worse — only dated columns do that. Teams reach for checkpoints because they're cheap and immediate; they're a filter, not a control system.
- **As a way to avoid deciding.** "We'll have a human check it" is often a way to ship without asking what happens when the system is wrong. Answer that question first; the checkpoint is the consequence of the answer, not a replacement for it.

---

`Last reviewed: 2026-07-25`
