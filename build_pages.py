"""
Prerenders one real HTML page per project, and rebuilds sitemap.xml.

WHY THIS EXISTS
---------------
Every hand-written page in this site is a thin shell: `data-render` slots that
app.js fills from data.js at runtime. That is fine for people and fine for
Googlebot's second, JavaScript-rendering pass -- but project.html carries ZERO
static words, its content is keyed off a `?slug=` query string, and a single
URL cannot be indexed as eleven different projects. The lab's actual research
was therefore invisible to search.

This script writes projects/<slug>.html with the content already in the HTML,
each with its own <title>, meta description and canonical, and lists them all
in sitemap.xml. project.html keeps working for old links but is marked
noindex, so the two URLs never compete for the same content.

RUNNING IT
----------
    python build_pages.py

Needs Windows: data.js is JavaScript, not JSON, so it is evaluated by the
Windows Script Host rather than parsed by hand -- a regex parser would drift
from the file the moment someone adds a nested object. The GENERATED pages are
committed, so deploying never needs this script; only editing data.js does.

Re-run after any change to data.js, then commit the result.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "projects")
REL = "../"          # generated pages sit one level down
TODAY = date.today().isoformat()

# Static pages, with the sitemap priority each one carries today.
STATIC = [
    ("", 1.0), ("research.html", 0.9), ("publications.html", 0.8),
    ("lab.html", 0.8), ("teaching.html", 0.7), ("about.html", 0.7),
    ("collaborate.html", 0.7),
]

# JScript (ES3) shim: evaluates data.js and prints pure-ASCII JSON. Everything
# non-ASCII is emitted as \uXXXX so the Windows console encoding cannot corrupt
# it. JScript 5.8 has no reliable JSON object, hence the hand-rolled writer.
SHIM = r"""
function esc(s) {
  var out = "", i, c, h;
  for (i = 0; i < s.length; i++) {
    c = s.charCodeAt(i);
    if (c === 34) out += '\\"';
    else if (c === 92) out += "\\\\";
    else if (c === 10) out += "\\n";
    else if (c === 13) out += "\\r";
    else if (c === 9) out += "\\t";
    else if (c < 32 || c > 126) {
      h = c.toString(16);
      while (h.length < 4) h = "0" + h;
      out += "\\u" + h;
    } else out += s.charAt(i);
  }
  return out;
}
function str(v) {
  if (v === null || v === undefined) return "null";
  var t = typeof v, parts = [], i, k;
  if (t === "string") return '"' + esc(v) + '"';
  if (t === "number" || t === "boolean") return String(v);
  if (v instanceof Array) {
    for (i = 0; i < v.length; i++) parts.push(str(v[i]));
    return "[" + parts.join(",") + "]";
  }
  for (k in v) if (v.hasOwnProperty(k)) parts.push('"' + esc(k) + '":' + str(v[k]));
  return "{" + parts.join(",") + "}";
}
var st = new ActiveXObject("ADODB.Stream");
st.Type = 2; st.Charset = "utf-8"; st.Open();
st.LoadFromFile(WScript.Arguments(0));
var src = st.ReadText(); st.Close();
var window = {};
eval(src);
var D = window.CMITAD || window.DATA || window.SITE_DATA;
WScript.Echo(str(D));
"""


def load_data():
    """Evaluate data.js and return it as a dict."""
    fd, shim = tempfile.mkstemp(suffix=".js")
    os.close(fd)
    with open(shim, "w", encoding="ascii") as f:
        f.write(SHIM)
    try:
        raw = subprocess.check_output(
            ["cscript", "//Nologo", "//E:JScript", shim,
             os.path.join(HERE, "assets", "js", "data.js")],
            text=True, encoding="ascii", errors="strict")
    finally:
        os.unlink(shim)
    return json.loads(raw)


def esc(t):
    """HTML-escape text. app.js sets textContent, so nothing is ever markup."""
    return (str(t).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def head(D, p, cat):
    site, base = D["site"], D["site"]["url"].rstrip("/")
    canon = f"{base}/projects/{p['slug']}.html"
    hero = next((i.get("poster") or i["src"]
                 for i in p.get("images", []) if i.get("src")), None)
    og = f"{base}/{hero}" if hero else f"{base}/assets/img/logo-cube.png"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(p['title'])} — {esc(site['name'])}</title>
<meta name="description" content="{esc(p['summary'])}">
<link rel="canonical" href="{canon}">
<!-- Rights. `noai`/`noimageai` is the de-facto opt-out signal; `tdm-reservation`
     is the W3C TDM Reservation Protocol, the machine-readable form of the
     Article 4(3) EU DSM reservation asserted in /LICENSE. Search indexing is
     deliberately left ON — /robots.txt names the harvesters, not the engines. -->
<meta name="robots" content="index, follow, max-image-preview:large, noai, noimageai">
<meta name="tdm-reservation" content="1">
<meta name="tdm-policy" content="{base}/LICENSE">
<meta name="copyright" content="© 2026 CM-iTAD Lab, Alfaisal University. All rights reserved.">
<meta name="rights" content="{base}/LICENSE">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{esc(site['name'])}">
<meta property="og:title" content="{esc(p['title'])}">
<meta property="og:description" content="{esc(p['summary'])}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="license" href="{REL}LICENSE">
<link rel="icon" href="{REL}assets/img/logo-cube.png">
<meta name="theme-color" content="#F3F6FA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0E2742" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="{REL}site.webmanifest">
<link rel="apple-touch-icon" href="{REL}assets/img/logo-cube.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&display=swap">
<link rel="stylesheet" href="{REL}assets/css/site.css">
{ldjson(D, p, cat, canon, og)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header" data-render="header"></header>
<main id="main">
"""


