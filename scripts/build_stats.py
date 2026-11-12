import json, os, sys, html, math, urllib.request
from datetime import datetime, timezone

USER = os.environ.get("GH_USER", "RejaulKorimSadi")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUTDIR = os.environ.get("OUTDIR", "assets")
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = open(os.path.join(HERE, "fonts.css"), encoding="utf-8").read()
e = html.escape
DARK = dict(bg="#090C11", panel="#0E131A", line="#1C2531", grid="#141B24", ink="#ECF0F3", muted="#8B98A7",
            faint="#4C5867", teal="#6FE3D3", amber="#F2B460", red="#FF5D4F")
LIGHT = dict(bg="#F6F2EA", panel="#FFFCF6", line="#E2DACB", grid="#ECE5D8", ink="#15181D", muted="#5C6672",
             faint="#A69E90", teal="#0D7A6E", amber="#A3600E", red="#C4372A")


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
             commits=None, prs=None, issues=None, contributed=None, total=None, langs={}, weeks=[])
    for r in own:
        try:
            for k, v in api(r["languages_url"]).items():
                d["langs"][k] = d["langs"].get(k, 0) + v
        except Exception:
            pass
    if TOKEN:
        q = """query($l:String!){user(login:$l){
          contributionsCollection{totalCommitContributions totalPullRequestContributions totalIssueContributions
            contributionCalendar{totalContributions weeks{contributionDays{contributionCount weekday date}}}}
          repositoriesContributedTo(contributionTypes:[COMMIT,PULL_REQUEST,ISSUE,REPOSITORY]){totalCount}}}"""
        try:
            u = api("https://api.github.com/graphql", {"query": q, "variables": {"l": USER}})["data"]["user"]
            c = u["contributionsCollection"]
            d.update(commits=c["totalCommitContributions"], prs=c["totalPullRequestContributions"],
                     issues=c["totalIssueContributions"], total=c["contributionCalendar"]["totalContributions"],
                     contributed=u["repositoriesContributedTo"]["totalCount"],
                     weeks=[[(x["contributionCount"], x["weekday"], x["date"]) for x in w["contributionDays"]] for w in c["contributionCalendar"]["weeks"]])
        except Exception as ex:
            print("graphql skipped:", ex)
    return d


def scan(P, W, H, dur=8):
    return (f'<rect x="-200" y="0" width="160" height="{H}" fill="{P["teal"]}" opacity=".06"><animateTransform attributeName="transform" type="translate" values="0 0;{W+260} 0" dur="{dur}s" repeatCount="indefinite"/></rect>'
            f'<rect x="-40" y="0" width="1.2" height="{H}" fill="{P["teal"]}" opacity=".35"><animateTransform attributeName="transform" type="translate" values="0 0;{W+260} 0" dur="{dur}s" repeatCount="indefinite"/></rect>')


