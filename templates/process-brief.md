# Process brief — the Process Filter on paper

The [interactive version](../site/index.html) does the arithmetic. This one is for meetings, whiteboards, and printing.

**Copy this page. Fill it in about one specific process.** If you can't name the process in a single sentence, that's your first finding.

---

**Process:** ______________________________________________

**Filled in by:** _______________________  **Date:** ______________

---

## Axis A — is this process a good target?

Score each 1–3. **1 = no, 2 = partly, 3 = yes.**

| | Question | Score | Note |
|---|---|:---:|---|
| **Frequent** | Does it happen daily or weekly — not annually? | ___ | |
| **Boring** | Is it repetitive and rule-ish rather than novel each time? | ___ | |
| **Text-shaped** | Language and documents in, language and documents out? | ___ | |
| **Measurable** | Can you count something before and after? | ___ | |
| **Tolerant** | Would a wrong answer get caught before it caused harm? | ___ | |

**Axis A total: ___ / 15**

## Axis B — can this organisation receive it?

| | Question | Score | Note |
|---|---|:---:|---|
| **Owned** | Is there one identifiable person who cares and will answer questions? | ___ | |
| **Reviewable** | Will someone actually look at the output? | ___ | |
| **Operable** | Could someone run this on Monday without you? | ___ | |

**Axis B total: ___ / 9**

---

## Do not add these together

The two axes measure different things and summing them destroys the entire diagnostic. A 13 and a 3 average out to something respectable and describe a disaster.

**The gap between them is the finding.**

Convert each to a rough band:

- **Axis A:** 12–15 = high · 8–11 = middling · below 8 = low
- **Axis B:** 7–9 = high · 5–6 = middling · below 5 = low

## Read your quadrant

### High A · High B — Build it

A good process in an organisation that can absorb it. This is the one you build, and it is rarer than anyone expects. Start with the smallest complete version, put an [eval sheet](eval-sheet.csv) under it before you tune anything, and write the [handover package](handover-package.md) while you build rather than at the end.

### High A · Low B — **The rotting demo**

The classic and most expensive failure in this whole field, and the reason the two axes are scored separately.

You have picked an excellent process. You will build something that works. You will demo it and people will be impressed. And then it will quietly stop being used, because there is no owner, or nobody reviews the output, or it can only be run by you.

**The problem is not technical and cannot be solved by building better.** Every additional hour of engineering makes this worse, not better — a more impressive artifact with nowhere to land.

Fix Axis B first, and it is usually one specific thing. Which of the three is lowest?

- **Not owned** → find the person, or accept that there isn't one. A name, not a team. If nobody will put their name on it, that is the answer to whether it should be built.
- **Not reviewable** → work out who looks at the output and when, before it exists. See [human checkpoints](../docs/practices/human-checkpoints.md).
- **Not operable** → whatever you build must be runnable by someone with no context. This constrains the design, so it has to be known now rather than discovered at handover.

Do not build until at least one of those has moved.

### Low A · High B — Wrong process, right organisation

Encouraging, actually. The organisation is ready — there's an owner, someone reviews, someone can operate it. You have picked the wrong target.

Look at which Axis A score is lowest and pick a different process nearby:

- **Not frequent** → the effort will never repay. Find the weekly version.
- **Not boring** → too much judgement per instance. Look for the routine part *inside* it, which is often the data-gathering rather than the decision.
- **Not text-shaped** → if the real work is in a spreadsheet, a diagram, or a phone call, this is not the tool.
- **Not measurable** → you will never know whether it works, and you will never be able to defend it. Find something countable.
- **Not tolerant** → errors reach the world uncaught. Either add a checkpoint upstream or choose something where being wrong is survivable.

Keep the organisational readiness. Spend it on a better target.

### Low A · Low B — Not this, not yet

Don't build. Say so plainly and early — this is the most valuable output the filter produces, and the cheapest.

The honest version: *"This isn't the right process, and we're not currently set up to run one anyway."* Both are fixable, neither is fixed by starting.

---

## Before you leave the room

Three questions, and the answers matter more than the numbers:

1. **If this works perfectly, whose job changes, and have they been asked?**

   _______________________________________________

2. **Who gets the phone call when the output is wrong in six months?**

   _______________________________________________

3. **What happens if you stop paying attention to this in three weeks?**

   _______________________________________________

If question 2 has no name in it, your Axis B score is optimistic regardless of what you wrote above.

---

**Verdict:** ______________________________________________

**Decision:** ☐ Build it  ☐ Fix Axis B first  ☐ Pick a different process  ☐ Not now

**Revisit on:** ______________
