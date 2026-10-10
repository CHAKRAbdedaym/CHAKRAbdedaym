#!/usr/bin/env python3
"""Draws the custom animated SVG assets for Chakra's GitHub profile README.

Usage:  python3 gen.py [out_dir]          -> animated assets
        STATIC=1 python3 gen.py preview   -> static frames (for rasterizing / QA)
"""
import os, sys, html, math, random, textwrap

STATIC = os.environ.get("STATIC") == "1"
OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(OUT, exist_ok=True)

W = 900
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'SF Mono', Menlo, Consolas, 'Liberation Mono', 'DejaVu Sans Mono', monospace"
SKY, SKY2, SKY3 = "#0ea5e9", "#38bdf8", "#7dd3fc"
CYAN, VIOLET, GREEN = "#22d3ee", "#8b5cf6", "#34d399"
AMBER, PINK, BLUE, RED = "#fbbf24", "#f472b6", "#60a5fa", "#f87171"
TEXT, MUTED = "#cbd5e1", "#94a3b8"

BASE_CSS = "text{font-family:%s}.m{font-family:%s}.chip{font-size:12.5px;font-weight:500}" % (SANS, MONO)

COMMON_DEFS = f'''
<linearGradient id="gBg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#040916"/><stop offset=".55" stop-color="#07142b"/><stop offset="1" stop-color="#062236"/></linearGradient>
<linearGradient id="gBorder" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{SKY}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="gTitle" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="{SKY3}"/></linearGradient>
<linearGradient id="gName" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="{SKY3}"/><stop offset="1" stop-color="{SKY}"/></linearGradient>
<linearGradient id="gSub" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{SKY}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<linearGradient id="gLine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{SKY}" stop-opacity=".9"/><stop offset=".6" stop-color="{SKY}" stop-opacity=".15"/><stop offset="1" stop-color="{SKY}" stop-opacity="0"/></linearGradient>
<linearGradient id="gSweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<linearGradient id="gV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<radialGradient id="gCore" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#0d3560"/><stop offset="1" stop-color="#050b1a"/></radialGradient>
<pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="{SKY2}" stroke-opacity=".06"/></pattern>
<filter id="blurS" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="blurL" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="45"/></filter>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
'''


# ------------------------------------------------------------------ helpers
def esc(s):
    return html.escape(s, quote=False)


def wrap(text, n):
    return textwrap.wrap(text, width=n, break_long_words=False)


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def doc(w, h, body, defs="", css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">\n'
            f'<defs>{COMMON_DEFS}{defs}</defs>\n<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n')


def rrect_path(x, y, w, h, r):
    return (f"M{x+r},{y} H{x+w-r} A{r},{r} 0 0 1 {x+w},{y+r} V{y+h-r} A{r},{r} 0 0 1 {x+w-r},{y+h} "
            f"H{x+r} A{r},{r} 0 0 1 {x},{y+h-r} V{y+r} A{r},{r} 0 0 1 {x+r},{y} Z")


def panel(w, h, body, defs="", css="", dot=False, dur=14):
    d = ""
    if dot and not STATIC:
        p = rrect_path(.75, .75, w - 1.5, h - 1.5, 22)
        d = (f'<circle r="9" fill="{CYAN}" opacity=".5" filter="url(#blurS)"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{p}"/></circle>'
             f'<circle r="2.8" fill="#fff"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{p}"/></circle>')
    inner = (f'<clipPath id="clip"><rect width="{w}" height="{h}" rx="22"/></clipPath>'
             f'<g clip-path="url(#clip)">'
             f'<rect width="{w}" height="{h}" fill="url(#gBg)"/>'
             f'<rect width="{w}" height="{h}" fill="url(#grid)"/>'
             f'<circle cx="{w-60}" cy="-10" r="140" fill="{SKY}" opacity=".14" filter="url(#blurL)"/>'
             f'<circle cx="40" cy="{h+10}" r="130" fill="{VIOLET}" opacity=".12" filter="url(#blurL)"/>'
             f'{body}</g>'
             f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="22" fill="none" stroke="url(#gBorder)" stroke-opacity=".55" stroke-width="1.5"/>'
             f'{d}')
    return doc(w, h, inner, defs, css)


def header(num, title):
    s = [f'<text x="30" y="40" class="m" font-size="14" font-weight="700" fill="{SKY}" letter-spacing="1">{num}</text>',
         f'<text x="66" y="41" font-size="23" font-weight="800" letter-spacing="4" fill="url(#gTitle)">{esc(title)}</text>',
         f'<rect x="30" y="56" width="{W-60}" height="2" rx="1" fill="url(#gLine)"/>']
    if not STATIC:
        s.append(f'<rect y="54" width="140" height="6" rx="3" fill="url(#gSweep)"><animate attributeName="x" values="-140;{W}" dur="6s" repeatCount="indefinite"/></rect>')
    return "".join(s)