def shell(P, W, H, label, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><style>{FONTS}
.d{{font-family:Disp}}.m{{font-family:Mono}}.s{{font-family:Sans}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{P["grid"]}"/></pattern></defs>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{P["bg"]}" stroke="{P["line"]}"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="url(#dots)"/>
<clipPath id="cl"><rect width="{W}" height="{H}" rx="16"/></clipPath>
<text x="28" y="42" class="m" font-size="12.5" letter-spacing="1.4" fill="{P["teal"]}">{e(label)}</text>
<text x="28" y="80" class="d" font-size="30" font-weight="600" fill="{P["ink"]}">{e(title)}</text>
{body}<g clip-path="url(#cl)">{scan(P, W, H)}</g></svg>'''


def stats_card(d, P):
    W, H = 590, 330
    f = lambda v: "–" if v is None else f"{v:,}"
    rows = [("Commits", f(d["commits"])), ("Pull requests", f(d["prs"])), ("Issues", f(d["issues"])),
            ("Repositories contributed to", f(d["contributed"])), ("Public repositories", f(d["repos"])), ("Stars earned", f(d["stars"]))]
    b = []
    for i, (lab, val) in enumerate(rows):
        y = 124 + i * 31
        b.append(f'<text x="28" y="{y}" class="s" font-size="15.5" fill="{P["ink"]}">{e(lab)}</text>'
                 f'<text x="330" y="{y}" class="m" font-size="15.5" font-weight="600" fill="{P["ink"]}" text-anchor="end">{e(val)}</text>'
                 f'<path d="M28 {y+9}H330" stroke="{P["line"]}" stroke-dasharray="2 4"/>')
    tot = d["total"] or 0
    frac = min(tot / 365, 1.0)
    r = 62; cx, cy = 465, 190; c = 2 * math.pi * r
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P["line"]}" stroke-width="10"/>'
             + (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P["teal"]}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{c*frac:.1f} {c:.1f}" transform="rotate(-90 {cx} {cy})">'
             f'<animate attributeName="stroke-dasharray" values="0 {c:.1f};{c*frac:.1f} {c:.1f};{c*frac:.1f} {c:.1f};0 {c:.1f}" keyTimes="0;.25;.85;1" dur="8s" repeatCount="indefinite"/></circle>' if frac > 0 else '') +
             f'<circle cx="{cx}" cy="{cy}" r="{r+16}" fill="none" stroke="{P["teal"]}" stroke-opacity=".4" stroke-dasharray="2 7"><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};360 {cx} {cy}" dur="16s" repeatCount="indefinite"/></circle>' +
             f'<text x="{cx}" y="{cy+8}" class="d" font-size="30" font-weight="600" fill="{P["ink"]}" text-anchor="middle">{f(d["total"])}</text>'
             f'<text x="{cx}" y="{cy+30}" class="m" font-size="10.5" letter-spacing="1.2" fill="{P["muted"]}" text-anchor="middle">CONTRIBUTIONS</text>')
    stamp = datetime.now(timezone.utc).strftime("%d %b %Y").upper()
    b.append(f'<text x="{W-28}" y="40" class="m" font-size="10.5" letter-spacing="1.5" fill="{P["faint"]}" text-anchor="end">UPDATED {stamp}</text>')
    return shell(P, W, H, "GITHUB · LAST 12 MONTHS", "Activity", "".join(b))


def languages_card(d, P):
    W, H = 590, 330
    pal = [P["teal"], P["amber"], P["red"], P["ink"], P["muted"], P["faint"]]
    total = sum(d["langs"].values()) or 1
    top = sorted(d["langs"].items(), key=lambda x: -x[1])[:5]
    rest = total - sum(v for _, v in top)
    if rest > 0:
        top.append(("Other", rest))
    b = [f'<rect x="28" y="110" width="534" height="16" rx="3" fill="{P["line"]}"/>']
    x = 28
    for i, (n, v) in enumerate(top):
        w = 534 * v / total
        b.append(f'<rect x="{x:.1f}" y="110" width="{max(w-2,1):.1f}" height="16" rx="2" fill="{pal[i]}"><animate attributeName="height" values="16;24;16" dur="2.4s" begin="{i*.3:.1f}s" repeatCount="indefinite"/><animate attributeName="y" values="110;106;110" dur="2.4s" begin="{i*.3:.1f}s" repeatCount="indefinite"/></rect>')
        x += w
        cx = 28 + (i % 2) * 280; cy = 172 + (i // 2) * 42
        b.append(f'<rect x="{cx}" y="{cy-12}" width="13" height="13" rx="2" fill="{pal[i]}"><animate attributeName="opacity" values="1;.35;1" dur="3s" begin="{i*.4:.1f}s" repeatCount="indefinite"/></rect>'
                 f'<text x="{cx+24}" y="{cy}" class="s" font-size="15.5" fill="{P["ink"]}">{e(n[:20])}</text>'
                 f'<text x="{cx+250}" y="{cy}" class="m" font-size="14" fill="{P["ink"]}" text-anchor="end">{100*v/total:.1f}%</text>')
    if not d["langs"]:
        b = [f'<text x="28" y="140" class="s" font-size="14" fill="{P["muted"]}">Language data appears after the first workflow run.</text>']
    return shell(P, W, H, "ACROSS MY PUBLIC REPOSITORIES", "Languages", "".join(b))


MON = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


def skyline(d, P):
    W, H = 1200, 400
    weeks = d.get("weeks") or []
    cell, dx, dy, x0, base = 19.2, 7, -8, 62, 330
    css = ('.b{transform-box:fill-box;transform-origin:50% 100%;animation:g 10s cubic-bezier(.2,.7,.2,1) infinite}'
           '@keyframes g{0%{transform:scaleY(.04)}22%{transform:scaleY(1)}86%{transform:scaleY(1)}100%{transform:scaleY(.04)}}')
    body = [f'<style>{css}</style>']
    mx = max([c for w in weeks for c, _, _ in w] or [0]) or 1
    shades = [P["faint"], P["teal"]]
    rows = []
    for di in range(6, -1, -1):
        for wi, w in enumerate(weeks):
            for c, wd, dt in w:
                if wd != di:
                    continue
                px = x0 + wi * cell + (6 - di) * dx
                py = base + (6 - di) * dy
                tw = cell - 4
                if c == 0:
                    rows.append(f'<path d="M{px:.1f} {py}h{tw:.1f}l{dx} {dy}h-{tw:.1f}z" fill="{P["line"]}" fill-opacity=".8"/>')
                    continue
                h = 6 + 92 * (c / mx) ** .5
                lv = min(int(4 * c / mx), 3)
                op = [.45, .65, .85, 1][lv]
                top = f'M{px:.1f} {py-h:.1f}h{tw:.1f}l{dx} {dy}h-{tw:.1f}z'
                front = f'M{px:.1f} {py-h:.1f}h{tw:.1f}v{h:.1f}h-{tw:.1f}z'
                side = f'M{px+tw:.1f} {py-h:.1f}l{dx} {dy}v{h:.1f}l-{dx} {-dy}z'
                rows.append(f'<g class="b" style="animation-delay:{wi*.045:.2f}s">'
                            f'<path d="{side}" fill="{P["teal"]}" fill-opacity="{op*.45:.2f}"/>'
                            f'<path d="{front}" fill="{P["teal"]}" fill-opacity="{op*.7:.2f}"/>'
                            f'<path d="{top}" fill="{P["teal"]}" fill-opacity="{op:.2f}"/></g>')
    body.extend(rows)
    last = None
    for wi, w in enumerate(weeks):
        if not w:
            continue
        m = int(w[0][2][5:7])
        if m != last and wi < len(weeks) - 2:
            body.append(f'<text x="{x0+wi*cell:.0f}" y="{base+24}" class="m" font-size="12" fill="{P["muted"]}">{MON[m-1]}</text>')
            last = m
    if not weeks:
        for di in range(7):
            for wi in range(53):
                px = x0 + wi * cell + (6 - di) * dx; py = base + (6 - di) * dy
                body.append(f'<path d="M{px:.1f} {py}h{cell-4:.1f}l{dx} {dy}h-{cell-4:.1f}z" fill="{P["line"]}" fill-opacity=".8"/>')
        body.append(f'<text x="{W/2}" y="{base-120}" class="s" font-size="16" fill="{P["muted"]}" text-anchor="middle">The first scan appears after the next daily update.</text>')
    tot = d.get("total")
    body.append(f'<text x="{W-28}" y="42" class="m" font-size="12.5" letter-spacing="1.4" fill="{P["muted"]}" text-anchor="end">{"" if tot is None else f"{tot:,} CONTRIBUTIONS · "}EACH TOWER IS ONE DAY</text>')
    return shell(P, W, H, "CONTRIBUTION SCAN · LAST 12 MONTHS", "Every day, in three dimensions", "".join(body))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        data = dict(repos=17, stars=9, commits=412, prs=6, issues=3, contributed=4, total=486,
                    langs={"Python": 61, "Jupyter Notebook": 22, "TeX": 8, "HTML": 5, "Shell": 2, "C++": 2})
    else:
        try:
            data = collect()
        except Exception as ex:
            print("GitHub API failed, keeping old cards:", ex)
            sys.exit(0)
    os.makedirs(OUTDIR, exist_ok=True)
    for mode, P in (("dark", DARK), ("light", LIGHT)):
        open(f"{OUTDIR}/stats-{mode}.svg", "w", encoding="utf-8").write(stats_card(data, P))
        open(f"{OUTDIR}/languages-{mode}.svg", "w", encoding="utf-8").write(languages_card(data, P))
        open(f"{OUTDIR}/skyline-{mode}.svg", "w", encoding="utf-8").write(skyline(data, P))
    print("cards written", {k: v for k, v in data.items() if k not in ("langs", "weeks")})
