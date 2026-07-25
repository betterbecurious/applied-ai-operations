#!/usr/bin/env python3
"""
Generate site/index.html from README.md and docs/.

docs/ is canonical. This script exists so the site is never a second
hand-maintained copy (HANDOVER.md section 4). It is a maintenance tool,
not a build step for the reader: site/index.html is committed, opens by
double-clicking, and deploys to GitHub Pages unchanged.

Run after editing any page:

    python3 build-site.py

No dependencies. Standard library only. Handles the markdown subset
actually used in this repo -- if you introduce new syntax, teach it here.
"""

import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
LAST_REVIEWED = "2026-07-25"

# Set once the repo has a home. GitHub-relative links in README.md (such as
# ../../issues) have no meaning on the published site, so they are rewritten
# against this.
REPO_URL = "https://github.com/betterbecurious/applied-ai-operations"

TOOLS = ["project", "skill", "connectors", "claude-code", "eval-sheet"]
PRACTICES = [
    "context-engineering", "the-loop", "human-checkpoints",
    "failure-modes", "data-hygiene", "handover-package",
]

VERB_ORDER = ["Design", "Build", "Evaluate", "Ship"]


# --------------------------------------------------------------------------
# Inline markdown
# --------------------------------------------------------------------------

def rewrite_href(href):
    """Turn a docs-relative link into a single-page anchor."""
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return href
    href = href.replace("../../", "").replace("../", "")
    if href in ("issues", "issues/"):
        return REPO_URL + "/issues"
    if href.startswith("README.md"):
        frag = href.split("#", 1)
        return "#" + frag[1] if len(frag) > 1 else "#top"
    if href.startswith("site/index.html"):
        return "#process-filter"
    # Repo files that live outside site/. Pages serves site/ as its root, so a
    # relative "../" escapes the deployment and 404s. Absolute repo URLs work
    # from the published site and from a double-clicked local copy alike.
    if href.startswith("templates/") or href == "LICENSE":
        return REPO_URL + "/blob/main/" + href
    href = re.sub(r"^docs/", "", href)
    m = re.match(r"^(?:tools/|practices/)?([a-z0-9-]+)\.md(#.*)?$", href)
    if m:
        return "#" + m.group(1)
    return href


def inline(text):
    """Convert inline markdown to HTML. Input is raw markdown, not escaped."""
    placeholders = []

    def stash(rendered):
        placeholders.append(rendered)
        return "\x00%d\x00" % (len(placeholders) - 1)

    # Code spans first: their contents must not be treated as markdown.
    text = re.sub(
        r"`([^`]+)`",
        lambda m: stash("<code>%s</code>" % html.escape(m.group(1))),
        text,
    )

    # Links, before escaping, so URLs survive intact.
    def link(m):
        label, href = m.group(1), rewrite_href(m.group(2))
        ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        return stash('<a href="%s"%s>%s</a>' % (html.escape(href), ext, inline(label)))

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)

    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)([^*]+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)

    for i, rendered in enumerate(placeholders):
        text = text.replace("\x00%d\x00" % i, rendered)
    return text


# --------------------------------------------------------------------------
# Block markdown
# --------------------------------------------------------------------------

def render(lines, heading_offset=1, slug_prefix=""):
    """Render a list of markdown lines to HTML."""
    out = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Fenced code
        if stripped.startswith("```"):
            i += 1
            body = []
            while i < n and not lines[i].strip().startswith("```"):
                body.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % "\n".join(body))
            continue

        # Raw HTML passthrough (details / summary blocks)
        if stripped.startswith("<details"):
            out.append('<details class="expand">')
            i += 1
            continue
        if stripped.startswith("</details>"):
            out.append("</details>")
            i += 1
            continue
        if stripped.startswith("<summary>"):
            inner = re.sub(r"^<summary>|</summary>$", "", stripped)
            # Summaries wrap their label in <strong> for GitHub's renderer.
            # Here the weight comes from CSS, so drop the tags rather than
            # escaping them into visible markup.
            inner = re.sub(r"</?strong>|</?b>", "", inner)
            out.append("<summary>%s</summary>" % inline(inner))
            i += 1
            continue

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = min(len(m.group(1)) + heading_offset, 6)
            text = m.group(2)
            slug = slug_prefix + re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            out.append('<h%d id="%s">%s</h%d>' % (level, slug, inline(text), level))
            i += 1
            continue

        # Tables
        if stripped.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            if len(rows) >= 2 and all(set(c) <= set("-: ") for c in rows[1]):
                head, body = rows[0], rows[2:]
            else:
                head, body = None, rows
            t = ['<div class="table-wrap"><table>']
            if head:
                t.append("<thead><tr>%s</tr></thead>" % "".join(
                    "<th>%s</th>" % inline(c) for c in head))
            t.append("<tbody>")
            for r in body:
                t.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r))
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue

        # Blockquote
        if stripped.startswith(">"):
            body = []
            while i < n and lines[i].strip().startswith(">"):
                body.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            out.append("<blockquote>%s</blockquote>" % render(body, heading_offset, slug_prefix))
            continue

        # Ordered list
        if re.match(r"^\d+\.\s", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % inline(x) for x in items))
            continue

        # Unordered list
        if stripped.startswith("- "):
            items = []
            while i < n and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(x) for x in items))
            continue

        # Paragraph
        body = []
        while i < n and lines[i].strip() and not re.match(
                r"^(#{1,6}\s|\||>|-\s|\d+\.\s|```|<details|</details|<summary|---$)",
                lines[i].strip()):
            body.append(lines[i].strip())
            i += 1
        if body:
            out.append("<p>%s</p>" % inline(" ".join(body)))
        else:
            i += 1

    return "\n".join(out)


