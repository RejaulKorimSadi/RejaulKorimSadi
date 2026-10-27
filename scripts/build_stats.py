import json, os, sys, html, math, urllib.request
from datetime import datetime, timezone

USER = os.environ.get("GH_USER", "RejaulKorimSadi")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUTDIR = os.environ.get("OUTDIR", "assets")
FONT = "'Segoe UI','Inter',-apple-system,'Helvetica Neue',Arial,sans-serif"
PALETTE = ["#56B4E9", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#F0E442", "#7f8ea3"]
INK, MUTED, LINE = "#e8eef6", "#9aa9bb", "#24344c"
e = html.escape


def api(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", USER)
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    repos = api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
    own = [r for r in repos if not r.get("fork")]
    d = dict(repos=len(own), stars=sum(r.get("stargazers_count", 0) for r in own),
             commits=None, prs=None, issues=None, contributed=None, total=None, langs={})
    for r in own:
        try:
            for k, v in api(r["languages_url"]).items():
                d["langs"][k] = d["langs"].get(k, 0) + v
        except Exception:
            pass
    if TOKEN:
        q = """query($l:String!){user(login:$l){
          contributionsCollection{totalCommitContributions totalPullRequestContributions totalIssueContributions
            contributionCalendar{totalContributions}}
          repositoriesContributedTo(contributionTypes:[COMMIT,PULL_REQUEST,ISSUE,REPOSITORY]){totalCount}}}"""
        try:
            u = api("https://api.github.com/graphql", {"query": q, "variables": {"l": USER}})["data"]["user"]
            c = u["contributionsCollection"]
            d.update(commits=c["totalCommitContributions"], prs=c["totalPullRequestContributions"],
                     issues=c["totalIssueContributions"], total=c["contributionCalendar"]["totalContributions"],
                     contributed=u["repositoriesContributedTo"]["totalCount"])
        except Exception as ex:
            print("graphql skipped:", ex)
    return d


def frame(W, H, title, body, key):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><linearGradient id="g{key}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset="1" stop-color="#132238"/></linearGradient>
<clipPath id="c{key}"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>
<style>.t{{font:700 19px {FONT};fill:{INK}}}.lab{{font:500 14px {FONT};fill:{MUTED}}}.val{{font:700 15px {FONT};fill:{INK}}}
.lg{{font:600 13px {FONT};fill:#c9d6e6}}.pc{{font-weight:400;fill:{MUTED}}}.ring{{font:800 26px {FONT};fill:{INK}}}.rl{{font:500 11px {FONT};fill:{MUTED}}}
.st{{font:400 10.5px {FONT};fill:#6f8096}}</style>
<g clip-path="url(#c{key})"><rect width="{W}" height="{H}" fill="url(#g{key})"/><rect width="{W}" height="5" fill="#56B4E9"/></g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{LINE}"/>
<text x="28" y="48" class="t">{e(title)}</text>
{body}</svg>'''


def languages_card(d):
    W, H = 600, 260
    total = sum(d["langs"].values()) or 1
    top = sorted(d["langs"].items(), key=lambda x: -x[1])[:8]
    rest = total - sum(v for _, v in top)
    if rest > 0:
        top.append(("Other", rest))
    x = 28; seg = []; leg = []
    for i, (n, v) in enumerate(top):
        w = 544 * v / total
        seg.append(f'<rect x="{x:.1f}" y="74" width="{w:.1f}" height="12" fill="{PALETTE[i % len(PALETTE)]}"/>')
        x += w
        cx = 28 + (i % 3) * 185; cy = 124 + (i // 3) * 32
        leg.append(f'<circle cx="{cx+6}" cy="{cy-5}" r="6" fill="{PALETTE[i % len(PALETTE)]}"/>'
                   f'<text x="{cx+20}" y="{cy}" class="lg">{e(n[:16])} <tspan class="pc">{100*v/total:.1f}%</tspan></text>')
    body = (f'<clipPath id="bar"><rect x="28" y="74" width="544" height="12" rx="6"/></clipPath>'
            f'<rect x="28" y="74" width="544" height="12" rx="6" fill="#1d2c42"/><g clip-path="url(#bar)">{"".join(seg)}</g>'
            + "".join(leg))
    if not d["langs"]:
        body = f'<text x="28" y="130" class="lab">Language stats appear after the first workflow run.</text>'
    return frame(W, H, "Most Used Languages", body, "l")


def stats_card(d):
    W, H = 600, 260
    f = lambda v: "–" if v is None else f"{v:,}"
    rows = [("★", "Total stars earned", f(d["stars"])), ("⟳", "Commits (last 12 months)", f(d["commits"])),
            ("⇄", "Pull requests", f(d["prs"])), ("◎", "Issues", f(d["issues"])),
            ("▣", "Contributed to (repos)", f(d["contributed"])), ("❐", "Public repositories", f(d["repos"]))]
    b = []
    for i, (ic, lab, val) in enumerate(rows):
        y = 86 + i * 27
        b.append(f'<text x="30" y="{y}" class="val" fill="#56B4E9" style="fill:#56B4E9">{ic}</text>'
                 f'<text x="56" y="{y}" class="lab">{e(lab)}</text><text x="340" y="{y}" class="val" text-anchor="end">{e(val)}</text>')
    tot = d["total"]
    goal = 365
    frac = min((tot or 0) / goal, 1.0)
    r = 58; cx, cy = 480, 140; circ = 2 * math.pi * r
    ring = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1d2c42" stroke-width="10"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#E69F00" stroke-width="10" stroke-linecap="round" '
            f'stroke-dasharray="{circ*frac:.1f} {circ:.1f}" transform="rotate(-90 {cx} {cy})"/>'
            f'<text x="{cx}" y="{cy+6}" class="ring" text-anchor="middle">{f(tot)}</text>'
            f'<text x="{cx}" y="{cy+28}" class="rl" text-anchor="middle">contributions</text>'
            f'<text x="{cx}" y="{cy+82}" class="rl" text-anchor="middle">last 12 months</text>')
    stamp = datetime.now(timezone.utc).strftime("%d %b %Y")
    body = "".join(b) + ring + f'<text x="{W-20}" y="{H-12}" class="st" text-anchor="end">updated {stamp}</text>'
    return frame(W, H, f"{USER}'s GitHub Stats", body, "s")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        data = dict(repos=17, stars=None, commits=None, prs=None, issues=None, contributed=None, total=34, langs={})
    else:
        try:
            data = collect()
        except Exception as ex:
            print("GitHub API failed, keeping old cards:", ex)
            sys.exit(0)
    os.makedirs(OUTDIR, exist_ok=True)
    open(f"{OUTDIR}/languages.svg", "w", encoding="utf-8").write(languages_card(data))
    open(f"{OUTDIR}/stats.svg", "w", encoding="utf-8").write(stats_card(data))
    print("cards written", {k: v for k, v in data.items() if k != "langs"})
