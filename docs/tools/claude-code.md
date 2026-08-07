# Claude Code

`Verb: Build` · [← Index](../../README.md)

---

## What it is

A version of Claude that runs in a terminal, in your editor, or in a desktop app, and can read and write files on your machine, run commands, and work across a whole folder rather than one pasted document.

It is named for developers and it is genuinely good for developers. **This page is not about that.** It is about why anyone who works with folders full of documents should be using it, and it assumes you have never opened a terminal.

Installation and current platforms: [Anthropic's Claude Code documentation](https://docs.claude.com/en/docs/claude-code/overview).

## Why it matters

Two reasons, and the second is the one people miss.

**One: some work is file-shaped, and chat is the wrong container for it.** You cannot paste sixty documents into a message. You can point Claude Code at a folder of sixty documents and ask what's in them, which ones contradict each other, and which ones haven't been touched since 2022. The unit of work becomes the folder, not the message, and a large class of tedious work stops being tedious.

**Two: it is how you run an [eval sheet](eval-sheet.md) more than once.**

This is the argument that earns the page. [The loop](../practices/the-loop.md) says an eval you run once is worthless. But re-running twenty test cases by hand, pasting each one, and recording each score is about forty minutes of miserable clerical work — and a control system that costs forty minutes of misery to operate is a control system that will be operated exactly twice.

Claude Code takes the eval from "an afternoon" to "a command." That is the difference between a system you can safely change and a system everyone is slightly afraid to touch. Automation of the *checking* is worth more than automation of the doing.

**You do not need to write code to use it.** You need to be able to say what you want in plain language and read what it proposes before agreeing. It writes the script. You review the behaviour.

## How to use it

**Start with reading, not writing.** Point it at a folder and ask questions. "What's in here?" "Which of these mention the 2024 tariff schedule?" "Summarise every document modified this year." No files change, nothing can break, and you learn how it behaves at zero risk.

**Then let it write, in a copy of the folder.** Take a duplicate. Let it reorganise, rename, extract, convert. Compare against the original. Delete the copy if it's wrong.

**Then use version control** — which is a fancy phrase for "a way to undo anything, permanently." Ask Claude Code to set it up and explain it. You will not regret this and you will eventually need it.

**Review before you agree.** It proposes actions and waits. That pause is the control, and clicking through it without reading is the entire risk profile of the tool. Anything that deletes, sends, publishes, or overwrites deserves an actual read.

**Then automate the eval.** Once your test cases are in a file, ask it to run each one and write the scores to a sheet. This is the highest-value thing on the page and it is why non-developers should care.

### Local or cloud — which is really a question about what you committed

Claude Code runs either on your own machine or on a fresh cloud machine that clones your repository. The local one sees your files, your network, and your personal configuration. The cloud one sees **only what is committed** — and that half is the part worth remembering, because it quietly decides whether what you built is yours or the organisation's. Configuration sitting in your personal Claude folder travels nowhere. Configuration committed to the repo travels: to a colleague, to a cloud session, to a run scheduled for next quarter. This is the [Project](project.md) argument wearing different clothes — the container is what makes a system transferable rather than personal — and it is why a `CLAUDE.md` and a committed `.claude/` directory belong in any repo you intend to hand over.

The corollary is the one people learn late: **state belongs in the repo, not in the conversation.** A long session feels like a project record and isn't one — it's a tool you happen to still be holding, and its memory is lossy. End each sitting by having Claude write the current state to a file, and commit it. Then any future session — yours next week, a colleague's, or a scheduled one that re-runs your [eval sheet](eval-sheet.md) — picks the thread up in two sentences. Which surfaces exist and what each can do changes quickly, so check [the Claude Code documentation](https://code.claude.com/docs/en/claude-code-on-the-web) rather than anything written here. The local-versus-cloud split underneath it is stable.

## Worked example

*(Invented. The Marbury Trust is not a real organisation.)*

A grants administrator maintained a [Skill](skill.md) that drafted first-pass assessments of grant applications against six funding criteria. It worked. The problem was the eval: twenty past applications with known outcomes, scored by hand, taking half a day. She had run it once, in March. By June she had made four changes to the Skill and had no idea whether it was still as good.

**What Claude Code did:**

- **Read the folder** — twenty application PDFs and a CSV of known outcomes, already sitting on her machine.
- **Ran each one** through the Skill and recorded the score against the known outcome.
- **Wrote the results** to a dated column in the eval sheet, next to March's.
- **Took four minutes** instead of half a day, and she wrote no code.
- **Found the regression immediately** — one of her four changes had dropped criterion 4 from 18/20 to 11/20.

<details>
<summary><strong>Expand: what she actually asked for, and what the regression turned out to be</strong></summary>

**The request, roughly as typed:**

> In this folder there are 20 application PDFs and a file `outcomes.csv` with what each one was actually awarded. Run each application through my assessment Skill, score its output against the six criteria the way `eval-sheet.csv` is set up, and add the results as a new dated column. Don't overwrite the March column. Show me the script before you run it.

That last sentence matters. She read the script — not to check the syntax, but to check the *behaviour*: is it reading the right files, is it writing where I expect, can it overwrite March. Those are ordinary comprehension questions, not programming ones.

**The regression:** in May she had added an instruction to keep assessments under 300 words. Criterion 4 was "evidence of financial sustainability," which requires citing specific figures from the applicant's accounts. Under the word limit, the assessments dropped the figures and asserted the conclusion instead — still fluent, still plausible, no longer evidenced.

Nobody would have caught this by reading a few outputs. They read *better* than the March versions: tighter, more confident, less hedged. The only thing that surfaced it was a dated column next to another dated column.

She kept the word limit and added an exception for criterion 4. Re-ran: 19/20. Total elapsed time, including the fix, under an hour — and the reason it was an hour rather than a project is that running the eval had stopped being expensive.

</details>

## What goes wrong

**People assume it's not for them.** By far the biggest loss on this page, and it's a naming problem rather than a capability one. The grants administrator above wrote nothing.

**Actions get approved without reading.** The approval step becomes muscle memory within a day. This is the one genuine risk and it's entirely behavioural.

**It's pointed at the only copy.** Work in a duplicate until you have version control. Then work anywhere.

**It's used as a chatbot with file access.** Asking it one small question at a time wastes what it's for. The leverage is in "do this across all of these, and tell me what didn't fit."

**Secrets sit in the folder.** It reads what's there, including the spreadsheet of passwords someone left in 2021. See [data hygiene](../practices/data-hygiene.md).

**The eval script is written and then never run.** Automating the eval and not scheduling it produces a faster way to do nothing. Put it in the [handover package](../practices/handover-package.md) with a named owner and a trigger.

## When not to use it

- **When the work isn't file-shaped.** One document, one question — use the chat interface. Nothing to be gained here.
- **When you can't yet describe what you want in plain language.** The constraint is clarity, not technical skill. Vague instructions plus file-writing access is the one genuinely bad combination.
- **On material you can't put through it.** The [data hygiene](../practices/data-hygiene.md) rules apply to folders exactly as they apply to messages.
- **When you won't read the proposals.** If you'll approve everything unread, restrict it to read-only questions. That's still most of the value, at none of the risk.
- **To avoid learning the underlying process.** If you can't do the task by hand, you can't tell whether it did it correctly — and you certainly can't score the eval.

---

`Last reviewed: 2026-07-25`
