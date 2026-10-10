#!/usr/bin/env python3
"""Builds Reelclip's static SEO pages, sitemap.xml and robots.txt.
Run from the repo root:  node tools/extract-data.js && python3 tools/build_seo.py
"""
import json, os, html, datetime, sys
sys.path.insert(0, os.path.dirname(__file__))
from seo_content import SITE, EMAIL, WORK_SEO, SERVICES, INDUSTRIES as CORE_INDUSTRIES, CITIES
from seo_niches import NEW_SECTORS, NICHES as RAW_NICHES, ALIASES, KEYWORDS
from seo_cards import CARD, angle, NICHE_WORK, SECTOR_WORK, SERVICE_WORK, FALLBACK_BY_SECTOR, FALLBACK_DEFAULT, FALLBACK_TEXT, NO_HERO_ON_BUSINESS
import re
INDUSTRIES = CORE_INDUSTRIES + NEW_SECTORS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TODAY = datetime.date.today().isoformat()
WORK = {w['slug']: w for w in json.load(open(os.path.join(os.path.dirname(__file__), 'work.json')))}
SVC = {s['slug']: s for s in SERVICES}
IND = {i['slug']: i for i in INDUSTRIES}
CITY = {c['slug']: c for c in CITIES}
for _k, _v in SECTOR_WORK.items(): IND[_k]['work'] = _v
for _k, _v in SERVICE_WORK.items(): SVC[_k]['work'] = _v
def slugify(t): return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t.lower().replace('&', 'and').replace('\u00e9', 'e'))).strip('-')
NICHES = [dict(name=n, slug=slugify(n), sector=sec, line=line, ideas=ideas) for n, sec, line, ideas in RAW_NICHES]
NICHE = {x['name']: x for x in NICHES}
assert not (set(x['slug'] for x in NICHES) & set(IND)), 'niche slug clashes with sector'
def city_niches(ct, k=10):
    out = []
    for b in ct['biz']:
        bl = b.lower()
        for kw, names in KEYWORDS:
            if kw in bl:
                for nm in names:
                    if nm in NICHE and nm not in out: out.append(nm)
    for nm in ['Restaurants', 'Professional Services', 'Residential Real Estate', 'Medical Clinics', 'Community Events', 'Lifestyle Brands']:
        if len(out) >= 6: break
        if nm not in out: out.append(nm)
    return out[:k]
def niche_cities(nm):
    hits = [c['slug'] for c in CITIES if nm in city_niches(c, 40)]
    sec = IND[NICHE[nm]['sector']]['cities']
    return list(dict.fromkeys(hits + sec + ['seattle', 'bellevue', 'tacoma']))[:12]
PAGES = []  # (path, priority)

e = lambda s: html.escape(str(s), quote=True)
def wurl(slug): return '/work/' + WORK_SEO[slug]['url']
def wname(w): return (w['title'] + ' – ' + w['client']) if w['titleFirst'] else (w['client'] + ' – ' + w['title'])
def absimg(p): return SITE + '/' + p.lstrip('/') if p and not p.startswith('http') else p

def jsonld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace('</', '<\\/') + '</script>'

ORG = {"@type": "ProfessionalService", "@id": SITE + "/#org", "name": "Reelclip", "url": SITE + "/",
       "logo": SITE + "/img/frog-stack-color.png", "image": SITE + "/img/ev-tt.jpg", "email": EMAIL,
       "description": "Seattle-based video production company creating commercials, brand films, product campaigns, event videos and music videos across Washington.",
       "address": {"@type": "PostalAddress", "addressLocality": "Seattle", "addressRegion": "WA", "addressCountry": "US"},
       "areaServed": [{"@type": "City", "name": c['name'] + ("" if ',' in c['name'] else ", WA")} for c in CITIES] + [{"@type": "State", "name": "Washington"}],
       "knowsAbout": [s['name'] for s in SERVICES]}

def head(title, desc, path, img='img/ev-tt.jpg', schema=None, robots='index,follow'):
    url = SITE + path
    blocks = ''.join(jsonld(s) for s in (schema or []))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#111111">
