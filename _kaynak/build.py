# -*- coding: utf-8 -*-
"""Lockout Turkey statik site üreticisi.  Kullanım: python3 build.py  →  ../site/"""
import json, os, shutil, html, re
from datetime import date
from data import SITE, CATEGORIES, POINTS, COLORS, SECTORS, STEPS, FAQ, REFS, FOOTER_TEXT
from blog import POSTS
import re
CATALOG_PDF = "lockout-turkey-katalog.pdf"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "site")
IMG_DIR = os.path.join(OUT, "img", "urunler")   # ürün fotoğrafları: img/urunler/<urun-id>.webp
e = html.escape

# ---------------------------------------------------------------- ikonlar
def svg(inner, w=3):
    return ('<svg viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (w, inner))

ICONS = {
    "padlock": svg('<path d="M42 54V40a18 18 0 0 1 36 0v14"/><rect x="30" y="54" width="60" height="48" rx="9"/><circle cx="60" cy="74" r="5"/><path d="M60 79v10"/>'),
    "breaker": svg('<rect x="32" y="14" width="56" height="92" rx="7"/><rect x="46" y="38" width="28" height="44" rx="4"/><rect x="51" y="43" width="18" height="16" rx="2"/><circle cx="45" cy="25" r="3"/><circle cx="75" cy="25" r="3"/><circle cx="45" cy="95" r="3"/><circle cx="75" cy="95" r="3"/>'),
    "valve": svg('<path d="M8 70h26M86 70h26"/><path d="M8 60v20M112 60v20"/><rect x="34" y="54" width="52" height="34" rx="7"/><path d="M60 54V40"/><path d="M60 40l40-10" stroke-width="7"/><circle cx="60" cy="71" r="7"/>'),
    "cable": svg('<path d="M28 86C10 60 22 26 52 22s52 14 46 44-26 30-38 22"/><rect x="40" y="78" width="30" height="26" rx="5"/><path d="M47 78v-6a8 8 0 0 1 16 0v6"/><circle cx="55" cy="91" r="3"/>'),
    "hasp": svg('<path d="M40 62V40a20 20 0 0 1 40 0v22"/><rect x="24" y="60" width="72" height="44" rx="7"/><circle cx="42" cy="76" r="5"/><circle cx="60" cy="76" r="5"/><circle cx="78" cy="76" r="5"/><circle cx="42" cy="92" r="5"/><circle cx="60" cy="92" r="5"/><circle cx="78" cy="92" r="5"/>'),
    "plug": svg('<rect x="24" y="18" width="72" height="62" rx="12" stroke-dasharray="6 6"/><rect x="40" y="34" width="40" height="34" rx="7"/><path d="M52 34V22M68 34V22"/><path d="M60 68v40"/>'),
    "tag": svg('<path d="M42 12h36l10 10v86H32V22z"/><circle cx="60" cy="30" r="6"/><path d="M44 52h32M44 64h32M44 76h22M44 90h28"/>'),
    "station": svg('<rect x="14" y="12" width="92" height="96" rx="7"/><path d="M26 38V32a6 6 0 0 1 12 0v6M54 38V32a6 6 0 0 1 12 0v6M82 38V32a6 6 0 0 1 12 0v6"/><rect x="22" y="38" width="20" height="16" rx="3"/><rect x="50" y="38" width="20" height="16" rx="3"/><rect x="78" y="38" width="20" height="16" rx="3"/><path d="M28 70h16v26H28zM52 70h16v26H52zM76 70h16v26H76z"/>'),
    "box": svg('<rect x="20" y="40" width="80" height="62" rx="7"/><path d="M20 58h80"/><path d="M46 40v-9h28v9"/><circle cx="36" cy="80" r="5"/><circle cx="52" cy="80" r="5"/><circle cx="68" cy="80" r="5"/><circle cx="84" cy="80" r="5"/>'),
    "kit": svg('<rect x="16" y="40" width="88" height="62" rx="9"/><path d="M44 40V30a6 6 0 0 1 6-6h20a6 6 0 0 1 6 6v10"/><rect x="48" y="66" width="24" height="20" rx="4"/><path d="M53 66v-5a7 7 0 0 1 14 0v5"/>'),
}
LOCK_SM = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/><path d="M12 15v2"/></svg>'
LOGO_SVG = '<svg class="wm-o" viewBox="0 0 72 108" aria-hidden="true"><path class="wm-sh" d="M18 34 V24 a18 18 0 0 1 36 0 V34"/><rect class="wm-body" x="2" y="31" width="68" height="77" rx="12"/><circle class="wm-kh" cx="36" cy="62" r="7"/><rect class="wm-kh" x="33" y="64" width="6" height="18" rx="2"/></svg>'
LOGO = '<span class="wm"><span class="wm-top">LOCK' + LOGO_SVG + 'UT</span><span class="wm-bot"><i></i><span>TURKEY</span><i></i></span></span>'
WA_ICON = '<svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.4.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2l-.5-.3z"/></svg>'
SEARCH_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
INFO_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F2B8B5" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 8v5"/><path d="M12 16.5v.01"/></svg>'

# ---------------------------------------------------------------- veri indeksleri
CAT = {c["slug"]: c for c in CATEGORIES}
for c in CATEGORIES: c["items"] = []
PROD, CODE = {}, {}
for p in json.load(open(os.path.join(HERE, "catalog.json"), encoding="utf-8")):
    p["url"] = p["id"] + ".html"
    p["icon"] = CAT[p["cat"]]["icon"]
    p["desc"] = p["short"]
    PROD[p["id"]] = p
    CODE[p["code"]] = p["id"]
    CAT[p["cat"]]["items"].append(p)
def _nat(p): return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", p["code"])]
for c in CATEGORIES: c["items"].sort(key=_nat)
def pid(ref):
    """Ürün kodunu (LT-...) ya da ürün kimliğini ürün kimliğine çevirir."""
    return CODE.get(ref, ref)
for pt in POINTS: pt["products"] = [pid(r) for r in pt["products"]]
REF_IDS = {k: pid(v) for k, v in REFS.items()}
COLOR_HEX = {c[0]: c[1] for c in COLORS}
GROUPS = {}
for p in PROD.values():
    if p["group"]: GROUPS.setdefault((p["cat"], p["group"]), []).append(p)

def cat_url(slug): return slug + ".html"

def p_image(p, k=0, lazy=True):
    imgs = [i for i in p["images"] if os.path.exists(os.path.join(IMG_DIR, i))]
    if len(imgs) > k:
        return '<img src="img/urunler/%s" alt="%s"%s width="800" height="800">' % (imgs[k], e(p["name"]), ' loading="lazy"' if lazy else '')
    return ICONS[p["icon"]]
def p_imgs(p):
    return [i for i in p["images"] if os.path.exists(os.path.join(IMG_DIR, i))]

def wa_href(text=""):
    num = "".join(ch for ch in SITE["whatsapp_num"] if ch.isdigit())
    from urllib.parse import quote
    return "https://wa.me/%s%s" % (num, ("?text=" + quote(text)) if text else "")

def tel_href():
    return "tel:" + SITE["phone_tel"] if SITE["phone_tel"] else "iletisim.html"

# ---------------------------------------------------------------- iskelet
NAV = [("urunler.html", "Ürünler"), ("./#nokta", "Nokta seçici"), ("set-olusturucu.html", "Set oluşturucu"),
       ("sektorler.html", "Sektörler"), ("loto-rehberi.html", "LOTO rehberi"), ("blog.html", "Blog"), ("kurumsal.html", "Kurumsal"),
       ("iletisim.html", "İletişim")]

def header(active):
    sub = "".join('<a href="%s">%s<span>%d</span></a>' % (cat_url(c["slug"]), e(c["name"]), len(c["items"])) for c in CATEGORIES)
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        if href == "urunler.html":
            items.append('<div class="has-sub"><a href="urunler.html"%s>Ürünler <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></a><div class="sub">%s<a href="urunler.html"><b>Tüm ürünler</b><span>%d</span></a></div></div>' % (cur, sub, len(PROD)))
        else:
            items.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    return f'''<div class="topbar"><div class="wrap">
<span class="mono">EKED / LOTO · Kilitleme ve Etiketleme Ekipmanları</span>
<div class="contacts"><a href="{tel_href()}">{e(SITE["phone"])}</a><a href="{wa_href()}" target="_blank" rel="noopener">WhatsApp: {e(SITE["whatsapp"])}</a><span>{e(SITE["email"])}</span></div>
</div></div>
<header class="header"><div class="wrap">
<a class="logo" href="./" aria-label="{e(SITE["brand"])} ana sayfa">{LOGO}</a>
<nav class="nav" aria-label="Ana menü">{"".join(items)}</nav>
<div class="header-actions">
<a class="cart-btn" href="teklif.html"><span class="cart-label">Teklif listesi</span><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" class="cart-ico"><path d="M9 5h11M9 12h11M9 19h11M4 5h.01M4 12h.01M4 19h.01"/></svg><span class="cart-count" data-cart-count>0</span><span class="sr-only">ürün</span></a>
<button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Menüyü aç"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
</div></div></header>'''

def footer():
    cats = "".join('<a href="%s">%s</a>' % (cat_url(c["slug"]), e(c["name"])) for c in CATEGORIES[:6])
    return f'''<footer class="footer"><div class="wrap">
<div class="about"><a class="logo" href="./">{LOGO}</a>
<p>{e(FOOTER_TEXT)}</p>{('<span>%s</span>' % e(SITE["address"])) if SITE["address"] else ''}</div>
<div class="col"><span class="mono">ÜRÜNLER</span>{cats}<a href="urunler.html">Tüm ürünler →</a></div>
<div class="col"><span class="mono">ARAÇLAR</span><a href="./#nokta">Nokta seçici</a><a href="set-olusturucu.html">Set oluşturucu</a><a href="teklif.html">Teklif listesi</a><a href="loto-rehberi.html">LOTO rehberi</a><a href="blog.html">Blog</a><a href="sektorler.html">Sektörler</a><a href="{CATALOG_PDF}" target="_blank" rel="noopener">Ürün kataloğu (PDF)</a></div>
<div class="col"><span class="mono">İLETİŞİM</span><a href="{tel_href()}">{e(SITE["phone"])}</a><a href="{wa_href()}" target="_blank" rel="noopener">WhatsApp: {e(SITE["whatsapp"])}</a><span>{e(SITE["email"])}</span><a href="kurumsal.html">Kurumsal</a></div>
</div>
<div class="wrap bottom"><span>© {date.today().year} {e(SITE["brand"])}. Tüm hakları saklıdır.</span><span><a href="kvkk.html">KVKK ve gizlilik</a></span></div>
</footer>
<a class="wa-float" href="{wa_href("Merhaba, LOTO ürünleri hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener" aria-label="WhatsApp ile yazın">{WA_ICON}</a>'''

def page(fname, title, desc, body, active=""):
    canonical = SITE["domain"] + ("/" if fname == "index.html" else "/" + fname)
    full_title = title if fname == "index.html" else "%s | %s" % (title, SITE["brand"])
    doc = f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="{e(SITE["brand"])}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta name="theme-color" content="#C8102E">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,800..900&amp;family=Barlow+Condensed:ital,wght@0,500;0,600;0,700;0,800;1,700&amp;family=Barlow:wght@400;500;600;700&amp;family=IBM+Plex+Mono:wght@400;500;600&amp;display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body>
{header(active)}
<main id="icerik">
{body}
</main>
{footer()}
<script src="data.js"></script>
<script src="app.js"></script>
</body>
</html>
'''
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(doc)
    PAGES.append(fname)

PAGES = []

# ---------------------------------------------------------------- bileşenler
def crumbs(*items):
    parts = ['<a href="./">Ana sayfa</a>']
    for href, label in items:
        parts.append('<span aria-hidden="true">/</span>')
        parts.append('<a href="%s">%s</a>' % (href, e(label)) if href else '<span>%s</span>' % e(label))
    return '<nav class="crumbs wrap" aria-label="Sayfa yolu">%s</nav>' % "".join(parts)

def product_card(p, show_cat=True):
    cat = CAT[p["cat"]]["name"]
    text = " ".join([p["name"], p["code"], p["desc"], cat, p["color"]])
    return f'''<article class="p-card" data-card data-cat="{p["cat"]}" data-text="{e(text)}">
<div class="p-img">{p_image(p)}</div>
<div class="p-body">{'<span class="p-cat">%s</span>' % e(cat) if show_cat else ''}
<h3><a href="{p["url"]}">{e(p["name"])}</a></h3><p>{e(p["desc"])}</p>
<div class="p-actions"><button class="btn btn-dark" type="button" data-add="{p["id"]}">+ Teklif listesi</button></div></div>
</article>'''

def cat_card(c):
    return f'''<a class="cat-card" href="{cat_url(c["slug"])}"><span class="ic">{ICONS[c["icon"]]}</span>
<h3>{e(c["name"])}</h3><p>{e(c["short"])}</p><span class="meta">Ürünleri gör →<span>{len(c["items"])} ürün</span></span></a>'''

def cta_block():
    return f'''<section class="wrap" style="padding-block: 72px"><div class="cta">
<div><span class="mono">SAHA KEŞFİ</span><h2 class="h2">Panolarınızı, vanalarınızı birlikte gezelim.</h2>
<p>Tesisinizdeki kilitleme noktalarını çıkarıp nokta başına ekipman listesini hazırlayalım. Uygulamalı personel eğitimi de planlanabilir.</p></div>
<div class="cta-actions"><a class="btn btn-white" href="iletisim.html">Keşif talep et</a><a class="btn btn-outline-white" href="{wa_href("Merhaba, saha keşfi talep etmek istiyorum.")}" target="_blank" rel="noopener">WhatsApp’tan yaz</a></div>
</div></section>'''

def finder_block():
    zones = '''<div class="zone" style="left:2.5%;top:7%;width:21%;height:86%"></div>
<div class="zone" style="left:26%;top:7%;width:29%;height:86%"></div>
<div class="zone" style="left:57.5%;top:7%;width:40%;height:86%"></div>
<span class="zone-label" style="left:4%;top:9.5%">Elektrik odası</span>
<span class="zone-label" style="left:27.5%;top:9.5%">Üretim hattı</span>
<span class="zone-label" style="left:59%;top:9.5%">Proses · tesisat</span>
<div class="wire" style="left:13%;top:30%;width:31%;height:2px"></div>
<div class="wire" style="left:13%;top:30%;width:2px;height:40%"></div>
<div class="wire" style="left:13%;top:70%;width:18%;height:2px"></div>
<div class="pipe" style="left:62%;top:24%;width:30%;height:6px"></div>
<div class="pipe" style="left:82%;top:24%;width:6px;height:54%"></div>
<div class="pipe" style="left:66%;top:75%;width:22%;height:6px"></div>
<div class="air" style="left:70%;top:60%;width:22%"></div>
<div class="machine" style="left:32%;top:44%;width:18%;height:18%"></div>
<span class="zone-label" style="left:33.5%;top:57%;font-size:10px">Pres · hat 2</span>'''
    hots = "".join('<button type="button" class="hot" data-point="%s" aria-pressed="%s" style="left:%d%%;top:%d%%"><span class="num">%s</span><span class="lbl">%s</span><span class="sr-only"> noktasını göster</span></button>'
                   % (p["id"], "true" if i == 0 else "false", p["x"], p["y"], p["no"], e(p["name"])) for i, p in enumerate(POINTS))
    p0 = POINTS[0]
    items = "".join('<a class="panel-item" href="%s"><span class="thumb">%s</span><span><b>%s</b><small>%s</small></span></a>' % (PROD[i]["url"], p_image(PROD[i]), e(PROD[i]["name"]), e(PROD[i]["code"] + " · " + CAT[PROD[i]["cat"]]["name"])) for i in p0["products"])
    return f'''<div class="finder">
<div class="kroki" id="kroki" role="group" aria-label="Tesis krokisi: kilitleme noktaları">{zones}{hots}
<div class="legend"><span><i style="width:16px;height:2px;background:var(--ink);opacity:.4"></i>Elektrik</span><span><i style="width:16px;height:5px;border-radius:3px;background:var(--pipe)"></i>Akışkan hattı</span><span><i style="width:16px;border-top:3px dotted var(--faint)"></i>Basınçlı hava</span></div>
</div>
<aside class="panel" id="nokta-panel" aria-live="polite">
<div class="panel-top"><span class="mono" data-f="meta">Nokta {p0["no"]} · {e(p0["zone"])}</span><span class="pill" data-f="energy">{e(p0["energy"])}</span></div>
<h2 data-f="name">{e(p0["name"])}</h2>
<div class="panel-list"><span class="panel-label">BU NOKTAYA UYAN EKİPMANLAR</span><div class="panel-list" data-f="list">{items}</div></div>
<div class="panel-tip">{INFO_ICON}<span data-f="tip">{e(p0["tip"])}</span></div>
<div class="panel-actions"><button type="button" class="btn btn-red" data-f="add">Hepsini teklif listesine ekle</button><a class="btn btn-ghost-dark" href="urunler.html">Tüm ürünler</a></div>
</aside></div>'''

def builder_block(heading_tag="h2"):
    return f'''<div class="builder" id="kit">
<div class="builder-q">
<div class="q-card"><div class="q-title"><span class="mono">1</span>Aynı anda kaç kişi bakım yapıyor?</div>
<div class="stepper stepper--big"><button type="button" data-w="-1" aria-label="Çalışan sayısını azalt">−</button><output data-k="workers" aria-live="polite">4</output><button type="button" data-w="1" aria-label="Çalışan sayısını arttır">+</button><span class="muted" style="margin-left:8px">çalışan</span></div></div>
<div class="q-card"><div class="q-title"><span class="mono">2</span>Hangi noktalardan kaç tane kilitlenecek?</div><div class="energy-rows" data-k="energy"></div></div>
<div class="q-card"><div class="q-title"><span class="mono">3</span>Anahtar sistemi</div>
<div class="seg" role="group" aria-label="Anahtar sistemi"><button type="button" data-key="farkli" aria-pressed="true">Farklı anahtar</button><button type="button" data-key="ayni" aria-pressed="false">Aynı anahtar</button><button type="button" data-key="master" aria-pressed="false">Master anahtar</button></div>
<p class="muted" style="font-size:14px" data-k="keynote"></p></div>
</div>
<div class="builder-out">
<div class="out-head"><b>Önerilen set</b><span class="mono" data-k="summary"></span></div>
<div data-k="list" aria-live="polite"></div>
<div class="out-foot"><span>Adetler ön öneridir, sahada netleştirilir. <span data-k="keyinfo"></span></span><button type="button" class="btn btn-red" data-kit-add>Seti teklif listesine ekle</button></div>
</div></div>'''

def colors_block():
    cards = "".join('<div class="lock-card"><div class="lock-shape"><i></i><u style="background:%s;border-color:%s"></u></div><b>%s</b><small>%s</small></div>'
                    % (hx, "#CFC4BA" if hx == "#FFFFFF" else hx, e(n), e(r)) for n, hx, r in COLORS)
    return f'''<section class="section section--paper"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Renk kodlama</span><h2 class="h2">Kilidin rengi, kimin çalıştığını söyler.</h2></div>
<p>Emniyet asma kilitlerini departman, ekip ya da yüklenici bazında renklendirin. Aşağıdaki dağılım bir örnektir; renk planı tesisinize göre birlikte belirlenir.</p></div>
<div class="locks">{cards}</div></div></section>'''

def faq_block(items, title="LOTO hakkında merak edilenler"):
    dets = "".join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in items)
    return f'''<section class="section"><div class="wrap faq">
<div><span class="eyebrow">Sık sorulanlar</span><h2 class="h2">{e(title)}</h2><p class="muted">Cevabı bulamazsanız WhatsApp’tan yazın; ürün fotoğrafı göndermeniz yeterli.</p><a class="btn btn-line" href="iletisim.html" style="align-self:flex-start">Bize ulaşın</a></div>
<div class="faq-list">{dets}</div></div></section>'''

def steps_block():
    st = "".join('<div class="step"><span class="mono">%02d</span><b>%s</b><p>%s</p></div>' % (i + 1, e(t), e(d)) for i, (t, d) in enumerate(STEPS))
    return st

def sector_cards():
    return "".join(f'''<a class="sector-card" href="sektorler.html#{s["id"]}"><h3>{e(s["name"])}</h3>
<div class="tags">{"".join("<span>%s</span>" % e(t) for t in s["tags"])}</div><span class="go">Önerilen ekipmanlar →</span></a>''' for s in SECTORS)

# ---------------------------------------------------------------- sayfalar
def build_index():
    body = f'''<section class="hero wrap" id="nokta">
<div class="hero-top"><div><span class="eyebrow">Tesisinizdeki her enerji noktası için</span>
<h1 class="h1">Kilitleyeceğin noktayı seç.<br><em>Doğru kilidi biz söyleyelim.</em></h1></div>
<p>Kategori listelerinde kaybolmayın. Tesis krokisinde bakım yapacağınız noktaya tıklayın; o noktaya uyan kilitleme ekipmanlarını ve uygulama notunu görün.</p></div>
{finder_block()}
</section>
<section class="wrap" style="padding-block: 8px 64px"><div class="trust">
<div><b>OSHA</b>29 CFR 1910.147 prosedürlerine uygun ekipman</div>
<div><b>6331</b>İSG Kanunu kapsamında uygulama desteği</div>
<div><b>FOTO</b>Şalterin fotoğrafını gönderin, uyan kilidi bulalım</div>
<div><b>ÖZEL</b>İsim, numara ve renk baskılı kilitler</div></div></section>
<section class="section section--paper"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Ürün grupları</span><h2 class="h2">Her enerji kaynağı için kilit.</h2></div>
<p>Elektrik panosundan vanaya, fişten basınçlı hava hattına kadar {len(PROD)} ürün, {len(CATEGORIES)} grupta.</p></div>
<div class="cat-grid">{"".join(cat_card(c) for c in CATEGORIES)}</div></div></section>
<section class="section" id="set"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Set oluşturucu</span><h2 class="h2">Üç soruyu yanıtlayın, LOTO setiniz hazır.</h2></div>
<p>Çalışan ve nokta sayısına göre kaç kilit, etiket ve cihaz gerektiğini hesaplayın; listeyi tek tuşla teklif listesine ekleyin.</p></div>
{builder_block()}</div></section>
{colors_block()}
<section class="section"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Sektörler</span><h2 class="h2">Her tesisin riskli noktası farklı.</h2></div><a class="link-arrow" href="sektorler.html">Tüm sektörler →</a></div>
<div class="sector-grid">{sector_cards()}</div></div></section>
<section class="section section--paper"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">LOTO prosedürü</span><h2 class="h2">Ekipman, doğru sırayla kullanılınca işe yarar.</h2></div><a class="link-arrow" href="loto-rehberi.html">Rehberin tamamı →</a></div>
<div class="steps">{steps_block()}</div></div></section>
{blog_block()}
{faq_block(FAQ)}
{cta_block()}'''
    page("index.html", "Lockout Turkey | EKED / LOTO Kilitleme ve Etiketleme Ekipmanları",
         "Emniyet asma kilitleri, şalter, vana, kablo ve fiş kilitleri, çoklandırıcılar, LOTO istasyonları ve setleri. Tesis krokisinden kilitleme noktası seçin, doğru ekipmanı bulun.", body, "")

def build_products():
    chips = '<button class="chip" type="button" data-filter="tumu" aria-pressed="true">Tümü</button>' + "".join(
        '<button class="chip" type="button" data-filter="%s" aria-pressed="false">%s</button>' % (c["slug"], e(c["name"])) for c in CATEGORIES)
    cards = "".join(product_card(p) for p in PROD.values())
    body = f'''{crumbs(("", "Ürünler"))}
<section class="wrap page-head"><div><span class="eyebrow">Ürün kataloğu</span><h1 class="h1">Tüm ürünler</h1>
<p class="lead">Ürün adı, kullanım noktası ya da kategoriye göre arayın. Aradığınızı bulamazsanız noktanın fotoğrafını gönderin.</p></div>
<div style="display:flex;flex-wrap:wrap;gap:10px"><a class="btn btn-dark" href="{CATALOG_PDF}" target="_blank" rel="noopener">Kataloğu indir (PDF)</a><a class="btn btn-line" href="./#nokta">Krokiden nokta seç</a></div></section>
<section class="wrap" style="padding-bottom:72px">
<div class="toolbar"><label class="search" for="urun-ara">{SEARCH_ICON}<span class="sr-only">Ürün ara</span><input id="urun-ara" type="search" placeholder="Örn. vana, sigorta, çoklandırıcı" autocomplete="off"></label><span class="result-count" id="urun-sayi">{len(PROD)} ürün</span></div>
<div class="chips" style="margin-bottom:24px" role="group" aria-label="Kategori filtresi">{chips}</div>
<div class="product-grid">{cards}</div>
<div class="empty" id="urun-bos" hidden><b>Bu aramayla eşleşen ürün yok.</b><p class="muted">Farklı bir kelime deneyin ya da noktanın fotoğrafını WhatsApp’tan gönderin.</p></div>
</section>'''
    page("urunler.html", "Tüm LOTO Ürünleri", "Lockout Turkey EKED / LOTO ürün kataloğu: emniyet asma kilitleri, şalter, vana, kablo, fiş ve pnömatik kilitler, çoklandırıcılar, etiketler, istasyonlar ve setler.", body, "urunler.html")

def build_categories():
    for c in CATEGORIES:
        prods = c["items"]
        others = "".join(cat_card(o) for o in CATEGORIES if o["slug"] != c["slug"])
        body = f'''{crumbs(("urunler.html", "Ürünler"), ("", c["name"]))}
<section class="wrap cat-hero"><span class="ic">{ICONS[c["icon"]]}</span>
<div><span class="eyebrow">{len(prods)} ürün</span><h1 class="h1" style="font-size:clamp(34px,4.4vw,58px)">{e(c["name"])}</h1>
<p class="lead">{e(c["intro"])}</p><div class="tags">{"".join("<span>%s</span>" % e(u) for u in c["uses"])}</div></div></section>
<section class="wrap" style="padding-bottom:48px"><div class="product-grid">{"".join(product_card(p, False) for p in prods)}</div></section>
<section class="wrap" style="padding-bottom:72px"><div class="photo-band"><div><b>Hangi model uyar, emin değil misiniz?</b><span class="muted">Kilitlenecek noktanın fotoğrafını ve varsa marka/modelini gönderin; uygun ürünü bildirelim.</span></div>
<a class="btn btn-red" href="{wa_href("Merhaba, " + c["name"] + " için ürün seçiminde yardım istiyorum.")}" target="_blank" rel="noopener">Fotoğraf gönder</a></div></section>
<section class="section section--paper"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Diğer gruplar</span><h2 class="h2">Diğer ürün grupları</h2></div></div>
<div class="cat-grid">{others}</div></div></section>'''
        page(cat_url(c["slug"]), c["name"], "%s: %s Lockout Turkey EKED / LOTO ürünleri." % (c["name"], c["short"]), body, "urunler.html")

def build_product_pages():
    for p in PROD.values():
        c = CAT[p["cat"]]
        if p["group"]:
            same = [x for x in c["items"] if x["id"] != p["id"] and x["group"] != p["group"]]
        else:
            same = [x for x in c["items"] if x["id"] != p["id"]]
        related = same[:4]
        points = [pt for pt in POINTS if p["id"] in pt["products"]]
        pt_html = ""
        if points:
            pt_html = '<p class="muted" style="font-size:14px">Krokide: ' + ", ".join('<a href="./#nokta">%s</a>' % e(pt["name"]) for pt in points) + "</p>"
        imgs = p_imgs(p)
        if imgs:
            main = '<div class="p-img gallery-main"><img id="pd-main" src="img/urunler/%s" alt="%s" width="800" height="800"></div>' % (imgs[0], e(p["name"]))
            thumbs = ""
            if len(imgs) > 1:
                thumbs = '<div class="thumbs" role="group" aria-label="Ürün görselleri">' + "".join(
                    '<button type="button" class="thumb-btn" data-img="img/urunler/%s" aria-label="%d. görsel" aria-pressed="%s"><img src="img/urunler/%s" alt="" loading="lazy" width="160" height="160"></button>'
                    % (im, k + 1, "true" if k == 0 else "false", im) for k, im in enumerate(imgs)) + "</div>"
            media = main + thumbs
        else:
            media = '<div class="p-img">%s</div>' % ICONS[p["icon"]]
        swatch = ""
        if p["group"]:
            sibs = sorted(GROUPS[(p["cat"], p["group"])], key=lambda x: x["code"])
            swatch = '<div class="variants"><span class="panel-label" style="color:var(--faint)">RENK SEÇENEKLERİ</span><div class="swatches">' + "".join(
                '<a class="swatch" href="%s" title="%s"%s><i style="background:%s"></i><span>%s</span></a>' % (
                    x["url"], e(x["code"] + " · " + x["color"]), ' aria-current="true"' if x["id"] == p["id"] else "",
                    COLOR_HEX.get(x["color"], "#999"), e(x["color"])) for x in sibs) + "</div></div>"
        feats = "".join("<li><span>%s</span></li>" % ("<b>%s:</b> %s" % (e(k), e(v)) if k else e(v)) for k, v in p["features"])
        intro = "".join('<p class="lead">%s</p>' % e(x) for x in p["intro"][:1])
        rows = [("Ürün kodu", e(p["code"])), ("Kategori", '<a href="%s">%s</a>' % (cat_url(c["slug"]), e(c["name"])))]
        seen = {"model", "ürün kodu"}
        for k, v in p["specs"]:
            if k.lower() in seen: continue
            seen.add(k.lower()); rows.append((e(k), e(v)))
        if p["color"] and "renk" not in seen: rows.append(("Renk", e(p["color"])))
        if p["pack"]: rows.append(("Paket içeriği", "<br>".join(e(x) for x in p["pack"])))
        spec = '<div class="table-scroll"><table class="spec"><tbody>' + "".join('<tr><th scope="row">%s</th><td>%s</td></tr>' % r for r in rows) + "</tbody></table></div>"
        kit = ""
        if p["kit"]:
            kit = '<div class="kit-box"><div class="out-head"><b>Set içeriği</b><span class="mono">%s</span></div>%s</div>' % (
                e(p["total"] or ""), "".join('<div class="kit-row"><span class="qty">%d</span><div><b style="font-size:15px">%s</b></div></div>' % (q, e(n)) for q, n in p["kit"]))
        more = "".join('<p>%s</p>' % e(x) for x in p["intro"][1:2])
        body = f"""{crumbs(("urunler.html", "Ürünler"), (cat_url(c["slug"]), c["name"]), ("", p["code"]))}
<section class="wrap pd">
<div class="pd-media">{media}</div>
<div class="pd-info"><a class="eyebrow" href="{cat_url(c["slug"])}" style="text-decoration:none">{e(c["name"])}</a>
<h1>{e(p["name"])}</h1>{intro}
{swatch}
<ul class="features">{feats}</ul>
<div class="buy"><div class="stepper"><button type="button" data-step="-1" data-target="#qty" aria-label="Adet azalt">−</button><label class="sr-only" for="qty">Adet</label><input id="qty" type="number" min="1" max="999" value="1" inputmode="numeric"><button type="button" data-step="1" data-target="#qty" aria-label="Adet arttır">+</button></div>
<button type="button" class="btn btn-red" data-add="{p["id"]}" data-qty-from="#qty">Teklif listesine ekle</button>
<a class="btn btn-line" href="{wa_href("Merhaba, " + p["name"] + " hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp’tan sor</a></div>
{pt_html}
{kit}
{spec}
{('<div class="prose" style="font-size:15px">' + more + '</div>') if more else ''}
</div></section>
<section class="section section--paper"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Aynı gruptan</span><h2 class="h2">Benzer ürünler</h2></div><a class="link-arrow" href="{cat_url(c["slug"])}">Tüm {e(c["name"].lower())} →</a></div>
<div class="product-grid">{"".join(product_card(r, False) for r in related)}</div></div></section>"""
        page(p["url"], p["name"], "%s. %s" % (p["name"], p["desc"]), body, "urunler.html")

def build_set_page():
    body = f'''{crumbs(("", "Set oluşturucu"))}
<section class="wrap page-head"><div><span class="eyebrow">Set oluşturucu</span><h1 class="h1">LOTO setinizi hesaplayın.</h1>
<p class="lead">Ekipte kaç kişi olduğunu, hangi noktaları kilitleyeceğinizi ve anahtar sistemini seçin. Liste anında güncellenir; tek tuşla teklif listesine ekleyebilirsiniz.</p></div></section>
<section class="wrap" style="padding-bottom:48px">{builder_block()}</section>
<section class="section section--paper"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Hesaplama mantığı</span><h2 class="h2">Liste nasıl oluşuyor?</h2></div></div>
<div class="steps">
<div class="step"><span class="mono">1–3 kişi</span><b>Kişisel kilitleme</b><p>Her çalışan her izolasyon noktasına kendi kilidini takar. Birden fazla kişi varsa her noktaya bir çoklandırıcı eklenir.</p></div>
<div class="step"><span class="mono">4+ kişi</span><b>Grup kilitleme</b><p>Her noktaya aynı anahtarlı bir ortak kilit takılır, anahtarlar grup kutusuna konur ve her çalışan kutuyu kendi kilidiyle kilitler.</p></div>
<div class="step"><span class="mono">Herkes</span><b>Kişisel etiket</b><p>Kilidi kimin taktığı her zaman görülmeli; her çalışana bir kişisel etiket eklenir.</p></div>
<div class="step"><span class="mono">Saklama</span><b>Çanta veya istasyon</b><p>5 kişiye kadar taşınabilir çanta, daha kalabalık ekiplerde duvar tipi istasyon önerilir.</p></div>
</div></div></section>
{cta_block()}'''
    page("set-olusturucu.html", "LOTO Set Oluşturucu", "Çalışan sayısı, kilitleme noktaları ve anahtar sistemine göre LOTO setinizi hesaplayın, teklif listesine ekleyin.", body, "set-olusturucu.html")

def link_for(ref):
    if ref in CAT:
        c = CAT[ref]; return '<a href="%s">%s%s</a>' % (cat_url(ref), ICONS[c["icon"]], e(c["name"]))
    p = PROD[pid(ref)]; return '<a href="%s">%s%s</a>' % (p["url"], ICONS[p["icon"]], e(p["name"]))

def build_sectors():
    blocks = "".join(f'''<div class="sector-block" id="{s["id"]}"><div><span class="eyebrow">Sektör</span><h2 class="h2" style="font-size:clamp(28px,3vw,38px)">{e(s["name"])}</h2>
<div class="tags">{"".join("<span>%s</span>" % e(t) for t in s["tags"])}</div></div>
<div><p class="lead">{e(s["text"])}</p><span class="panel-label" style="color:var(--faint)">ÖNERİLEN EKİPMANLAR</span><div class="rec-list">{"".join(link_for(r) for r in s["cats"])}</div></div></div>''' for s in SECTORS)
    body = f'''{crumbs(("", "Sektörler"))}
<section class="wrap page-head"><div><span class="eyebrow">Sektörler</span><h1 class="h1">Sektörünüze göre kilitleme.</h1>
<p class="lead">Her sektörde enerji kaynakları ve sık yapılan bakım işleri farklıdır. Kendi tesisinize en yakın örneği inceleyin.</p></div></section>
<section class="wrap" style="padding-bottom:48px">{blocks}</section>
{cta_block()}'''
    page("sektorler.html", "Sektörlere Göre LOTO Çözümleri", "Enerji, çimento, gıda, otomotiv, kimya ve lojistik sektörleri için kilitleme noktaları ve önerilen EKED / LOTO ekipmanları.", body, "sektorler.html")

def build_guide():
    steps = "".join('<div class="step"><span class="mono">%02d</span><b>%s</b><p>%s</p></div>' % (i + 1, e(t), e(d)) for i, (t, d) in enumerate(STEPS))
    body = f'''{crumbs(("", "LOTO rehberi"))}
<section class="wrap page-head"><div><span class="eyebrow">LOTO rehberi</span><h1 class="h1">Kilitleme ve etiketleme, adım adım.</h1>
<p class="lead">EKED prosedürünün temel adımları, kilit kuralları ve mevzuat özeti. Tesisinize özel prosedür için saha keşfi talep edebilirsiniz.</p></div></section>
<section class="wrap guide" style="padding-bottom:72px">
<article class="prose">
<h2 id="nedir">EKED / LOTO nedir?</h2>
<p>EKED; Enerji Kesme, Kilitleme, Etiketleme ve Doğrulama adımlarının kısaltmasıdır. Uluslararası literatürde Lockout / Tagout (LOTO) olarak bilinir. Amaç, bakım, onarım, temizlik ya da ayar sırasında makinenin beklenmedik şekilde çalışmasını ve içinde kalan enerjinin açığa çıkmasını önlemektir.</p>
<p>Kilit enerjiyi fiziksel olarak keser; etiket ise kimin, ne zaman ve neden kilitlediğini gösterir. Etiket tek başına kilidin yerini tutmaz.</p>
<h2 id="enerji">Hangi enerjiler kilitlenir?</h2>
<ul><li><b>Elektrik:</b> panolar, şalterler, sigortalar, fişler</li><li><b>Akışkan:</b> su, buhar, gaz ve kimyasal hatlarındaki vanalar</li><li><b>Pnömatik ve hidrolik:</b> basınçlı hava ve yağ hatları</li><li><b>Mekanik:</b> yay gerilimi, yükseltilmiş parçalar, dönen kütleler</li><li><b>Termal:</b> sıcak yüzeyler ve akışkanlar</li></ul>
<h2 id="adimlar">Prosedürün adımları</h2>
</article>
<aside><nav class="toc" aria-label="Rehber içeriği"><span class="panel-label" style="color:var(--faint)">BU SAYFADA</span><a href="#nedir">EKED / LOTO nedir?</a><a href="#enerji">Hangi enerjiler kilitlenir?</a><a href="#adimlar">Prosedürün adımları</a><a href="#kurallar">Kilit kuralları</a><a href="#grup">Grup kilitleme</a><a href="#mevzuat">Mevzuat</a><a href="#sss">Sık sorulanlar</a></nav></aside>
</section>
<section class="wrap" style="padding-bottom:56px"><div class="steps">{steps}</div>
<p class="muted" style="margin-top:20px;max-width:72ch">İş bitince enerji ters sırayla verilir: alan kontrol edilir, çalışanlar uzaklaştırılır, her kişi kendi kilidini kendisi çıkarır ve ilgili herkes bilgilendirilir.</p></section>
<section class="wrap" style="padding-bottom:72px"><article class="prose">
<h2 id="kurallar">Kilit kuralları</h2>
<ul><li><b>Bir kişi, bir kilit, bir anahtar.</b> Her çalışan kendi kişisel kilidini takar; anahtarı yalnızca kendisinde durur.</li><li>Emniyet asma kilitleri yalnızca LOTO için kullanılır; dolap ya da kapı kilidi olarak kullanılmaz.</li><li>Kilidi yalnızca takan kişi çıkarır. Kişi yerinde değilse yazılı bir kilit çıkarma prosedürü uygulanır.</li><li>Renk kodu, kilidin hangi departmana ya da ekibe ait olduğunu uzaktan gösterir.</li></ul>
<h2 id="grup">Grup kilitleme</h2>
<p>Çok sayıda kişinin çok sayıda noktada çalıştığı işlerde her çalışanın her noktaya kilit takması pratik değildir. Bu durumda yetkili kişi tüm izolasyon noktalarını aynı anahtarlı ortak kilitlerle kilitler, anahtarları grup kilitleme kutusuna koyar. Her çalışan kutuya kendi kilidini takar; son kilit çıkmadan anahtarlara ulaşılamaz.</p>
<p>Kaç kilit ve kutu gerektiğini <a href="set-olusturucu.html">set oluşturucu</a> ile hesaplayabilirsiniz.</p>
<h2 id="mevzuat">Mevzuat</h2>
<p>LOTO prosedürlerinin temel referansı ABD İş Güvenliği ve Sağlığı İdaresi'nin <b>OSHA 29 CFR 1910.147</b> standardıdır. Türkiye'de <b>6331 sayılı İş Sağlığı ve Güvenliği Kanunu</b> işverene risk değerlendirmesi yapma ve tehlikelere karşı önlem alma yükümlülüğü getirir; bakım ve onarım sırasında tehlikeli enerjinin kontrolü bu önlemlerin başında gelir. İş ekipmanlarının kullanımına ilişkin yönetmelik de bakım sırasında ekipmanın enerjiden ayrılmasını ister.</p>
<p class="muted" style="font-size:15px">Bu sayfa genel bilgilendirme amaçlıdır; tesisinize özel prosedür iş güvenliği uzmanınızla birlikte hazırlanmalıdır.</p>
</article></section>
<div id="sss">{faq_block(FAQ)}</div>
{cta_block()}'''
    page("loto-rehberi.html", "LOTO Rehberi: Kilitleme ve Etiketleme Adımları", "EKED / LOTO nedir, hangi enerjiler kilitlenir, prosedürün adımları, kilit kuralları, grup kilitleme ve mevzuat özeti.", body, "loto-rehberi.html")

def build_about():
    hero_p = PROD[pid("LT-PR-U07")]
    cats = "".join('<a href="%s">%s%s<span>%d</span></a>' % (cat_url(c["slug"]), ICONS[c["icon"]], e(c["name"]), len(c["items"])) for c in CATEGORIES)
    body = f"""{crumbs(("", "Kurumsal"))}
<section class="wrap about-hero">
<div class="about-copy"><span class="eyebrow">Kurumsal · Lockout Turkey</span><h1 class="h1">Biz kimiz?</h1>
<p class="lead">Lockout Turkey, iş sağlığı ve güvenliği alanında kilitleme ve etiketleme (EKED / LOTO) ekipmanları sunan bir markadır. Bakım, onarım ve temizlik sırasında makinelerin beklenmedik şekilde çalışmasını önleyen ekipmanları işletmelere tek noktadan tedarik ediyoruz.</p>
<p class="lead">Temel hedefimiz; çalışan güvenliğini artırmak, iş kazalarını önlemek ve işletmelerin LOTO uygulamalarını doğru ekipmanla, uluslararası standartlara uygun şekilde kurmasına yardımcı olmaktır.</p>
<div style="display:flex;flex-wrap:wrap;gap:10px"><a class="btn btn-red" href="urunler.html">Ürünlerimiz</a><a class="btn btn-line" href="{CATALOG_PDF}" target="_blank" rel="noopener">Katalog (PDF)</a></div></div>
<div class="about-visual"><div class="p-img">{p_image(hero_p, lazy=False)}</div></div>
</section>
<section class="wrap" style="padding-bottom:56px"><div class="stats">
<div><b>{len(PROD)}</b><span>Ürün çeşidi</span></div>
<div><b>{len(CATEGORIES)}</b><span>Ürün grubu</span></div>
<div><b>8</b><span>Renk emniyet kilidi</span></div>
<div><b>OSHA</b><span>29 CFR 1910.147 uyumlu ürünler</span></div>
<div><b>İstanbul</b><span>Ümraniye’den Türkiye geneline</span></div>
</div></section>
<section class="section section--paper"><div class="wrap mv">
<div class="mv-card"><span class="mv-mark">M</span><h2 class="h2">Misyonumuz</h2>
<p>İşletmelerin enerji izolasyonu ihtiyaçlarına doğru, dayanıklı ve kullanımı kolay kilitleme ve etiketleme çözümleri sunmak.</p>
<p>Her teklifte yalnızca ürünü değil, ürünün doğru noktada doğru şekilde kullanılmasını da önemsemek.</p></div>
<div class="mv-card"><span class="mv-mark">V</span><h2 class="h2">Vizyonumuz</h2>
<p>Türkiye’de LOTO ekipmanı denildiğinde akla gelen, ulaşılabilir ve güvenilir tedarikçilerden biri olmak.</p>
<p>LOTO uygulamalarını yalnızca büyük tesislerin değil, her ölçekteki işletmenin günlük bakım rutini haline getirmek.</p></div>
</div></section>
<section class="section"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Neye inanıyoruz</span><h2 class="h2">Değerlerimiz</h2></div></div>
<div class="values">
<div><b>Güvenlik</b><p>Tüm işlerimizin merkezinde insan güvenliği yer alır.</p></div>
<div><b>Doğru ürün</b><p>Satıştan önce kilitlenecek noktayı anlamaya çalışırız; uymayan ürünü önermeyiz.</p></div>
<div><b>Güvenilirlik</b><p>Müşterilerimizle ve iş ortaklarımızla uzun vadeli ilişkiler kurarız.</p></div>
<div><b>Hız</b><p>Teklif ve sevkiyatta hızlı dönüş, sahadaki bakımın beklememesi demektir.</p></div>
</div></div></section>
<section class="section section--paper"><div class="wrap why">
<div><span class="eyebrow">Farkımız</span><h2 class="h2">Neden Lockout Turkey?</h2>
<ul class="features">
<li><span>Kişisel kilitlerden LOTO istasyonlarına kadar {len(PROD)} ürün tek noktada</span></li>
<li><span>Fotoğraf ya da model bilgisiyle ürün seçim desteği</span></li>
<li><span>Renk, anahtar sistemi ve isim/numara baskısıyla kişiye özel kilitler</span></li>
<li><span>Tesis krokisi ve set oluşturucu ile kolay ürün seçimi</span></li>
<li><span>Kurumsal faturalı satış ve hızlı teklif</span></li>
</ul></div>
<blockquote class="quote">“Önce güvenlik” anlayışıyla her gün daha güvenli çalışma alanları için çalışıyoruz. Bizim için her kilit, bir çalışanın güvencesidir.<cite>Lockout Turkey</cite></blockquote>
</div></section>
<section class="section"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Ürünler</span><h2 class="h2">Ürün kategorilerimiz</h2></div><a class="link-arrow" href="urunler.html">Tüm ürünler →</a></div>
<div class="cat-chips">{cats}</div></div></section>
<section class="section section--paper"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">İletişim</span><h2 class="h2">Size destek olmak için buradayız.</h2></div></div>
<div class="two-col">{contact_form()}
<div class="card"><span class="panel-label" style="color:var(--faint)">MERKEZ</span><ul class="info-list">
<li><span>Adres</span><b>{e(SITE["address"])}</b></li>
<li><span>Telefon / WhatsApp</span><b>{e(SITE["phone"])}</b></li>
<li><span>E-posta</span><b>{e(SITE["email"])}</b></li></ul>
<a class="btn btn-line" href="https://www.google.com/maps/search/?api=1&amp;query={e(SITE["address"])}" target="_blank" rel="noopener">Haritada aç</a></div>
</div></div></section>"""
    page("kurumsal.html", "Kurumsal", "Lockout Turkey hakkında: biz kimiz, misyonumuz, vizyonumuz ve değerlerimiz. EKED / LOTO kilitleme ve etiketleme ekipmanları.", body, "kurumsal.html")

def contact_form():
    return '''<form class="card" id="iletisim-form" novalidate>
<h2 class="h3">Mesaj gönderin</h2>
<div class="fields-2"><div class="field"><label for="c-ad">Ad Soyad</label><input id="c-ad" name="ad" required autocomplete="name"></div>
<div class="field"><label for="c-firma">Firma</label><input id="c-firma" name="firma" autocomplete="organization"></div></div>
<div class="fields-2"><div class="field"><label for="c-tel">Telefon</label><input id="c-tel" name="telefon" type="tel" autocomplete="tel"></div>
<div class="field"><label for="c-mail">E-posta</label><input id="c-mail" name="eposta" type="email" autocomplete="email"></div></div>
<div class="field"><label for="c-mesaj">Mesajınız</label><textarea id="c-mesaj" name="mesaj" required></textarea></div>
<button class="btn btn-red" type="submit">Mesajı hazırla</button>
<div class="output-box" id="iletisim-cikti" hidden><p class="notice">Mesajınız hazır. WhatsApp ya da e-posta ile gönderin; açılmazsa metni kopyalayıp yapıştırın.</p>
<label class="sr-only" for="iletisim-metin">Mesaj metni</label><textarea id="iletisim-metin" readonly></textarea>
<div style="display:flex;flex-wrap:wrap;gap:10px"><a class="btn btn-dark" id="iletisim-wa" href="#" target="_blank" rel="noopener">WhatsApp ile gönder</a><a class="btn btn-line" id="iletisim-mail" href="#">E-posta ile gönder</a><button class="btn btn-line" type="button" data-copy="#iletisim-metin">Metni kopyala</button></div></div>
</form>'''

def build_contact():
    body = f'''{crumbs(("", "İletişim"))}
<section class="wrap page-head"><div><span class="eyebrow">İletişim</span><h1 class="h1">Teklif, numune, saha keşfi.</h1>
<p class="lead">Ürün kodu, fotoğraf ya da sadece ihtiyacınızı yazın; size dönüş yapalım.</p></div></section>
<section class="wrap" style="padding-bottom:72px"><div class="two-col">
{contact_form()}
<div class="card"><span class="panel-label" style="color:var(--faint)">İLETİŞİM BİLGİLERİ</span><ul class="info-list">
<li><span>Telefon</span><b>{e(SITE["phone"])}</b></li><li><span>WhatsApp</span><b>{e(SITE["whatsapp"])}</b></li>
<li><span>E-posta</span><b>{e(SITE["email"])}</b></li>{('<li><span>Adres</span><b>%s</b></li>' % e(SITE["address"])) if SITE["address"] else ''}{('<li><span>Çalışma saatleri</span><b>%s</b></li>' % e(SITE["hours"])) if SITE["hours"] else ''}</ul>
{('<a class="btn btn-line" href="https://www.google.com/maps/search/?api=1&amp;query=%s" target="_blank" rel="noopener">Haritada aç</a>' % e(SITE["address"])) if SITE["address"] else '<a class="btn btn-red" href="%s" target="_blank" rel="noopener">WhatsApp’tan yazın</a>' % wa_href("Merhaba, LOTO ürünleri hakkında bilgi almak istiyorum.")}</div>
</div></section>'''
    page("iletisim.html", "İletişim", "Lockout Turkey iletişim bilgileri; teklif, ürün seçimi ve saha keşfi için bize ulaşın.", body, "iletisim.html")

def build_cart():
    body = f'''{crumbs(("", "Teklif listesi"))}
<section class="wrap page-head"><div><span class="eyebrow">Teklif listesi</span><h1 class="h1">Teklif listeniz</h1>
<p class="lead">Adetleri düzenleyin, firma bilgilerinizi ekleyin; listeyi WhatsApp ya da e-posta ile gönderin.</p></div></section>
<section class="wrap" style="padding-bottom:72px">
<div class="empty" id="teklif-bos"><b>Listeniz boş.</b><p class="muted">Ürün sayfalarından, krokiden ya da set oluşturucudan ürün ekleyebilirsiniz.</p>
<div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center"><a class="btn btn-red" href="urunler.html">Ürünlere göz at</a><a class="btn btn-line" href="set-olusturucu.html">Set oluştur</a></div></div>
<div class="two-col" id="teklif-root" hidden>
<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;gap:12px"><h2 class="h3">Ürünler</h2><button class="btn btn-line" type="button" id="teklif-temizle" style="min-height:40px">Listeyi temizle</button></div><div id="teklif-satir"></div>
<a class="link-arrow" href="urunler.html">+ Ürün ekle</a></div>
<form class="card" id="teklif-form" novalidate><h2 class="h3">Bilgileriniz</h2>
<div class="field"><label for="t-firma">Firma</label><input id="t-firma" name="firma" autocomplete="organization"></div>
<div class="fields-2"><div class="field"><label for="t-ad">Ad Soyad</label><input id="t-ad" name="ad" autocomplete="name"></div>
<div class="field"><label for="t-tel">Telefon</label><input id="t-tel" name="telefon" type="tel" autocomplete="tel"></div></div>
<div class="fields-2"><div class="field"><label for="t-mail">E-posta</label><input id="t-mail" name="eposta" type="email" autocomplete="email"></div>
<div class="field"><label for="t-sehir">Şehir</label><input id="t-sehir" name="sehir" autocomplete="address-level1"></div></div>
<div class="field"><label for="t-not">Not</label><textarea id="t-not" name="not" placeholder="Renk, anahtar sistemi, baskı isteği…"></textarea></div>
<button class="btn btn-red" type="submit">Teklif talebini hazırla</button>
<div class="output-box" id="teklif-cikti" hidden><p class="notice">Talebiniz hazır. WhatsApp ya da e-posta ile gönderin; açılmazsa metni kopyalayıp yapıştırın.</p>
<label class="sr-only" for="teklif-metin">Talep metni</label><textarea id="teklif-metin" readonly></textarea>
<div style="display:flex;flex-wrap:wrap;gap:10px"><a class="btn btn-dark" id="teklif-wa" href="#" target="_blank" rel="noopener">WhatsApp ile gönder</a><a class="btn btn-line" id="teklif-mail" href="#">E-posta ile gönder</a><button class="btn btn-line" type="button" data-copy="#teklif-metin">Metni kopyala</button></div></div>
</form></div></section>'''
    page("teklif.html", "Teklif Listesi", "Seçtiğiniz LOTO ürünleri için teklif talebi oluşturun.", body, "")

def build_kvkk():
    owner = SITE.get("legal_name") or SITE["brand"]
    addr = (", " + e(SITE["address"])) if SITE["address"] else ""
    body = f"""{crumbs(("", "KVKK ve gizlilik"))}
<section class="wrap page-head"><div><span class="eyebrow">Yasal</span><h1 class="h1">KVKK ve gizlilik</h1>
<p class="lead">6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında kişisel verilerinizin nasıl işlendiğini aşağıda bulabilirsiniz.</p></div></section>
<section class="wrap" style="padding-bottom:72px"><article class="prose">
<h2>Veri sorumlusu</h2>
<p>Kişisel verileriniz, veri sorumlusu sıfatıyla {e(owner)}{addr} tarafından aşağıda açıklanan kapsamda işlenmektedir. İletişim: {e(SITE["email"])}</p>
<h2>İşlenen kişisel veriler</h2>
<p>Teklif, iletişim ve bilgi talepleriniz sırasında bize ilettiğiniz ad soyad, firma adı, telefon numarası, e-posta adresi, şehir ve mesaj içeriği.</p>
<h2>İşleme amaçları</h2>
<ul><li>Teklif ve bilgi taleplerinizi yanıtlamak, sizinle iletişime geçmek</li><li>Sipariş, satış ve teslimat süreçlerini yürütmek</li><li>Fatura düzenlemek ve yasal yükümlülükleri yerine getirmek</li></ul>
<h2>Toplama yöntemi ve hukuki sebep</h2>
<p>Verileriniz; sitedeki formlar aracılığıyla hazırlanıp sizin tarafınızdan WhatsApp veya e-posta ile gönderilen mesajlar ve telefon görüşmeleri yoluyla toplanır. Kanun'un 5. maddesindeki bir sözleşmenin kurulması veya ifasıyla doğrudan ilgili olması, hukuki yükümlülüğün yerine getirilmesi ve meşru menfaat hukuki sebeplerine dayanılarak işlenir.</p>
<h2>Aktarım</h2>
<p>Kişisel verileriniz, yasal zorunluluklar dışında üçüncü kişilerle paylaşılmaz; yalnızca kargo, muhasebe ve mali müşavirlik gibi hizmetlerin yürütülmesi için gerekli olduğu ölçüde ilgili hizmet sağlayıcılara aktarılabilir.</p>
<h2>Haklarınız</h2>
<p>Kanun'un 11. maddesi uyarınca verilerinizin işlenip işlenmediğini öğrenme, bilgi talep etme, düzeltilmesini veya silinmesini isteme, aktarıldığı kişileri öğrenme ve işlemeye itiraz etme haklarına sahipsiniz. Taleplerinizi {e(SITE["email"])} adresine iletebilirsiniz.</p>
<h2>Çerezler ve tarayıcı depolama</h2>
<p>Bu site reklam veya takip çerezi kullanmaz. Yazı tipleri Google Fonts üzerinden yüklenir. Teklif listeniz yalnızca kendi tarayıcınızda saklanır ve siz göndermedikçe bize ulaşmaz.</p>
</article></section>"""
    page("kvkk.html", "KVKK ve Gizlilik", "Lockout Turkey KVKK aydınlatma metni ve gizlilik bilgileri.", body, "")


# ---------------------------------------------------------------- blog
AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
def tr_date(iso):
    y, m, d = iso.split("-"); return "%d %s %s" % (int(d), AYLAR[int(m) - 1], y)
def post_url(p): return "blog-%s.html" % p["slug"]
POSTS.sort(key=lambda p: p["date"], reverse=True)
def render_body(html_body):
    def plink(m):
        p = PROD[pid(m.group(1))]
        return '<a href="%s">%s</a>' % (p["url"], e(p["name"]))
    def clink(m):
        c = CAT[m.group(1)]
        return '<a href="%s">%s</a>' % (cat_url(c["slug"]), e(c["name"].lower()))
    html_body = re.sub(r"\{p:([^}]+)\}", plink, html_body)
    return re.sub(r"\{c:([^}]+)\}", clink, html_body)
def post_card(p):
    cover = PROD[pid(p["cover"])]
    return f"""<a class="post-card" href="{post_url(p)}"><div class="post-img">{p_image(cover)}</div>
<div class="post-body"><div class="post-meta"><span>{e(p["tag"])}</span><span>{tr_date(p["date"])} · {p["minutes"]} dk</span></div>
<h3>{e(p["title"])}</h3><p>{e(p["summary"])}</p><span class="go">Yazıyı oku →</span></div></a>"""
def blog_block():
    return f"""<section class="section"><div class="wrap">
<div class="section-head"><div><span class="eyebrow">Blog</span><h2 class="h2">Sahadan notlar.</h2></div><a class="link-arrow" href="blog.html">Tüm yazılar →</a></div>
<div class="post-grid">{"".join(post_card(p) for p in POSTS[:3])}</div></div></section>"""
def build_blog():
    first, rest = POSTS[0], POSTS[1:]
    cover = PROD[pid(first["cover"])]
    body = f"""{crumbs(("", "Blog"))}
<section class="wrap page-head"><div><span class="eyebrow">Blog</span><h1 class="h1">Kilitleme ve etiketleme üzerine.</h1>
<p class="lead">Ürün seçimi, prosedür ve saha uygulamaları hakkında kısa ve uygulanabilir yazılar.</p></div></section>
<section class="wrap" style="padding-bottom:40px"><a class="post-feature" href="{post_url(first)}"><div class="post-img">{p_image(cover, lazy=False)}</div>
<div class="post-body"><div class="post-meta"><span>{e(first["tag"])}</span><span>{tr_date(first["date"])} · {first["minutes"]} dk okuma</span></div>
<h2 class="h2">{e(first["title"])}</h2><p class="lead">{e(first["summary"])}</p><span class="go">Yazıyı oku →</span></div></a></section>
<section class="wrap" style="padding-bottom:72px"><div class="post-grid">{"".join(post_card(p) for p in rest)}</div></section>
{cta_block()}"""
    page("blog.html", "Blog", "Lockout Turkey blog: emniyet asma kilidi seçimi, şalter ve vana kilitleme, grup kilitleme ve LOTO istasyonları üzerine yazılar.", body, "blog.html")
    for i, p in enumerate(POSTS):
        others = [x for x in POSTS if x is not p][:3]
        prods = [PROD[pid(c)] for c in p["products"]][:4]
        body = f"""{crumbs(("blog.html", "Blog"), ("", p["title"]))}
<article class="wrap post">
<header class="post-head"><div class="post-meta"><span>{e(p["tag"])}</span><span>{tr_date(p["date"])} · {p["minutes"]} dk okuma</span></div>
<h1 class="h1">{e(p["title"])}</h1><p class="lead">{e(p["summary"])}</p></header>
<div class="prose post-text">{render_body(p["body"])}</div>
<aside class="post-cta"><b>Doğru ürünü birlikte seçelim</b><span class="muted">Kilitleyeceğiniz noktanın fotoğrafını gönderin, uygun ekipmanı bildirelim.</span>
<a class="btn btn-red" href="{wa_href("Merhaba, " + p["title"] + " yazınızı okudum, bilgi almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp’tan yazın</a></aside>
</article>
<section class="section section--paper"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Yazıda geçen ürünler</span><h2 class="h2">İlgili ürünler</h2></div></div>
<div class="product-grid">{"".join(product_card(x) for x in prods)}</div></div></section>
<section class="section"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Blog</span><h2 class="h2">Diğer yazılar</h2></div><a class="link-arrow" href="blog.html">Tüm yazılar →</a></div>
<div class="post-grid">{"".join(post_card(x) for x in others)}</div></div></section>"""
        page(post_url(p), p["title"], p["summary"], body, "blog.html")

# ---------------------------------------------------------------- yardımcı dosyalar
def write_assets():
    shutil.copy(os.path.join(HERE, "style.css"), os.path.join(OUT, "style.css"))
    shutil.copy(os.path.join(HERE, "app.js"), os.path.join(OUT, "app.js"))
    data = {
        "site": {k: SITE[k] for k in ("whatsapp_num", "email")},
        "icons": ICONS,
        "products": {i: {"name": p["name"], "code": p["code"], "cat": CAT[p["cat"]]["name"], "url": p["url"], "icon": p["icon"],
                         "img": (p_imgs(p) or [""])[0]} for i, p in PROD.items()},
        "points": POINTS,
        "refs": REF_IDS,
    }
    with open(os.path.join(OUT, "data.js"), "w", encoding="utf-8") as f:
        f.write("window.BOSS = " + json.dumps(data, ensure_ascii=False) + ";\n")
    with open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#C8102E"/><path d="M11.5 14.5V11a4.5 4.5 0 0 1 9 0v3.5" fill="none" stroke="#fff" stroke-width="2.8" stroke-linecap="round"/><rect x="8" y="13.5" width="16" height="13" rx="3" fill="#fff"/></svg>')
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE["domain"])
    today = date.today().isoformat()
    urls = "".join("<url><loc>%s/%s</loc><lastmod>%s</lastmod></url>" % (SITE["domain"], "" if p == "index.html" else p, today) for p in PAGES if p not in ("teklif.html",))
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>' % urls)

if __name__ == "__main__":
    if os.path.exists(OUT):
        keep_img = os.path.join(OUT, "img")
        for name in os.listdir(OUT):
            if name == "img": continue
            path = os.path.join(OUT, name)
            shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
    os.makedirs(IMG_DIR, exist_ok=True)
    build_index(); build_products(); build_categories(); build_product_pages(); build_set_page()
    build_sectors(); build_guide(); build_about(); build_contact(); build_cart(); build_kvkk(); build_blog()
    write_assets()
    print("%d sayfa üretildi → %s" % (len(PAGES), os.path.normpath(OUT)))
