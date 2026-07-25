# Connectors

`Verb: Build` · [← Index](../../README.md)

---

## What it is

A connector gives a system access to a real data source — your files, your ticketing system, your calendar — instead of whatever you remembered to paste into the message.

Most connectors are built on the Model Context Protocol, an open standard for how tools describe themselves to a model. You don't need to understand MCP to use one; you need to understand it if you're building one. Reference: [modelcontextprotocol.io](https://modelcontextprotocol.io/) and [Anthropic's connector documentation](https://docs.claude.com/).

## Why it matters

Pasting is a checkpoint disguised as a chore. Every time you paste, you decide what's relevant, you notice what's missing, and you see what you're handing over. Connecting removes all three of those, which is the point and also the risk.

The gain is real: a system that reads the actual ticket cannot work from a stale summary of the ticket, and a system that can look things up stops asking you to fetch them. That's the difference between a tool you operate and a system that runs.

But the important sentence on this page is this one:

**A connector is not a plumbing decision. It is a permission decision.**

When you connect a source, you are not granting access to the document you have in mind. You are granting access to *everything that source can reach*, for every future conversation, including ones you won't be watching. Whether that's fine is usually a question about the source's own permission model, not about the AI at all — and it's a question most people skip because the connect button is a button.

There's a second-order version that's easy to miss and covered properly in [failure modes](../practices/failure-modes.md): once a system can read untrusted documents, text inside those documents can attempt to instruct it. A connector turns "read this" into "read whatever arrives." Anything that can arrive from outside your organisation is untrusted input, and that includes email, shared files, and support tickets.

## How to use it

**Start with exactly one.**

This is the strongest recommendation on the page and it gets ignored constantly. Connect one source, use it for two weeks, and only then consider a second. The reasons compound:

- **You can attribute problems.** With one connector, a bad output has one new variable. With four, you are debugging a system, and you will not do it — you'll shrug and stop trusting the output.
- **You find out what the source is actually like.** Most data is messier than the people who own it believe. One connector teaches you that cheaply.
- **The permission conversation stays finite.** One source, one scope question, one answer you can defend.

**Then, before you connect anything:**

1. **Ask what the credential can reach, not what you'll use it for.** If it's your own account, the answer is "everything you can see." Assume the widest scope, because that's the scope you're granting.
2. **Prefer read-only.** A system that can only read has a bounded worst case. A system that can write has an unbounded one. Add write access when a specific task demands it, to that task, deliberately.
3. **Prefer narrow over convenient.** One folder beats the whole drive. One project beats the whole workspace. Narrowing is annoying once; over-broad access is a risk permanently.
4. **Decide where untrusted text enters.** Write it down. It determines where your [human checkpoints](../practices/human-checkpoints.md) go.
5. **Check what's actually in there first.** Connect it, then ask the system to describe what it can see. People are routinely surprised, and it is much better to be surprised on day one.

## Worked example

*(Invented. Halvard Instruments is not a real company.)*

A scientific-instruments distributor wanted a system to draft responses to inbound technical support email. The instinct was to connect everything: the mail system, the CRM, the product documentation drive, and the parts database. Four connectors, day one.

**What they did instead:**

- **Connected one thing** — the product documentation drive, read-only, scoped to the published-manuals folder. Not email, not the CRM.
- **Kept the human in the loop for input** — the support agent pastes the customer's question. The system looks up the manual.
- **Found the mess immediately** — the folder held three superseded manual versions with no version markers. The system cited the 2019 torque spec. Nobody had noticed because humans opened files by date.
- **Fixed the data, not the prompt** — archived the superseded versions. This was the whole win.
- **Added a second connector in week five** — the parts database, read-only. Still no email connector.

<details>
<summary><strong>Expand: why email stayed disconnected</strong></summary>

Connecting the mail system was the obvious next step and they deliberately didn't take it. Three reasons, in the order they mattered:

1. **Scope.** The available credential could read the whole support mailbox, including threads containing customer pricing and one ongoing warranty dispute. There was no way to grant "just the technical questions" — that category exists in a human's head, not in the mail system's permission model.

2. **Untrusted input.** Inbound email is the canonical untrusted channel. A connected mail reader will eventually process a message containing text written to be read as an instruction. With a human pasting the question, there is a person between the outside world and the system — not a perfect control, but a real one, and free.

3. **No demand for it.** Pasting the question cost about eight seconds. The bottleneck was never the paste; it was finding the right spec in the right manual. They had already solved that.

The rule they wrote down: *a connector has to remove a bottleneck that actually exists.* "It would be more integrated" is not a bottleneck.

**What the archiving fix was worth:** more than every other change combined. The system was accurate afterwards not because it got better instructions but because the underlying data stopped being wrong. This is the most common shape of a real result and the least satisfying to write on a slide.

</details>

## What goes wrong

**Everything is connected on day one.** Then output is unreliable, nobody can say why, and the project is quietly abandoned as "not accurate enough." The model was fine. There were four variables.

**The scope is the credential's scope, not the intended scope.** Somebody connects with an admin account because it was the one that worked. The system can now read HR files that nobody remembers exist.

**Nobody looked at the data.** Duplicates, superseded versions, an abandoned folder from a 2021 migration. A connector faithfully surfaces all of it, and the system's confident wrong answer is a *data* problem wearing an AI costume.

**Write access arrives early and casually.** It's granted "so it can file the ticket," and now a failure mode that used to produce a bad draft produces a bad record in a system of record.

**Untrusted input arrives with no checkpoint.** The connector is added, the review gate isn't moved, and text from outside the organisation now reaches a system that acts on text.

**Nobody re-checks the scope.** Access granted in March is still granted in November, to a source that has since been reorganised.

## When not to use it

- **When pasting works.** Genuinely. If the human doing the copying is providing useful judgement about relevance, a connector removes that judgement and calls it efficiency.
- **When you can't answer "what can this credential reach?"** Not yet. Go find out. This is not a formality.
- **When the underlying data is a mess.** Fix the data first. Connecting to a bad source produces confident, sourced, wrong answers — strictly worse than no source at all, because now it has a citation.
- **When the source contains material that shouldn't be in scope** and the permission model can't exclude it. See [data hygiene](../practices/data-hygiene.md).
- **When you'd be adding your second, third, and fourth simultaneously.** Add one. Wait. This is the point of the page.

---

`Last reviewed: 2026-07-25`
