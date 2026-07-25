# The loop

`Verb: Evaluate` · [← Index](../../README.md)

---

## What it is

```
Design → [ Build ⇄ Evaluate ] → Ship
```

The two brackets in the middle. You change something, you measure it against the same cases you measured last time, and the comparison tells you whether you improved it or broke it.

## Why it matters

**This is the most important page in the reference, and the idea it carries is the one everything else is arranged around.**

**Evaluation is a control system, not a report card.**

A report card is a judgement delivered at the end: 52 out of 60, well done. It's a number about the past. A control system is something you steer with: it runs, you read it, you adjust, you run it again, and the *difference between the readings* is the signal.

Which is why **an eval you run once tells you nothing.** Not "tells you a little" — nothing. A single score of 52/60 is uninterpretable. Is that good? Compared to what? You have no idea whether the system is improving, degrading, or holding, because you have exactly one data point and improvement is a shape, not a value.

The second run is where the entire value arrives. That's when 52 becomes 57 and you know your change worked, or 52 becomes 48 and you know it didn't, or 52 stays 52 and you know your clever refinement did nothing and you should stop polishing it.

**This is the difference between a demo and a system.** A demo is a thing that worked once, in front of people, on cases chosen by the person demoing. A system is a thing you can change on a Tuesday and still trust on Wednesday. The only mechanism that converts the first into the second is a loop — not better engineering, not a better model, not more careful prompting. A loop.

And it's what makes a system *changeable*. Without one, every modification is a gamble, so eventually nobody modifies anything, and a frozen system in a moving organisation degrades by standing still. **The loop is not overhead on top of building. It is what makes building safe.**

## How to use it

**One change at a time.** Change two things, score improves, and you've learned nothing about either. This is tedious and it is the whole method.

**Re-run the same cases.** Not fresh ones. The comparison requires the cases to be fixed — new cases measure a different thing and quietly reset your baseline.

**Keep every dated column.** Never overwrite a run. The [eval sheet](../tools/eval-sheet.md) is a history, and the history is the product.

**Watch the columns you weren't trying to change.** The most valuable thing a loop catches isn't the improvement you aimed for — it's the regression you didn't. A change that raises accuracy and drops refusal correctness looks like a win in every way except the one that matters.

**Make it cheap or it won't happen.** A loop that costs half a day gets run twice. Automate the running with [Claude Code](../tools/claude-code.md) and the loop becomes something you do casually, which is the only version that's real.

### When to stop looping

The question people don't ask, and the reason projects run on forever.

Stop when **any** of these is true:

- **Two consecutive rounds produce no meaningful change.** You've found the plateau. More rounds will produce noise you'll mistake for signal.
- **The remaining failures are all the same kind, and it's a kind you can route around.** Don't fix it — write it into [known limitations](handover-package.md) and put a [checkpoint](human-checkpoints.md) there. A documented blind spot with a human in front of it beats six more rounds.
- **You're changing the cases instead of the system.** Unmistakable sign you're done, or that you're gaming your own test.
- **It's good enough for the actual decision it feeds.** A first-pass triage that a human reviews doesn't need 60/60. Ask what the output is *for*.

**Perfection is not the target and chasing it is a failure mode.** The target is: good enough, measured, with the gap written down and owned.

## Worked example

*(Invented. Pellworth Insurance is not a real company.)*

A claims team built a system to draft first-response letters. Baseline on 14 May: 44/60 across accuracy, tone, and correct escalation.

**Four rounds, one change each:**

| Round | Change | Score | Read |
|---|---|---|---|
| 1 · 21 May | Added explicit output format | 44 → 51 | Big win. Most of it was structural. |
| 2 · 28 May | Added two worked examples | 51 → 54 | Real, smaller. |
| 3 · 4 Jun | Rewrote tone instructions to be warmer | 54 → **49** | **Regression.** Tone up 4, escalation down 9. |
| 4 · 11 Jun | Reverted round 3, added escalation checklist | 49 → 56 | Recovered plus a bit. |
| 5 · 18 Jun | Reordered instructions | 56 → 56 | Nothing. **Stopped here.** |

They shipped at 56/60 with four known failures documented, all of them the same kind.

<details>
<summary><strong>Expand: round 3, and why they stopped at 56</strong></summary>

**Round 3 is the round that justifies the whole practice.**

The change was reasonable: claimants had said the letters felt cold, so the tone instructions were rewritten to be warmer and more empathetic. Read individually, the new letters were *clearly better*. Everyone on the team preferred them. If they had judged by reading a handful of outputs — which is what almost everyone does — they would have shipped it.

The escalation column dropped from 17/20 to 8/20.

The warmer register had reframed the escalation cases. A claim that should have produced *"this claim requires assessment by our specialist team before we can respond substantively"* now produced *"we completely understand how distressing this must be, and we want to reassure you that we're looking after this for you personally."* Warm, human, and it silently converted a hard stop into a soft reassurance. The specialist referral was gone.

Nobody reading that letter would flag it. It's a nice letter. It is exactly the failure mode in [failure modes](failure-modes.md): **wrong but looks right** — and it looked right *better* than the correct version did.

Only the column caught it. A number next to another number, on cases where someone had written down in advance that the correct answer was to escalate.

**Why they stopped at 56 rather than pushing for 60.**

The four remaining failures were all one kind: claims involving more than one policy, where the letter addressed only the first. Fixable, probably — several more rounds of work.

They didn't fix it. They wrote it into known limitations, and added one line to the handler's checklist: *multi-policy claim → do not send the draft, escalate to a senior handler.* Twenty minutes instead of three weeks, and arguably safer, because a human now looks at exactly the cases the system is worst at.

Round 5 is the other half of the lesson. A sensible-sounding change produced a score of 56, identical to round 4. Two rounds without movement, so they stopped. Without the number, someone would still be reordering instructions today, feeling productive.

</details>

## What goes wrong

**There's no second run.** The eval is built, run, celebrated, and never opened again. The single most common failure in this entire reference.

**Several things change between runs.** The score moves and nothing is learned. Especially likely when someone "tidied things up" between rounds.

**Only the target column gets read.** The change did what it was meant to; something else broke. Regressions hide in the columns nobody was watching.

**Cases get changed mid-loop.** Usually well-intentioned — "these cases are unrealistic." Now every previous column is meaningless.

**Small movements get over-read.** 54 to 55 on twenty cases scored by one human is noise. Don't build a theory on it.

**The loop never ends.** No stopping rule, so it runs until attention runs out — which means it ends at an arbitrary point rather than a defensible one.

**Judging by reading a few outputs.** The most seductive one, because it feels responsible and it's how round 3 above would have shipped. Fluency is not accuracy, and reading outputs measures fluency.

## When not to use it

- **When nothing will change.** A frozen system doesn't need a loop — it needs a scheduled re-run to catch [drift](failure-modes.md), which is a different, slower thing.
- **Before you have a baseline.** The loop starts at the second measurement. The first is just the [eval sheet](../tools/eval-sheet.md).
- **On genuinely one-off work.** Nothing to regress.
- **When you're past the stopping condition.** Continuing to loop after two flat rounds isn't diligence — it's optimising noise, and you'll eventually "improve" the system into a worse one.
- **As a substitute for shipping.** A system in permanent evaluation is a system nobody uses. At some point it has to reach a person, with a [handover package](handover-package.md).

---

`Last reviewed: 2026-07-25`