<link rel="icon" href="/img/frog-stack-color.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Reelclip">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{absimg(img)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{absimg(img)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;900&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/seo.css">
{blocks}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
  <a class="logo" href="/" aria-label="Reelclip home"><img src="/img/frog-stack-color.png" alt="" width="44" height="40"><span>REELCLIP</span></a>
  <nav class="main" aria-label="Main">
    <a href="/work">WORK</a><a href="/services">SERVICES</a><a href="/industries">INDUSTRIES</a><a href="/locations">LOCATIONS</a>
    <a href="/#contact" class="cta">START A PROJECT</a>
  </nav>
</div></header>
<main id="main" class="wrap">
'''

def crumbs(items):
    """items: list of (name, path or None)"""
    links = ' <span>/</span> '.join((f'<a href="{p}">{e(n)}</a>' if p else f'<span aria-current="page">{e(n)}</span>') for n, p in items)
    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, **({"item": SITE + p} if p else {})} for i, (n, p) in enumerate(items)]}
    return f'<nav class="crumbs" aria-label="Breadcrumb">{links}</nav>', schema

def foot():
    svc = ''.join(f'<li><a href="/services/{s["slug"]}">{e(s["name"])}</a></li>' for s in SERVICES[:6]) + '<li><a href="/services">All services \u2192</a></li>'
    ind = ''.join(f'<li><a href="/industries/{i["slug"]}">{e(i["name"])}</a></li>' for i in CORE_INDUSTRIES) + '<li><a href="/industries">All industries \u2192</a></li>'
    feat = sorted([k for k in WORK_SEO if WORK_SEO[k].get('feature')], key=lambda k: WORK_SEO[k]['feature'])[:8]
    wk = ''.join(f'<li><a href="{wurl(k)}">{e(WORK[k]["client"] if not WORK[k]["titleFirst"] else WORK[k]["title"])}</a></li>' for k in feat)
    MAIN = ['seattle','bellevue','tacoma','redmond','kirkland','renton','federal-way','everett']
    cities = ''.join(f'<a href="/locations/{c}">{e(CITY[c]["name"])}</a>' for c in MAIN)
    rest = ''.join(f'<a href="/locations/{c["slug"]}">{e(c["name"])}</a>' for c in CITIES if c['slug'] not in MAIN)
    return f'''</main>
<footer class="site"><div class="wrap">
  <div class="cols">
    <div><a class="logo" href="/"><img src="/img/frog-stack-color.png" alt="" width="44" height="40"><span>REELCLIP</span></a>
      <p class="muted" style="margin-top:14px;font-size:14px">Seattle-based video production for commercials, brand films, product launches, events and music videos. Available across Washington.</p>
      <p style="margin-top:14px;font-size:14px"><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
    <div><h4>SERVICES</h4><ul>{svc}</ul></div>
    <div><h4>INDUSTRIES</h4><ul>{ind}</ul></div>
    <div><h4>WORK</h4><ul>{wk}<li><a href="/work">All work →</a></li></ul></div>
    <div><h4>AREAS SERVED</h4><div class="city-cloud">{cities}</div>
      <details class="more-areas"><summary>{len(CITIES) - len(MAIN)} more areas</summary><div class="city-cloud">{rest}</div></details>
      <p style="margin-top:12px"><a href="/locations">Areas served \u2192</a></p></div>
  </div>
  <div class="base"><span>© {datetime.date.today().year} Reelclip · Seattle, WA</span><span><a href="/">Home</a> · <a href="/work">Work</a> · <a href="/locations">Locations</a> · <a href="/#contact">Contact</a></span></div>
</div></footer>
<script>
document.addEventListener('click',function(ev){{var b=ev.target.closest('[data-embed]');if(!b)return;ev.preventDefault();var f=document.createElement('iframe');f.src=b.getAttribute('data-embed');f.title=b.getAttribute('aria-label')||'Video';f.allow='autoplay; fullscreen; picture-in-picture';f.allowFullscreen=true;b.parentNode.replaceChild(f,b);}});
</script>
</body>
</html>
'''

def cta_band(title="Let's make something worth watching.", text="Tell us what you're building. We'll come back with ideas, a plan and a quote."):
    return f'''<section><div class="cta-band"><div><h2>{e(title)}</h2><p>{e(text)}</p></div>
<a class="btn" href="/#contact">START A PROJECT →</a></div></section>'''

PATHS = f'''<section><div class="section-head"><h2>How we can work together</h2></div>
<div class="paths">
<a href="/?type=project#contact"><b>One-time production</b><span>Product launches, commercials, special events and individual campaigns.</span><em>DISCUSS A PROJECT →</em></a>
<a href="/services/content-partnerships"><b>Ongoing creative partnership</b><span>Regular campaign content, monthly production, event coverage and recurring assets.</span><em>EXPLORE A PARTNERSHIP →</em></a>
<a href="/services/production-crew"><b>Production crew + support</b><span>You have the creative; we bring filming, editing, crew coordination and execution.</span><em>HIRE OUR TEAM →</em></a>
</div></section>'''

def work_cards(slugs, n=None, ctx=None):
    out = []
    for k in slugs[:n] if n else slugs:
        if k not in WORK: continue
        w = WORK[k]
        a = angle(k, ctx)
        if not a and ctx and 'example' in ctx and k in FALLBACK_TEXT: a = FALLBACK_TEXT[k]
        img, text = (a if a else (w["img"], CARD.get(k, w["aboutShort"])))
        out.append(f'''<a class="work-card" href="{wurl(k)}"><div class="thumb"><img src="/{e(img)}" alt="{e(wname(w))}" loading="lazy" width="640" height="360"></div>
<span class="k">{e(w["type"])}{(" · " + e(w["year"])) if w["year"] else ""}</span><span class="n">{e(wname(w))}</span><span class="s">{e(text)}</span></a>''')
    return '<div class="grid g3">' + ''.join(out) + '</div>'

def faq_html(faqs):
    return ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faqs)

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def write(path, content, priority='0.6'):
    fp = os.path.join(ROOT, path.lstrip('/') + ('index.html' if path.endswith('/') else '.html'))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w').write(content)
    PAGES.append((path.rstrip('/') or '/', priority))

# ---------- services ----------
def build_services():
    cards = ''.join(f'<a class="card" href="/services/{s["slug"]}"><span class="tag">{e(s["short"])}</span><h3>{e(s["name"])}</h3><p>{e(s["lede"])}</p></a>' for s in SERVICES)
    c, cs = crumbs([("Home", "/"), ("Services", None)])
    body = f'''{c}<div class="hero"><p class="eyebrow"><i></i>Production services</p><h1>Video production services in Seattle</h1>
<p class="lede">Commercials, brand films, product launches, event coverage, social content, corporate video and music videos, from concept to final delivery, for businesses across Washington.</p>
<div class="ctas"><a class="btn" href="/#contact">START A PROJECT →</a><a class="btn ghost" href="/work">SEE THE WORK</a></div></div>
<section><div class="grid g3">{cards}</div></section>{PATHS}{cta_band()}'''
    write('/services/', head("Video Production Services in Seattle | Reelclip",
        "Reelclip's Seattle video production services: commercials, brand films, product launches, event videography, social, corporate and music videos.",
        '/services', schema=[cs]) + body + foot(), '0.9')
    for s in SERVICES:
        c, cs = crumbs([("Home", "/"), ("Services", "/services"), (s['name'], None)])
        rel = ''.join(f'<a href="/services/{r}">{e(SVC[r]["name"])}</a>' for r in s['related'])
        inds = [i for i in INDUSTRIES if s['slug'] in i['services']]
        indchips = ''.join(f'<a href="/industries/{i["slug"]}">{e(i["name"])}</a>' for i in inds)
        cities = ''.join((f'<a href="/locations/{ct["slug"]}/{s["slug"]}">' if s['slug'] in SVC_LINES else f'<a href="/locations/{ct["slug"]}">') + f'{e(s["name"])} in {e(ct["name"])}</a>' for ct in CITIES)
        steps = ''.join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in s['steps'])
        img = WORK[s['work'][0]]['img'] if s['work'] and s['work'][0] in WORK else 'img/ev-tt.jpg'
        schema = [cs, faq_schema(s['faqs']), {"@context": "https://schema.org", "@type": "Service", "name": s['name'], "serviceType": s['name'],
                  "description": s['desc'], "provider": {"@id": SITE + "/#org", "@type": "ProfessionalService", "name": "Reelclip", "url": SITE + "/"},
                  "areaServed": ORG['areaServed'], "url": SITE + "/services/" + s['slug']}]
        body = f'''{c}<div class="hero"><p class="eyebrow"><i></i>{e(s["short"])}</p><h1>{e(s["h1"])}</h1><p class="lede">{e(s["lede"])}</p>
<div class="ctas"><a class="btn" href="/#contact">START A PROJECT →</a>{'<a class="btn ghost" href="#work">SEE EXAMPLES</a>' if s['work'] else '<a class="btn ghost" href="/work">SEE OUR WORK</a>'}</div>
<div class="hero-media"><img src="/{e(img)}" alt="{e(s["name"])} by Reelclip" width="1600" height="900" fetchpriority="high"></div></div>
<section class="grid g2"><div style="display:flex;flex-direction:column;gap:16px">{"".join(f"<p class=muted>{e(p)}</p>" for p in s["intro"])}</div>
<div class="card"><h3>What's included</h3><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in s["includes"])}</ul></div></section>
<section><div class="section-head"><h2>How it works</h2></div><ol class="steps">{steps}</ol></section>
<section><div class="card"><h3>Typical deliverables</h3><ul class="ticks c2">{"".join(f"<li>{e(x)}</li>" for x in s["deliverables"])}</ul></div></section>
{f'<section id="work"><div class="section-head"><h2>{e(s["name"])} we\'ve made</h2><a class="btn ghost" href="/work">ALL WORK</a></div>{work_cards(s["work"], ctx=[s["slug"]])}</section>' if s["work"] else ''}
{f'<section><div class="section-head"><h2>Industries</h2></div><div class="chips">{indchips}</div></section>' if indchips else ''}
<section><div class="section-head"><h2>Questions</h2></div>{faq_html(s["faqs"])}</section>
{PATHS}
<section><div class="section-head"><h2>Related services</h2></div><div class="chips">{rel}</div>
<p class="mono" style="margin:28px 0 12px;color:var(--soft)">AVAILABLE ACROSS WASHINGTON</p><div class="chips">{cities}<a href="/locations">All areas →</a></div></section>
{cta_band()}'''
        write('/services/' + s['slug'], head(s['title'], s['desc'], '/services/' + s['slug'], img, schema) + body + foot(), '0.9')

# ---------- work ----------
def video_embed(w):
    poster = w['img']
    if w['vimeo']:
        src = f"https://player.vimeo.com/video/{w['vimeo']}?autoplay=1&title=0&byline=0&portrait=0"
    elif w['drive']:
        src = f"https://drive.google.com/file/d/{w['drive']}/preview"
    elif w['youtube']:
        src = f"https://www.youtube-nocookie.com/embed/{w['youtube']}?autoplay=1&rel=0"
    elif w['file']:
        return f'<div class="hero-media"><video src="/{e(w["file"])}" poster="/{e(w["poster"] or poster)}" controls playsinline preload="none" style="width:100%;height:100%;object-fit:cover"></video></div>', None
    else:
        return f'<div class="hero-media"><img src="/{e(poster)}" alt="{e(wname(w))}"></div>', None
    btn = f'''<a href="{e(src)}" data-embed="{e(src)}" aria-label="Play {e(wname(w))}" style="position:absolute;inset:0;display:block"><img src="/{e(poster)}" alt="{e(wname(w))}" width="1600" height="900" fetchpriority="high" style="width:100%;height:100%;object-fit:cover"><span style="position:absolute;inset:0;margin:auto;width:84px;height:84px;border-radius:999px;background:var(--yellow);display:flex;align-items:center;justify-content:center"><svg width="26" height="26" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l14 8-14 8z" fill="#111"/></svg></span></a>'''
    return f'<div class="hero-media">{btn}</div>', src

def hero_video(k, poster=None):
    """Playable hero (click to load) for project k, with an optional context poster."""
    w = dict(WORK[k])
    # multi-film projects: play the film that matches the poster (e.g. pickleball still -> pickleball recap)
    if poster and w.get('films'):
        key = {'ev-pb': 'Pickleball', 'ev-go': 'Grand Opening', 'ev-tt': 'Sneaker Con'}
        for pre, word in key.items():
            if '/' + pre in '/' + poster.split('img/')[-1] or poster.split('/')[-1].startswith(pre):
                f = next((f for f in w['films'] if word in f['name']), None)
                if f and f.get('vimeo'): w['vimeo'] = f['vimeo']
                break
    if poster:
        w['img'] = poster
        if w.get('file'): w['poster'] = poster
    return video_embed(w)[0]

def fallback_for(sector):
    return FALLBACK_BY_SECTOR.get(sector, FALLBACK_DEFAULT)

def build_work():
    order = sorted(WORK_SEO, key=lambda k: WORK_SEO[k].get('feature', 99))
    groups = [("Commercial + brand", ['product', 'brand']), ("Events + activations", ['events']), ("Music videos", ['music'])]
    secs = ''
    for label, inds in groups:
        ks = [k for k in order if k in WORK and WORK[k]['industry'] in inds]
        secs += f'<section><div class="section-head"><h2>{e(label)}</h2></div>{work_cards(ks)}</section>'
    c, cs = crumbs([("Home", "/"), ("Work", None)])
    items = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": SITE + wurl(k), "name": wname(WORK[k])} for i, k in enumerate(order) if k in WORK]}
    body = f'''{c}<div class="hero"><p class="eyebrow"><i></i>Selected work</p><h1>Video production work</h1>
<p class="lede">Commercials, brand films, product launches, corporate events and music videos made in Seattle, Bellevue, Tacoma and across Washington.</p></div>{secs}{cta_band()}'''
    write('/work/', head("Video Production Portfolio | Commercials, Events + Music Videos | Reelclip",
        "Reelclip's portfolio: TurboTax event production, Chilean Salmon, NuWav, Peristera, Gerard Cycles, Jack's BBQ, Lula Coffee, Zadart and Washington music videos.",
        '/work', schema=[cs, items]) + body + foot(), '0.9')

    for k in order:
        if k not in WORK: continue
        w, m = WORK[k], WORK_SEO[k]
        name = wname(w)
        desc = (w['brief'] or w['aboutShort'])[:155]
        c, cs = crumbs([("Home", "/"), ("Work", "/work"), (name, None)])
        player, embed = video_embed(w)
        metas = [("Client", w['client'] if not w['titleFirst'] else w['title']), ("Service", w['type']), ("Deliverables", w['deliverables'] or '—'), ("Year", w['year'] or '—')]
        approach = ''.join(f'<div class="card"><span class="tag">{e(a)}</span><p>{e(b)}</p></div>' for a, b in w['approach'])
        beats = ''.join(f'<div class="beat">{f"<img src=/{e(b["img"])} alt=\"{e(b["title"])}\" loading=lazy width=800 height=600>" if b["img"] else ""}<h3>{e(b["title"])}</h3><p class="muted">{e(b["text"])}</p></div>' for b in w['beats'])
        films = ''.join(f'<div class="work-card"><div class="thumb"><img src="/{e(f["img"])}" alt="{e(f["name"])}" loading="lazy"></div><span class="k">{e(f["len"])}</span><span class="n">{e(f["name"])}</span><span class="s">{e(f["crew"])}</span></div>' for f in w['films'])
        frames = ''.join(f'<img src="/{e(s)}" alt="{e(w["stillAlts"][i] if i < len(w["stillAlts"]) else name)}" loading="lazy" width="480" height="270">' for i, s in enumerate(w['stills'][:12]))
        credits = ''.join(f'<span>{e(r[0])}</span><span>{f"<a href={chr(34)}{e(r[2])}{chr(34)} rel=noopener target=_blank>{e(r[1])}</a>" if len(r) > 2 and r[2] else e(r[1])}</span>' for r in w['creditList'])
        facts = ''.join(f'<dt>{e(a)}</dt><dd>{e(b)}</dd>' for a, b in w['facts'].items())
        svc = ''.join(f'<a href="/services/{s}">{e(SVC[s]["name"])}</a>' for s in m['services'])
        ind = ''.join(f'<a href="/industries/{i}">{e(IND[i]["name"])}</a>' for i in m['industries'])
        loc = ''.join(f'<a href="/locations/{ct}">Video production in {e(CITY[ct]["name"])}</a>' for ct in m['cities'] if ct in CITY)
        more = [x for x in order if x != k and x in WORK and WORK[x]['industry'] == w['industry']][:3]
        schema = [cs]
        vid = {"@context": "https://schema.org", "@type": "VideoObject", "name": name, "description": w['brief'] or w['aboutShort'] or name,
               "thumbnailUrl": [absimg(w['img'])], "publisher": {"@id": SITE + "/#org", "@type": "Organization", "name": "Reelclip"}}
        if w['year']: vid["uploadDate"] = w['year']
        if embed: vid["embedUrl"] = embed.split('?')[0]
        if w['vimeo']: vid["url"] = "https://vimeo.com/" + w['vimeo']
        schema.append(vid)
        schema.append({"@context": "https://schema.org", "@type": "CreativeWork", "name": name, "about": m['h2'], "creator": {"@id": SITE + "/#org", "@type": "Organization", "name": "Reelclip"}, "url": SITE + wurl(k), "image": absimg(w['img'])})
        body = f'''{c}<div class="hero"><p class="eyebrow"><i></i>{e(m["h2"])}</p><h1>{e(name)}</h1>
<div class="meta">{"".join(f"<div><span>{e(a)}</span><span>{e(b)}</span></div>" for a, b in metas)}</div>{player}</div>
<section class="grid g2"><div style="display:flex;flex-direction:column;gap:14px"><p class="eyebrow">The brief</p><h2 style="font-size:clamp(24px,2.6vw,36px);line-height:1.1">{e(w["brief"])}</h2></div>
<div style="display:flex;flex-direction:column;gap:14px"><p class="eyebrow">The result</p><p class="muted" style="font-size:19px">{e(w["result"])}</p>
{f'<div class="quote">“{e(w["line"])}”<small>Creative statement</small></div>' if w["line"] else ""}</div></section>
{f'<section><div class="section-head"><h2>Approach</h2></div><div class="grid g4">{approach}</div></section>' if approach else ""}
{f'<section><div class="section-head"><h2>The films</h2></div><div class="grid g3">{films}</div></section>' if films else ""}
{f'<section><div class="section-head"><h2>How we shot it</h2></div><div class="grid g3">{beats}</div></section>' if beats else ""}
{f'<section><div class="card"><h3>Scope of work</h3><ul class="ticks c2">{"".join(f"<li>{e(x)}</li>" for x in w["scope"])}</ul></div></section>' if w["scope"] else ""}
{f'<section><div class="section-head"><h2>Frames</h2></div><div class="frames">{frames}</div></section>' if frames else ""}
<section class="grid g2">{f'<div class="card"><h3>About {e(w["client"] if not w["titleFirst"] else w["title"])}</h3>{("".join(f"<h4 style=\"margin:6px 0 0;font-size:15px\">{e(sec['name'])}</h4>" + "".join(f"<p>{e(p)}</p>" for p in sec['paras']) for sec in w["aboutSections"])) if w.get("aboutSections") else ("".join(f"<p>{e(p)}</p>" for p in w["about"]) or f"<p>{e(w["aboutShort"])}</p>")}{f"<dl class=facts style=margin-top:8px>{facts}</dl>" if facts else ""}</div>' if (w["about"] or w["aboutShort"]) else ""}
{f'<div class="card"><h3>Credits</h3><div class="credits">{credits}</div></div>' if credits else ""}</section>
<section><p class="mono" style="color:var(--soft);margin-bottom:12px">SERVICES</p><div class="chips">{svc}</div>
{f'<p class="mono" style="color:var(--soft);margin:22px 0 12px">INDUSTRIES</p><div class="chips">{ind}</div>' if ind else ""}
{f'<p class="mono" style="color:var(--soft);margin:22px 0 12px">LOCATIONS</p><div class="chips">{loc}</div>' if loc else ""}</section>
{f'<section><div class="section-head"><h2>More like this</h2></div>{work_cards(more)}</section>' if more else ""}
{cta_band("Want something like this?", "Tell us about your launch, event or campaign and we'll show you how we'd approach it.")}'''
        write(wurl(k), head(m['title'] + ' | Reelclip', desc, wurl(k), w['img'], schema) + body + foot(), '0.8')

# ---------- industries ----------
def build_industries():
    cards = ''.join(f'<a class="card" href="/industries/{i["slug"]}"><span class="tag">{sum(1 for x in NICHES if x["sector"]==i["slug"])} specialties</span><h3>{e(i["name"])}</h3><p>{e(i["lede"])}</p></a>' for i in INDUSTRIES)
    groups = ''.join(f'<div><h3 style="font-size:18px;margin-bottom:12px"><a href="/industries/{i["slug"]}" style="text-decoration:none">{e(i["name"])}</a></h3><div class="chips">' + ''.join(f'<a href="/industries/{x["slug"]}">{e(x["name"])}</a>' for x in NICHES if x['sector'] == i['slug']) + '</div></div>' for i in INDUSTRIES)
    c, cs = crumbs([("Home", "/"), ("Industries", None)])
    total = len(NICHES) + len(ALIASES)
    body = f'''{c}<div class="hero"><p class="eyebrow"><i></i>Industries</p><h1>Video production for every industry</h1>
<p class="lede">From restaurants and law firms to biotech, pickleball clubs and private jets: {total}+ industries, one creative production team, available across Washington.</p>
<div class="ctas"><a class="btn" href="/#contact">START A PROJECT \u2192</a><a class="btn ghost" href="#all">FIND YOUR INDUSTRY</a></div></div>
<section><div class="grid g3">{cards}</div></section>
<section id="all"><div class="section-head"><h2>Every industry we serve</h2></div><div class="grid g2" style="gap:36px 28px">{groups}</div></section>{cta_band()}'''
    write('/industries/', head("Video Production for Every Industry | Washington | Reelclip",
        "Video production for 100+ industries: restaurants, spirits, law firms, startups, real estate, healthcare, biotech, sports, manufacturing and more across Washington.",
        '/industries', schema=[cs]) + body + foot(), '0.8')
    for i in INDUSTRIES:
        c, cs = crumbs([("Home", "/"), ("Industries", "/industries"), (i['name'], None)])
        swork = [k for k in i['work'] if k in WORK]
        sexample = not swork
        if sexample: swork = [fallback_for(i['slug'])]
        sa = FALLBACK_TEXT.get(swork[0]) if sexample else angle(swork[0], [i['slug']])
        img = (SECTOR_IMG.get(i['slug']) or [sa[0] if sa else WORK[swork[0]]['img']])[0]
        shero = hero_video(swork[0], img)
        svc = ''.join(f'<a class="card" href="/services/{s}"><span class="tag">Service</span><h3>{e(SVC[s]["name"])}</h3><p>{e(SVC[s]["lede"])}</p></a>' for s in i['services'])
        locs = ''.join(f'<a href="/locations/{ct}">{e(i["name"].split(",")[0])} video in {e(CITY[ct]["name"])}</a>' for ct in i['cities'] if ct in CITY)
        body = f'''{c}<div class="hero"><p class="eyebrow"><i></i>{e(i["name"])}</p><h1>{e(i["h1"])}</h1><p class="lede">{e(i["lede"])}</p>
<div class="ctas"><a class="btn" href="/#contact">START A PROJECT →</a><a class="btn ghost" href="#work">SEE THE WORK</a></div>
{shero}<p class="mono" style="color:var(--soft);margin-top:-8px">{("EXAMPLE HERO FILM: " if sexample else "WATCH: ") + e(wname(WORK[swork[0]]).upper())}</p></div>
<section class="grid g2"><div style="display:flex;flex-direction:column;gap:16px">{"".join(f"<p class=muted>{e(p)}</p>" for p in i["intro"])}</div>
<div class="card"><h3>What we make</h3><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in i["makes"])}</ul></div></section>
<section id="work"><div class="section-head"><h2>{"A hero film we've made" if sexample else "Work"}</h2></div>{work_cards(swork, ctx=(["example"] if sexample else [i["slug"]]))}</section>
{('<section><div class="section-head"><h2>Specialties</h2></div><div class="chips">' + ''.join(f'<a href="/industries/{x["slug"]}">{e(x["name"])}</a>' for x in NICHES if x['sector'] == i['slug']) + '</div></section>') if any(x['sector'] == i['slug'] for x in NICHES) else ''}
<section><div class="section-head"><h2>Services for {e(i["name"].lower())}</h2></div><div class="grid g4">{svc}</div></section>
<section><div class="section-head"><h2>Questions</h2></div>{faq_html(i["faqs"])}</section>
<section><p class="mono" style="color:var(--soft);margin-bottom:12px">WHERE WE WORK</p><div class="chips">{locs}<a href="/locations">All areas →</a></div></section>
{cta_band()}'''
        write('/industries/' + i['slug'], head(i['title'], i['desc'], '/industries/' + i['slug'], img, [cs, faq_schema(i['faqs'])]) + body + foot(), '0.7')

SECTOR_IMG = {
 'food-beverage': ['img/jacks-bbq.jpg','img/lula.jpg','img/ev-cs.jpg','img/lula-06.jpg'],
 'fashion-apparel': ['img/nuwav.jpg','img/peristera.jpg'],
 'automotive': ['img/zadart.jpg','img/zadart-02.jpg','img/zadart-04.jpg'],
 'corporate-events': ['img/ev-go-cover.jpg','img/ev-tt.jpg','img/ev-go-05.jpg','img/ev-pb-00.jpg'],
 'hospitality-nightlife': ['img/ev-ms-h1.jpg','img/ev-la.jpg','img/lula.jpg'],
 'music-entertainment': ['img/ev-ms-h2.jpg','img/mv-cc.jpg','img/mv-dt.jpg','img/mv-ch.jpg'],
 'retail-brands': ['img/ev-go-cover.jpg','img/ev-go-01.jpg','img/gerard-cycles.jpg'],
 'sports-fitness': ['img/ev-pb-00.jpg','img/ev-pb-03.jpg','img/gerard-cycles.jpg'],
 'luxury-lifestyle': ['img/peristera.jpg','img/zadart-03.jpg','img/nuwav.jpg'],
}
def build_niches():
    for idx, x in enumerate(NICHES):
        sec = IND[x['sector']]; nm = x['name']; low = nm.lower()
        path = '/industries/' + x['slug']
        c, cs = crumbs([("Home", "/"), ("Industries", "/industries"), (sec['name'], "/industries/" + sec['slug']), (nm, None)])
        ws = [k for k in NICHE_WORK.get(nm, []) if k in WORK]
        example = not ws
        if example: ws = [fallback_for(x['sector'])]
        a0 = (angle(ws[0], [x['sector']]) or FALLBACK_TEXT.get(ws[0])) if example else angle(ws[0], [nm, x['sector']])
        img = a0[0] if a0 else WORK[ws[0]]['img']
        hero = hero_video(ws[0], img)
        makes = x['ideas'] + [m for m in sec['makes'] if m not in x['ideas']][:5]
        svc = ''.join(f'<a class="card" href="/services/{s}"><span class="tag">Service</span><h3>{e(SVC[s]["name"])} for {e(low)}</h3><p>{e(SVC[s]["lede"])}</p></a>' for s in sec['services'])
        cities = niche_cities(nm)
        locs = ''.join(f'<a href="/locations/{ct}">{e(nm)} video in {e(CITY[ct]["name"])}</a>' for ct in cities if ct in CITY)
        sib = ''.join(f'<a href="/industries/{y["slug"]}">{e(y["name"])}</a>' for y in NICHES if y['sector'] == x['sector'] and y is not x)
        faqs = [(f"Do you make video for {low}?", x['line'] + " Reelclip is based in Seattle and works across Washington."),
                (f"What kind of videos do {low} need?", "Most start with " + ', '.join(i.lower() for i in x['ideas'][:-1]) + f" and {x['ideas'][-1].lower()}, then add vertical cutdowns for social. We'll recommend the right mix for your goals and budget."),
                sec['faqs'][0],
                (f"How much does video for {low} cost?", "It depends on scope: shoot days, crew, locations and how many deliverables you need. Share your budget range on the project form and we'll design the strongest version that fits it.")]
        title = f"Video Production for {nm} | Seattle + Washington | Reelclip"
        if len(title) > 70: title = f"{nm} Video Production | Reelclip"
        desc = f"{x['line']} Seattle-based Reelclip makes video for {low} across Washington."
        if len(desc) > 160: desc = x['line'][:157].rstrip() + ('\u2026' if len(x['line']) > 157 else '')
        schema = [cs, faq_schema(faqs), {"@context": "https://schema.org", "@type": "Service", "name": f"Video production for {low}", "serviceType": "Video production",
                  "audience": {"@type": "BusinessAudience", "name": nm}, "description": x['line'],
                  "provider": {"@id": SITE + "/#org", "@type": "ProfessionalService", "name": "Reelclip", "url": SITE + "/"},
                  "areaServed": {"@type": "State", "name": "Washington"}, "url": SITE + path}]
        body = f"""{c}<div class="hero"><p class="eyebrow"><i></i>{e(sec["name"])}</p><h1>Video production for {e(low)}</h1>
<p class="lede">{e(x["line"])}</p>
<div class="ctas"><a class="btn" href="/#contact">START A PROJECT \u2192</a><a class="btn ghost" href="#work">{"SEE AN EXAMPLE" if example else "SEE RELATED WORK"}</a></div>
{hero}<p class="mono" style="color:var(--soft);margin-top:-8px">{("EXAMPLE HERO FILM: " if example else "WATCH: ") + e(wname(WORK[ws[0]]).upper())}</p></div>
<section class="grid g2"><div style="display:flex;flex-direction:column;gap:16px"><h2>Video made for {e(low)}</h2><p class="muted">{e(sec["intro"][0])}</p><p class="muted">{e(sec["intro"][1])}</p></div>
<div class="card"><h3>What we make for {e(low)}</h3><ul class="ticks">{"".join(f"<li>{e(m)}</li>" for m in makes)}</ul></div></section>
<section><div class="section-head"><h2>Services</h2><a class="btn ghost" href="/services">ALL SERVICES</a></div><div class="grid g4">{svc}</div></section>
<section id="work"><div class="section-head"><h2>{"A hero film we've made" if example else "Related work"}</h2><a class="btn ghost" href="/work">ALL WORK</a></div>{work_cards(ws, ctx=([x["sector"], "example"] if example else [nm, x["sector"]]))}</section>
<section><div class="section-head"><h2>Questions from {e(low)}</h2></div>{faq_html(faqs)}</section>
{PATHS}
<section><p class="mono" style="color:var(--soft);margin-bottom:12px">{e(nm.upper())} VIDEO ACROSS WASHINGTON</p><div class="chips">{locs}<a href="/locations">All areas \u2192</a></div>
<p class="mono" style="color:var(--soft);margin:22px 0 12px">MORE IN {e(sec["name"].upper())}</p><div class="chips"><a href="/industries/{sec["slug"]}">{e(sec["name"])}</a>{sib}</div></section>
{cta_band(f"Let's make something for your {low.rstrip('s') if low.endswith('s') and not low.endswith('ss') else low} brand." if False else "Let's make something worth watching.", f"Tell us about your business and what you need. We make video for {low} across Washington.")}"""
        write(path, head(title, desc, path, img, schema) + body + foot(), '0.6')

# ---------- locations ----------
REGION_WORK = {"King County": ["turbotax-three-event-campaign", "chilean-salmon-culinary-event-film", "gerard-cycles-brand-film"],
               "Pierce County": ["turbotax-three-event-campaign", "tha-baby-street-runner", "slotlifebaby-different-time"]}
HERO_POOL = ['img/ev-tt.jpg','img/gerard-cycles.jpg','img/zadart-02.jpg','img/ev-go-cover.jpg','img/ev-pb-00.jpg','img/jacks-bbq.jpg','img/nuwav.jpg','img/lula.jpg','img/ev-cs.jpg','img/zadart.jpg','img/peristera.jpg','img/ev-go-02.jpg']
DEFAULT_WORK = ["turbotax-three-event-campaign", "nuwav-jacket-launch-commercial", "zadart-exotic-car-campaign"]
TIER_TEXT = {"home": "{n} is part of our home turf. We shoot here all the time, and we can usually be on site quickly.",
             "regular": "We drive to {n} regularly. Distance isn't a problem: we're happy to make the trip for the right project.",
             "travel": "We take projects in {n} by arrangement. We don't mind the drive, and we'll build any travel into a clear quote up front."}
SVC_LINES = {
  "commercial-video-production": "Commercials and ad campaigns for {n} businesses, built for social, web and paid media.",
  "brand-films": "Brand and founder films that show who's behind your {n} business.",
  "product-video-production": "Launch videos and product content for brands based in or launching in {n}.",
  "event-videography": "Event recaps, interviews and photography for events and activations in {n}.",
  "social-media-video": "Reels, TikToks and ad creative for {n} brands that need a steady stream of content.",
  "corporate-video-production": "Recruiting, training and leadership video for {n} companies and teams.",
}

def nearby(ct):
    same = [c for c in CITIES if c['county'] == ct['county'] and c['slug'] != ct['slug']]
    if len(same) < 4:
        same += [c for c in CITIES if c['tier'] == 'home' and c['slug'] != ct['slug'] and c not in same]
    return same[:8]

def build_locations():
    groups = {}
    for ct in CITIES: groups.setdefault(ct['county'], []).append(ct)
    secs = ''.join(f'<section><div class="section-head"><h2>{e(cty)}</h2></div><div class="grid g4">' + ''.join(
        f'<a class="card" href="/locations/{ct["slug"]}"><span class="tag">{e(ct["county"])}</span><h3>{e(ct["name"])}</h3><p>{e(ct["angle"].split(". ")[0].rstrip(".") + ".")}</p></a>' for ct in cs_) + '</div></section>'
        for cty, cs_ in groups.items())
    c, cs = crumbs([("Home", "/"), ("Locations", None)])
    body = f'''{c}<div class="hero"><p class="eyebrow"><i></i>Areas served</p><h1>Seattle-based. Available across Washington.</h1>
<p class="lede">Reelclip is based in Seattle and shoots across King, Pierce, Snohomish, Thurston and Kitsap counties, and anywhere in Washington by arrangement. We don't mind the drive.</p>
<div class="ctas"><a class="btn" href="/#contact">START A PROJECT →</a></div></div>{secs}{cta_band()}'''
    write('/locations/', head("Areas Served | Video Production Across Washington | Reelclip",
        "Reelclip provides video production in Seattle, Bellevue, Tacoma, Federal Way, Tukwila, Everett, Olympia and cities across Washington.",
        '/locations', schema=[cs, {"@context": "https://schema.org", **ORG}]) + body + foot(), '0.8')
    for ct in CITIES:
        n = ct['name']; nwa = n if ',' in n else n + ', WA'
        c, cs = crumbs([("Home", "/"), ("Locations", "/locations"), (n, None)])
        here = [k for k, m in WORK_SEO.items() if ct['slug'] in m['cities']]
        here = [k for k in here if k not in NO_HERO_ON_BUSINESS] + [k for k in here if k in NO_HERO_ON_BUSINESS]  # business work leads
        region = [x for x in REGION_WORK.get(ct['county'], DEFAULT_WORK) if x not in here]
        ws = ([k for k in here if k not in NO_HERO_ON_BUSINESS] + [k for k in region if k not in NO_HERO_ON_BUSINESS] + [k for k in here if k in NO_HERO_ON_BUSINESS] + [k for k in region if k in NO_HERO_ON_BUSINESS])[:3]
        biz_here = [k for k in here if k not in NO_HERO_ON_BUSINESS]
        img = WORK[biz_here[0]]['img'] if biz_here else HERO_POOL[sum(map(ord, ct['slug'])) % len(HERO_POOL)]
        svc = ''.join(f'<a class="card" href="/locations/{ct["slug"]}/{s}"><span class="tag">{e(SVC[s]["short"])}</span><h3>{e(SVC[s]["name"])} in {e(n)}</h3><p>{e(t.format(n=n))}</p></a>' for s, t in SVC_LINES.items())
        near = ''.join(f'<a href="/locations/{x["slug"]}">{e(x["name"])}</a>' for x in nearby(ct))
        faqs = [(f"Do you offer video production in {n}?", TIER_TEXT[ct['tier']].format(n=n) + f" Reelclip is based in Seattle, {ct['route'] if ct['tier']!='home' or ct['slug']!='seattle' else 'and shoots all over the city'}."),
                (f"What kinds of {n} businesses do you work with?", f"We make video for {', '.join(x.lower() for x in ct['biz'][:-1])} and {ct['biz'][-1].lower()} in {n}, plus brands anywhere that want to film here."),
                (f"Can you film at our location in {n}?", "Yes. We film at offices, stores, restaurants, venues, warehouses and homes, and scout public locations when the story calls for it."),
                ("How do we get a quote?", "Use the project form with your goals, timeline and budget range. We'll reply with questions, ideas and a clear quote.")]
        did = (f"<p class=muted>Work we've filmed in {e(n)}: " + ', '.join(f'<a href="{wurl(k)}">{e(wname(WORK[k]))}</a>' for k in here) + ".</p>") if here else ''
        schema = [cs, faq_schema(faqs), {"@context": "https://schema.org", "@type": "Service", "name": f"Video production in {nwa}", "serviceType": "Video production",
                  "provider": {"@id": SITE + "/#org", "@type": "ProfessionalService", "name": "Reelclip", "url": SITE + "/"},
                  "areaServed": {"@type": "City", "name": nwa}, "url": SITE + "/locations/" + ct['slug']}]
        title = f"Video Production in {nwa} | Commercials, Events + Brand Films | Reelclip"
        if len(title) > 70: title = f"Video Production in {nwa} | Reelclip"
        desc = f"Video production in {nwa} from Seattle's Reelclip: commercials, brand films, product launches, events and social content for {n} businesses."
        body = f'''{c}<div class="hero"><p class="eyebrow"><i></i>{e(ct["county"])}</p><h1>Video production in {e(nwa)}</h1>
<p class="lede">Commercials, brand films, product launches, events and social content for {e(n)} businesses, from a Seattle team {e(ct["route"]) if ct["slug"]!="seattle" else "that calls this city home"}.</p>
<div class="ctas"><a class="btn" href="/#contact">START A PROJECT IN {e(n.upper())} →</a><a class="btn ghost" href="/work">SEE THE WORK</a></div>
<div class="hero-media"><img src="/{e(img)}" alt="{e(("A Reelclip shoot in " + n) if biz_here else "A still from a Reelclip production")}" width="1600" height="900" fetchpriority="high"></div></div>
<section class="grid g2"><div style="display:flex;flex-direction:column;gap:16px"><h2>Video for {e(n)} businesses</h2><p class="muted">{e(ct["angle"])}</p>
<p class="muted">{e(TIER_TEXT[ct["tier"]].format(n=n))}</p>{did}</div>
<div class="card"><h3>{e(n)} industries we work with</h3><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in ct["biz"])}</ul></div></section>
<section><div class="section-head"><h2>What we make in {e(n)}</h2><a class="btn ghost" href="/services">ALL SERVICES</a></div><div class="grid g3">{svc}</div></section>
<section><div class="section-head"><h2>Industries we serve in {e(n)}</h2><a class="btn ghost" href="/industries">ALL INDUSTRIES</a></div><div class="chips">{"".join(f'<a href="/industries/{NICHE[x]["slug"]}">{e(x)} video</a>' for x in city_niches(ct, 12))}</div></section>
<section><div class="card"><h3>Why {e(n)} brands hire Reelclip</h3><ul class="ticks c2"><li>Commercial polish with a creative point of view</li><li>One team from concept to final delivery</li><li>Crew sized to your budget and timeline</li><li>Vertical and horizontal versions planned from day one</li><li>Fast turnaround for events and launches</li><li>We film wherever your story lives: your space or a location you choose</li></ul></div></section>
<section><div class="section-head"><h2>{"Work from " + e(n) if biz_here else ("Work near " + e(n) if ct["county"] in REGION_WORK else "Recent work")}</h2><a class="btn ghost" href="/work">ALL WORK</a></div>{work_cards(ws)}</section>
<section><div class="section-head"><h2>{e(n)} video production questions</h2></div>{faq_html(faqs)}</section>
{PATHS}
<section><p class="mono" style="color:var(--soft);margin-bottom:12px">NEARBY AREAS</p><div class="chips">{near}<a href="/locations">All areas →</a></div></section>
{cta_band(f"Planning a shoot in {n}?", "Tell us what you're making and when. We'll come back with a plan and a quote.")}'''
        write('/locations/' + ct['slug'] + '/', head(title, desc, '/locations/' + ct['slug'], img, schema) + body + foot(), '0.7' if ct['tier'] != 'home' else '0.8')

# what each service means for a city's local industries (used to make city x service pages specific)
SVC_BRIDGE = {
  "commercial-video-production": "For {n}'s {b0} and {b1}, that usually means a hero spot plus cutdowns for paid social, YouTube and your website, planned so every version looks intentional.",
  "brand-films": "For {b0} and {b1} in {n}, a brand film is the piece that explains who you are on your homepage, in pitches and in hiring, and keeps working for years.",
  "product-video-production": "For {n} {b0} and {b1}, we plan launch films, teasers and product-page loops together so the whole launch looks consistent.",
  "event-videography": "From {b0} to {b1}, {n} events get a shot list, clean interview audio and recaps delivered while people are still talking about it.",
  "social-media-video": "For {b0} and {b1} in {n}, we batch-shoot vertical content so one production day turns into weeks of posts.",
  "corporate-video-production": "For {n}'s {b0} and {b1}, we make recruiting, training and leadership video that doesn't feel corporate.",
}

def build_city_services():
    for ct in CITIES:
        n = ct['name']; nwa = n if ',' in n else n + ', WA'
        b = [x.lower() for x in ct['biz']]
        here = [k for k, m in WORK_SEO.items() if ct['slug'] in m['cities']]
        for sl in SVC_LINES:
            sv = SVC[sl]
            path = f"/locations/{ct['slug']}/{sl}"
            c, cs = crumbs([("Home", "/"), ("Locations", "/locations"), (n, "/locations/" + ct['slug']), (sv['name'], None)])
            pool = [k for k in sv['work'] if k in WORK]
            ws = [k for k in pool if k in here] + [k for k in pool if k not in here]
            ws = ws[:3]
            img = WORK[ws[0]]['img'] if ws else HERO_POOL[0]
            alt_img = WORK[pool[sum(map(ord, ct['slug'])) % len(pool)]]['img'] if pool else HERO_POOL[0]
            a1 = angle(pool[sum(map(ord, ct['slug'])) % len(pool)], [sl]) if pool else None
            if a1: alt_img = a1[0]
            if ws and WORK[ws[0]]['img'] in [WORK[k]['img'] for k in here] and len(ws) > 1: pass
            title = f"{sv['name']} in {nwa} | Reelclip"
            desc = f"{sv['name']} in {nwa}. " + SVC_LINES[sl].format(n=n) + " From Seattle's Reelclip."
            if len(desc) > 160: desc = f"{sv['name']} in {nwa}: " + SVC_LINES[sl].format(n=n)
            other = ''.join(f'<a href="/locations/{ct["slug"]}/{o}">{e(SVC[o]["name"])} in {e(n)}</a>' for o in SVC_LINES if o != sl)
            near = ''.join(f'<a href="/locations/{x["slug"]}/{sl}">{e(sv["name"])} in {e(x["name"])}</a>' for x in nearby(ct))
            faqs = [(f"Do you offer {sv['name'].lower()} in {n}?", TIER_TEXT[ct['tier']].format(n=n) + f" We bring the full {sv['name'].lower()} process to {n}: planning, crew, filming, editing and delivery."),
                    sv['faqs'][0], sv['faqs'][1] if len(sv['faqs']) > 1 else sv['faqs'][0],
                    (f"Can you film at our location in {n}?", f"Yes. We film at your office, store, venue or site in {n}, or anywhere else you choose for the story.")]
            steps = ''.join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in sv['steps'])
            did = (f'<p class="muted">Work we\'ve filmed in {e(n)}: ' + ', '.join(f'<a href="{wurl(k)}">{e(wname(WORK[k]))}</a>' for k in here) + '.</p>') if here else ''
            schema = [cs, faq_schema(faqs), {"@context": "https://schema.org", "@type": "Service", "name": f"{sv['name']} in {nwa}", "serviceType": sv['name'],
                      "description": desc, "provider": {"@id": SITE + "/#org", "@type": "ProfessionalService", "name": "Reelclip", "url": SITE + "/"},
                      "areaServed": {"@type": "City", "name": nwa}, "url": SITE + path}]
            body = f"""{c}<div class="hero"><p class="eyebrow"><i></i>{e(sv["short"])} · {e(ct["county"])}</p><h1>{e(sv["name"])} in {e(nwa)}</h1>
<p class="lede">{e(SVC_LINES[sl].format(n=n))} {e(sv["lede"])}</p>
<div class="ctas"><a class="btn" href="/#contact">START A PROJECT IN {e(n.upper())} →</a><a class="btn ghost" href="/services/{sl}">ABOUT {e(sv["short"].upper())}</a></div>
<div class="hero-media"><img src="/{e(img if here else alt_img)}" alt="{e(sv["name"])} by Reelclip" width="1600" height="900" fetchpriority="high"></div></div>
<section class="grid g2"><div style="display:flex;flex-direction:column;gap:16px"><h2>{e(sv["name"])} for {e(n)} businesses</h2>
<p class="muted">{e(SVC_BRIDGE[sl].format(n=n, b0=b[0], b1=b[1]))}</p><p class="muted">{e(ct["angle"])}</p><p class="muted">{e(sv["intro"][0])}</p>{did}</div>
<div class="card"><h3>What's included</h3><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in sv["includes"])}</ul></div></section>
<section><div class="section-head"><h2>How it works in {e(n)}</h2></div><ol class="steps">{steps}</ol></section>
<section class="grid g2"><div class="card"><h3>Typical deliverables</h3><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in sv["deliverables"])}</ul></div>
<div class="card"><h3>{e(n)} businesses we make this for</h3><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in ct["biz"])}</ul></div></section>
<section><p class="mono" style="color:var(--soft);margin-bottom:12px">{e(sv["name"].upper())} FOR {e(n.upper())} INDUSTRIES</p><div class="chips">{"".join(f'<a href="/industries/{NICHE[x]["slug"]}">{e(x)}</a>' for x in city_niches(ct, 8))}</div></section>
<section><div class="section-head"><h2>{e(sv["name"])} examples</h2><a class="btn ghost" href="/work">ALL WORK</a></div>{work_cards(ws, ctx=[sl])}</section>
<section><div class="section-head"><h2>Questions about {e(sv["name"].lower())} in {e(n)}</h2></div>{faq_html(faqs)}</section>
<section><p class="mono" style="color:var(--soft);margin-bottom:12px">MORE IN {e(n.upper())}</p><div class="chips"><a href="/locations/{ct["slug"]}">Video production in {e(n)}</a>{other}</div>
<p class="mono" style="color:var(--soft);margin:22px 0 12px">{e(sv["name"].upper())} NEARBY</p><div class="chips">{near}</div></section>
{cta_band(f"Planning {sv['short'].lower()} in {n}?", "Tell us what you're making and when. We'll come back with a plan and a quote.")}"""
            write(path, head(title, desc, path, img if here else alt_img, schema) + body + foot(), '0.6')

def build_sitemap():
    urls = [('/', '1.0')] + PAGES
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{SITE}{p if p != "/" else "/"}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for p, pr in urls) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(xml)
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /tools/\n\nSitemap: {SITE}/sitemap.xml\n")
    return len(urls)

if __name__ == '__main__':
    build_services(); build_work(); build_industries(); build_locations(); build_city_services(); build_niches()
    n = build_sitemap()
    json.dump(ORG, open(os.path.join(os.path.dirname(__file__), 'org.json'), 'w'), ensure_ascii=False)
    print(f"built {len(PAGES)} pages, sitemap has {n} URLs")