def ldjson(D, p, cat, canon, og):
    """Schema.org. Gives Google an explicit author/date rather than a guess."""
    node = {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": p["title"], "description": p["summary"], "url": canon,
        "image": og, "datePublished": str(p["year"]),
        "keywords": ", ".join(p.get("tags", [])) or None,
        "about": cat["label"],
        "author": {"@type": "Organization", "name": D["site"]["name"],
                   "url": D["site"]["url"]},
        "publisher": {"@type": "Organization", "name": D["site"]["name"],
                      "url": D["site"]["url"]},
        "isPartOf": {"@type": "WebSite", "name": D["site"]["name"],
                     "url": D["site"]["url"]},
    }
    node = {k: v for k, v in node.items() if v is not None}
    return ('<script type="application/ld+json">'
            + json.dumps(node, ensure_ascii=False) + "</script>")


def figure(im, p):
    """Mirrors app.js media(): a motion image shows its poster behind a control
    and NEVER autoplays (WCAG 2.2.2). The toggle script is inlined below."""
    alt = esc(im.get("alt") or p["title"])
    cls = "figure" if im.get("fit") == "contain" else "figure figure--cover"
    if im.get("motion") and im.get("poster"):
        inner = (f'<div class="motion">'
                 f'<img src="{REL}{im["poster"]}" alt="{alt}" loading="lazy" '
                 f'data-still="{REL}{im["poster"]}" data-motion="{REL}{im["src"]}">'
                 f'<button class="motion__btn" type="button" aria-pressed="false">'
                 f'<span>Play animation</span></button></div>')
    else:
        inner = f'<img src="{REL}{im["src"]}" alt="{alt}" loading="lazy">'
    cap = f'<figcaption>{esc(im["caption"])}</figcaption>' if im.get("caption") else ""
    return f'<figure class="{cls}" style="margin:0">{inner}{cap}</figure>'


def card(p, cat):
    img = next((i for i in p.get("images", []) if i.get("src")), None)
    media = ""
    if img:
        src = img.get("poster") or img["src"]
        extra = " card__media--contain" if img.get("fit") == "contain" else ""
        media = (f'<div class="card__media{extra}"><img src="{REL}{src}" '
                 f'alt="{esc(img.get("alt") or p["title"])}" loading="lazy"></div>')
    return (f'<a class="card" href="{p["slug"]}.html">{media}'
            f'<div class="card__body"><div class="card__meta">'
            f'<span class="tag">{esc(cat["label"])}</span>'
            f'<span class="tag tag--year">{p["year"]}</span></div>'
            f'<h3 class="card__title">{esc(p["title"])}</h3>'
            f'<p class="card__sum">{esc(p["summary"])}</p>'
            f'<span class="card__more">View project →</span></div></a>')