def cw(t, size=12.5):
    return int(len(t) * size * 0.58 + 22)


def chips(items, x, y, max_w, accent, size=12.5, h=26, gap=8):
    out, cx, cy = [], x, y
    for it in items:
        w = cw(it, size)
        if cx + w > x + max_w and cx > x:
            cx, cy = x, cy + h + gap
        out.append(f'<rect x="{cx}" y="{cy}" width="{w}" height="{h}" rx="{h//2}" fill="{accent}" fill-opacity=".10" stroke="{accent}" stroke-opacity=".38"/>')
        out.append(f'<text x="{cx+w/2:.1f}" y="{cy+h/2+4.3:.1f}" text-anchor="middle" class="chip" fill="#e0f2fe">{esc(it)}</text>')
        cx += w + gap
    return "".join(out), cy + h - y


def frame(w, h, accent, r=16, dot=True, dur=9, off=0):
    s = [f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="{r}" fill="#0a1224" fill-opacity=".92" stroke="{accent}" stroke-opacity=".28" stroke-width="1.5"/>',
         f'<rect x="{r}" y="1" width="52" height="2.5" rx="1.2" fill="{accent}" opacity=".95"/>']
    if dot and not STATIC:
        p = rrect_path(.75, .75, w - 1.5, h - 1.5, r)
        s.append(f'<circle r="7" fill="{accent}" opacity=".5" filter="url(#blurS)"><animateMotion dur="{dur}s" begin="-{off}s" repeatCount="indefinite" path="{p}"/></circle>')
        s.append(f'<circle r="2.3" fill="#fff"><animateMotion dur="{dur}s" begin="-{off}s" repeatCount="indefinite" path="{p}"/></circle>')
    return "".join(s)


def place(x, y, w, h, content, accent, dot=True, dur=9, off=0):
    return f'<g transform="translate({x},{y})">{frame(w, h, accent, dot=dot, dur=dur, off=off)}{content}</g>'


# ------------------------------------------------------------------ hero
HERO_CSS = """
.tw{opacity:.12;animation:tw 4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.08}50%{opacity:.9}}
.f1{animation:f1 16s ease-in-out infinite alternate}
@keyframes f1{to{transform:translate(70px,50px)}}
.f2{animation:f2 20s ease-in-out infinite alternate}
@keyframes f2{to{transform:translate(-90px,-40px)}}
.cyc{animation:cyc 12s linear infinite}
@keyframes cyc{0%{opacity:0;transform:translateY(8px)}4%{opacity:1;transform:translateY(0)}22%{opacity:1;transform:translateY(0)}26%{opacity:0;transform:translateY(-6px)}100%{opacity:0;transform:translateY(-6px)}}
"""