# --------------------------------------------------------------------------
# Source parsing
# --------------------------------------------------------------------------

def load_page(path, slug):
    """Read a docs page: title, verb, body lines (chrome stripped)."""
    raw = path.read_text(encoding="utf-8").split("\n")
    title = raw[0].lstrip("# ").strip()
    verb = ""
    body = []
    for line in raw[1:]:
        s = line.strip()
        m = re.match(r"^`Verb:\s*(\w+)`", s)
        if m:
            verb = m.group(1)
            continue
        if s.startswith("`Last reviewed:"):
            continue
        body.append(line)
    if not verb:
        sys.exit("error: %s has no `Verb:` line" % path)
    # offset 1: the page's "## What it is" becomes h3 under the section's h2.
    return {"slug": slug, "title": title, "verb": verb,
            "html": render(body, heading_offset=1, slug_prefix=slug + "-")}


def readme_sections():
    """Split README.md into {heading: [lines]} plus the intro."""
    raw = (ROOT / "README.md").read_text(encoding="utf-8").split("\n")
    sections, current, key = {}, [], "__intro__"
    for line in raw:
        m = re.match(r"^##\s+(.*)$", line.strip())
        if m:
            sections[key] = current
            key, current = m.group(1), []
        else:
            current.append(line)
    sections[key] = current
    return sections


# --------------------------------------------------------------------------
# Page assembly
# --------------------------------------------------------------------------

CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --paper:#fbfaf8; --paper-2:#f3f1ed; --ink:#1c1a17; --ink-2:#524d45;
  --ink-3:#847d72; --rule:#e0dcd4; --accent:#3d4f63; --accent-soft:#eaeef3;
  --code-bg:#f0eee9; --max:44rem;
  --design:#8a6a2f; --design-bg:#f7f0e0;
  --build:#2f5d8a; --build-bg:#e4eef7;
  --evaluate:#6a4a86; --evaluate-bg:#efe8f6;
  --ship:#3d6b4a; --ship-bg:#e5f0e8;
}
@media (prefers-color-scheme:dark){
  :root{
    --paper:#16181a; --paper-2:#1e2124; --ink:#e8e6e3; --ink-2:#b0aca6;
    --ink-3:#84807a; --rule:#2f3337; --accent:#9db6d0; --accent-soft:#23303d;
    --code-bg:#22262a;
    --design:#d4ac6a; --design-bg:#332a17;
    --build:#8fb8dd; --build-bg:#1b2a38;
    --evaluate:#b79ad6; --evaluate-bg:#2a2136;
    --ship:#8dc39d; --ship-bg:#1c2f23;
  }
}
html{scroll-behavior:smooth;scroll-padding-top:1.5rem;-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--paper);color:var(--ink);
  font:16px/1.65 ui-serif,Charter,"Bitstream Charter","Iowan Old Style",Georgia,serif;
  font-feature-settings:"kern","liga";
}
.layout{display:grid;grid-template-columns:16rem minmax(0,1fr);gap:3.5rem;
  max-width:74rem;margin:0 auto;padding:0 1.5rem}