def build_project(D, p, cats):
    cat = cats.get(p["category"], {"label": p["category"]})
    out = [head(D, p, cat)]

    rows = [("Theme", cat["label"]), ("Year", str(p["year"])), ("Status", p["status"])]
    if p.get("tags"):
        rows.append(("Methods", ", ".join(p["tags"])))
    spec = "".join(f'<div class="spec__row"><span class="spec__k">{esc(k)}</span>'
                   f'<span>{esc(v)}</span></div>' for k, v in rows)

    links = "".join(f'<a class="btn btn--ghost" href="{esc(l["href"])}" target="_blank" '
                    f'rel="noopener">{esc(l["label"])}</a>' for l in p.get("links", []))
    links = f'<div class="btn-row">{links}</div>' if links else ""

    out.append(f"""  <div class="wrap section">
    <p class="breadcrumb"><a href="{REL}research.html">Research</a><span> / {esc(cat['label'])}</span></p>
    <div class="detail__head">
      <div>
        <h1 class="h-display">{esc(p['title'])}</h1>
        <p class="lead" style="margin-top:20px;max-width:62ch">{esc(p['summary'])}</p>
        {links}
      </div>
      <div class="spec">{spec}</div>
    </div>
  </div>
""")

    m = p.get("model")
    if m and m.get("src"):
        cap = f'<figcaption>{esc(m["caption"])}</figcaption>' if m.get("caption") else ""
        poster = f' poster="{REL}{m["poster"]}"' if m.get("poster") else ""
        out.append(f"""  <div class="wrap section--tight">
    <figure class="figure model" style="margin:0"><model-viewer src="{REL}{m['src']}"{poster}
      alt="{esc(m.get('alt') or p['title'])}" camera-controls touch-action="pan-y"
      interaction-prompt="none" shadow-intensity="0.6" environment-image="neutral"
      max-camera-orbit="auto 100deg auto" loading="lazy"></model-viewer>{cap}</figure>
  </div>
""")

    figs = [figure(im, p) for im in p.get("images", []) if im.get("src")]
    if figs:
        grid = "grid--2" if len(figs) > 1 else "grid--1"
        out.append(f'  <div class="wrap section--tight"><div class="grid {grid}">'
                   + "".join(figs) + "</div></div>\n")

    if p.get("body"):
        paras = "".join(f"<p>{esc(t)}</p>" for t in p["body"])
        out.append(f'  <div class="wrap section--tight">'
                   f'<div class="detail__body">{paras}</div></div>\n')

    pub = next((x for x in D["publications"] if x["slug"] == p.get("publicationSlug")), None)
    if pub:
        out.append(f"""  <div class="wrap section--tight"><div class="callout">
    <div class="mono-label" style="margin-bottom:8px">Related publication</div>
    <p>{esc(pub['authors'])} ({pub['year']}). {esc(pub['title'])}. {esc(pub['venue'])}.</p>
  </div></div>
""")

    more = [x for x in D["projects"]
            if x["category"] == p["category"] and x["slug"] != p["slug"]][:3]
    if more:
        out.append(f'  <div class="wrap section"><p class="eyebrow">More in '
                   f'{esc(cat["label"])}</p><div class="grid grid--3">'
                   + "".join(card(x, cats.get(x["category"], cat)) for x in more)
                   + "</div></div>\n")

    out.append(f"""</main>
<footer class="site-footer" data-render="footer"></footer>
<script src="{REL}assets/js/data.js"></script>
<script src="{REL}assets/js/app.js"></script>
""")
    if any(im.get("motion") for im in p.get("images", [])):
        out.append("""<script>
/* Content here is static, so app.js never builds these controls. Same contract
   as media() in app.js: poster by default, animation only on request. */
(function () {
  var bs = document.querySelectorAll(".motion__btn");
  for (var i = 0; i < bs.length; i++) (function (b) {
    var img = b.parentNode.querySelector("img"), label = b.querySelector("span");
    b.addEventListener("click", function () {
      var playing = b.getAttribute("aria-pressed") === "true";
      img.setAttribute("src", playing ? img.getAttribute("data-still")
                                      : img.getAttribute("data-motion"));
      b.setAttribute("aria-pressed", String(!playing));
      label.textContent = playing ? "Play animation" : "Pause animation";
    });
  })(bs[i]);
})();
</script>
""")
    if m and m.get("src"):
        out.append(f'<script type="module" id="cm-model-viewer" '
                   f'src="{REL}assets/js/vendor/model-viewer.min.js"></script>\n')
    out.append("</body>\n</html>\n")
    return "".join(out)


def build_sitemap(D, slugs):
    base = D["site"]["url"].rstrip("/")
    urls = [(f"{base}/{path}", pri) for path, pri in STATIC]
    urls += [(f"{base}/projects/{s}.html", 0.8) for s in slugs]
    body = "".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
        f"    <priority>{pri}</priority>\n  </url>\n" for u, pri in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + body + "</urlset>\n")


def main():
    D = load_data()
    cats = {c["id"]: c for c in D["categories"]}
    os.makedirs(OUT_DIR, exist_ok=True)

    slugs = [p["slug"] for p in D["projects"]]
    written = []
    for p in D["projects"]:
        path = os.path.join(OUT_DIR, p["slug"] + ".html")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(build_project(D, p, cats))
        written.append(p["slug"])
        print(f"  projects/{p['slug']}.html  {os.path.getsize(path):,d}B")

    # Remove pages for projects that no longer exist, so the sitemap and the
    # directory cannot drift apart.
    for f in os.listdir(OUT_DIR):
        if f.endswith(".html") and f[:-5] not in slugs:
            os.unlink(os.path.join(OUT_DIR, f))
            print(f"  removed stale projects/{f}")

    sm = os.path.join(HERE, "sitemap.xml")
    with open(sm, "w", encoding="utf-8", newline="\n") as f:
        f.write(build_sitemap(D, slugs))
    print(f"\n  sitemap.xml  {len(STATIC)} static + {len(slugs)} project URLs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
