# Changelog

What changed, when, and why. Review entries are logged even when nothing changed — "reviewed, no changes" is information.

## 2026-08-07

**Added**
- `docs/tools/claude-code.md` — a "Local or cloud" subsection under *How to use it*. Two paragraphs: what a cloud session can and cannot see, and the consequence that committed configuration is the line between a personal tool and a transferable one. Deliberately does not restate CLI flags, permission-mode names, or per-surface feature tables — those are the fastest-moving details on the surface, so the page links out instead.
- `README.md` — link to the published site at the top.

**Source:** a private working note on Claude Code session types (German, 2026-08-07). Only the durable architectural point was taken; the rest was product detail with a short shelf life. Repo stays English per `HANDOVER.md` §10.

## 2026-07-25 — Initial scaffold

**Added**
- `README.md` — thesis, spine, page index, exclusions with reasoning, review routine, license and contribution position.
- `docs/tools/skill.md` — first tool page, written as the format exemplar.
- `docs/practices/handover-package.md` — first practice page, written as the format exemplar.
- `LICENSE` — CC BY 4.0.
- `HANDOVER.md` — the brief this repo was built from, with §12 decisions resolved inline.

**Decided** (resolving `HANDOVER.md` §12)
- **Attribution:** published under Billie Jeurink's name, contact `billie@bjeurink.com`. Anonymous publication was rejected as inconsistent with §3 — an opinionated reference needs someone accountable for the opinions.
- **License:** CC BY 4.0. The repo is prose, not code; MIT is a poor fit. BY-SA was rejected as unnecessary friction for a reference meant to be quoted and taught from.
- **Contributions:** issues open, pull requests closed. §12.4 named the tension correctly — merged prose from many hands converges on the hedged, position-free thing this repo exists not to be. Issues preserve the staleness signal, which is the larger risk.
- **Domain:** GitHub Pages default. Revisit if the reference gets linked widely enough that a stable custom URL earns its DNS.
- **Brand and design tokens:** unresolved. Site remains at neutral default per §12.1.

**Format rules agreed** (after the §13 step 2 review, recorded as `HANDOVER.md` §6 addenda)
- **Worked examples compress by default,** full transcript in a `<details>` block. Guarded by the rule that the visible version must be self-sufficient — this keeps it on the right side of §8's ban on accordions that hide content from a learner.
- **Refusal conditions are a required element** on pages describing something that produces output. Not in the original §6 spec. Added because most systems handle the dangerous ten-percent case as confidently as the easy ninety.

**Added — remaining content**
- Nine remaining pages: `project`, `connectors`, `claude-code`, `eval-sheet`, `context-engineering`, `the-loop`, `human-checkpoints`, `failure-modes`, `data-hygiene`.
- `templates/eval-sheet.csv`, `templates/process-brief.md`, `templates/handover-package.md`.
- `site/index.html` — single file, no build step, scroll-spy sidebar, verb tags, Process Filter placed above the reading material.
- `build-site.py` — generates the site from `README.md` and `docs/`.

**Deviations from `HANDOVER.md` §5**
- `build-site.py` sits at the repo root, which the §5 structure doesn't list. Justified by §4: the site "must be generated from or deliberately synced with the docs," and two hand-maintained copies diverge. The reader still gets no build step — `site/index.html` is committed and opens by double-clicking. `docs/` is stated as canonical in the README and in the site footer.
- `.github/workflows/pages.yml` deploys `site/` to GitHub Pages. Serving from the branch root instead would put the reference at `/applied-ai-operations/site/`; §7 calls the Process Filter "the single most linkable thing in the repo," and a clean URL is worth one file. The workflow uploads a folder — it compiles nothing, and forks inherit it working.

**Verified at time of writing**
- All seven outbound links return 200.
- All in-page anchors and relative links in `site/index.html` resolve.
- All nine Process Filter band combinations return distinct, correct verdicts, with the axes reported separately and never summed.

**Outstanding**
- `REPO_URL` in `build-site.py` is a placeholder until the repo has a GitHub home.
- Brand and design tokens (`HANDOVER.md` §12.1) — site is on a neutral default.