/* Sidebar */
.sidebar{position:sticky;top:0;align-self:start;height:100vh;overflow-y:auto;
  padding:2.5rem 0 3rem;font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
.sidebar .brand{font-weight:650;font-size:.9rem;letter-spacing:-.01em;
  color:var(--ink);text-decoration:none;display:block;line-height:1.3}
.sidebar .brand span{display:block;font-weight:400;font-size:.76rem;color:var(--ink-3);
  margin-top:.2rem}
.sidebar nav{margin-top:1.75rem}
.sidebar .group{font-size:.68rem;text-transform:uppercase;letter-spacing:.09em;
  color:var(--ink-3);margin:1.5rem 0 .5rem;font-weight:600}
.sidebar a.nav{display:block;padding:.26rem 0 .26rem .7rem;font-size:.83rem;
  color:var(--ink-2);text-decoration:none;border-left:2px solid var(--rule);
  transition:color .12s,border-color .12s}
.sidebar a.nav:hover{color:var(--ink)}
.sidebar a.nav.active{color:var(--accent);border-left-color:var(--accent);font-weight:550}
.sidebar .foot{margin-top:2rem;padding-top:1rem;border-top:1px solid var(--rule);
  font-size:.72rem;color:var(--ink-3);line-height:1.5}
.sidebar .foot a{color:var(--ink-3)}

/* Content */
main{padding:2.5rem 0 6rem;min-width:0;max-width:var(--max)}
h1,h2,h3,h4{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
  letter-spacing:-.021em;line-height:1.22;color:var(--ink)}
h1{font-size:2.35rem;font-weight:680;margin:0 0 1rem}
h2{font-size:1.42rem;font-weight:640;margin:0 0 .35rem}
h3{font-size:1.12rem;font-weight:640;margin:2.35rem 0 .6rem}
h4{font-size:.95rem;font-weight:640;margin:1.6rem 0 .4rem}
h5{font-size:.86rem;font-weight:650;margin:1.35rem 0 .35rem;color:var(--ink-2);
  text-transform:uppercase;letter-spacing:.05em;
  font-family:ui-sans-serif,system-ui,-apple-system,sans-serif}
h6{font-size:.85rem;font-weight:620;margin:1.2rem 0 .3rem;color:var(--ink-2)}
p{margin:0 0 1rem}
a{color:var(--accent);text-decoration:underline;text-decoration-thickness:1px;
  text-underline-offset:2px}
ul,ol{margin:0 0 1rem;padding-left:1.25rem}
li{margin-bottom:.4rem}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.855em;
  background:var(--code-bg);padding:.1em .35em;border-radius:3px}
pre{background:var(--code-bg);padding:1rem 1.1rem;border-radius:6px;overflow-x:auto;
  margin:0 0 1.25rem;border:1px solid var(--rule)}
pre code{background:none;padding:0;font-size:.83rem;line-height:1.55}
blockquote{margin:0 0 1.25rem;padding:.1rem 0 .1rem 1.1rem;
  border-left:2px solid var(--rule);color:var(--ink-2)}
blockquote p:last-child{margin-bottom:0}
hr{border:0;border-top:1px solid var(--rule);margin:3rem 0}
.table-wrap{overflow-x:auto;margin:0 0 1.35rem;
  -webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:.87rem;
  font-family:ui-sans-serif,system-ui,-apple-system,sans-serif}
th,td{text-align:left;padding:.5rem .7rem;border-bottom:1px solid var(--rule);
  vertical-align:top}
th{font-weight:620;font-size:.76rem;text-transform:uppercase;letter-spacing:.05em;
  color:var(--ink-3);border-bottom-width:1.5px}
details.expand{margin:0 0 1.35rem;border:1px solid var(--rule);border-radius:6px;
  background:var(--paper-2)}
details.expand summary{cursor:pointer;padding:.6rem .9rem;font-size:.85rem;font-weight:600;
  font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;color:var(--ink-2);
  list-style:none;user-select:none}
details.expand summary::-webkit-details-marker{display:none}
details.expand summary::before{content:"\\203A";display:inline-block;margin-right:.5rem;
  transition:transform .15s;color:var(--ink-3)}
details.expand[open] summary::before{transform:rotate(90deg)}
details.expand summary:hover{color:var(--ink)}
details.expand > *:not(summary){padding-left:.9rem;padding-right:.9rem}
details.expand > *:last-child{padding-bottom:.4rem}

/* Section headers */
section{scroll-margin-top:1.5rem}
.section-head{margin:4.5rem 0 1.5rem;padding-top:1.5rem;border-top:1px solid var(--rule)}
.section-head:first-child{border-top:0;padding-top:0}
.verb{display:inline-block;font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;
  font-size:.66rem;font-weight:650;text-transform:uppercase;letter-spacing:.08em;
  padding:.2rem .5rem;border-radius:3px;vertical-align:.18em;margin-left:.6rem}
.verb-Design{color:var(--design);background:var(--design-bg)}
.verb-Build{color:var(--build);background:var(--build-bg)}
.verb-Evaluate{color:var(--evaluate);background:var(--evaluate-bg)}
.verb-Ship{color:var(--ship);background:var(--ship-bg)}

/* Hero */
.hero{padding:3.5rem 0 1rem}
.thesis{font-size:1.16rem;line-height:1.55;color:var(--ink);margin:0 0 1.25rem}
.spine{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92rem;
  background:var(--paper-2);border:1px solid var(--rule);border-radius:6px;
  padding:.9rem 1.1rem;margin:0 0 1.25rem;text-align:center;overflow-x:auto;
  white-space:nowrap}