def hero():
    H, cx, cy = 380, 722, 190
    rnd = random.Random(11)
    parts = []
    for _ in range(36):
        x, y = rnd.uniform(18, 882), rnd.uniform(14, 366)
        r = rnd.choice([.8, 1, 1.2, 1.6, 2])
        d, du = rnd.uniform(0, 6), rnd.uniform(3, 7)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#bae6fd" class="tw" style="animation-delay:-{d:.1f}s;animation-duration:{du:.1f}s"/>')
    particles = "".join(parts)

    rings = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{SKY2}" stroke-opacity="{o}" {dash}/>'
        for r, o, dash in [(62, .35, ""), (104, .28, 'stroke-dasharray="3 7"'), (146, .22, "")])

    def spin(r, dur, dots, rev=False):
        frm, to = (f"360 {cx} {cy}", f"0 {cx} {cy}") if rev else (f"0 {cx} {cy}", f"360 {cx} {cy}")
        g = []
        for ang, col, rad in dots:
            x, y = cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang))
            g.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{col}" stroke-opacity=".16"/>')
            g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad*2.8:.1f}" fill="{col}" opacity=".5" filter="url(#blurS)"/>'
                     f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="{col}"/>')
        anim = "" if STATIC else f'<animateTransform attributeName="transform" type="rotate" from="{frm}" to="{to}" dur="{dur}s" repeatCount="indefinite"/>'
        return f'<g>{"".join(g)}{anim}</g>'

    orbit = (rings
             + spin(62, 9, [(20, CYAN, 4.5)])
             + spin(104, 17, [(200, SKY2, 5), (330, VIOLET, 4)], rev=True)
             + spin(146, 28, [(80, GREEN, 4), (190, SKY3, 3.2), (300, PINK, 4)]))
    pulse = "" if STATIC else (
        f'<circle cx="{cx}" cy="{cy}" r="38" fill="none" stroke="{SKY2}" stroke-width="1.5">'
        f'<animate attributeName="r" values="38;74" dur="3.2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".6;0" dur="3.2s" repeatCount="indefinite"/></circle>')
    core = (f'<circle cx="{cx}" cy="{cy}" r="48" fill="{SKY}" opacity=".2" filter="url(#blurS)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="38" fill="url(#gCore)" stroke="{SKY2}" stroke-opacity=".85" stroke-width="1.5"/>'
            f'<text x="{cx}" y="{cy+10}" text-anchor="middle" font-size="29" font-weight="800" letter-spacing="1" fill="url(#gTitle)">CA</text>')

    msgs = ["Building CI/CD pipelines & cloud-native systems",
            "Shipping RAG & AI-powered applications",
            "Automating everything, from commit to production",
            "Open to a PFE internship · February 2027"]
    cyc = "".join(
        f'<g class="cyc" style="animation-delay:{i*3}s" opacity="{1 if i == 0 else 0}">'
        f'<text x="60" y="352" class="m" font-size="16" fill="{SKY3}"><tspan fill="{GREEN}">&gt; </tspan>{esc(m)}</text></g>'
        for i, m in enumerate(msgs))

    live = "" if STATIC else (
        f'<circle cx="84" cy="65" r="5" fill="none" stroke="{GREEN}"><animate attributeName="r" values="5;15" dur="2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".8;0" dur="2s" repeatCount="indefinite"/></circle>')

    body = (
        f'<circle cx="120" cy="40" r="150" fill="{SKY}" opacity=".28" filter="url(#blurL)" class="f1"/>'
        f'<circle cx="780" cy="340" r="170" fill="{VIOLET}" opacity=".22" filter="url(#blurL)" class="f2"/>'
        f'<circle cx="560" cy="30" r="110" fill="{CYAN}" opacity=".13" filter="url(#blurL)" class="f1"/>'
        + particles
        + ('' if STATIC else f'<rect x="0" y="-70" width="{W}" height="70" fill="{SKY2}" opacity=".05"><animate attributeName="y" values="-70;{H}" dur="7s" repeatCount="indefinite"/></rect>')
        + orbit + pulse + core
        + f'<rect x="60" y="48" width="352" height="34" rx="17" fill="{SKY}" fill-opacity=".12" stroke="{SKY2}" stroke-opacity=".55"/>'
        + f'<circle cx="84" cy="65" r="5" fill="{GREEN}"/>' + live
        + f'<text x="102" y="70" class="m" font-size="12.5" font-weight="700" letter-spacing="1.4" fill="{SKY3}">OPEN TO PFE INTERNSHIP · FEB 2027</text>'
        + f'<text x="58" y="164" font-size="70" font-weight="800" letter-spacing="3" fill="url(#gName)" filter="url(#glow)">CHAKRA</text>'
        + f'<text x="58" y="238" font-size="70" font-weight="800" letter-spacing="3" fill="url(#gName)" filter="url(#glow)">ABDEDAYM</text>'
        + f'<text x="60" y="284" font-size="24" font-weight="600" letter-spacing="1.2" fill="url(#gSub)">DevOps  ·  AI  ·  Full-Stack Engineer</text>'
        + f'<text x="60" y="312" font-size="14" fill="{MUTED}">Computer Engineering student · FST Marrakech · Marrakech, Morocco</text>'
        + cyc)
    write("hero.svg", panel(W, H, body, css=HERO_CSS, dot=True, dur=16))


# ------------------------------------------------------------------ about / terminal
def about():
    CW = 9.0
    K, S, P = "#7dd3fc", "#fde68a", "#64748b"
    pad = lambda k: ('"%s":' % k).ljust(14)
    lines = [
        ([("$ ", GREEN), ("whoami", "#ffffff")], True),
        ([("chakra-abdedaym", SKY3), (" — computer engineering student · 5th year", TEXT)], False),
        ([("$ ", GREEN), ("cat profile.json", "#ffffff")], True),
        ([("{", MUTED)], False),
        ([("  ", None), (pad("school"), K), ('"FST Marrakech — Networks & Information Systems"', S), (",", P)], False),
        ([("  ", None), (pad("location"), K), ('"Marrakech, Morocco"', S), (",", P)], False),
        ([("  ", None), (pad("focus"), K), ('["DevOps", "AI", "Full-Stack"]', S), (",", P)], False),
        ([("  ", None), (pad("languages"), K), ('["Arabic", "French", "English"]', S), (",", P)], False),
        ([("  ", None), (pad("seeking"), K), ('"PFE internship · starting February 2027"', S)], False),
        ([("}", MUTED)], False),
        ([("$ ", GREEN)], True),
    ]
    y0, dy = 152, 24
    t, starts = 0.6, []
    for segs, cmd in lines:
        n = sum(len(x[0]) for x in segs)
        d = max(.5, n * .07) if cmd else max(.3, n * .028)
        starts.append((t, d, n))
        t += d + (.55 if cmd else .12)
    T = round(t + 5.5, 1)

    defs, body = [], []
    for i, ((segs, cmd), (s, d, n)) in enumerate(zip(lines, starts)):
        y = y0 + i * dy
        wt = n * CW + 8
        if STATIC:
            clip = f'<rect x="56" y="{y-16}" width="{wt+60:.0f}" height="22"/>'
        else:
            kt = f"0;{s/T:.4f};{(s+d)/T:.4f};{(T-1.0)/T:.4f};{(T-0.4)/T:.4f};1"
            clip = (f'<rect x="56" y="{y-16}" width="0" height="22"><animate attributeName="width" '
                    f'values="0;0;{wt:.0f};{wt:.0f};0;0" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></rect>')
        defs.append(f'<clipPath id="c{i}">{clip}</clipPath>')
        tsp = "".join((f'<tspan fill="{c}">{esc(tx)}</tspan>' if c else f'<tspan>{esc(tx)}</tspan>') for tx, c in segs)
        body.append(f'<text x="60" y="{y}" class="m" font-size="15" clip-path="url(#c{i})" style="white-space:pre" xml:space="preserve">{tsp}</text>')

    ci = len(lines) - 1
    s, d, n = starts[ci]
    cyy = y0 + ci * dy
    blink = "" if STATIC else '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/>'
    cur = f'<rect x="{60+n*CW+2:.0f}" y="{cyy-14}" width="9" height="18" rx="1.5" fill="{SKY3}">{blink}</rect>'
    if STATIC:
        body.append(cur)
    else:
        kt = f"0;{(s+d)/T:.4f};{(s+d+.02)/T:.4f};{(T-1.0)/T:.4f};{(T-0.4)/T:.4f};1"
        body.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/>{cur}</g>')

    wh = (y0 + (len(lines) - 1) * dy) + 26 - 76
    window = (
        f'<rect x="30" y="76" width="840" height="{wh}" rx="14" fill="#050a16" stroke="#1e3a5f" stroke-width="1.2"/>'
        f'<path d="M30,114 V90 a14,14 0 0 1 14,-14 H856 a14,14 0 0 1 14,14 V114 Z" fill="#0b1630"/>'
        f'<circle cx="56" cy="95" r="6" fill="#ff5f57"/><circle cx="78" cy="95" r="6" fill="#febc2e"/><circle cx="100" cy="95" r="6" fill="#28c840"/>'
        f'<text x="450" y="100" text-anchor="middle" class="m" font-size="12.5" fill="{MUTED}">chakra@fst-marrakech — zsh</text>'
        f'<rect x="30" y="114" width="840" height="1" fill="#1e3a5f"/>')
    H = 76 + wh + 30
    write("about.svg", panel(W, H, header("01", "ABOUT") + window + "".join(body), defs="".join(defs)))


# ------------------------------------------------------------------ experience
EXP = [
    dict(date="JUL — SEP 2026", loc="Casablanca", role="Full-Stack Developer Intern", co="ONEE — Electricity Branch", accent=SKY,
         intro="Built two web platforms in parallel to digitalize ONEE processes:", para=None,
         bullets=[("Public procurement platform", "full tender lifecycle from launch to reporting, replacing legacy MS Access workflows"),
                  ("Document management system (DMS)", "centralize, secure and streamline document retrieval")],
         chips=["Java", "Spring Boot", "Spring Security", "Spring Data JPA", "REST API", "PostgreSQL", "React", "TypeScript",
                "Docker", "Kubernetes", "Terraform", "GitLab CI/CD"]),
    dict(date="JUN — JUL 2025", loc="Marrakech", role="Full-Stack & AI Developer Intern", co="IAWEB.DEV", accent=VIOLET,
         intro=None,
         para="Designed and built an enterprise RAG-based intelligent assistant that answers natural-language questions over an internal "
              "document repository — document ingestion & processing, vector indexing and a responsive user interface.",
         bullets=[], chips=["Python", "FastAPI", "LangChain", "Qdrant", "PostgreSQL", "React", "TypeScript", "Docker"]),
]


def exp_card(e, w=786):
    pad, a = 24, e["accent"]
    dw = int(len(e["date"]) * 7.6 + 28)
    s = [f'<rect x="{pad}" y="{pad}" width="{dw}" height="26" rx="13" fill="{a}" fill-opacity=".14" stroke="{a}" stroke-opacity=".5"/>',
         f'<text x="{pad+dw/2}" y="{pad+17.5}" text-anchor="middle" class="m" font-size="12" font-weight="700" letter-spacing="1.2" fill="#e0f2fe">{e["date"]}</text>',
         f'<text x="{w-pad}" y="{pad+17.5}" text-anchor="end" class="m" font-size="12" fill="{MUTED}">{esc(e["loc"])}</text>',
         f'<text x="{pad}" y="88" font-size="23" font-weight="700" fill="#ffffff">{esc(e["role"])}</text>',
         f'<text x="{pad}" y="114" font-size="15" font-weight="600" fill="{a if a != VIOLET else "#c4b5fd"}">{esc(e["co"])}</text>']
    y = 146
    for ln in (wrap(e["intro"], 96) if e["intro"] else []) + (wrap(e["para"], 96) if e["para"] else []):
        s.append(f'<text x="{pad}" y="{y}" font-size="14.5" fill="{TEXT}">{esc(ln)}</text>')
        y += 22
    for lead, rest in e["bullets"]:
        ls = wrap(f"{lead} — {rest}", 86)
        for k, ln in enumerate(ls):
            if k == 0:
                s.append(f'<path d="M{pad+6},{y-9} l4,4 l-4,4 l-4,-4 Z" fill="{a}"/>')
                s.append(f'<text x="{pad+20}" y="{y}" font-size="14.5" fill="{TEXT}"><tspan font-weight="700" fill="#ffffff">{esc(lead)}</tspan>{esc(ln[len(lead):])}</text>')
            else:
                s.append(f'<text x="{pad+20}" y="{y}" font-size="14.5" fill="{TEXT}">{esc(ln)}</text>')
            y += 22
    c, ch = chips(e["chips"], pad, y - 6, w - 2 * pad, a)
    s.append(c)
    return "".join(s), int(y - 6 + ch + pad)


def experience():
    y, parts, nodes = 84, [], []
    cards = [exp_card(e) for e in EXP]
    for i, (e, (c, h)) in enumerate(zip(EXP, cards)):
        parts.append(place(84, y, 786, h, c, e["accent"], dur=11, off=i * 5))
        ny = y + 37
        nodes.append(f'<rect x="57" y="{ny-.75}" width="27" height="1.5" fill="{e["accent"]}" opacity=".55"/>'
                     f'<circle cx="48" cy="{ny}" r="9" fill="#06101f" stroke="{e["accent"]}" stroke-width="2"/>'
                     f'<circle cx="48" cy="{ny}" r="3.5" fill="{e["accent"]}"/>'
                     + ("" if STATIC else f'<circle cx="48" cy="{ny}" r="9" fill="none" stroke="{e["accent"]}"><animate attributeName="r" values="9;20" dur="2.6s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0" dur="2.6s" repeatCount="indefinite"/></circle>'))
        y += h + 22
    end = y - 22
    line = f'<rect x="46.5" y="84" width="3" height="{end-84}" rx="1.5" fill="url(#gV)" opacity=".7"/>'
    if not STATIC:
        line += f'<rect x="45" y="84" width="6" height="40" rx="3" fill="{CYAN}" opacity=".9" filter="url(#blurS)"><animate attributeName="y" values="84;{end-40}" dur="4s" repeatCount="indefinite"/></rect>'
    write("experience.svg", panel(W, end + 30, header("02", "EXPERIENCE") + line + "".join(nodes) + "".join(parts)))


# ------------------------------------------------------------------ projects
PROJECTS = [
    dict(n="01", tag="MICROSERVICES · CI/CD · AWS EKS", title="Industrial Project Management Platform", accent=SKY,
         desc="Microservices platform for teams, tasks and resource allocation. Automated CI/CD with quality analysis and security "
              "scanning, deployed on AWS EKS with full observability of apps and Kubernetes resources.",
         chips=["Java 21", "Spring Boot", "Angular", "PostgreSQL", "Docker", "Jenkins", "SonarQube", "Trivy", "Kubernetes", "AWS EKS", "Helm", "Prometheus", "Grafana"]),
    dict(n="02", medal="3rd Place · RAMADANIA Hackathon", title="AgriTrackers AI — Agricultural Monitoring", accent=GREEN,
         desc="Helps insurers monitor farmland and assess crop condition from Sentinel-2 imagery, NDVI analysis and RAG-based "
              "summaries that support agricultural claims.",
         chips=["Python", "Django REST", "React", "RAG", "Machine Learning", "Computer Vision", "Sentinel-2", "NDVI"]),
    dict(n="03", tag="SAAS · ANGULAR · MICROSERVICES", title="UI Generator — SaaS Interface Platform", accent=VIOLET,
         desc="SaaS platform to design and customize Angular user interfaces: project, component and configuration management on a "
              "microservices architecture with CI/CD and observability.",
         chips=["Angular", "NgRx", "Quarkus", "Spring Cloud", "Consul", "Keycloak", "PostgreSQL", "MongoDB", "Jenkins", "SonarQube", "ELK", "Jaeger"]),
    dict(n="04", tag="DEVOPS · JENKINS · TERRAFORM", title="DevOps Pipeline Automation", accent=AMBER,
         desc="Reusable CI/CD pipelines for Spring, Angular and Laravel apps: quality gates, containerization, AWS deployment and "
              "automated email notifications.",
         chips=["Jenkins", "SonarQube", "Terraform", "AWS EC2", "Docker", "Docker Compose", "Spring", "Angular", "Laravel"]),
]


def proj_card(p, w=410):
    pad, a = 22, p["accent"]
    s = [f'<text x="{w-pad}" y="56" text-anchor="end" class="m" font-size="54" font-weight="800" fill="none" stroke="{a}" stroke-opacity=".28" stroke-width="1.2">{p["n"]}</text>']
    if p.get("medal"):
        tw = int(len(p["medal"]) * 7.4 + 54)
        s.append(f'<rect x="{pad}" y="20" width="{tw}" height="24" rx="12" fill="#f59e0b" fill-opacity=".14" stroke="#f59e0b" stroke-opacity=".6"/>'
                 f'<circle cx="{pad+13}" cy="32" r="8" fill="#cd7f32" stroke="#fbbf24" stroke-width="1"/>'
                 f'<text x="{pad+13}" y="36" text-anchor="middle" class="m" font-size="10.5" font-weight="800" fill="#1c1003">3</text>'
                 f'<text x="{pad+28}" y="36" class="m" font-size="11" font-weight="700" letter-spacing=".6" fill="#fde68a">{esc(p["medal"].upper())}</text>')
    else:
        s.append(f'<text x="{pad}" y="36" class="m" font-size="11" font-weight="700" letter-spacing="1.4" fill="{a}">{esc(p["tag"])}</text>')
    y = 78
    for ln in wrap(p["title"], 30):
        s.append(f'<text x="{pad}" y="{y+19}" font-size="19" font-weight="700" fill="#ffffff">{esc(ln)}</text>')
        y += 25
    y += 6
    for ln in wrap(p["desc"], 52):
        s.append(f'<text x="{pad}" y="{y+14}" font-size="13.5" fill="{TEXT}">{esc(ln)}</text>')
        y += 20
    y += 10
    c, ch = chips(p["chips"], pad, y, w - 2 * pad, a, size=12, h=24, gap=7)
    s.append(c)
    return "".join(s), int(y + ch + pad)


def projects():
    cards = [proj_card(p) for p in PROJECTS]
    parts, y = [], 84
    for r in range(2):
        a, b = cards[r * 2], cards[r * 2 + 1]
        h = max(a[1], b[1])
        for k, (c, _) in enumerate((a, b)):
            p = PROJECTS[r * 2 + k]
            parts.append(place(30 + k * 430, y, 410, h, c, p["accent"], dur=10 + r + k, off=(r * 2 + k) * 2.5))
        y += h + 20
    write("projects.svg", panel(W, y - 20 + 30, header("03", "FEATURED PROJECTS") + "".join(parts)))


# ------------------------------------------------------------------ stack (bento)
def stack():
    rows = [
        [("Languages", ["Java", "Python", "TypeScript", "C#", "C", "SQL", "PHP"], SKY, 270),
         ("Frameworks & Runtime", ["Spring Boot", "Angular", "React", "Next.js 14", ".NET", "Django", "FastAPI", "Node.js", "Tailwind CSS"], VIOLET, 555)],
        [("Databases", ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Supabase"], GREEN, 270),
         ("DevOps & CI/CD", ["Docker", "Kubernetes", "Jenkins", "GitHub Actions", "GitLab CI/CD"], CYAN, 270),
         ("Cloud & Infra", ["AWS", "Terraform", "OpenSearch", "Nginx", "Vercel"], AMBER, 270)],
        [("AI / ML", ["Deep Learning", "Reinforcement Learning", "MCP", "RAG", "AI Agents", "PyTorch", "TensorFlow", "NLP"], PINK, 555),
         ("Tools", ["Git", "Postman", "n8n", "Grafana", "Swagger / OpenAPI", "Jira"], BLUE, 270)],
    ]
    parts, y, k = [], 84, 0
    for row in rows:
        built = []
        for cat, items, acc, w in row:
            pad = 20
            c = (f'<rect x="{pad}" y="22" width="8" height="8" rx="2" fill="{acc}"/>'
                 f'<text x="{pad+16}" y="30" class="m" font-size="12" font-weight="700" letter-spacing="2" fill="{acc}">{esc(cat.upper())}</text>')
            cc, ch = chips(items, pad, 48, w - 2 * pad, acc)
            built.append((c + cc, 48 + ch + pad, acc, w))
        h = max(b[1] for b in built)
        x = 30
        for c, _, acc, w in built:
            parts.append(place(x, y, w, h, c, acc, dur=9 + (k % 4), off=k * 1.7))
            x += w + 15
            k += 1
        y += h + 15
    write("stack.svg", panel(W, y - 15 + 30, header("04", "TECH STACK") + "".join(parts)))


# ------------------------------------------------------------------ achievements
def ach_card(badge, title, sub, accent, w, medal=False, force_h=None):
    pad, tx = 18, 18 + 56 + 12
    tw = w - tx - pad
    tl, sl = wrap(title, max(8, int(tw / 8.3))), wrap(sub, max(8, int(tw / 6.7)))
    th = len(tl) * 20 + len(sl) * 17 + 4
    h = max(82, th + 2 * pad)
    if force_h:
        h = force_h
    cy = h / 2
    s = []
    if medal:
        s.append(f'<circle cx="{pad+28}" cy="{cy}" r="26" fill="#cd7f32" fill-opacity=".18" stroke="#f59e0b" stroke-opacity=".7" stroke-width="1.5"/>'
                 f'<circle cx="{pad+28}" cy="{cy}" r="17" fill="#cd7f32" stroke="#fbbf24"/>'
                 f'<text x="{pad+28}" y="{cy+7}" text-anchor="middle" class="m" font-size="20" font-weight="800" fill="#1c1003">3</text>')
    else:
        s.append(f'<circle cx="{pad+28}" cy="{cy}" r="26" fill="{accent}" fill-opacity=".13" stroke="{accent}" stroke-opacity=".65" stroke-width="1.5"/>'
                 f'<text x="{pad+28}" y="{cy+4.5}" text-anchor="middle" class="m" font-size="12.5" font-weight="800" letter-spacing=".5" fill="#ffffff">{esc(badge)}</text>')
    y = cy - th / 2 + 14
    for ln in tl:
        s.append(f'<text x="{tx}" y="{y:.1f}" font-size="15" font-weight="700" fill="#ffffff">{esc(ln)}</text>')
        y += 20
    y -= 2
    for ln in sl:
        s.append(f'<text x="{tx}" y="{y+1:.1f}" font-size="12.5" fill="{MUTED}">{esc(ln)}</text>')
        y += 17
    return "".join(s), int(h)


def achievements():
    sections = [
        ("CERTIFICATIONS", [
            ("AWS", "AWS Cloud Practitioner Essentials", "Amazon Web Services · 2025", AMBER, False),
            ("JAVA", "Java 17 & Java 21", "Oracle certifications", RED, False),
            ("AI", "AI Foundations", "Oracle certification", VIOLET, False)]),
        ("ACHIEVEMENTS & ACTIVITIES", [
            ("3", "3rd Place", "RAMADANIA · SkillUp IT 2026 · DEV4DAYS", "#f59e0b", True),
            ("IRISI", "IRISI Club — FST Marrakech", "Design & Project Management Coordinator · 2024 – 2026", PINK, False),
            ("Aa", "Languages", "Arabic (native) · French (fluent) · English (fluent)", GREEN, False)]),
        ("EDUCATION", [
            ("FST", "State Engineering Degree", "Computer Networks & Information Systems · FST Marrakech · 2024 – 2027", SKY, False),
            ("MIP", "DEUST — Math, CS & Physics", "FST Errachidia · 2022 – 2024", CYAN, False),
            ("BAC", "High School Diploma", "Physical Sciences · Lycée Assalam, Tiznit · 2021 – 2022", BLUE, False)]),
    ]
    parts, y, k = [], 82, 0
    for label, cards in sections:
        parts.append(f'<text x="30" y="{y+12}" class="m" font-size="11.5" font-weight="700" letter-spacing="2.4" fill="{MUTED}">{esc(label)}</text>')
        y += 24
        built = [ach_card(b, t, sb, a, 270, m) for b, t, sb, a, m in cards]
        h = max(x[1] for x in built)
        built = [ach_card(b, t, sb, a, 270, m, force_h=h) for b, t, sb, a, m in cards]
        for i, ((c, _), (_, _, _, a, _)) in enumerate(zip(built, cards)):
            parts.append(place(30 + i * 285, y, 270, h, c, a, dot=False))
            k += 1
        y += h + 22
    write("achievements.svg", panel(W, y - 22 + 30, header("05", "CERTIFICATIONS & MORE") + "".join(parts)))


# ------------------------------------------------------------------ connect
def connect():
    H = 270
    body = (
        f'<rect x="305" y="34" width="290" height="32" rx="16" fill="{GREEN}" fill-opacity=".1" stroke="{GREEN}" stroke-opacity=".5"/>'
        f'<circle cx="327" cy="50" r="4.5" fill="{GREEN}"/>'
        + ('' if STATIC else f'<circle cx="327" cy="50" r="4.5" fill="none" stroke="{GREEN}"><animate attributeName="r" values="4.5;13" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="2s" repeatCount="indefinite"/></circle>')
        + f'<text x="342" y="55" class="m" font-size="12" font-weight="700" letter-spacing="1.4" fill="#a7f3d0">AVAILABLE · FEBRUARY 2027</text>'
        + f'<text x="450" y="130" text-anchor="middle" font-size="44" font-weight="800" letter-spacing="1" fill="url(#gName)" filter="url(#glow)">Let’s build something great.</text>'
        + f'<text x="450" y="172" text-anchor="middle" font-size="17" fill="{TEXT}">Looking for a final-year internship (PFE) starting February 2027</text>'
        + f'<text x="450" y="200" text-anchor="middle" font-size="17" font-weight="600" fill="url(#gSub)">DevOps  ·  Artificial Intelligence  ·  Full-Stack</text>'
        + f'<text x="450" y="236" text-anchor="middle" class="m" font-size="13" fill="{MUTED}">chakraabdedaym@gmail.com  ·  linkedin.com/in/chakra-abdedaym</text>')
    write("connect.svg", panel(W, H, body, dot=True, dur=18))


# ------------------------------------------------------------------ buttons
def buttons():
    w, h = 310, 50
    shimmer = "" if STATIC else (
        f'<clipPath id="bc"><rect width="{w}" height="{h}" rx="25"/></clipPath>'
        f'<g clip-path="url(#bc)"><rect y="-10" width="50" height="{h+20}" fill="#fff" opacity=".28" transform="skewX(-20)">'
        f'<animate attributeName="x" values="-90;-90;{w+60}" keyTimes="0;.45;1" dur="3.6s" repeatCount="indefinite"/></rect></g>')
    defs = f'<linearGradient id="gBtn" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{SKY}"/><stop offset="1" stop-color="#2563eb"/></linearGradient>'
    body = (f'<rect width="{w}" height="{h}" rx="25" fill="url(#gBtn)"/>'
            f'<g transform="translate(24,17)" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"><rect width="22" height="16" rx="3"/><path d="M1.5 3.5 L11 10 L20.5 3.5"/></g>'
            f'<text x="60" y="31" font-size="15" font-weight="600" fill="#ffffff">chakraabdedaym@gmail.com</text>' + shimmer)
    write("btn-email.svg", doc(w, h, body, defs))
    body = (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="#0a1224" stroke="url(#gBorder)" stroke-width="1.5"/>'
            f'<rect x="22" y="14" width="22" height="22" rx="5" fill="{SKY}"/>'
            f'<text x="33" y="30.5" text-anchor="middle" font-size="14" font-weight="800" fill="#04101f">in</text>'
            f'<text x="58" y="31" font-size="15" font-weight="600" fill="#e0f2fe">LinkedIn · chakra-abdedaym</text>')
    write("btn-linkedin.svg", doc(w, h, body))


# ------------------------------------------------------------------ footer
def footer():
    H = 190

    def wave(y0, A, L, fill, op, dur, rev=False):
        d = f"M0,{y0} Q{L/4:.0f},{y0-A} {L/2:.0f},{y0}"
        for k in range(2, int(1800 / (L / 2)) + 1):
            d += f" T{L/2*k:.0f},{y0}"
        d += f" V{H} H0 Z"
        a = ("" if STATIC else
             f'<animateTransform attributeName="transform" type="translate" from="{-L if rev else 0} 0" to="{0 if rev else -L} 0" dur="{dur}s" repeatCount="indefinite"/>')
        return f'<path d="{d}" fill="{fill}" fill-opacity="{op}">{a}</path>'

    body = (
        f'<text x="450" y="70" text-anchor="middle" font-size="26" font-weight="800" letter-spacing="1.5" fill="url(#gName)" filter="url(#glow)">Think → Build → Break → Fix → Improve</text>'
        f'<text x="450" y="100" text-anchor="middle" font-size="14" font-style="italic" fill="{MUTED}">“A good engineer doesn’t just use tools — they understand the system behind them.”</text>'
        + wave(140, 14, 450, SKY, .22, 11) + wave(150, 11, 300, VIOLET, .28, 8, True) + wave(160, 9, 600, SKY2, .30, 14))
    write("footer.svg", panel(W, H, body))


if __name__ == "__main__":
    hero(); about(); experience(); projects(); stack(); achievements(); connect(); buttons(); footer()
    print("generated into", OUT, "(static)" if STATIC else "")
