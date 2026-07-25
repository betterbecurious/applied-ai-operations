# Data hygiene

`Verb: Design` · [← Index](../../README.md)

---

## What it is

What never goes into a prompt, a repo, or a shared Project.

Three categories: **secrets**, **personal data**, and **client-confidential material**. That's the page. The rest is where the edges are.

## Why it matters

Not because of a compliance framework. Because of two properties of these systems that people consistently misjudge.

**One: a shared container widens the audience.** The whole benefit of a [Project](../tools/project.md) is that other people can use it. Which means everything in its knowledge slot is now visible to everyone who has it, forever, including the people who join next year. Someone uploads a spreadsheet to answer today's question and has quietly changed who can see it.

**Two: pasted text goes somewhere.** Not somewhere sinister — into a service, under a data processing agreement, subject to retention rules that vary by product and plan. The problem isn't that this is dangerous; it's that most people have never checked what their organisation's agreement actually says, and "I pasted the client's file into a chat" is a sentence you don't want to discover you can't defend. Check your own agreement and Anthropic's [current terms](https://www.anthropic.com/legal/commercial-terms) rather than trusting a claim on a page like this one.

**No compliance lecture.** You know that personal data is regulated. What's useful is the list of things people actually do wrong, which is short and specific.

## How to use it

### Never, no exceptions

**Secrets.** API keys, passwords, tokens, connection strings, private keys. Not in a message, not in a knowledge file, and above all **not in a repo** — a committed secret is in the history even after you delete it, and public repos are scraped continuously. If one gets in, rotate the credential. Don't just remove the file; the credential is what's compromised, not the file.

**Personal data you don't need.** Names, addresses, dates of birth, ID numbers, health information, anything about an identifiable person — unless that person's data is genuinely the subject of the task and your organisation's agreement covers it. The test is *need*, not sensitivity: a lot of personal data gets pasted simply because it was in the same document as the relevant part.

**Client-confidential material in anything shared or public.** This includes the [worked examples in your documentation](handover-package.md), which is where it most often escapes.

### The edges people get wrong

**Redact before you paste, not after you notice.** Deleting a message doesn't unsend it.

**Screenshots and attachments carry more than you're looking at.** A spreadsheet has other tabs. A PDF has metadata. A screenshot has the rest of the window — the browser tabs, the notification, the adjacent row.

**"Anonymised" usually isn't.** Removing the name from a document that gives a job title, a location, and a date is not anonymisation if the population is small. In a 40-person organisation, "the facilities manager, in March" is a name.

**Your test cases are the biggest leak risk in the whole workflow.** [Eval sheets](../tools/eval-sheet.md) are built from real cases, because real cases are the good ones — and then the sheet gets committed to a repo, attached to a [handover package](handover-package.md), and shown in a slide. Sanitise cases when you create them, not when you share them, because by the time you're sharing them you've forgotten what's in row 14.

**Invent your examples.** Every example in this reference is invented, and that's a policy, not a coincidence. Made-up examples are also usually *better* — you can construct them to demonstrate exactly the point.

**Check the folder, not just the file.** [Claude Code](../tools/claude-code.md) reads what's in the directory. That includes the `.env` file, the old export, and the credentials someone left in 2021.

**Ask what the credential can reach.** A [connector](../tools/connectors.md) grants the scope of the account, not the scope of your intention.

## Worked example

*(Invented. Hallowdene Recruitment is not a real agency.)*

A recruitment agency built a system to screen CVs against role requirements. It worked well and they wanted to write it up as a case study.

**Where the data actually leaked — and it wasn't the CVs:**

- **The CVs themselves were handled fine.** Candidates had consented to processing, the agency's agreement covered it, the container wasn't shared outside the team. Genuinely no issue.
- **The eval sheet was the problem.** Twenty real CVs as test cases, including names, addresses, employment history, and two candidates who had disclosed a disability.
- **It had already spread** — committed to the internal repo, attached to the handover package, and one row screenshotted into a slide for a management meeting.
- **The screenshot was the worst part.** A real candidate's employment history, in a deck that had been emailed to eleven people, including two outside the company.
- **The fix took an afternoon** — twenty fully invented CVs, constructed to hit the same edge cases. Better test cases, as it turned out.

<details>
<summary><strong>Expand: why the invented cases were better, and the four rules they wrote</strong></summary>

**The invented set outperformed the real one**, which surprised everyone.

The twenty real CVs had been chosen because they were to hand. They clustered: sixteen were mid-career candidates in one sector, because that was the live vacancy that month. Two edge cases the team knew the system struggled with — career gaps and non-UK qualifications — weren't represented at all, because no such candidate had applied recently.

The invented set was built from the failure list rather than from the inbox: three with career gaps of varying lengths, two with overseas qualifications, one with a career change, one deliberately over-qualified, two where the correct answer was "insufficient information, do not score." That last pair had no equivalent in the real set, and it was the pair that caught a genuine problem — the system scored incomplete CVs rather than flagging them.

**The general lesson:** real cases feel more rigorous and are frequently a biased sample of whatever was recent. Constructed cases can be built to cover the space deliberately. You lose some realism, and you gain coverage — and you stop carrying a liability around in a spreadsheet.

**The four rules they wrote down:**

1. **Test cases are invented by default.** Using a real one requires a stated reason and sanitisation at the moment of creation.
2. **Before anything leaves the team** — repo, deck, handover, email — one person checks it for real data. Named person, not "someone."
3. **No screenshots of working files.** If a slide needs an eval sheet, it gets a purpose-built one with invented rows.
4. **Sanitise at creation, never at sharing.** By the time you're sharing, you've forgotten what's in there.

Rule 4 is the one that would have prevented all of it.

</details>

## What goes wrong

**Test cases are real data.** The single most common leak in this entire workflow, and the most invisible, because a spreadsheet of test cases doesn't feel like a file of personal data.

**Secrets in the repo.** Committed once, present in history forever, and public repos are scraped within minutes.

**A knowledge file uploaded to answer one question.** It stays. The container gets shared next quarter with someone who was never meant to see it.

**Documentation leaks what the system protected.** The system was careful. The write-up used a real example.

**Screenshots.** Everything visible, plus everything adjacent.

**Anonymisation that isn't.** Small populations re-identify from role, location, and date.

**Nobody checks the folder.** Claude Code reads the directory, not the file you had in mind.

## When not to use it

There is no version of this you skip. But keep it proportionate:

- **Don't turn it into an approval process.** A hygiene rule that requires a committee gets routed around, and the routing-around is the actual risk. Four written rules and one named checker beats a policy document.
- **Don't over-redact to the point of uselessness.** A test case stripped of everything that made it a test case doesn't test anything. Invent a replacement instead of gutting the original — that's the move, and it produces better cases anyway.
- **Don't confuse this with [failure modes](failure-modes.md).** This page is about what you put in. That page is about what comes out and what arrives from outside. Both matter and the controls are different.
- **Don't let it stop you starting.** Most work has no sensitive data in it at all. Identify the parts that do, handle those specifically, and get on with it.

---

`Last reviewed: 2026-07-25`