.meta{font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;font-size:.78rem;
  color:var(--ink-3);margin:0}

/* Process Filter */
.pf{border:1.5px solid var(--rule);border-radius:10px;background:var(--paper-2);
  padding:1.6rem;margin:2rem 0 1rem}
.pf h2{margin-bottom:.4rem}
.pf .lede{font-size:.92rem;color:var(--ink-2);margin-bottom:1.5rem}
.pf fieldset{border:0;padding:0;margin:0 0 1.5rem}
.pf legend{font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;font-size:.8rem;
  font-weight:650;padding:0;margin-bottom:.15rem;color:var(--ink)}
.pf .axis-note{font-size:.8rem;color:var(--ink-3);margin:0 0 .9rem;
  font-family:ui-sans-serif,system-ui,-apple-system,sans-serif}
.crit{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:.6rem 1rem;
  align-items:center;padding:.5rem 0;border-bottom:1px solid var(--rule)}
.crit:last-of-type{border-bottom:0}
.crit-label{font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;font-size:.85rem;
  line-height:1.4}
.crit-label b{font-weight:640}
.crit-label span{display:block;color:var(--ink-3);font-size:.78rem}
.scale{display:flex;gap:.25rem}
.scale input{position:absolute;opacity:0;pointer-events:none}
.scale label{cursor:pointer;width:2.1rem;height:1.9rem;display:grid;place-items:center;
  border:1px solid var(--rule);border-radius:4px;background:var(--paper);
  font-family:ui-sans-serif,system-ui,sans-serif;font-size:.8rem;color:var(--ink-2);
  transition:background .12s,color .12s,border-color .12s}
.scale label:hover{border-color:var(--accent)}
.scale input:checked + label{background:var(--accent);border-color:var(--accent);
  color:var(--paper);font-weight:640}
