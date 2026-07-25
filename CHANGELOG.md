# Changelog

What changed, when, and why. Review entries are logged even when nothing changed — "reviewed, no changes" is information.

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

**Outstanding**
- Nine remaining pages, pending format sign-off on the two exemplars (`HANDOVER.md` §13, step 2).
- `templates/` — three files.
- `site/index.html` — including the Process Filter.
