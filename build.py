#!/usr/bin/env python3
"""Build sajansachdeva.com into docs/ (served by GitHub Pages).

Add an essay: drop a Markdown file in posts/ with a header like

    title: My Essay
    dek: One line under the title.
    date: 2026-10-18
    slug: my-essay
    ---

then run `python3 build.py`, commit and push.
"""
import datetime as dt
import html
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
SITE = "https://sajansachdeva.com"
NAME = "Sajan Sachdeva"
TAGLINE = "Essays on where business and AI actually meet."
LINKEDIN = "https://www.linkedin.com/in/sajansachdeva"

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700'
    '&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400'
    '&display=swap" rel="stylesheet">'
)

THEME_BOOT = """<script>
(function(){try{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);}catch(e){}})();
</script>"""

THEME_TOGGLE = """<script>
(function(){
  var b=document.querySelector('.theme-toggle'); if(!b) return;
  b.addEventListener('click',function(){
    var r=document.documentElement, cur=r.getAttribute('data-theme');
    if(!cur){cur=window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}
    var next=cur==='dark'?'light':'dark'; r.setAttribute('data-theme',next);
    try{localStorage.setItem('theme',next);}catch(e){}
  });
})();
</script>"""

ICON_MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
ICON_SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'


def page(title, description, body, path, current="", og_type="website"):
    full_title = NAME if title == NAME else f"{title} · {NAME}"
    url = SITE + path
    here = ' aria-current="page"'
    nav = "".join(
        f'<a href="{href}"{here if key == current else ""}>{label}</a>'
        for key, href, label in [("writing", "/", "Writing"), ("about", "/about/", "About")]
    )
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{NAME}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#faf9f6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#131416" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{NAME}" href="/feed.xml">
{FONTS}
<link rel="stylesheet" href="/style.css">
{THEME_BOOT}
</head>
<body>
<header class="site-head"><div class="wrap">
  <a class="wordmark" href="/">{NAME}</a>
  <nav class="nav" aria-label="Main">{nav}
    <button class="theme-toggle" type="button" aria-label="Switch light or dark theme">{ICON_MOON}{ICON_SUN}</button>
  </nav>
</div></header>
<main>
{body}
</main>
<footer class="site-foot"><div class="wrap">
  <span>© {dt.date.today().year} {NAME} · London</span>
  <nav aria-label="Elsewhere"><a href="{LINKEDIN}" rel="me">LinkedIn</a><a href="/feed.xml">RSS</a></nav>
</div></footer>
{THEME_TOGGLE}
</body>
</html>
"""


def read_posts():
    posts = []
    for f in sorted((ROOT / "posts").glob("*.md")):
        head, body = f.read_text().split("\n---\n", 1)
        meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
        meta["date"] = dt.date.fromisoformat(meta["date"])
        rendered = markdown.markdown(body, extensions=["smarty"])
        # diagrams open full size on tap (they're small on a phone)
        meta["html"] = re.sub(r'(<img [^>]*src="([^"]+)"[^>]*>)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', rendered)
        meta["minutes"] = max(1, round(len(body.split()) / 230))
        meta["path"] = f"/writing/{meta['slug']}/"
        posts.append(meta)
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def fmt(d):
    return f"{d.day} {d.strftime('%b %Y')}"


def write(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "static", OUT, dirs_exist_ok=True)
    posts = read_posts()

    # home
    items = "".join(
        f'<li><a href="{p["path"]}"><span class="pl-title">{html.escape(p["title"])}</span>'
        f'<span class="pl-date">{fmt(p["date"])}</span>'
        f'<span class="pl-dek">{html.escape(p["dek"])}</span></a></li>'
        for p in posts
    )
    home = f"""<section class="intro"><div class="wrap">
  <h1>I write about where business and AI actually meet.</h1>
  <p>I’m Sajan. I’ve spent nearly ten years inside e-commerce operations at Flipkart and Amazon: category P&amp;Ls, inventory, delivery promises, vendor chargebacks. In 2026 I co-founded FlowPotato, an AI operations co-pilot for product brands.</p>
  <p>These essays are about the daily workflows, not the demos — what AI is actually good for once it meets a real business.</p>
  <p class="small"><a href="/about/">More about me</a> · <a href="{LINKEDIN}" rel="me">LinkedIn</a></p>
</div></section>
<section class="wrap" aria-labelledby="writing">
  <h2 class="section-label" id="writing">Writing</h2>
  <ul class="post-list">{items}</ul>