.scale input:focus-visible + label{outline:2px solid var(--accent);outline-offset:2px}
@media (prefers-color-scheme:dark){
  .scale input:checked + label{color:#16181a}
}
.totals{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1.5rem 0 0}
.total{background:var(--paper);border:1px solid var(--rule);border-radius:6px;
  padding:.8rem .9rem;font-family:ui-sans-serif,system-ui,sans-serif}
.total .k{font-size:.7rem;text-transform:uppercase;letter-spacing:.07em;color:var(--ink-3)}
.total .v{font-size:1.6rem;font-weight:660;line-height:1.2;margin:.15rem 0}
.total .b{font-size:.76rem;color:var(--ink-2)}
.never-sum{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.78rem;
  color:var(--ink-3);text-align:center;margin:.8rem 0 0}
.verdict{margin-top:1.25rem;padding:1.1rem 1.2rem;border-radius:8px;
  background:var(--paper);border:1px solid var(--rule);border-left:3px solid var(--accent)}
.verdict h3{margin:0 0 .5rem;font-size:1.05rem}
.verdict p{font-size:.9rem;margin-bottom:.7rem}
.verdict p:last-child{margin-bottom:0}
.verdict.warn{border-left-color:var(--design)}
.verdict.good{border-left-color:var(--ship)}
.verdict.stop{border-left-color:var(--evaluate)}
.verdict .weakest{font-size:.86rem;background:var(--paper-2);padding:.6rem .75rem;
  border-radius:5px;margin-top:.8rem}
.pf-actions{display:flex;gap:.6rem;margin-top:1rem;flex-wrap:wrap}
.btn{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.8rem;padding:.45rem .85rem;
  border:1px solid var(--rule);border-radius:5px;background:var(--paper);color:var(--ink-2);
  cursor:pointer}
.btn:hover{border-color:var(--accent);color:var(--accent)}

footer{border-top:1px solid var(--rule);margin-top:5rem;padding:2rem 0 4rem;
  font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;font-size:.82rem;
  color:var(--ink-3)}
footer .reviewed{font-weight:600;color:var(--ink-2)}

@media (max-width:960px){
  .layout{grid-template-columns:1fr;gap:0}
  .sidebar{position:static;height:auto;padding:1.75rem 0 1.25rem;
    border-bottom:1px solid var(--rule)}
  .sidebar nav,.sidebar .foot{display:none}
  main{padding-top:1.5rem}
  .hero{padding-top:2rem}
  h1{font-size:1.85rem}
  .pf{padding:1.1rem;margin-left:-.35rem;margin-right:-.35rem}
  .crit{grid-template-columns:1fr}
  .totals{grid-template-columns:1fr}
}
"""

PF_HTML = """
<section id="process-filter" class="pf">
  <h2>The Process Filter</h2>
  <p class="lede">Before you build anything: is this process a sensible target, and can
  this organisation actually receive it? Score both. They are different questions, and
  the gap between them is the answer.</p>

  <form id="pf-form">
    <fieldset>
      <legend>Axis A &mdash; is this process a good target?</legend>
      <p class="axis-note">1 = no &middot; 2 = partly &middot; 3 = yes</p>
      <div id="axis-a"></div>
    </fieldset>

    <fieldset>
      <legend>Axis B &mdash; can this organisation receive it?</legend>
      <p class="axis-note">1 = no &middot; 2 = partly &middot; 3 = yes</p>
      <div id="axis-b"></div>
    </fieldset>
  </form>

  <div class="totals">
    <div class="total">
      <div class="k">Axis A &mdash; the process</div>
      <div class="v"><span id="tot-a">&mdash;</span> <span style="font-size:.9rem;color:var(--ink-3)">/ 15</span></div>
      <div class="b" id="band-a">not yet scored</div>
    </div>
    <div class="total">
      <div class="k">Axis B &mdash; the organisation</div>
      <div class="v"><span id="tot-b">&mdash;</span> <span style="font-size:.9rem;color:var(--ink-3)">/ 9</span></div>
      <div class="b" id="band-b">not yet scored</div>
    </div>
  </div>
  <p class="never-sum">These are never added together. Summing them averages a
  disaster into a respectable number.</p>

  <div class="verdict" id="verdict" hidden></div>

  <div class="pf-actions">
    <button type="button" class="btn" id="pf-copy">Copy summary</button>
    <button type="button" class="btn" id="pf-reset">Reset</button>
    <a class="btn" href="__REPO__/blob/main/templates/process-brief.md"
       target="_blank" rel="noopener" style="text-decoration:none">Paper version</a>
  </div>
</section>
"""

PF_JS = r"""
var AXIS_A = [
  ["Frequent","Daily or weekly, not annual",
   "Not frequent enough. The effort will never repay itself — find the weekly version of this task."],
  ["Boring","Repetitive and rule-ish, not novel each time",
   "Too much judgement per instance. Look for the routine part inside it, which is usually the data-gathering rather than the decision."],
  ["Text-shaped","Language and documents in, the same out",
   "Not text-shaped. If the real work lives in a spreadsheet, a diagram, or a phone call, this is the wrong tool."],
  ["Measurable","You can count something before and after",
   "Not measurable. You will never know whether it works and never be able to defend it. Find something countable."],
  ["Tolerant","A wrong answer gets caught before it causes harm",
   "Not tolerant. Errors reach the world uncaught. Add a checkpoint upstream, or choose something where being wrong is survivable."]
];
var AXIS_B = [
  ["Owned","One identifiable person cares and will answer questions",
   "No owner. Find the person, or accept there isn't one — a name, not a team. If nobody will put their name on it, that is your answer about whether to build it."],
  ["Reviewable","Someone will actually look at the output",
   "Nobody reviews it. Work out who looks at the output and when, before it exists — not after."],
  ["Operable","Someone can run it on Monday without you",
   "Not operable without you. Whatever you build has to be runnable by someone with no context, and that constrains the design, so it has to be known now."]
];

function bandA(s){ return s >= 12 ? "high" : s >= 8 ? "mid" : "low"; }
function bandB(s){ return s >= 7  ? "high" : s >= 5 ? "mid" : "low"; }

var VERDICTS = {
  "high|high": ["good","Build it",
    ["A good process in an organisation that can absorb it. This is the one you build, and it is rarer than anyone expects.",
     "Start with the smallest complete version. Put an eval sheet under it before you tune anything, and write the handover package while you build rather than at the end."]],
  "high|mid": ["good","Build it — but close the Axis B gap first",
    ["The process is well chosen. The organisation is nearly ready, and 'nearly' is where systems quietly die.",
     "Fix the weakest Axis B item before you write anything. It is almost always faster than the build, and skipping it is how a good process becomes a rotting demo."]],
  "high|low": ["warn","The rotting demo",
    ["You have picked an excellent process. You will build something that works, you will demo it, and people will be impressed. Then it will stop being used — because there is no owner, or nobody reviews the output, or it can only be run by you.",
     "This is the classic and most expensive failure in the field, and it is the reason the two axes are scored separately. The problem is not technical and cannot be solved by building better. Every additional hour of engineering makes it worse: a more impressive artifact with nowhere to land.",
     "Do not build until at least one Axis B score has moved."]],
  "mid|high": ["warn","Narrow the process",
    ["The organisation is ready — there is an owner, someone reviews, someone can operate it. That readiness is genuinely scarce and you should spend it well.",
     "The process is only a partial fit. Narrow it to the part that scores highest, or find a neighbouring process that does."]],
  "mid|mid": ["warn","Not compelling yet",
    ["Middling on both axes. Nothing here is disqualifying and nothing here is a reason to start.",
     "Pick the single lowest score across both axes and improve that one thing. Then score it again. Building now means building something mediocre into an organisation that will half-adopt it."]],
  "mid|low": ["stop","Fix the organisation first",
    ["The process is a partial fit and the organisation cannot currently receive it. The second problem is the one that will sink you, and it is the one that building cannot fix.",
     "Nothing you build lands anywhere until Axis B moves. Work on that, and revisit the process choice while you do."]],
  "low|high": ["warn","Wrong process, right organisation",
    ["Encouraging, actually. The organisation is ready and that is the harder half.",
     "You have picked the wrong target. Keep the organisational readiness and spend it on a better one — look at your lowest Axis A score for where to look next."]],
  "low|mid": ["stop","Wrong process",
    ["This process is a poor fit regardless of the organisational picture.",
     "Choose a different target before going further. The Axis A weakness below is where to start looking."]],
  "low|low": ["stop","Not this, not yet",
    ["Don't build. Saying so plainly and early is the most valuable output this filter produces, and by far the cheapest.",
     "The honest version: this isn't the right process, and you're not currently set up to run one anyway. Both are fixable. Neither is fixed by starting."]]
};

function buildAxis(el, defs, name){
  defs.forEach(function(d, i){
    var row = document.createElement("div");
    row.className = "crit";
    var lbl = document.createElement("div");
    lbl.className = "crit-label";
    lbl.innerHTML = "<b>" + d[0] + "</b><span>" + d[1] + "</span>";
    var scale = document.createElement("div");
    scale.className = "scale";
    scale.setAttribute("role","group");
    scale.setAttribute("aria-label", d[0] + ": " + d[1]);
    for (var v = 1; v <= 3; v++){
      var id = name + i + "-" + v;
      var input = document.createElement("input");
      input.type = "radio"; input.name = name + i; input.value = v; input.id = id;
      var l = document.createElement("label");
      l.setAttribute("for", id); l.textContent = v;
      l.title = v === 1 ? "No" : v === 2 ? "Partly" : "Yes";
      scale.appendChild(input); scale.appendChild(l);
    }
    row.appendChild(lbl); row.appendChild(scale);
    el.appendChild(row);
  });
}

function scores(name, count){
  var out = [];
  for (var i = 0; i < count; i++){
    var c = document.querySelector('input[name="' + name + i + '"]:checked');
    out.push(c ? parseInt(c.value, 10) : null);
  }
  return out;
}

function weakest(vals, defs){
  var lowIdx = -1, low = 4;
  vals.forEach(function(v, i){ if (v !== null && v < low){ low = v; lowIdx = i; } });
  return (lowIdx >= 0 && low <= 2) ? defs[lowIdx] : null;
}

function update(){
  var a = scores("a", 5), b = scores("b", 3);
  var doneA = a.every(function(v){ return v !== null; });
  var doneB = b.every(function(v){ return v !== null; });
  var sumA = a.reduce(function(x, y){ return x + (y || 0); }, 0);
  var sumB = b.reduce(function(x, y){ return x + (y || 0); }, 0);

  document.getElementById("tot-a").textContent = doneA ? sumA : (sumA || "—");
  document.getElementById("tot-b").textContent = doneB ? sumB : (sumB || "—");

  var labels = {high:"High", mid:"Middling", low:"Low"};
  document.getElementById("band-a").textContent =
    doneA ? labels[bandA(sumA)] : (5 - a.filter(function(v){return v!==null;}).length) + " left to score";
  document.getElementById("band-b").textContent =
    doneB ? labels[bandB(sumB)] : (3 - b.filter(function(v){return v!==null;}).length) + " left to score";

  var box = document.getElementById("verdict");
  if (!doneA || !doneB){ box.hidden = true; return; }

  var key = bandA(sumA) + "|" + bandB(sumB);
  var v = VERDICTS[key];
  box.hidden = false;
  box.className = "verdict " + v[0];

  var h = "<h3>" + v[1] + "</h3>";
  v[2].forEach(function(p){ h += "<p>" + p + "</p>"; });

  var wa = weakest(a, AXIS_A), wb = weakest(b, AXIS_B);
  if (wa || wb){
    h += '<div class="weakest"><strong>Weakest link';
    h += (wa && wb) ? "s" : "";
    h += ":</strong> ";
    var parts = [];
    if (wb) parts.push("<em>" + wb[0] + "</em> — " + wb[2]);
    if (wa) parts.push("<em>" + wa[0] + "</em> — " + wa[2]);
    h += parts.join(" ") + "</div>";
  }
  h += '<p style="margin-top:.8rem;font-size:.82rem;color:var(--ink-3)">' +
       "Before you leave the room: if this works perfectly, whose job changes, and have " +
       "they been asked? Who gets the phone call when the output is wrong in six months? " +
       "If that second question has no name in it, your Axis B score is optimistic.</p>";
  box.innerHTML = h;
}

function summary(){
  var a = scores("a", 5), b = scores("b", 3);
  var sumA = a.reduce(function(x,y){ return x + (y||0); }, 0);
  var sumB = b.reduce(function(x,y){ return x + (y||0); }, 0);
  var lines = ["Process Filter result", ""];
  lines.push("Axis A - the process: " + sumA + "/15");
  AXIS_A.forEach(function(d,i){ lines.push("  " + d[0] + ": " + (a[i] || "-")); });
  lines.push("");
  lines.push("Axis B - the organisation: " + sumB + "/9");
  AXIS_B.forEach(function(d,i){ lines.push("  " + d[0] + ": " + (b[i] || "-")); });
  lines.push("");
  lines.push("Scored separately. Not summed.");
  var v = VERDICTS[bandA(sumA) + "|" + bandB(sumB)];
  if (a.every(function(x){return x!==null;}) && b.every(function(x){return x!==null;})){
    lines.push("");
    lines.push("Verdict: " + v[1]);
    lines.push(v[2][0]);
  }
  return lines.join("\n");
}

(function(){
  var ea = document.getElementById("axis-a"), eb = document.getElementById("axis-b");
  if (!ea) return;
  buildAxis(ea, AXIS_A, "a");
  buildAxis(eb, AXIS_B, "b");
  document.getElementById("pf-form").addEventListener("change", update);
  document.getElementById("pf-reset").addEventListener("click", function(){
    document.getElementById("pf-form").reset();
    update();
  });
  document.getElementById("pf-copy").addEventListener("click", function(){
    var btn = this, text = summary();
    var done = function(ok){
      btn.textContent = ok ? "Copied" : "Press ⌘C";
      setTimeout(function(){ btn.textContent = "Copy summary"; }, 1600);
    };
    if (navigator.clipboard && window.isSecureContext){
      navigator.clipboard.writeText(text).then(function(){ done(true); }, function(){ done(false); });
    } else {
      var ta = document.createElement("textarea");
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { done(document.execCommand("copy")); } catch(e){ done(false); }
      document.body.removeChild(ta);
    }
  });
  update();
})();

/* Scroll-spy */
(function(){
  var links = [].slice.call(document.querySelectorAll(".sidebar a.nav"));
  var map = {};
  links.forEach(function(l){ map[l.getAttribute("href").slice(1)] = l; });
  var targets = Object.keys(map)
    .map(function(id){ return document.getElementById(id); })
    .filter(Boolean);
  if (!targets.length) return;

  var visible = {};
  var obs = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ visible[e.target.id] = e.isIntersecting; });
    var current = null;
    for (var i = 0; i < targets.length; i++){
      if (visible[targets[i].id]){ current = targets[i].id; break; }
    }
    if (!current) return;
    links.forEach(function(l){ l.classList.remove("active"); });
    if (map[current]){
      map[current].classList.add("active");
      map[current].scrollIntoView({block:"nearest"});
    }
  }, {rootMargin:"0px 0px -70% 0px", threshold:0});

  targets.forEach(function(t){ obs.observe(t); });
})();
"""


def build():
    sec = readme_sections()
    tools = [load_page(ROOT / "docs" / "tools" / (s + ".md"), s) for s in TOOLS]
    practices = [load_page(ROOT / "docs" / "practices" / (s + ".md"), s) for s in PRACTICES]

    intro = sec["__intro__"]
    thesis = next(l.strip().strip("*") for l in intro if l.strip().startswith("**The bottleneck"))
    spine = "Design → [ Build ⇄ Evaluate ] → Ship"

    # Sidebar
    nav = ['<a class="brand" href="#top">Applied AI Operations'
           '<span>Design · Build · Evaluate · Ship</span></a>', "<nav>"]
    nav.append('<a class="nav" href="#process-filter">The Process Filter</a>')
    nav.append('<div class="group">The Tools</div>')
    for p in tools:
        nav.append('<a class="nav" href="#%s">%s</a>' % (p["slug"], html.escape(p["title"])))
    nav.append('<div class="group">The Practices</div>')
    for p in practices:
        nav.append('<a class="nav" href="#%s">%s</a>' % (p["slug"], html.escape(p["title"])))
    nav.append('<div class="group">Positions</div>')
    nav.append('<a class="nav" href="#out-of-scope">Out of scope</a>')
    nav.append('<a class="nav" href="#freshness">Freshness</a>')
    nav.append('<a class="nav" href="#about">Author &amp; license</a>')
    nav.append("</nav>")
    nav.append('<div class="foot">Canonical source is <code>docs/</code>.<br>'
               'This page is generated from it.<br><br>'
               '<a href="%s">Repository</a></div>' % html.escape(REPO_URL))

    def section(p):
        return (
            '<section id="%s">\n'
            '<div class="section-head"><h2>%s<span class="verb verb-%s">%s</span></h2></div>\n'
            "%s\n</section>" % (p["slug"], html.escape(p["title"]), p["verb"], p["verb"], p["html"])
        )

    body = []
    body.append('<div class="hero" id="top">')
    body.append("<h1>Applied AI Operations</h1>")
    body.append('<p class="thesis">%s</p>' % inline(thesis))
    body.append('<div class="spine">%s</div>' % spine)
    body.append(render([l for l in sec["The spine"] if not l.strip().startswith("```")
                        and "Design →" not in l], heading_offset=2))
    body.append('<p class="meta">An opinionated reference, not documentation. '
                'No prerequisites, no reading order.</p>')
    body.append("</div>")

    body.append(PF_HTML.replace("__REPO__", html.escape(REPO_URL)))

    body.append('<section id="who-its-for"><div class="section-head">'
                '<h2>Who this is for</h2></div>')
    body.append(render(sec["Who this is for"], heading_offset=2, slug_prefix="who-"))
    body.append('<h3 id="not-documentation">This is not documentation</h3>')
    body.append(render(sec["This is not documentation"], heading_offset=2, slug_prefix="notdocs-"))
    body.append("</section>")

    body.append('<section><div class="section-head"><h2>The Tools</h2></div>'
                "<p>What you use. Five of them.</p></section>")
    body.extend(section(p) for p in tools)

    body.append('<section><div class="section-head"><h2>The Practices</h2></div>'
                "<p>How you use them well. Six of them.</p></section>")
    body.extend(section(p) for p in practices)

    body.append('<section id="out-of-scope"><div class="section-head">'
                "<h2>Deliberately out of scope</h2></div>")
    body.append(render(sec["Deliberately out of scope"], heading_offset=2, slug_prefix="oos-"))
    body.append("</section>")

    body.append('<section id="freshness"><div class="section-head"><h2>Freshness</h2></div>')
    body.append(render(sec["Freshness"], heading_offset=2, slug_prefix="fresh-"))
    body.append("</section>")

    body.append('<section id="about"><div class="section-head">'
                "<h2>Contributing, license, author</h2></div>")
    body.append(render(sec["Contributing"], heading_offset=2, slug_prefix="contrib-"))
    body.append(render(sec["License"], heading_offset=2, slug_prefix="lic-"))
    body.append(render(sec["Author"], heading_offset=2, slug_prefix="author-"))
    body.append("</section>")

    doc = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Applied AI Operations</title>
<meta name="description" content="An opinionated reference for putting AI systems inside an organisation and making them stay there. Design, Build, Evaluate, Ship.">
<meta name="author" content="Billie Jeurink">
<meta property="og:title" content="Applied AI Operations">
<meta property="og:description" content="The bottleneck with AI is not the model. It's that almost nobody knows how to put one inside an organisation and make it stay there.">
<meta property="og:type" content="website">
<!--
  GENERATED FILE - do not edit by hand.
  Canonical source is README.md and docs/. Regenerate with:  python3 build-site.py
-->
<style>__CSS__</style>
</head>
<body>
<div class="layout">
<aside class="sidebar">__NAV__</aside>
<main>
__BODY__
<footer>
<p><span class="reviewed">Last reviewed: __REVIEWED__</span> &mdash; reviewed, not merely updated.
Reviewed monthly and after any significant Claude platform release.</p>
<p>Written and maintained by Billie Jeurink.
<a href="mailto:billie@bjeurink.com">billie@bjeurink.com</a>.
Licensed <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>.</p>
<p>The canonical source for this content is <code>docs/</code> in the repository.
This page is generated from it by <code>build-site.py</code>; where they disagree, the docs are right.</p>
</footer>
</main>
</div>
<script>__JS__</script>
</body>
</html>
"""
    doc = doc.replace("__CSS__", CSS.strip())
    doc = doc.replace("__NAV__", "\n".join(nav))
    doc = doc.replace("__BODY__", "\n".join(body))
    doc = doc.replace("__REVIEWED__", LAST_REVIEWED)
    doc = doc.replace("__JS__", PF_JS.strip())

    out = ROOT / "site" / "index.html"
    out.write_text(doc, encoding="utf-8")
    print("wrote %s (%.1f KB)" % (out, len(doc) / 1024))
    print("  %d tool pages, %d practice pages" % (len(tools), len(practices)))


if __name__ == "__main__":
    build()
