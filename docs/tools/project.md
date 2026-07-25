# Project

`Verb: Design` · [← Index](../../README.md)

---

## What it is

A container with three slots: **instructions** that apply to every conversation started inside it, **knowledge** files it can always see, and a **scope** — a boundary around what the container is for.

For how to create one and what it currently holds, see [Anthropic's help centre](https://support.claude.com/). This page is about what to put in which slot, and why the scope is the part that matters.

## Why it matters

**The container is what makes a system transferable rather than personal.**

Without one, everything that makes your outputs good lives in your head and in the way you happen to phrase things on a given morning. You are not operating a system; you are being good at something. Those look identical from the outside and behave completely differently the week you're on holiday.

A Project is the first artifact someone else can be handed. It's also the first thing that can be wrong in a way you can *find* — instructions on a screen can be read, argued with, and corrected. A habit can't.

The underrated slot is scope. A Project called "Marketing" is a folder. A Project called "Responding to inbound RFPs" is a container — because you can say what belongs in it, which means you can write instructions that are true *every single time*. Instructions that are only sometimes true are worse than none: they teach the reader to ignore the instructions.

## How to use it

**Name it after a job to be done, not a department.** "Supplier onboarding" beats "Procurement." The test: can you write five instructions that are true for every task in this container? If not, the scope is too wide.

**Instructions hold what is invariant.** Audience, tone, house conventions, standing constraints, what to always ask for before starting. If something is true only for one task type, it belongs in a [Skill](skill.md) — that boundary is the whole subject of [context engineering](../practices/context-engineering.md).

**Write the "never" list.** Most Project instructions say what to do. The ones that survive contact with reality say what not to do: never invent a figure that isn't in the source, never name a client in an external draft, never proceed without the reference number. Prohibitions are more durable than aspirations because they're checkable.

**Knowledge is a curated shelf, not an archive.** Every irrelevant document competes with the relevant ones. Add a file when you notice yourself pasting the same thing twice; remove it when it goes out of date. Uploading the whole shared drive is the most common way to make a Project worse.

**One Project per job.** The mega-Project that handles everything is a Project whose instructions can't be true, which means it has no instructions.

## Worked example

*(Invented. Calder & Vance is not a real practice.)*

A six-person architecture practice writes planning-application design-and-access statements — perhaps two a month, always the same six sections, always against the same local authority's validation checklist. Quality depended entirely on which of the two senior architects wrote it.

**The Project — "Planning statements":**

- **Scope** — planning applications only. Not client correspondence, not fee proposals, not tender work; those are separate containers.
- **Instructions** — the six mandatory sections in order; British English; cite the specific policy number, never "relevant policy"; plain language over planning jargon since these are read by committee members and neighbours.
- **Never** — never assert a site constraint that isn't in the uploaded survey; never state a dimension without a source; never name the client in text that goes on the public register.
- **Knowledge** — the authority's validation checklist, the local plan policy index, and three past statements that were approved without revision.

<details>
<summary><strong>Expand: what went in each slot, and what deliberately didn't</strong></summary>

**Instructions (invariant across every statement):**
1. Structure: Assessment, Involvement, Evaluation, Design, Access, Policy compliance. In that order, always.
2. British English. Metric units. Dates as DD Month YYYY.
3. Cite policies by number and title. "In accordance with relevant policy" is not a citation.
4. Write for a lay reader on a planning committee. Expand any acronym on first use.
5. Before starting, ask for: site address, application reference, survey document, and client brief. Do not proceed with a missing survey.

**Never:**
- Never assert a site constraint, dimension, or measurement not present in the uploaded survey.
- Never name the client or any individual — these documents go on a public register.
- Never characterise a neighbouring objection; summarise it factually or omit it.

**Knowledge (four files, deliberately):**
- The authority's current validation checklist.
- The local plan policy index.
- Two approved past statements, chosen because they were approved without revision.
- A one-page house style note.

**Deliberately excluded from knowledge:** the practice's full past-project archive, the RIBA plan of work, and general planning guidance. All relevant, none needed *every time* — and each one would have diluted the four files that are.

**What stayed in Skills instead:** the heritage-impact section (only applies in conservation areas) and the transport-statement variant (only above a floor-area threshold). Both are real procedures, neither is universal, so neither belongs in Project instructions.

</details>

The practice found the split itself was the useful part. Two things they had assumed were "how we write statements" turned out to apply to maybe a third of cases — which is why they had been quietly wrong in the other two thirds.

## What goes wrong

**The Project is department-shaped.** "Finance," "Marketing," "Ops." Nothing can be written in the instructions that's true for every task, so the instructions become vague encouragement.

**The knowledge base becomes a dumping ground.** Someone uploads forty files because it seems thorough. Output quality drops and nobody connects the two events.

**Instructions duplicate a Skill.** The same procedure now exists in two places at two levels of staleness. When they disagree, you will not be able to tell which one is being followed.

**It's a personal Project that never gets shared.** All the transferability benefit, unrealised, and now a colleague's request routes through you forever. This is the failure the [handover package](../practices/handover-package.md) exists to prevent.

**Confidential material lands in a shared container.** The container is exactly the thing that widens the audience for whatever is in it. Read [data hygiene](../practices/data-hygiene.md) *before* filling the knowledge slot, not after.

**Nobody owns it.** Instructions drift out of date, the checklist in knowledge is superseded, and the Project keeps confidently producing work to last year's standard.

## When not to use it

- **For a one-off.** No container needed. Just ask.
- **When the work has no invariants.** If nothing is true every time, you don't have a job to be done yet — you have a department. Narrow the scope or don't build the container.
- **When the material is sensitive and the container is shared.** Either the material doesn't go in, or the container isn't shared. Not both.
- **As a substitute for scoping the work.** A Project can't make an unclear job clear. If you can't name what belongs inside it, run the [Process Filter](../../site/index.html) first.

---

`Last reviewed: 2026-07-25`
