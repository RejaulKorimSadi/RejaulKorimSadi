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


def shell(P, W, H, label, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><style>{FONTS}
.d{{font-family:Disp}}.m{{font-family:Mono}}.s{{font-family:Sans}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{P["grid"]}"/></pattern></defs>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{P["bg"]}" stroke="{P["line"]}"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="url(#dots)"/>
<text x="28" y="40" class="m" font-size="11" letter-spacing="1.8" fill="{P["teal"]}">{e(label)}</text>
<text x="28" y="76" class="d" font-size="27" font-weight="600" fill="{P["ink"]}">{e(title)}</text>
{body}</svg>'''


def stats_card(d, P):
    W, H = 590, 300
    f = lambda v: "–" if v is None else f"{v:,}"
    rows = [("Commits", f(d["commits"])), ("Pull requests", f(d["prs"])), ("Issues", f(d["issues"])),
            ("Repositories contributed to", f(d["contributed"])), ("Public repositories", f(d["repos"])), ("Stars earned", f(d["stars"]))]
    b = []
    for i, (lab, val) in enumerate(rows):
        y = 116 + i * 28
        b.append(f'<text x="28" y="{y}" class="s" font-size="14" fill="{P["muted"]}">{e(lab)}</text>'
                 f'<text x="330" y="{y}" class="m" font-size="14" font-weight="600" fill="{P["ink"]}" text-anchor="end">{e(val)}</text>'
                 f'<path d="M28 {y+9}H330" stroke="{P["line"]}" stroke-dasharray="2 4"/>')
    tot = d["total"] or 0
    frac = min(tot / 365, 1.0)
    r = 62; cx, cy = 465, 170; c = 2 * math.pi * r
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P["line"]}" stroke-width="10"/>'
             + (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P["teal"]}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{c*frac:.1f} {c:.1f}" transform="rotate(-90 {cx} {cy})">'
             f'<animate attributeName="stroke-dasharray" values="0 {c:.1f};{c*frac:.1f} {c:.1f}" dur="1.6s" fill="freeze"/></circle>' if frac > 0 else '') +
             f'<text x="{cx}" y="{cy+8}" class="d" font-size="30" font-weight="600" fill="{P["ink"]}" text-anchor="middle">{f(d["total"])}</text>'
             f'<text x="{cx}" y="{cy+30}" class="m" font-size="10.5" letter-spacing="1.2" fill="{P["muted"]}" text-anchor="middle">CONTRIBUTIONS</text>')
    stamp = datetime.now(timezone.utc).strftime("%d %b %Y").upper()
    b.append(f'<text x="{W-28}" y="40" class="m" font-size="10.5" letter-spacing="1.5" fill="{P["faint"]}" text-anchor="end">UPDATED {stamp}</text>')
    return shell(P, W, H, "GITHUB · LAST 12 MONTHS", "Activity", "".join(b))


def languages_card(d, P):
    W, H = 590, 300
    pal = [P["teal"], P["amber"], P["red"], P["ink"], P["muted"], P["faint"]]
    total = sum(d["langs"].values()) or 1
    top = sorted(d["langs"].items(), key=lambda x: -x[1])[:5]
    rest = total - sum(v for _, v in top)
    if rest > 0:
        top.append(("Other", rest))
    b = [f'<rect x="28" y="104" width="534" height="14" rx="3" fill="{P["line"]}"/>']
    x = 28
    for i, (n, v) in enumerate(top):
        w = 534 * v / total
        b.append(f'<rect x="{x:.1f}" y="104" width="{max(w-2,1):.1f}" height="14" rx="2" fill="{pal[i]}"><animate attributeName="opacity" values="0;1" dur=".6s" begin="{i*.12:.2f}s" fill="freeze"/></rect>')
        x += w
        cx = 28 + (i % 2) * 280; cy = 158 + (i // 2) * 36
        b.append(f'<rect x="{cx}" y="{cy-11}" width="12" height="12" rx="2" fill="{pal[i]}"/>'
                 f'<text x="{cx+22}" y="{cy}" class="s" font-size="14" fill="{P["ink"]}">{e(n[:20])}</text>'
                 f'<text x="{cx+250}" y="{cy}" class="m" font-size="13" fill="{P["muted"]}" text-anchor="end">{100*v/total:.1f}%</text>')
    if not d["langs"]:
        b = [f'<text x="28" y="140" class="s" font-size="14" fill="{P["muted"]}">Language data appears after the first workflow run.</text>']
    return shell(P, W, H, "ACROSS MY PUBLIC REPOSITORIES", "Languages", "".join(b))


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
    print("cards written", {k: v for k, v in data.items() if k != "langs"})
