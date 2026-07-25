# Eval sheet

`Verb: Evaluate` · [← Index](../../README.md)

---

## What it is

A spreadsheet. Roughly twenty rows, one per test case, with columns for the input, what good looks like, the score, and the date it was run.

That's it. [Take the template](../../templates/eval-sheet.csv) and open it in whatever you already have.

## Why it matters

**This is deliberately not a framework, and that is the position of the page.**

There is a whole product category selling evaluation platforms with dashboards, LLM-as-judge pipelines, and statistical rigour. Some of it is good. Almost none of it is what you need, because your actual situation is that you have **no** evaluation, and the distance from zero to a spreadsheet is the only distance that matters. The distance from a spreadsheet to a platform is a rounding error by comparison.

**Crude beats absent.** A sheet of twenty cases scored 1–3 by one person with an opinion will catch nearly every regression that matters. It is also the only version that will still be run in six months, because it costs twenty minutes and requires nothing to be installed, funded, or maintained.

And the sheet is the thing that makes the whole reference work. [The loop](../practices/the-loop.md) needs something to compare against. The [handover package](../practices/handover-package.md) is hollow without a filled-in sheet with real numbers in it. **The eval sheet is what turns an opinion about quality into a fact about quality**, and facts are what survive a change of owner.

One more time, because it's the thesis: an eval you run once tells you nothing. It gives you a number with nothing to compare it to. **The value is entirely in the second run.**

## How to use it

**Choose about twenty cases.** Fewer than ten and one bad case swings the result. More than thirty and you'll stop running it, which is the only real failure. Twenty is the number because twenty gets re-run.

**Choose them like this — the mix matters more than the count:**

| Roughly | Kind of case | Why |
|---|---|---|
| 10 | **Typical** | The ordinary work. Establishes the baseline. |
| 5 | **Edge** | Real but awkward — the long one, the incomplete one, the one in a different format. |
| 3 | **Should refuse** | Cases where the correct output is "stop and ask." Almost always omitted, and they're where the expensive failures live. |
| 2 | **Known past failures** | Things it got wrong before. These are your regression tests. |

Use real historical cases with known-good answers where you can. Cases you invent tend to be cases the system already handles, because you invented them with the system in mind.

**Score 1–3. Resist adding precision you don't have.**

- **3** — I'd send this. Maybe a word.
- **2** — Right shape, needs real editing.
- **1** — Wrong, or would have to be redone.

Score each *dimension* separately if the output has more than one thing that can be wrong — accuracy and tone fail independently, and averaging them hides both. Three columns is usually plenty.

**Score against a written standard, not a feeling.** Write "what good looks like" for each case *before* you look at the output. Otherwise you're grading on fluency, and fluent-and-wrong is the failure mode this whole exercise exists to catch.

**Date every run and keep the old columns.** The columns side by side are the entire product. Never overwrite a run.

**Re-run whenever anything changes** — the Skill, the Project instructions, a connected source, or the model. And re-run on a calendar even when nothing changed, because [drift](../practices/failure-modes.md) doesn't announce itself.

## Worked example

*(Invented. Ashgrove Legal is not a real firm.)*

A small conveyancing firm built a system to extract key terms from lease documents into a standard summary. It felt accurate. "Felt accurate" was the entire quality process.

**The sheet they built:**

- **20 cases** — 10 standard residential leases, 5 awkward (a 200-page commercial lease, two scanned-and-OCR'd, one with handwritten amendments), 3 that should refuse (missing pages, an unsigned draft, a lease in Welsh), 2 past failures.
- **3 score columns** — term accuracy, completeness, correct refusal. Scored 1–3.
- **First run, 14 March** — 52/60. Good on standard leases, poor on scans, and **0/3 on refusals**: it summarised the unsigned draft as though it were executed.
- **The refusal failures were the finding.** Nothing else on the sheet was news.
- **Second run, 2 April, after one instruction change** — 57/60, refusals 3/3.

<details>
<summary><strong>Expand: the sheet's structure, and the case that changed their mind</strong></summary>

**Columns, left to right:**

`case_id` · `case_type` · `input_ref` · `what_good_looks_like` · `2026-03-14_accuracy` · `2026-03-14_completeness` · `2026-03-14_refusal` · `2026-04-02_accuracy` · `2026-04-02_completeness` · `2026-04-02_refusal` · `notes`

Dates in the column headers, old runs never overwritten. That's the whole design. It opens in anything and it will still open in ten years.

**The case that changed their mind — case 17, the unsigned draft.**

`what_good_looks_like`: *"Identifies that the document is an unexecuted draft and stops. Does not produce a summary of terms."*

What it actually produced was a clean, well-structured, entirely accurate summary of the terms in the draft — with no indication anywhere that the document wasn't a completed lease. Every extracted term was correct. Score: 1.

This is the failure the sheet exists for. Read on its own, that output is *good*. It's accurate, it's well-formatted, and a junior reading it at 5pm files it. It is only wrong in a way you can see when someone has written down, in advance, that the right answer was to refuse.

**The fix** was one line added to the Skill: check for execution — signatures, dates, and a completed parties block — before extracting anything; if absent, report the document as a draft and stop.

**What the second run then justified:** it wasn't the 52→57. It was the evidence that fixing the refusal cases hadn't broken the standard ones. Accuracy on the ten standard leases held at 28/30. Without the March column, a change that fixed one thing and quietly broke another would have looked exactly like an improvement.

</details>

## What goes wrong

**It's built and run once.** The most common failure by a wide margin, and it produces a number that feels like rigour and functions as decoration. One run has nothing to compare to.

**Every case is a happy path.** All twenty are things the system does well, so the sheet scores 58/60 forever and detects nothing. If you're not failing some cases, your cases are too easy.

**No refusal cases.** Everything is "produce the right output," nothing is "recognise you shouldn't." The dangerous failures live here.

**Scoring drifts.** Three months in, "2" means something different. Keep the written standard next to the score, and re-read it before each run.

**The old columns get overwritten.** Someone tidies the sheet. The comparison — the only thing of value — is gone.

**It's scored by the person who built the system.** Optimism is not a character flaw here, it's a structural bias. Where you can, have someone else score, or at least score before you look at whose change it was.

**It gets upgraded into a project.** Someone proposes a proper evaluation framework. Six weeks later there is no framework and no spreadsheet either.

## When not to use it

Almost never — if a system produces output anyone relies on, it needs a sheet. But honestly:

- **Before you know what good looks like.** You can't score against a standard you can't write. Do the work by hand first. This is the one legitimate "later."
- **For genuinely one-off work.** Nothing to regress.
- **When the output is purely subjective** and no two reviewers would agree. Rare, and usually a sign the task isn't specified — but if you truly can't write `what_good_looks_like`, a score column is theatre.
- **When you'd build the framework instead.** If the choice is a real platform in six weeks or a spreadsheet this afternoon, take the spreadsheet. You can always upgrade a habit. You can't upgrade a habit you never formed.

---

`Last reviewed: 2026-07-25`