</section>"""
    write("index.html", page(NAME, TAGLINE, home, "/", "writing"))

    # essays
    for i, p in enumerate(posts):
        older = posts[i + 1] if i + 1 < len(posts) else None
        nxt = (
            f'<div><div class="next-label">Previous essay</div><a class="next" href="{older["path"]}">{html.escape(older["title"])}</a></div>'
            if older else ""
        )
        body = f"""<article class="wrap">
  <header class="post-head">
    <p class="post-meta"><time datetime="{p["date"].isoformat()}">{fmt(p["date"])}</time> · {p["minutes"]} min read</p>
    <h1>{html.escape(p["title"])}</h1>
    <p class="dek">{html.escape(p["dek"])}</p>
  </header>
  <div class="prose">{p["html"]}</div>
  <footer class="post-foot">
    {nxt}
    <div><a href="/">← All writing</a></div>
  </footer>
</article>"""
        write(f"writing/{p['slug']}/index.html", page(p["title"], p["dek"], body, p["path"], "writing", "article"))

    # about
    write("about/index.html", page("About", f"About {NAME}: operator, product manager and founder in London.", ABOUT, "/about/", "about"))

    # 404
    write("404.html", page("Not found", "Page not found.", '<section class="wrap notfound"><h1>Nothing here.</h1><p><a href="/">Back to the writing</a></p></section>', "/404.html"))

    # feed, sitemap, robots, CNAME
    entries = "".join(
        f"""<item><title>{html.escape(p["title"])}</title><link>{SITE}{p["path"]}</link><guid>{SITE}{p["path"]}</guid>
<pubDate>{dt.datetime.combine(p["date"], dt.time(9)).strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>
<description>{html.escape(p["html"])}</description></item>"""
        for p in posts
    )
    write("feed.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>{NAME}</title><link>{SITE}/</link><description>{TAGLINE}</description><language>en-gb</language>
{entries}</channel></rss>
""")
    urls = ["/", "/about/"] + [p["path"] for p in posts]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          + "".join(f"<url><loc>{SITE}{u}</loc></url>" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    write("CNAME", "sajansachdeva.com\n")
    write(".nojekyll", "")
    print(f"Built {len(posts)} essays into {OUT}")


ABOUT = f"""<section class="wrap about">
  <header class="post-head">
    <h1>About</h1>
  </header>
  <div class="prose">
    <p>I’m an operator and product manager based in London. For nearly ten years I’ve worked on the unglamorous machinery of e-commerce: how products get bought, shipped, received and paid for. First at Flipkart in Bangalore, then at Amazon in Bangalore and London.</p>
    <p>At Amazon I’m a Senior Product Manager in Vendor Experience, where I work on sourcing lead times, delivery windows and vendor chargebacks across Europe. In January 2026 I co-founded FlowPotato, an AI operations co-pilot for product brands.</p>
    <p>I write about the space between business and AI: where it earns its keep, where it doesn’t, and what it takes to turn operational judgment into software.</p>
  </div>

  <h2 class="section-label">Work</h2>
  <ul class="cv">
    <li><span class="when">2026 – now</span><span><span class="what">Co-founder &amp; CEO</span> <span class="where">· FlowPotato, London</span></span></li>
    <li><span class="when">2023 – now</span><span><span class="what">Senior Product Manager, Vendor Experience</span> <span class="where">· Amazon, London</span></span><span class="note">Sourcing lead times, delivery windows and vendor chargebacks across the EU.</span></li>
    <li><span class="when">2022 – 2023</span><span><span class="what">Senior Product Manager, Fashion EU</span> <span class="where">· Amazon, London</span></span><span class="note">Pan-EU inventory optimisation, stock availability and delivery promises.</span></li>
    <li><span class="when">2018 – 2022</span><span><span class="what">Category &amp; Program Management, Books and Fashion</span> <span class="where">· Amazon, Bangalore</span></span><span class="note">Category P&amp;Ls, pricing, publisher and brand partnerships.</span></li>
    <li><span class="when">2016 – 2018</span><span><span class="what">Category Manager, Men’s Accessories</span> <span class="where">· Flipkart, Bangalore</span></span><span class="note">End-to-end category P&amp;L.</span></li>
    <li><span class="when">2024</span><span><span class="what">Host</span> <span class="where">· The Desi Expats podcast</span></span><span class="note">Conversations with South Asian expats building careers in the UK.</span></li>
  </ul>

  <h2 class="section-label">Education</h2>
  <ul class="cv">
    <li><span class="when">2014 – 2016</span><span><span class="what">MBA, Strategy &amp; Operations</span> <span class="where">· IIM Bangalore</span></span></li>
    <li><span class="when">2011 – 2014</span><span><span class="what">B.Com (Hons)</span> <span class="where">· Shri Ram College of Commerce, Delhi</span></span></li>
  </ul>

  <h2 class="section-label">Get in touch</h2>
  <div class="prose" style="border:0;padding-top:12px">
    <p>The best way to reach me is a message on <a href="{LINKEDIN}" rel="me">LinkedIn</a>.</p>
  </div>
</section>"""


if __name__ == "__main__":
    build()
