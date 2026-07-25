# Handover package — [system name]

> **Fill every section or don't hand over.** A section you can't complete is a design finding, not a paperwork problem.
>
> Reasoning behind each item: [the handover package](../docs/practices/handover-package.md).
>
> Delete this block and the guidance in *italics* before you hand it to anyone.

**System:** ______________________________________________

**Handed over by:** ____________________  **To:** ____________________

**Date:** ______________

---

## 1. Runbook

*Two pages maximum. Written for someone who was in none of the meetings.*

### What this does

*Two sentences. What goes in, what comes out, who it's for.*

### What it does not do

*The scope boundary, stated positively. Prevents the most common misuse.*

### How to run it

*Numbered steps. Include where it lives and what access is needed.*

1.
2.
3.

### What good output looks like

*A real example. Paste it in full.*

### What bad output looks like

**Do not skip this.** *A real example of the system getting it wrong, with a note on what makes it wrong. The reader must be able to recognise failure without having to define it themselves — this is the section that lets someone spot a problem on a Tuesday.*

---

## 2. Eval sheet — with real numbers

*Not a blank template. The sheet you actually ran, with the scores you actually got, dated. A blank sheet says "you should test this." A filled one says "here is the bar."*

**Location of the sheet:** ______________________________________________

**Last run:** ______________  **Scored by:** ______________

**Scores:**

| Dimension | Score | Bar |
|---|---|---|
| | / | |
| | / | |
| | / | |

**Cases it failed, by name:**

*List them. A sheet that scored full marks means the cases were too easy and tells the next owner nothing about where the edges are.*

-
-

**How to re-run it:**

*Steps, or a link to the script. If re-running costs more than half an hour, it will not happen — fix that before handing over.*

**Re-run when:** any change to the system, its instructions, or a connected data source — **and** on a calendar, at least quarterly, to catch drift.

---

## 3. Owner

*One person. A name, not a team. "The ops team owns it" means nobody owns it.*

**Owner:** ______________________  **Role:** ______________________

**Contact:** ______________________

**They have agreed to this:** ☐ Yes — *confirm out loud before writing the name. An owner who learns about their ownership from a document is not an owner.*

**What ownership means here:**
- Gets the question when output looks wrong
- Re-runs the eval sheet when anything changes, and quarterly regardless
- Has the authority to take the system out of service

**Backup / cover during absence:** ______________________

---

## 4. Escalation path

*Two branches, and they are different.*

### It's broken — errors, produces nothing, obvious nonsense

**Goes to:** ______________________  **Contact:** ______________________

**In the meantime:** ______________________

### It's wrong — confident, plausible, incorrect output

*The more dangerous branch and the more likely one. Needs a stated destination.*

**Goes to:** ______________________  **Contact:** ______________________

**In the meantime:** *usually "stop using it and do it by hand." Say it explicitly so it reads as a sanctioned option rather than a failure.*

______________________

### Out-of-service threshold

*A specific, checkable condition that takes the system offline without needing a debate.*

*Example: "If two consecutive eval runs drop below 16/20 on any column, the system comes out of service until reviewed."*

______________________________________________

---

## 5. Known limitations

*Everything you know it can't do, written down while you still remember. This section buys more credibility than the rest of the document combined, and it is the one people soften. Don't.*

*Include the ones that feel obvious to you — obvious-to-you is precisely the category that doesn't transfer.*

**Never tested on:**
-
-

**Known to fail on:**
-
-

**Cannot see / has no access to:**

*Often the most valuable line in the whole document. What is structurally invisible to this system?*

-

**Assumes (and will break if this changes):**

*Input formats, field names, policy versions, source structures. Each one is a drift tripwire.*

-
-

---

## Sign-off

| | Name | Date |
|---|---|---|
| Handed over by | | |
| Received and understood by | | |

**The receiving owner confirms they can:** ☐ run it · ☐ recognise bad output · ☐ re-run the eval · ☐ take it out of service

*If any box is unchecked, the handover is not complete. Fix the gap rather than the document.*

---

**Next scheduled review:** ______________
