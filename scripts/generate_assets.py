#!/usr/bin/env python3
"""Generates every animated SVG used by the profile README into ../assets"""
import os, math, random
from xml.sax.saxutils import escape as esc

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "assets")
os.makedirs(os.path.join(OUT, "projects"), exist_ok=True)

MONO = "JetBrains Mono, Fira Code, SF Mono, Consolas, Menlo, DejaVu Sans Mono, monospace"
SANS = "Inter, Segoe UI, Helvetica, Arial, sans-serif"
P, C, G = "#9945FF", "#22d3ee", "#14F195"      # purple / cyan / solana green


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def hexs(r, n=6):
    return "".join(r.choice("0123456789abcdef") for _ in range(n))


GLOW = ('<filter id="glow" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="4" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')

SHIMMER = ('<linearGradient id="tg" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">'
           f'<stop offset="0" stop-color="{P}"/><stop offset="0.5" stop-color="{C}"/><stop offset="1" stop-color="{G}"/>'
           '<animate attributeName="x1" values="0;1" dur="5s" repeatCount="indefinite"/>'
           '<animate attributeName="x2" values="1;2" dur="5s" repeatCount="indefinite"/></linearGradient>')


# ───────────────────────────── HERO ─────────────────────────────
def hero():
    W, H = 1200, 450
    r = random.Random(11)
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
      'aria-label="Everest Paudel - Backend Engineer, Distributed Systems, Web3">')
    a('<defs>')
    a('<radialGradient id="bg" cx="50%" cy="0%" r="95%"><stop offset="0" stop-color="#1c1245"/>'
      '<stop offset="0.5" stop-color="#0a0f22"/><stop offset="1" stop-color="#05070f"/></radialGradient>')
    a(SHIMMER)
    a('<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
      '<path d="M40 0H0V40" fill="none" stroke="#26334f" stroke-width="1"/>'
      '<animateTransform attributeName="patternTransform" type="translate" from="0 0" to="0 40" dur="3s" repeatCount="indefinite"/></pattern>')
    a('<linearGradient id="gf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
      '<stop offset="0.45" stop-color="#fff" stop-opacity="0.9"/><stop offset="1" stop-color="#fff" stop-opacity="0.05"/></linearGradient>')
    a(f'<mask id="gm"><rect width="{W}" height="{H}" fill="url(#gf)"/></mask>')
    a('<linearGradient id="sc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22d3ee" stop-opacity="0"/>'
      '<stop offset="0.5" stop-color="#22d3ee" stop-opacity="0.9"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></linearGradient>')
    a(f'<clipPath id="rc"><rect width="{W}" height="{H}" rx="20"/></clipPath>')
    a(GLOW)
    a('</defs>')
    a(f'<rect width="{W}" height="{H}" rx="20" fill="url(#bg)"/>')
    a('<g clip-path="url(#rc)">')
    a(f'<g mask="url(#gm)"><rect width="{W}" height="{H}" fill="url(#grid)"/></g>')

    # scanning line
    a(f'<rect x="0" y="0" width="{W}" height="2" fill="url(#sc)" opacity="0.35">'
      f'<animate attributeName="y" from="-4" to="{H}" dur="6s" repeatCount="indefinite"/></rect>')

    # floating tokens
    words = ["0x9f3a", "gRPC", "SOL", "Go", "Rust", "AMQP", "SHA-256", "PDA", "ED25519", "JWT",
             "PKCE", "SPL", "0xC0DE", "Redis", "OIDC", "NaCl", "tx:ok", "AQI", "nonce", "K8s"]
    for i, wd in enumerate(words):
        x = 30 + (i * 59) % 1150
        dur = 11 + (i * 7) % 9
        col = [C, P, G][i % 3]
        a(f'<text x="{x}" y="{H+20}" font-family="{MONO}" font-size="14" fill="{col}" opacity="0.22">{esc(wd)}'
          f'<animateTransform attributeName="transform" type="translate" from="0 0" to="0 -{H+60}" dur="{dur}s" begin="-{(i*3)%dur}s" repeatCount="indefinite"/></text>')

    # network clusters
    pts = []
    for x0 in (30, 930):
        for _ in range(8):
            pts.append((x0 + r.random() * 240, 28 + r.random() * 225))
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = math.dist(pts[i], pts[j])
            if d < 115:
                dur = 2 + r.random() * 2
                a(f'<line x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{pts[j][0]:.0f}" y2="{pts[j][1]:.0f}" stroke="#4b5f95" stroke-width="1">'
                  f'<animate attributeName="stroke-opacity" values="0.15;0.7;0.15" dur="{dur:.1f}s" repeatCount="indefinite"/></line>')
    for i, (x, y) in enumerate(pts):
        col = [C, P, G][i % 3]
        dur = 1.6 + r.random() * 1.8
        a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.5" fill="{col}" filter="url(#glow)">'
          f'<animate attributeName="r" values="3;6;3" dur="{dur:.1f}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0.5;1;0.5" dur="{dur:.1f}s" repeatCount="indefinite"/></circle>')

    # text
    a(f'<text x="600" y="98" text-anchor="middle" font-family="{MONO}" font-size="19" fill="{G}" letter-spacing="1" xml:space="preserve">'
      '$ whoami<tspan fill="#8b949e"> --verbose</tspan>'
      '<tspan fill="#e6edf3"> _</tspan><animate attributeName="opacity" values="1;1;0.6;1" dur="2s" repeatCount="indefinite"/></text>')
    a(f'<text x="600" y="186" text-anchor="middle" font-family="{SANS}" font-size="78" font-weight="800" letter-spacing="7" '
      'fill="url(#tg)" filter="url(#glow)">EVEREST PAUDEL</text>')
    roles = ["Backend Engineer  \u00b7  Go & Node.js", "Distributed Systems  \u00b7  gRPC  \u00b7  RabbitMQ  \u00b7  Redis",
             "Web3 Builder  \u00b7  Solana  \u00b7  Rust  \u00b7  Anchor", "Secure by design  \u00b7  OAuth2  \u00b7  OIDC  \u00b7  Cryptography"]
    for i, t in enumerate(roles):
        a(f'<text x="600" y="240" text-anchor="middle" font-family="{MONO}" font-size="25" fill="#e6edf3" opacity="0" xml:space="preserve">{esc(t)}'
          f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.04;0.21;0.25;1" dur="14s" begin="{i*3.5}s" repeatCount="indefinite"/></text>')
    a(f'<text x="600" y="282" text-anchor="middle" font-family="{MONO}" font-size="15" fill="#8b949e">'
      'Kathmandu, Nepal  //  B.Sc. CSIT  //  building systems that don\'t go down</text>')

    # blockchain
    by, bw, bh = 330, 140, 72
    xs = [60 + 188 * i for i in range(6)]
    for i in range(5):
        a(f'<line x1="{xs[i]+bw}" y1="{by+bh/2}" x2="{xs[i+1]}" y2="{by+bh/2}" stroke="{C}" stroke-width="2" stroke-dasharray="6 6" opacity="0.7">'
          '<animate attributeName="stroke-dashoffset" from="0" to="-24" dur="0.9s" repeatCount="indefinite"/></line>')
    for i, x in enumerate(xs):
        begin = max(0.0, 0.39 + 1.04 * i - 0.15)
        a(f'<rect x="{x}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="#0c1326" stroke="#26334f" stroke-width="1.5"/>')
        a(f'<rect x="{x}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="none" stroke="{G}" stroke-width="2" stroke-opacity="0.25" filter="url(#glow)">'
          f'<animate attributeName="stroke-opacity" values="0.2;1;0.2;0.2" keyTimes="0;0.06;0.2;1" dur="6s" begin="{begin:.2f}s" repeatCount="indefinite"/></rect>')
        a(f'<text x="{x+14}" y="{by+24}" font-family="{MONO}" font-size="11" fill="#8b949e" letter-spacing="1">BLOCK #{40210+i}</text>')
        a(f'<text x="{x+14}" y="{by+46}" font-family="{MONO}" font-size="15" fill="{C}">0x{hexs(r)}</text>')
        a(f'<text x="{x+14}" y="{by+63}" font-family="{MONO}" font-size="10" fill="{G}">\u2713 validated</text>')
    path = f"M{xs[0]} {by+bh/2} H{xs[-1]+bw}"
    for k, (rad, op) in enumerate([(6, 1), (4, 0.55), (3, 0.3)]):
        a(f'<circle r="{rad}" fill="{G}" opacity="{op}" filter="url(#glow)">'
          f'<animateMotion dur="6s" begin="-{k*0.18:.2f}s" repeatCount="indefinite" path="{path}"/></circle>')
    a('</g>')
    a(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="19" fill="none" stroke="url(#tg)" stroke-width="1.5" stroke-opacity="0.55"/>')
    a('</svg>')
    write("hero.svg", "\n".join(o))


# ───────────────────────────── TERMINAL ─────────────────────────────
def terminal():
    W, H = 920, 372
    cw, fs, lh, x0, y0 = 9.0, 15, 25, 30, 84
    prompt = [("\u279c ", G), ("~ ", C)]
    K, V = "#c4a7ff", "#e3b341"
    lines = [
        (prompt + [("whoami", "#e6edf3")], 0.07),
        ([("Everest Paudel \u2014 Backend Engineer (Go & Node.js) \u00b7 Kathmandu, NP", "#e6edf3")], 0.022),
        (prompt + [("cat expertise.yml", "#e6edf3")], 0.07),
        ([("  core:     ", K), ("[Go, Rust, TypeScript, Node.js]", V)], 0.022),
        ([("  systems:  ", K), ("[gRPC, RabbitMQ, Redis, PostgreSQL, WebSockets]", V)], 0.022),
        ([("  web3:     ", K), ("[Solana, Anchor, SPL, MagicBlock, EVM]", V)], 0.022),
        ([("  security: ", K), ("[OAuth2, OIDC, PKCE, NaCl, JWT, replay-protection]", V)], 0.022),
        ([("  infra:    ", K), ("[Docker, Kubernetes, AWS, Jenkins, Git]", V)], 0.022),
        (prompt + [("./ship --next", "#e6edf3")], 0.07),
        ([("\u2714 ", G), ("deping \u00b7 kipay \u00b7 breezo \u00b7 nid \u00b7 paydao \u00b7 godec", G)], 0.022),
        (prompt, 0.07),
    ]
    # schedule
    t = 0.6
    sched = []
    for segs, dt in lines:
        n = sum(len(s) for s, _ in segs)
        sched.append((t, n, dt))
        t += n * dt + 0.35
    T = t + 5.0
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: whoami">')
    a('<defs>' + SHIMMER + GLOW)
    for i, (t0, n, dt) in enumerate(sched):
        kt, vals = [0.0], [0.0]
        if t0 > 0:
            kt.append(t0 / T); vals.append(0.0)
        for k in range(1, n + 1):
            kt.append((t0 + k * dt) / T)
            vals.append(k * cw + (8 if k == n else 0))
        kt.append(0.985); vals.append(0.0)
        a(f'<clipPath id="c{i}"><rect x="{x0}" y="{y0 + i*lh - 18}" width="0" height="{lh}">'
          f'<animate attributeName="width" calcMode="discrete" dur="{T:.2f}s" repeatCount="indefinite" '
          f'keyTimes="{";".join(f"{k:.4f}" for k in kt)}" values="{";".join(f"{v:.1f}" for v in vals)}"/></rect></clipPath>')
    a('</defs>')
    a(f'<rect width="{W}" height="{H}" rx="14" fill="#0a0e1a" stroke="url(#tg)" stroke-width="1.5"/>')
    a(f'<path d="M0 14a14 14 0 0 1 14-14h{W-28}a14 14 0 0 1 14 14v30H0z" fill="#111830"/>')
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        a(f'<circle cx="{26+i*22}" cy="22" r="6.5" fill="{c}"/>')
    a(f'<text x="{W/2}" y="27" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#8b949e">everest@paudel.dev \u2014 zsh \u2014 ~/backend</text>')
    a(f'<text x="{W-24}" y="27" text-anchor="end" font-family="{MONO}" font-size="12" fill="{G}">\u25cf online</text>')
    for i, (segs, dt) in enumerate(lines):
        y = y0 + i * lh
        ts = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in segs)
        a(f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" clip-path="url(#c{i})" xml:space="preserve" style="white-space:pre">{ts}</text>')
    # cursor
    t_last, n_last, dt_last = sched[-1]
    cx = x0 + n_last * cw + 4
    cy = y0 + (len(lines) - 1) * lh - 15
    on = (t_last + n_last * dt_last) / T
    a(f'<g opacity="0"><animate attributeName="opacity" calcMode="discrete" dur="{T:.2f}s" repeatCount="indefinite" '
      f'keyTimes="0;{on:.4f};0.985" values="0;1;0"/>'
      f'<rect x="{cx}" y="{cy}" width="9" height="19" fill="{G}"><animate attributeName="opacity" values="1;0;1" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect></g>')
    a('</svg>')
    write("terminal.svg", "\n".join(o))


# ───────────────────────────── ORBIT ─────────────────────────────
def orbit():
    W, H, cx, cy = 900, 500, 450, 250
    rings = [
        (100, 1, 28, [("Go", "#00ADD8"), ("Rust", "#f97316"), ("TypeScript", "#3b82f6"), ("Node.js", "#84cc16")]),
        (160, -1, 42, [("gRPC", C), ("RabbitMQ", "#ff6600"), ("Redis", "#ef4444"), ("PostgreSQL", "#60a5fa"),
                        ("MongoDB", "#22c55e"), ("WebSockets", "#a78bfa")]),
        (220, 1, 60, [("Solana", G), ("Anchor", "#c4a7ff"), ("MagicBlock", "#f472b6"), ("Docker", "#38bdf8"),
                       ("Kubernetes", "#3b82f6"), ("AWS", "#f59e0b"), ("OAuth2", "#fb7185"), ("NaCl", "#e3b341")]),
    ]
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Orbiting tech stack">')
    a('<defs>' + SHIMMER + GLOW)
    a(f'<radialGradient id="core" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{P}"/><stop offset="1" stop-color="#3a1a80"/></radialGradient>')
    a(f'<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{P}" stop-opacity="0.35"/><stop offset="1" stop-color="{P}" stop-opacity="0"/></radialGradient>')
    a('</defs>')
    a(f'<rect width="{W}" height="{H}" rx="18" fill="#080c18" stroke="#1c2540"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="250" fill="url(#halo)"/>')
    for rad, d, dur, items in rings:
        a(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="#2a3760" stroke-width="1.2" stroke-dasharray="3 7">'
          f'<animate attributeName="stroke-dashoffset" from="0" to="{-10*d*3}" dur="3s" repeatCount="indefinite"/></circle>')
    # core pulses
    for k in range(2):
        a(f'<circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{P}" stroke-width="2">'
          f'<animate attributeName="r" values="40;78" dur="3s" begin="{k*1.5}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0.7;0" dur="3s" begin="{k*1.5}s" repeatCount="indefinite"/></circle>')
    a(f'<circle cx="{cx}" cy="{cy}" r="40" fill="url(#core)" stroke="url(#tg)" stroke-width="2.5" filter="url(#glow)"/>')
    a(f'<text x="{cx}" y="{cy+9}" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="800" fill="#fff">EP</text>')
    for rad, d, dur, items in rings:
        n = len(items)
        fr, to = (0, 360) if d == 1 else (360, 0)
        cfr, cto = (0, -360) if d == 1 else (0, 360)
        a(f'<g transform="translate({cx} {cy})"><g><animateTransform attributeName="transform" type="rotate" from="{fr}" to="{to}" dur="{dur}s" repeatCount="indefinite"/>')
        for k, (label, col) in enumerate(items):
            ang = 360 / n * k + (rad % 40)
            pw = len(label) * 6.9 + 26
            a(f'<g transform="rotate({ang:.1f}) translate({rad} 0)"><g><animateTransform attributeName="transform" type="rotate" from="{cfr}" to="{cto}" dur="{dur}s" repeatCount="indefinite"/>'
              f'<g transform="rotate({-ang:.1f})">'
              f'<rect x="{-pw/2:.1f}" y="-14" width="{pw:.1f}" height="28" rx="14" fill="#0d1428" stroke="{col}" stroke-width="1.6"/>'
              f'<circle cx="{-pw/2+11:.1f}" cy="0" r="3" fill="{col}"/>'
              f'<text x="6" y="4.5" text-anchor="middle" font-family="{MONO}" font-size="11.5" font-weight="600" fill="#e6edf3">{esc(label)}</text>'
              '</g></g></g>')
        a('</g></g>')
    # left / right copy
    a(f'<text x="26" y="196" font-family="{MONO}" font-size="11" letter-spacing="2" fill="#6b7688">WHAT I DO</text>')
    for i, t in enumerate(["I build the", "parts of the", "internet you", "never see."]):
        a(f'<text x="26" y="{226+i*27}" font-family="{SANS}" font-size="20" font-weight="700" fill="url(#tg)">{t}</text>')
    a(f'<text x="738" y="196" font-family="{MONO}" font-size="11" letter-spacing="2" fill="#6b7688">ORBITS</text>')
    for i, (col, t) in enumerate([("#84cc16", "inner  \u00b7 languages"), (C, "middle \u00b7 backend"), (G, "outer  \u00b7 web3/infra")]):
        a(f'<circle cx="744" cy="{222+i*26}" r="4" fill="{col}"/><text x="756" y="{226+i*26}" font-family="{MONO}" font-size="12" fill="#c9d1d9" xml:space="preserve">{esc(t)}</text>')
    a('</svg>')
    write("orbit.svg", "\n".join(o))


# ───────────────────────────── PIPELINE ─────────────────────────────
def pipeline():
    W, H = 1200, 340
    stages = [("CLIENT", "REST \u00b7 JWT", "#60a5fa"), ("GO API", "net/http \u00b7 gRPC", "#00ADD8"), ("REDIS", "job scheduling", "#ef4444"),
              ("RABBITMQ", "event queues", "#ff6600"), ("RUST WORKERS", "edge nodes", "#f97316"), ("SOLANA", "Anchor \u00b7 SPL", G)]
    cxs = [100 + 190 * i for i in range(6)]
    by, bh, bw = 96, 84, 152
    ymid = by + bh / 2
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Event-driven backend pipeline">')
    a('<defs>' + SHIMMER + GLOW)
    a('<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#4b5f95"/></marker>')
    a('</defs>')
    a(f'<rect width="{W}" height="{H}" rx="18" fill="#080c18" stroke="#1c2540"/>')
    a(f'<text x="34" y="44" font-family="{MONO}" font-size="12" letter-spacing="2" fill="#6b7688">EVENT-DRIVEN PIPELINE  //  request \u2192 queue \u2192 edge \u2192 consensus</text>')
    for i in range(5):
        a(f'<line x1="{cxs[i]+bw/2+4}" y1="{ymid}" x2="{cxs[i+1]-bw/2-6}" y2="{ymid}" stroke="#4b5f95" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#ar)">'
          '<animate attributeName="stroke-dashoffset" from="0" to="-20" dur="0.8s" repeatCount="indefinite"/></line>')
    for i, ((name, sub, col), cx) in enumerate(zip(stages, cxs)):
        begin = (i * 1.19 - 0.2) % 2
        a(f'<rect x="{cx-bw/2}" y="{by}" width="{bw}" height="{bh}" rx="14" fill="#0d1428" stroke="{col}" stroke-width="1.5" stroke-opacity="0.6"/>')
        a(f'<rect x="{cx-bw/2}" y="{by}" width="{bw}" height="{bh}" rx="14" fill="{col}" fill-opacity="0.0" stroke="{col}" stroke-width="2.5" filter="url(#glow)" stroke-opacity="0.2">'
          f'<animate attributeName="stroke-opacity" values="0.15;1;0.15;0.15" keyTimes="0;0.1;0.3;1" dur="2s" begin="{begin:.2f}s" repeatCount="indefinite"/>'
          f'<animate attributeName="fill-opacity" values="0;0.16;0;0" keyTimes="0;0.1;0.3;1" dur="2s" begin="{begin:.2f}s" repeatCount="indefinite"/></rect>')
        a(f'<text x="{cx}" y="{ymid-3}" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="800" fill="#e6edf3" letter-spacing="1">{name}</text>')
        a(f'<text x="{cx}" y="{ymid+18}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{col}">{esc(sub)}</text>')
    # packets forward
    path = f"M{cxs[0]} {ymid} H{cxs[-1]}"
    for k, col in enumerate([C, G, P]):
        a(f'<circle r="6" fill="{col}" filter="url(#glow)"><animateMotion dur="6s" begin="{k*2}s" repeatCount="indefinite" path="{path}"/></circle>')
    # return telemetry
    ret = f"M{cxs[4]} {by+bh} C {cxs[4]} 300, {cxs[1]} 300, {cxs[1]} {by+bh}"
    a(f'<path d="{ret}" fill="none" stroke="#f97316" stroke-width="1.6" stroke-dasharray="6 6" opacity="0.7">'
      '<animate attributeName="stroke-dashoffset" from="0" to="-24" dur="1.2s" repeatCount="indefinite"/></path>')
    for k in range(3):
        a(f'<circle r="4.5" fill="#f97316" filter="url(#glow)"><animateMotion dur="4.5s" begin="{k*1.5}s" repeatCount="indefinite" path="{ret}"/></circle>')
    a(f'<text x="{(cxs[1]+cxs[4])/2}" y="{H-14}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#f97316">'
      '\u21c4 bidirectional gRPC telemetry \u00b7 anti-cheat \u00b7 two-packet state machine</text>')
    a(f'<text x="{cxs[5]}" y="{by+bh+40}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{G}">on-chain rewards</text>')
    a(f'<text x="{cxs[0]}" y="{by+bh+40}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="#60a5fa">users / merchants</text>')
    a('</svg>')
    write("pipeline.svg", "\n".join(o))


# ───────────────────────────── MARQUEE ─────────────────────────────
def marquee():
    W, H = 1200, 124
    row1 = [("Go", "#00ADD8"), ("Rust", "#f97316"), ("TypeScript", "#3b82f6"), ("JavaScript", "#eab308"), ("Node.js", "#84cc16"),
            ("NestJS", "#ef4444"), ("Express", "#9ca3af"), ("C/C++", "#60a5fa"), ("SQL", "#22d3ee"), ("React", "#38bdf8"),
            ("Next.js", "#e5e7eb"), ("Tailwind", "#2dd4bf")]
    row2 = [("PostgreSQL", "#60a5fa"), ("Redis", "#ef4444"), ("MongoDB", "#22c55e"), ("RabbitMQ", "#ff6600"), ("gRPC", C),
            ("WebSockets", "#a78bfa"), ("Docker", "#38bdf8"), ("Kubernetes", "#3b82f6"), ("AWS", "#f59e0b"), ("Jenkins", "#f87171"),
            ("Solana", G), ("Anchor", "#c4a7ff"), ("SPL", "#f472b6"), ("OAuth2", "#fb7185"), ("JWT", "#e3b341"), ("NaCl", "#94a3b8")]

    def pills(items, y):
        x, out = 0, []
        for label, col in items:
            w = len(label) * 8.6 + 40
            out.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="36" rx="18" fill="#0d1428" stroke="{col}" stroke-opacity="0.8" stroke-width="1.5"/>'
                       f'<circle cx="{x+18:.0f}" cy="{y+18}" r="4" fill="{col}"/>'
                       f'<text x="{x+30:.0f}" y="{y+23}" font-family="{MONO}" font-size="14" font-weight="600" fill="#e6edf3">{esc(label)}</text>')
            x += w + 14
        return "".join(out), x

    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack marquee">')
    a('<defs><linearGradient id="fd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000"/><stop offset="0.08" stop-color="#fff"/>'
      '<stop offset="0.92" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
      f'<mask id="fm"><rect width="{W}" height="{H}" fill="url(#fd)"/></mask></defs>')
    a(f'<g mask="url(#fm)">')
    for row, y, direction in ((row1, 10, -1), (row2, 68, 1)):
        body, cw = pills(row, y)
        copies = math.ceil(W / cw) + 1
        fr, to = (0, -cw) if direction == -1 else (-cw, 0)
        a(f'<g><animateTransform attributeName="transform" type="translate" from="{fr:.0f} 0" to="{to:.0f} 0" dur="{cw/55:.1f}s" repeatCount="indefinite"/>')
        for c in range(copies):
            a(f'<g transform="translate({c*cw:.0f} 0)">{body}</g>')
        a('</g>')
    a('</g></svg>')
    write("marquee.svg", "\n".join(o))


# ───────────────────────────── SECTION HEADERS ─────────────────────────────
def header(fname, title, sub):
    W, H = 1200, 76
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">'
         '<defs>' + SHIMMER +
         f'<linearGradient id="hl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C}" stop-opacity="0"/><stop offset="0.5" stop-color="{G}"/><stop offset="1" stop-color="{C}" stop-opacity="0"/></linearGradient></defs>'
         f'<g transform="translate(30 36)"><rect x="-9" y="-9" width="18" height="18" fill="none" stroke="{G}" stroke-width="2.2">'
         '<animateTransform attributeName="transform" type="rotate" from="45" to="405" dur="6s" repeatCount="indefinite"/></rect>'
         f'<rect x="-3.5" y="-3.5" width="7" height="7" fill="{P}"><animateTransform attributeName="transform" type="rotate" from="45" to="-315" dur="6s" repeatCount="indefinite"/></rect></g>'
         f'<text x="64" y="47" font-family="{SANS}" font-size="32" font-weight="800" letter-spacing="4" fill="url(#tg)">{esc(title)}</text>'
         f'<text x="{W-20}" y="45" text-anchor="end" font-family="{MONO}" font-size="15" fill="#6b7688">{esc(sub)}</text>'
         f'<rect x="0" y="66" width="{W}" height="2" fill="#1c2540"/>'
         f'<rect y="65" width="260" height="4" rx="2" fill="url(#hl)"><animate attributeName="x" from="-260" to="{W}" dur="3.2s" repeatCount="indefinite"/></rect></svg>')
    write(fname, s)


# ───────────────────────────── STATS TILES ─────────────────────────────
def stats():
    W, H = 1200, 150
    tiles = [("8+", "products shipped", "payments \u00b7 identity \u00b7 IoT \u00b7 DAO \u00b7 edu"),
             ("6", "languages", "Go \u00b7 Rust \u00b7 TS \u00b7 JS \u00b7 SQL \u00b7 C/C++"),
             ("gRPC", "service backbone", "bidirectional streams, Go \u21c4 Rust"),
             ("SOL+EVM", "on-chain integrations", "Anchor programs, wallet verification")]
    tw, gap = 270, 40
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Highlights">')
    a('<defs>' + SHIMMER + GLOW + '</defs>')
    for i, (big, lab, sub) in enumerate(tiles):
        x = i * (tw + gap)
        a(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="{3+i*0.4:.1f}s" repeatCount="indefinite"/>'
          f'<rect x="{x+1}" y="6" width="{tw-2}" height="{H-16}" rx="16" fill="#0a0f1f" stroke="#1c2540" stroke-width="1.5"/>'
          f'<rect x="{x+1}" y="6" width="{tw-2}" height="{H-16}" rx="16" fill="none" stroke="url(#tg)" stroke-width="2" stroke-dasharray="90 700">'
          f'<animate attributeName="stroke-dashoffset" from="0" to="-790" dur="{5+i}s" repeatCount="indefinite"/></rect>'
          f'<text x="{x+tw/2}" y="72" text-anchor="middle" font-family="{SANS}" font-size="42" font-weight="800" fill="url(#tg)">{esc(big)}</text>'
          f'<text x="{x+tw/2}" y="98" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="#e6edf3">{esc(lab)}</text>'
          f'<text x="{x+tw/2}" y="120" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="#6b7688">{esc(sub)}</text></g>')
    a('</svg>')
    write("stats.svg", "\n".join(o))


# ───────────────────────────── PROJECT CARDS ─────────────────────────────
PROJECTS = [
    ("deping", "DePing.xyz", "Decentralized uptime monitoring network", "#6366f1", "INFRA \u00b7 WEB3", "deping.xyz",
     ["Rust edge workers \u21c4 Go core over bidirectional gRPC", "Two-Packet state machine + anti-cheat engine", "Solana Anchor SPL rewards + Telegram alerts"],
     ["Go", "Rust", "gRPC", "RabbitMQ", "Redis", "PostgreSQL", "Solana"]),
    ("kipay", "Kipay.xyz", "Non-custodial crypto payment gateway", "#14b8a6", "PAYMENTS", "kipay.xyz",
     ["Go modular monolith on native net/http", "Rust multi-currency verifier via gRPC streams", "Hosted checkout, payment links, signed webhooks"],
     ["Go", "Rust", "gRPC", "React", "PostgreSQL"]),
    ("breezo", "BREEZO Network", "Decentralized air-quality IoT network", "#22c55e", "IOT \u00b7 WEB3", "breezonetwork.xyz",
     ["ESP32 sensors \u2192 sub-second Socket.IO dashboards", "NaCl crypto + replay protection on telemetry", "Solana node registry + SPL token rewards"],
     ["Node.js", "TypeScript", "MongoDB", "Socket.IO", "Solana"]),
    ("nid", "NID.xyz", "Handle-based decentralized identity provider", "#8b5cf6", "IDENTITY", "nid.xyz",
     ["OAuth 2.0 + OIDC + PKCE identity provider in Go", ".nid handles verified via EVM & Solana wallets", "Central sessions, connected apps, instant revoke"],
     ["Go", "React", "TypeScript", "PostgreSQL", "Solana"]),
    ("paydao", "PayDAO", "Realtime DAO treasury governance on Solana", "#f97316", "DAO \u00b7 WEB3", "paymentdao.vercel.app",
     ["MagicBlock Ephemeral Rollups for realtime voting", "Auto treasury execution + duplicate-vote guard", "Atomic commit & undelegate back to Solana"],
     ["Rust", "Anchor", "Solana", "MagicBlock", "React"]),
    ("godec", "Godec.xyz", "On-chain apps with wallet-based ownership", "#a855f7", "WEB3", "solana-minihack.vercel.app",
     ["Wallet-based authentication", "On-chain Todo, Notes and Voting apps", "Censorship-resistant data ownership"],
     ["Rust", "Solana", "React"]),
    ("exampaper", "ExamPaper.org", "Exam prep & academic resource platform", "#4a6cf7", "EDTECH", "exampaper.org",
     ["Role-based authentication & access", "Mock tests and exam library", "Search, filtering, resource management"],
     ["Appwrite", "TypeScript", "React"]),
    ("codenumber", "CodeNumber.net", "TU-syllabus coding education platform", "#00c2b3", "EDTECH", "codenumber.net",
     ["Monaco editor: code in the browser", "Structured syllabus-based learning", "Authentication & storage"],
     ["Appwrite", "TypeScript", "React"]),
]


def card(pid, name, tag, col, cat, dom, bullets, techs):
    W, H = 600, 272
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(name)}">')
    a('<defs>' + GLOW +
      f'<linearGradient id="bd" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect"><stop offset="0" stop-color="{col}"/><stop offset="0.5" stop-color="{C}"/><stop offset="1" stop-color="{col}"/>'
      '<animate attributeName="x1" values="0;1" dur="4s" repeatCount="indefinite"/><animate attributeName="x2" values="1;2" dur="4s" repeatCount="indefinite"/></linearGradient>'
      f'<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{col}" stop-opacity="0"/><stop offset="0.5" stop-color="{col}" stop-opacity="0.16"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>'
      f'<clipPath id="cc"><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16"/></clipPath></defs>')
    a(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="17" fill="#0a0f1f" stroke="url(#bd)" stroke-width="2"/>')
    a('<g clip-path="url(#cc)">')
    a(f'<rect x="-160" y="0" width="160" height="{H}" fill="url(#sw)"><animate attributeName="x" from="-160" to="{W}" dur="5s" repeatCount="indefinite"/></rect>')
    a(f'<rect x="0" y="0" width="5" height="{H}" fill="{col}"/>')
    a('</g>')
    # orbit ornament
    a(f'<g transform="translate(548 150)" opacity="0.55"><circle r="32" fill="none" stroke="{col}" stroke-width="1.3" stroke-dasharray="4 6">'
      '<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="14s" repeatCount="indefinite"/></circle>'
      f'<circle r="18" fill="none" stroke="{C}" stroke-width="1" stroke-dasharray="2 5"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="9s" repeatCount="indefinite"/></circle>'
      f'<circle r="4" fill="{col}" filter="url(#glow)"><animate attributeName="r" values="3;6;3" dur="2.4s" repeatCount="indefinite"/></circle></g>')
    # badge
    bw = len(cat) * 7.6 + 24
    a(f'<rect x="{W-bw-22}" y="24" width="{bw:.0f}" height="24" rx="12" fill="{col}" fill-opacity="0.14" stroke="{col}" stroke-opacity="0.8"/>'
      f'<text x="{W-bw/2-22}" y="40" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1" fill="{col}">{esc(cat)}</text>')
    a(f'<text x="30" y="58" font-family="{SANS}" font-size="28" font-weight="800" fill="{col}">{esc(name)}</text>')
    a(f'<text x="30" y="82" font-family="{SANS}" font-size="14.5" fill="#9da7b3">{esc(tag)}</text>')
    a(f'<rect x="30" y="98" width="{W-60}" height="1" fill="#1c2540"/>')
    for i, b in enumerate(bullets):
        y = 126 + i * 27
        a(f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.92;1" dur="9s" begin="{i*0.35}s" repeatCount="indefinite"/>'
          f'<text x="30" y="{y}" font-family="{MONO}" font-size="12.5" fill="{col}">\u25b8</text>'
          f'<text x="48" y="{y}" font-family="{MONO}" font-size="12.5" fill="#c9d1d9">{esc(b)}</text></g>')
    x = 30
    for t in techs:
        w = len(t) * 6.9 + 20
        a(f'<rect x="{x:.0f}" y="{H-70}" width="{w:.0f}" height="24" rx="12" fill="#0d1428" stroke="{col}" stroke-opacity="0.55"/>'
          f'<text x="{x+w/2:.0f}" y="{H-54}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#e6edf3">{esc(t)}</text>')
        x += w + 7
    a(f'<circle cx="38" cy="{H-22}" r="4" fill="{G}"><animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>'
      f'<animate attributeName="r" values="3.5;5;3.5" dur="1.6s" repeatCount="indefinite"/></circle>')
    a(f'<text x="52" y="{H-18}" font-family="{MONO}" font-size="12" fill="{G}">LIVE</text>'
      f'<text x="94" y="{H-18}" font-family="{MONO}" font-size="12" fill="#6b7688">{esc(dom)}</text>')
    a(f'<text x="{W-24}" y="{H-18}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{col}">open \u2197</text>')
    a('</svg>')
    write(f"projects/{pid}.svg", "\n".join(o))


if __name__ == "__main__":
    hero(); terminal(); orbit(); pipeline(); marquee(); stats()
    header("hdr-about.svg", "ABOUT ME", "// whoami")
    header("hdr-expertise.svg", "EXPERTISE", "// stack.orbit()")
    header("hdr-pipeline.svg", "HOW I BUILD", "// event-driven by default")
    header("hdr-projects.svg", "PROJECTS", "// shipped, live, on-chain")
    header("hdr-analytics.svg", "ANALYTICS", "// git log --stat")
    header("hdr-education.svg", "EDUCATION", "// B.Sc. CSIT, TU")
    header("hdr-connect.svg", "LET'S CONNECT", "// open to opportunities")
    for p in PROJECTS:
        card(*p)
    print("done ->", os.path.abspath(OUT))
