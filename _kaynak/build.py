# -*- coding: utf-8 -*-
"""Lockout Turkey · 2. tasarım statik site üreticisi.  python3 build.py → ../site/
Görseller ve katalog PDF'i ../site/img ve ../site/lockout-turkey-katalog.pdf olarak durur (silinmez)."""
import json, os, re, shutil, html
from datetime import date
from urllib.parse import quote
from data import SITE, CATEGORIES, COLORS, STEPS, FAQ, FOOTER_TEXT
from blog import POSTS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "site")
IMG_DIR = os.path.join(OUT, "img", "urunler")
CATALOG_PDF = "lockout-turkey-katalog.pdf"
KEEP = {"img", CATALOG_PDF}
e = html.escape

# ---------------------------------------------------------------- veri
CAT = {c["slug"]: c for c in CATEGORIES}
for c in CATEGORIES: c["items"] = []
PROD, CODE = {}, {}
for p in json.load(open(os.path.join(HERE, "catalog.json"), encoding="utf-8")):
    p["url"] = p["id"] + ".html"
    PROD[p["id"]] = p; CODE[p["code"]] = p["id"]; CAT[p["cat"]]["items"].append(p)
def nat(p): return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", p["code"])]
for c in CATEGORIES: c["items"].sort(key=nat)
def P(code): return PROD[CODE.get(code, code)]
COLOR_HEX = {c[0]: c[1] for c in COLORS}
GROUPS = {}
for p in PROD.values():
    if p["group"]: GROUPS.setdefault((p["cat"], p["group"]), []).append(p)
for g in GROUPS.values(): g.sort(key=nat)

def imgs(p): return [i for i in p["images"] if os.path.exists(os.path.join(IMG_DIR, i))]
def img(p, k=0, lazy=True, alt=None):
    l = imgs(p)
    if len(l) > k:
        return '<img src="img/urunler/%s" alt="%s" width="800" height="800"%s>' % (l[k], e(alt if alt is not None else p["name"]), ' loading="lazy"' if lazy else "")
    return ICON_LOCK
def cat_url(slug): return slug + ".html"
def cat_cover(c): return c["items"][0]
def wa(text=""): return "https://wa.me/%s%s" % (SITE["whatsapp_num"], ("?text=" + quote(text)) if text else "")
def tel(): return "tel:" + SITE["phone_tel"]

# ---------------------------------------------------------------- ikonlar
def ic(path, w=2): return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (w, path)
ICON_LOCK = ic('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>', 1.6)
I_PHONE = ic('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>')
I_MAIL = ic('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>')
I_PIN = ic('<path d="M12 22s7-6.1 7-12a7 7 0 0 0-14 0c0 5.9 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>')
I_SEARCH = ic('<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>')
I_DOC = ic('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>')
I_SHIELD = ic('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>')
I_CHAT = ic('<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>')
I_TAG = ic('<path d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9z"/><circle cx="8" cy="8" r="1.5"/>')
I_BOX = ic('<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>')
I_CHEV = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
WA_ICON = '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.4.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2l-.5-.3z"/></svg>'
LOGO = ('<span class="wm"><span class="wm-top">LOCK<svg class="wm-o" viewBox="0 0 72 108" aria-hidden="true"><path class="wm-sh" d="M18 34 V24 a18 18 0 0 1 36 0 V34"/>'
        '<rect class="wm-body" x="2" y="31" width="68" height="77" rx="12"/><circle class="wm-kh" cx="36" cy="62" r="7"/><rect class="wm-kh" x="33" y="64" width="6" height="18" rx="2"/></svg>UT</span>'
        '<span class="wm-bot"><i></i><span>TURKEY</span><i></i></span></span>')

# ---------------------------------------------------------------- iskelet
NAV = [("./", "Anasayfa"), ("urunler.html", "Ürünler"), ("kurumsal.html", "Kurumsal"), ("loto-rehberi.html", "LOTO Rehberi"), ("blog.html", "Blog"), ("iletisim.html", "İletişim")]
PAGES = []

def header(active):
    mega = "".join('<a href="%s">%s<div>%s<span>%d ürün</span></div></a>' % (cat_url(c["slug"]), img(cat_cover(c), alt=""), e(c["name"]), len(c["items"])) for c in CATEGORIES)
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        if href == "urunler.html":
            items.append('<div class="mega-wrap"><a class="mega-btn" href="urunler.html"%s>Ürünler %s</a><div class="mega">%s<a class="all" href="urunler.html">Tüm ürünler (%d) →</a></div></div>' % (cur, I_CHEV, mega, len(PROD)))
        else:
            items.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    return f'''<div class="topbar"><div class="wrap">
<div class="l"><a href="{tel()}">{e(SITE["phone"])}</a><a href="{wa()}" target="_blank" rel="noopener">WhatsApp</a><span>{e(SITE["email"])}</span></div>
<div class="r"><span>EKED / LOTO ekipmanları</span><a href="{CATALOG_PDF}" target="_blank" rel="noopener">Katalog (PDF)</a></div></div></div>
<header class="header"><div class="wrap">
<a class="logo" href="./" aria-label="{e(SITE["brand"])} anasayfa">{LOGO}</a>
<nav class="nav" aria-label="Ana menü">{"".join(items)}</nav>
<div class="h-actions"><a class="icon-btn" href="urunler.html#ara" aria-label="Ürün ara">{I_SEARCH}</a>
<a class="cart-btn" href="teklif.html"><span class="cart-label">Teklif sepeti</span><span class="cart-count" data-cart-count>0</span><span class="sr-only">ürün</span></a>
<button class="icon-btn nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Menüyü aç"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button></div>
</div></header>'''

def footer():
    cats = "".join('<a href="%s">%s</a>' % (cat_url(c["slug"]), e(c["name"])) for c in CATEGORIES[:7])
    return f'''<footer class="footer"><div class="tape"></div><div class="wrap cols">
<div class="about"><a class="logo" href="./">{LOGO}</a><p>{e(FOOTER_TEXT)}</p>
<a class="btn btn-red btn-sm" style="align-self:flex-start" href="{CATALOG_PDF}" target="_blank" rel="noopener">{I_DOC} Ürün kataloğu (PDF)</a></div>
<div class="col"><b>Ürünler</b>{cats}<a href="urunler.html">Tüm ürünler →</a></div>
<div class="col"><b>Kurumsal</b><a href="kurumsal.html">Hakkımızda</a><a href="loto-rehberi.html">LOTO rehberi</a><a href="blog.html">Blog</a><a href="teklif.html">Teklif sepeti</a><a href="iletisim.html">İletişim</a><a href="kvkk.html">KVKK ve gizlilik</a></div>
<div class="col"><b>İletişim</b><a href="{tel()}">{e(SITE["phone"])}</a><a href="{wa()}" target="_blank" rel="noopener">WhatsApp</a><span>{e(SITE["email"])}</span><span>{e(SITE["address"])}</span></div>
</div><div class="bottom"><div class="wrap"><span>© {date.today().year} {e(SITE["brand"])}. Tüm hakları saklıdır.</span><span>EKED · LOTO kilitleme ve etiketleme ekipmanları</span></div></div></footer>
<a class="wa-float" href="{wa("Merhaba, LOTO ürünleri hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener" aria-label="WhatsApp ile yazın">{WA_ICON}</a>'''

def page(fname, title, desc, body, active=""):
    canonical = SITE["domain"] + ("/" if fname == "index.html" else "/" + fname)
    full = title if fname == "index.html" else "%s | %s" % (title, SITE["brand"])
    doc = f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:locale" content="tr_TR"><meta property="og:site_name" content="{e(SITE["brand"])}">
<meta property="og:title" content="{e(full)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canonical}">
<meta name="theme-color" content="#D0121F">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,800..900&amp;family=Saira+Semi+Condensed:wght@500;600;700;800&amp;family=Source+Sans+3:wght@400;600;700&amp;family=IBM+Plex+Mono:wght@500;600&amp;display=swap">
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
<script src="extra.js"></script>
</body>
</html>
'''
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(doc)
    PAGES.append(fname)

def crumbs(*items):
    parts = ['<a href="./">Anasayfa</a>']
    for href, label in items:
        parts.append('<span aria-hidden="true">›</span>')
        parts.append('<a href="%s">%s</a>' % (href, e(label)) if href else '<span>%s</span>' % e(label))
    return '<nav class="crumbs" aria-label="Sayfa yolu">%s</nav>' % "".join(parts)

def band(crumb_items, kicker, title, lead=""):
    return f'''<section class="ph-band"><div class="wrap">{crumbs(*crumb_items)}<span class="kicker">{e(kicker)}</span><h1 class="t1">{e(title)}</h1>{('<p class="lead">%s</p>' % e(lead)) if lead else ''}</div></section>'''

# ---------------------------------------------------------------- bileşenler
def cdots(p):
    if not p["group"]: return ""
    return '<div class="cdots" aria-label="Renk seçenekleri">' + "".join('<i style="background:%s" title="%s"></i>' % (COLOR_HEX.get(x["color"], "#999"), e(x["color"])) for x in GROUPS[(p["cat"], p["group"])]) + "</div>"

def pcard(p, tab=None):
    name = p["name"][len(p["code"]):].strip()
    text = " ".join([p["name"], p["short"], CAT[p["cat"]]["name"], p["color"]])
    extra = (' data-tabitem="%s"' % tab) if tab else ""
    return f'''<article class="pc" data-card data-cat="{p["cat"]}" data-text="{e(text)}"{extra}><div class="ph">{img(p)}</div>
<div class="bd"><span class="code">{e(p["code"])}</span><h3><a href="{p["url"]}">{e(name)}</a></h3>{cdots(p)}
<div class="ac"><a class="btn btn-line" href="{p["url"]}">İncele</a><button class="btn btn-red" type="button" data-add="{p["id"]}">+ Teklif</button></div></div></article>'''

def cat_card(c, i):
    return f'''<a class="cat" href="{cat_url(c["slug"])}"><span class="nb">{i:02d}</span><div class="ph">{img(cat_cover(c), alt="")}</div>
<div class="tx"><h3>{e(c["name"])}</h3><p>{e(c["short"])}</p><span class="ct">Ürünleri gör →<span>{len(c["items"])} ürün</span></span></div></a>'''

AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
def tr_date(iso): y, m, d = iso.split("-"); return "%d %s %s" % (int(d), AYLAR[int(m) - 1], y)
POSTS.sort(key=lambda p: p["date"], reverse=True)
def post_url(p): return "blog-%s.html" % p["slug"]
def post_card(p):
    return f'''<a class="post-c" href="{post_url(p)}"><div class="ph">{img(P(p["cover"]), alt="")}</div><div class="bd">
<div class="meta"><span class="tg">{e(p["tag"])}</span><span>{tr_date(p["date"])}</span><span>{p["minutes"]} dk okuma</span></div>
<h3>{e(p["title"])}</h3><p>{e(p["summary"])}</p><span class="go">Devamını oku →</span></div></a>'''
def render_body(b):
    b = b.replace('Ekibinize kaç kilit ve hangi kutunun gerektiğini <a href="set-olusturucu.html">set oluşturucu</a> ile hızlıca hesaplayabilirsiniz.',
                  'Ekibinize uygun kutuyu <a href="grup-kilitleme-kutulari-ve-cantalar.html">grup kilitleme kutuları</a> arasından seçebilir ya da ekip ve nokta sayınızı yazarak bize sorabilirsiniz.')
    b = re.sub(r"\{p:([^}]+)\}", lambda m: '<a href="%s">%s</a>' % (P(m.group(1))["url"], e(P(m.group(1))["name"])), b)
    return re.sub(r"\{c:([^}]+)\}", lambda m: '<a href="%s">%s</a>' % (cat_url(m.group(1)), e(CAT[m.group(1)]["name"].lower())), b)

def cta():
    return f'''<section class="cta"><div class="wrap"><div><h2>Tesisiniz için toplu teklif mi lazım?</h2><p>Ürünleri teklif sepetine ekleyin ya da ihtiyacınızı WhatsApp’tan yazın; size özel teklifle dönelim.</p></div>
<div class="acts"><a class="btn btn-red" href="teklif.html">Teklif sepeti</a><a class="btn btn-ghost" href="{wa("Merhaba, toplu teklif almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp’tan yaz</a></div></div><div class="tape"></div></section>'''

def faq(items):
    d = "".join('<details%s><summary>%s</summary><p>%s</p></details>' % (" open" if i == 0 else "", e(q), e(a)) for i, (q, a) in enumerate(items))
    return f'''<section class="sec sec-soft"><div class="wrap faq"><div><span class="kicker">Sık sorulanlar</span><h2 class="t2">LOTO hakkında merak edilenler</h2>
<p class="muted">Aradığınız cevabı bulamazsanız bize yazın; ürün fotoğrafı göndermeniz yeterli.</p><a class="btn btn-dark" style="align-self:flex-start" href="iletisim.html">Bize ulaşın</a></div>
<div class="faq-list">{d}</div></div></section>'''

def contact_form():
    return '''<form class="card" id="iletisim-form" novalidate><h2 class="t3">İletişim formu</h2>
<div class="fields-2"><div class="field"><label for="c-ad">Ad Soyad</label><input id="c-ad" name="ad" required autocomplete="name"></div>
<div class="field"><label for="c-firma">Firma</label><input id="c-firma" name="firma" autocomplete="organization"></div></div>
<div class="fields-2"><div class="field"><label for="c-tel">Telefon</label><input id="c-tel" name="telefon" type="tel" autocomplete="tel"></div>
<div class="field"><label for="c-mail">E-posta</label><input id="c-mail" name="eposta" type="email" autocomplete="email"></div></div>
<div class="field"><label for="c-mesaj">Mesajınız</label><textarea id="c-mesaj" name="mesaj" required></textarea></div>
<button class="btn btn-red" type="submit" style="align-self:flex-start">Mesajı hazırla</button>
<div class="output-box" id="iletisim-cikti" hidden><p class="notice">Mesajınız hazır. WhatsApp ya da e-posta ile gönderin; açılmazsa metni kopyalayıp yapıştırın.</p>
<label class="sr-only" for="iletisim-metin">Mesaj metni</label><textarea id="iletisim-metin" readonly></textarea>
<div style="display:flex;flex-wrap:wrap;gap:10px"><a class="btn btn-dark" id="iletisim-wa" href="#" target="_blank" rel="noopener">WhatsApp ile gönder</a><a class="btn btn-line" id="iletisim-mail" href="#">E-posta ile gönder</a><button class="btn btn-line" type="button" data-copy="#iletisim-metin">Metni kopyala</button></div></div></form>'''

def info_card(title="Bize ulaşın"):
    return f'''<div class="card card-soft"><h2 class="t3">{e(title)}</h2><ul class="info-list">
<li><i>{I_PHONE}</i><div><span>Telefon / WhatsApp</span><b>{e(SITE["phone"])}</b></div></li>
<li><i>{I_MAIL}</i><div><span>E-posta</span><b>{e(SITE["email"])}</b></div></li>
<li><i>{I_PIN}</i><div><span>Adres</span><b>{e(SITE["address"])}</b></div></li></ul>
<div style="display:flex;flex-wrap:wrap;gap:10px"><a class="btn btn-red" href="{wa("Merhaba, LOTO ürünleri hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp’tan yaz</a>
<a class="btn btn-line" href="https://www.google.com/maps/search/?api=1&amp;query={quote(SITE["address"])}" target="_blank" rel="noopener">Haritada aç</a></div></div>'''

# ---------------------------------------------------------------- sayfalar
COLOR_ROLES = {c[0]: c[2] for c in COLORS}
def build_index():
    hero_imgs = [P("LT-PR-U07"), P("LT-G11"), P("LT-D01")]
    collage = "".join('<a href="%s" aria-label="%s">%s</a>' % (p["url"], e(p["name"]), img(p, lazy=False, alt="")) for p in hero_imgs)
    picker_group = GROUPS[("emniyet-asma-kilitleri", "Plastik Çene Emniyet Asma Kilidi 38 mm")]
    first = picker_group[0]
    dots = "".join('<button type="button" class="dot" style="background:%s" aria-pressed="%s" aria-label="%s" data-pick="%s" data-img="img/urunler/%s" data-url="%s" data-code="%s" data-color="%s" data-role="%s"></button>'
                   % (COLOR_HEX.get(p["color"], "#999"), "true" if i == 0 else "false", e(p["color"]), p["id"], (imgs(p) or [""])[0], p["url"], e(p["code"]), e(p["color"]), e(COLOR_ROLES.get(p["color"], "")))
                   for i, p in enumerate(picker_group))
    sets = [P(c) for c in ("LT-X02C", "LT-8773D", "LT-X07UN", "LT-PR-U07")]
    tab_cats = ["emniyet-asma-kilitleri", "salter-kilitleri", "vana-kilitleri", "coklandiricilar"]
    tabs = "".join('<button class="tab" type="button" role="tab" aria-selected="%s" data-tab="%s">%s</button>' % ("true" if i == 0 else "false", s, e(CAT[s]["name"])) for i, s in enumerate(tab_cats))
    tab_items = ""
    for i, s in enumerate(tab_cats):
        items = CAT[s]["items"]
        if s == "emniyet-asma-kilitleri":
            seen, pick = set(), []
            for p in items:
                if p["group"] not in seen: seen.add(p["group"]); pick.append(p)
            items = pick + [p for p in items if p not in pick]
        tab_items += "".join(pcard(p, s) for p in items[:8])
    steps = "".join('<div class="step"><span class="n">%02d</span><b>%s</b><p>%s</p></div>' % (i + 1, e(t), e(d)) for i, (t, d) in enumerate(STEPS))
    body = f'''<section class="hero"><div class="wrap">
<div class="hero-copy"><span class="hero-badge"><b>EKED</b>Kilitleme ve etiketleme ekipmanları</span>
<h1>Bakımdan önce enerjiyi kilitleyin. <span>Kes, kilitle, etiketle.</span></h1>
<p>Emniyet asma kilitlerinden şalter ve vana kilitlerine, LOTO istasyonlarından hazır setlere kadar {len(PROD)} ürün. Doğru kilidi seçmek için fotoğraf göndermeniz yeterli.</p>
<div class="hero-actions"><a class="btn btn-white" href="urunler.html">Ürünleri incele</a><a class="btn btn-ghost" href="{wa("Merhaba, LOTO ürünleri için teklif almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp’tan teklif al</a></div></div>
<div class="hero-card">{collage}
<div class="chip-float b"><i>{I_BOX}</i><div><b>{len(PROD)} ürün</b>{len(CATEGORIES)} ürün grubu</div></div>
<div class="chip-float a"><i>{I_SHIELD}</i><div><b>OSHA 29 CFR 1910.147</b>uyumlu LOTO ekipmanı</div></div></div>
</div><div class="tape"></div></section>
<section class="wrap"><div class="stats">
<div><b>{len(PROD)}</b><span>LOTO / EKED ürünü</span></div><div><b>{len(CATEGORIES)}</b><span>ürün grubu</span></div>
<div><b>8 renk</b><span>emniyet asma kilidi</span></div><div><b>Ümraniye</b><span>İstanbul’dan Türkiye geneline</span></div></div></section>
<section class="sec sec-soft"><div class="wrap"><div class="sec-head"><div><span class="kicker">Kategoriler</span><h2 class="t2">Ürün gruplarımız</h2></div>
<a class="btn btn-dark" href="urunler.html">Tüm ürünler</a></div>
<div class="cats">{"".join(cat_card(c, i + 1) for i, c in enumerate(CATEGORIES))}</div></div></section>
<section class="sec"><div class="wrap picker">
<div class="picker-img"><img id="pick-img" src="img/urunler/{(imgs(first) or [""])[0]}" alt="Emniyet asma kilidi renk seçenekleri" width="800" height="800"></div>
<div class="picker-tx"><span class="kicker">Renk kodlama</span><h2 class="t2">8 renk, tek standart.</h2>
<p class="lead">Kilit rengi sahada kimin çalıştığını bir bakışta gösterir. Bir renk seçin, o renkteki emniyet asma kilidini görün.</p>
<div class="dots" role="group" aria-label="Kilit rengi">{dots}</div>
<div class="picker-info" aria-live="polite"><b id="pick-name">{e(first["color"])} · {e(first["code"])}</b><span id="pick-role">Örnek kullanım: {e(COLOR_ROLES.get(first["color"], ""))}</span>
<a id="pick-link" href="{first["url"]}">Ürünü incele →</a></div></div></div></section>
<section class="sec sec-dark"><div class="wrap"><div class="sec-head"><div><span class="kicker">LOTO nasıl uygulanır?</span><h2 class="t2">7 adımda güvenli enerji izolasyonu</h2></div>
<a class="btn btn-white" href="loto-rehberi.html">Rehberin tamamı</a></div><div class="steps">{steps}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="kicker">Hazır setler</span><h2 class="t2">Tek pakette eksiksiz LOTO</h2></div>
<a class="btn btn-line" href="{cat_url("loto-setleri")}">Tüm setler</a></div><div class="grid">{"".join(pcard(p) for p in sets)}</div></div></section>
<section class="sec sec-soft"><div class="wrap"><div class="sec-head"><div><span class="kicker">Öne çıkanlar</span><h2 class="t2">En çok tercih edilen ürünler</h2></div></div>
<div class="tabs" role="tablist" aria-label="Kategoriye göre ürünler">{tabs}</div><div class="grid" id="tabgrid">{tab_items}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="kicker">Neden Lockout Turkey?</span><h2 class="t2">Ekipmandan fazlası</h2></div></div>
<div class="why"><div><i>{I_SHIELD}</i><b>Standartlara uygun</b><p>Ürünler OSHA 29 CFR 1910.147 ve iş güvenliği mevzuatının gerekliliklerine uygundur.</p></div>
<div><i>{I_CHAT}</i><b>Ürün seçim desteği</b><p>Hangi şaltere hangi kilit uyar? Fotoğrafını gönderin, doğru ekipmanı birlikte seçelim.</p></div>
<div><i>{I_TAG}</i><b>Kişiye özel</b><p>Renk kodlu kilitler, farklı / aynı / master anahtar sistemleri ve isim baskısı.</p></div>
<div><i>{I_DOC}</i><b>Kurumsal satış</b><p>Toplu alım ve setlerde size özel teklif, kurumsal faturalı satış.</p></div></div></div></section>
{cta()}
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="kicker">Blog</span><h2 class="t2">Güvenli çalışma notları</h2></div><a class="btn btn-line" href="blog.html">Tüm yazılar</a></div>
<div class="posts">{"".join(post_card(p) for p in POSTS[:3])}</div></div></section>
{faq(FAQ)}'''
    page("index.html", "Lockout Turkey | EKED / LOTO Kilitleme ve Etiketleme Ekipmanları",
         "Emniyet asma kilitleri, şalter, vana ve kablo kilitleri, çoklandırıcılar, LOTO istasyonları ve setleri. %d ürün, ürün seçim desteği ve hızlı teklif." % len(PROD), body, "./")

def side(active=None, filter_mode=False):
    if filter_mode:
        rows = '<button type="button" data-filter="tumu" aria-pressed="true">Tüm ürünler<span>%d</span></button>' % len(PROD)
        rows += "".join('<button type="button" data-filter="%s" aria-pressed="false">%s<span>%d</span></button>' % (c["slug"], e(c["name"]), len(c["items"])) for c in CATEGORIES)
    else:
        rows = '<a href="urunler.html">Tüm ürünler<span>%d</span></a>' % len(PROD)
        rows += "".join('<a href="%s"%s>%s<span>%d</span></a>' % (cat_url(c["slug"]), ' aria-current="page"' if c["slug"] == active else "", e(c["name"]), len(c["items"])) for c in CATEGORIES)
    return f'''<aside class="side" aria-label="Kategoriler"><span class="lbl">Kategoriler</span>{rows}
<a class="btn btn-red btn-sm dl" href="{CATALOG_PDF}" target="_blank" rel="noopener" style="justify-content:center">{I_DOC} Katalog (PDF)</a></aside>'''

def build_products():
    body = f'''{band([("", "Ürünler")], "Ürün kataloğu", "Tüm ürünler", "Ürün adı, kodu ya da kullanım noktasına göre arayın; kategoriye göre filtreleyin.")}
<section class="wrap shop">{side(filter_mode=True)}
<div class="shop-main"><label class="searchbar" for="urun-ara" id="ara">{I_SEARCH}<span class="sr-only">Ürün ara</span><input id="urun-ara" type="search" placeholder="Örn. LT-G01, vana, sigorta, çoklandırıcı" autocomplete="off"></label>
<span class="count" id="urun-sayi">{len(PROD)} ürün</span>
<div class="grid">{"".join(pcard(p) for c in CATEGORIES for p in c["items"])}</div>
<div class="empty" id="urun-bos" hidden><b>Bu aramayla eşleşen ürün yok.</b><p class="muted">Farklı bir kelime deneyin ya da noktanın fotoğrafını WhatsApp’tan gönderin.</p></div></div></section>
{cta()}'''
    page("urunler.html", "Tüm Ürünler", "Lockout Turkey EKED / LOTO ürün kataloğu: %d ürün, %d kategori." % (len(PROD), len(CATEGORIES)), body, "urunler.html")

def build_categories():
    for c in CATEGORIES:
        body = f'''{band([("urunler.html", "Ürünler"), ("", c["name"])], "%d ürün" % len(c["items"]), c["name"], c["intro"])}
<section class="wrap shop">{side(c["slug"])}
<div class="shop-main"><div class="grid">{"".join(pcard(p) for p in c["items"])}</div></div></section>
{cta()}'''
        page(cat_url(c["slug"]), c["name"], "%s: %s" % (c["name"], c["short"]), body, "urunler.html")

def build_product_pages():
    for p in PROD.values():
        c = CAT[p["cat"]]
        l = imgs(p)
        thumbs = "".join('<button type="button" class="thumb-btn" data-img="img/urunler/%s" aria-label="%d. görsel" aria-pressed="%s"><img src="img/urunler/%s" alt="" loading="lazy" width="160" height="160"></button>' % (im, k + 1, "true" if k == 0 else "false", im) for k, im in enumerate(l)) if len(l) > 1 else ""
        main = '<img id="pd-main" src="img/urunler/%s" alt="%s" width="800" height="800">' % (l[0], e(p["name"])) if l else ICON_LOCK
        sw = ""
        if p["group"]:
            sw = '<div><span class="kicker" style="margin-bottom:10px">Renk: %s</span><div class="swatches">%s</div></div>' % (e(p["color"]), "".join(
                '<a class="swatch" href="%s" title="%s" style="background:%s"%s><span class="sr-only">%s</span></a>' % (x["url"], e(x["code"] + " · " + x["color"]), COLOR_HEX.get(x["color"], "#999"), ' aria-current="true"' if x["id"] == p["id"] else "", e(x["color"])) for x in GROUPS[(p["cat"], p["group"])]))
        name = p["name"][len(p["code"]):].strip()
        rows = [("Ürün kodu", e(p["code"])), ("Kategori", '<a href="%s">%s</a>' % (cat_url(c["slug"]), e(c["name"])))]
        seen = {"model", "ürün kodu"}
        for k, v in p["specs"]:
            if k.lower() in seen: continue
            seen.add(k.lower()); rows.append((e(k), e(v)))
        if p["color"] and "renk" not in seen: rows.append(("Renk", e(p["color"])))
        spec = '<div class="table-scroll"><table class="spec"><tbody>' + "".join('<tr><th scope="row">%s</th><td>%s</td></tr>' % r for r in rows) + "</tbody></table></div>"
        feats = "".join("<li><span>%s</span></li>" % ("<b>%s:</b> %s" % (e(k), e(v)) if k else e(v)) for k, v in p["features"])
        tabs, panels = [], []
        def add(tid, label, content):
            sel = not tabs
            tabs.append('<button class="tab" type="button" role="tab" id="t-%s" aria-controls="p-%s" aria-selected="%s" data-ptab="%s">%s</button>' % (tid, tid, "true" if sel else "false", tid, label))
            panels.append('<div class="panel" role="tabpanel" id="p-%s" aria-labelledby="t-%s"%s>%s</div>' % (tid, tid, "" if sel else " hidden", content))
        if p["kit"]:
            add("set", "Set içeriği (%s)" % e(p["total"]) if p["total"] else "Set içeriği", '<ul class="kitlist">' + "".join("<li><b>%d×</b>%s</li>" % (q, e(n)) for q, n in p["kit"]) + "</ul>")
        detail = "".join('<p>%s</p>' % e(x) for x in p["intro"][:2])
        if feats: detail += '<ul class="feat" style="margin-top:20px">%s</ul>' % feats
        add("detay", "Ürün detayı", '<div class="prose" style="max-width:none">%s</div>' % detail if detail else "")
        add("teknik", "Teknik özellikler", spec)
        if p["pack"]: add("paket", "Paket içeriği", '<ul class="kitlist">' + "".join("<li>%s</li>" % e(x) for x in p["pack"]) + "</ul>")
        related = [x for x in c["items"] if x["id"] != p["id"] and (not p["group"] or x["group"] != p["group"])][:4]
        body = f'''<section class="ph-band" style="border-bottom:none;background:none"><div class="wrap" style="padding-block:20px 0">{crumbs(("urunler.html", "Ürünler"), (cat_url(c["slug"]), c["name"]), ("", p["code"]))}</div></section>
<section class="wrap pd"><div class="gal">{('<div class="thumbs">%s</div>' % thumbs) if thumbs else ''}<div class="main">{main}</div></div>
<div class="info"><span class="code" style="font-size:14px">{e(p["code"])}</span><h1>{e(name)}</h1><p class="lead">{e(p["short"])}</p>{sw}
<div class="buy"><div class="stepper"><button type="button" data-step="-1" data-target="#qty" aria-label="Adet azalt">−</button><label class="sr-only" for="qty">Adet</label><input id="qty" type="number" min="1" max="999" value="1" inputmode="numeric"><button type="button" data-step="1" data-target="#qty" aria-label="Adet arttır">+</button></div>
<button type="button" class="btn btn-red" data-add="{p["id"]}" data-qty-from="#qty">Teklif sepetine ekle</button>
<a class="btn btn-line" href="{wa("Merhaba, " + p["name"] + " hakkında bilgi / teklif almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp’tan sor</a></div>
<div class="badges"><span>OSHA uyumlu LOTO</span><span>Özelleştirilebilir</span><span>Ürün seçim desteği</span></div>
<p class="muted" style="font-size:15px">Kategori: <a href="{cat_url(c["slug"])}">{e(c["name"])}</a></p></div></section>
<section class="wrap pd-tabs"><div class="tabs" role="tablist" aria-label="Ürün bilgileri">{"".join(tabs)}</div>{"".join(panels)}</section>
<section class="sec sec-soft"><div class="wrap"><div class="sec-head"><div><span class="kicker">{e(c["name"])}</span><h2 class="t2">Benzer ürünler</h2></div><a class="btn btn-line" href="{cat_url(c["slug"])}">Tümünü gör</a></div>
<div class="grid">{"".join(pcard(x) for x in related)}</div></div></section>'''
        page(p["url"], p["name"], "%s. %s" % (p["name"], p["short"]), body, "urunler.html")

def build_about():
    body = f'''{band([("", "Kurumsal")], "Kurumsal · Lockout Turkey", "Biz kimiz?")}
<section class="sec"><div class="wrap two" style="align-items:center">
<div class="prose"><p style="font-size:20px;color:var(--ink)">Lockout Turkey, iş sağlığı ve güvenliği alanında kilitleme ve etiketleme (EKED / LOTO) ekipmanları sunan bir markadır. Bakım, onarım ve temizlik sırasında makinelerin beklenmedik şekilde çalışmasını önleyen ekipmanları işletmelere tek noktadan tedarik ediyoruz.</p>
<p>Temel hedefimiz; çalışan güvenliğini artırmak, iş kazalarını önlemek ve işletmelerin LOTO uygulamalarını doğru ekipmanla, uluslararası standartlara uygun şekilde kurmasına yardımcı olmaktır.</p>
<div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:8px"><a class="btn btn-red" href="urunler.html">Ürünlerimiz</a><a class="btn btn-line" href="{CATALOG_PDF}" target="_blank" rel="noopener">Katalog (PDF)</a></div></div>
<div class="hero-card" style="box-shadow:0 24px 60px rgba(20,20,20,.12)">{"".join('<a href="%s" aria-label="%s">%s</a>' % (x["url"], e(x["name"]), img(x, alt="")) for x in (P("LT-X02CY"), P("LT-G13"), P("LT-K42")))}</div></div></section>
<section class="wrap"><div class="stats"><div><b>{len(PROD)}</b><span>ürün çeşidi</span></div><div><b>{len(CATEGORIES)}</b><span>ürün grubu</span></div><div><b>8 renk</b><span>emniyet asma kilidi</span></div><div><b>OSHA</b><span>29 CFR 1910.147 uyumlu ürünler</span></div></div></section>
<section class="sec"><div class="wrap mv">
<div><span class="kicker" style="color:#FFFFFF">Misyon</span><h2>Misyonumuz</h2><p>İşletmelerin enerji izolasyonu ihtiyaçlarına doğru, dayanıklı ve kullanımı kolay kilitleme ve etiketleme çözümleri sunmak.</p><p>Her teklifte yalnızca ürünü değil, ürünün doğru noktada doğru şekilde kullanılmasını da önemsemek.</p></div>
<div><span class="kicker">Vizyon</span><h2>Vizyonumuz</h2><p>Türkiye’de LOTO ekipmanı denildiğinde akla gelen, ulaşılabilir ve güvenilir tedarikçilerden biri olmak.</p><p>LOTO uygulamalarını her ölçekteki işletmenin günlük bakım rutini haline getirmek.</p></div></div></section>
<section class="sec sec-soft"><div class="wrap"><div class="sec-head"><div><span class="kicker">Neye inanıyoruz</span><h2 class="t2">Değerlerimiz</h2></div></div>
<div class="why"><div><i>{I_SHIELD}</i><b>Güvenlik</b><p>Tüm işlerimizin merkezinde insan güvenliği yer alır.</p></div>
<div><i>{I_SEARCH}</i><b>Doğru ürün</b><p>Satıştan önce kilitlenecek noktayı anlarız; uymayan ürünü önermeyiz.</p></div>
<div><i>{I_CHAT}</i><b>Güvenilirlik</b><p>Müşterilerimizle ve iş ortaklarımızla uzun vadeli ilişkiler kurarız.</p></div>
<div><i>{I_BOX}</i><b>Hız</b><p>Teklif ve sevkiyatta hızlı dönüş, bakımın beklememesi demektir.</p></div></div></div></section>
<section class="sec"><div class="wrap two" style="align-items:center"><div><span class="kicker">Farkımız</span><h2 class="t2" style="margin:12px 0 22px">Neden Lockout Turkey?</h2>
<ul class="feat" style="grid-template-columns:1fr"><li><span>Kişisel kilitlerden LOTO istasyonlarına kadar {len(PROD)} ürün tek noktada</span></li><li><span>Fotoğraf ya da model bilgisiyle ürün seçim desteği</span></li>
<li><span>Renk, anahtar sistemi ve isim/numara baskısıyla kişiye özel kilitler</span></li><li><span>Kurumsal faturalı satış ve hızlı teklif</span></li></ul></div>
<p class="quote">Önce güvenlik anlayışıyla her gün daha güvenli çalışma alanları için çalışıyoruz. Bizim için her kilit, bir çalışanın güvencesidir.</p></div></section>
<section class="sec sec-soft"><div class="wrap"><div class="sec-head"><div><span class="kicker">Ürünler</span><h2 class="t2">Ürün kategorilerimiz</h2></div></div>
<div class="cats">{"".join(cat_card(c, i + 1) for i, c in enumerate(CATEGORIES))}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="kicker">İletişim</span><h2 class="t2">Size destek olmak için buradayız.</h2></div></div>
<div class="two">{contact_form()}{info_card("Merkez")}</div></div></section>'''
    page("kurumsal.html", "Kurumsal", "Lockout Turkey hakkında: biz kimiz, misyonumuz, vizyonumuz ve değerlerimiz.", body, "kurumsal.html")

def build_guide():
    steps = "".join('<div class="step"><span class="n">%02d</span><b>%s</b><p>%s</p></div>' % (i + 1, e(t), e(d)) for i, (t, d) in enumerate(STEPS))
    body = f'''{band([("", "LOTO Rehberi")], "LOTO rehberi", "Kilitleme ve etiketleme, adım adım.", "EKED prosedürünün temel adımları, kilit kuralları ve mevzuat özeti.")}
<section class="sec"><div class="wrap"><article class="prose">
<h2 style="margin-top:0">EKED / LOTO nedir?</h2>
<p>EKED; Enerji Kesme, Kilitleme, Etiketleme ve Doğrulama adımlarının kısaltmasıdır. Uluslararası literatürde Lockout / Tagout (LOTO) olarak bilinir. Amaç, bakım, onarım, temizlik ya da ayar sırasında makinenin beklenmedik şekilde çalışmasını ve içinde kalan enerjinin açığa çıkmasını önlemektir.</p>
<p>Kilit enerjiyi fiziksel olarak keser; etiket ise kimin, ne zaman ve neden kilitlediğini gösterir. Etiket tek başına kilidin yerini tutmaz.</p>
<h2>Hangi enerjiler kilitlenir?</h2>
<ul><li><b>Elektrik:</b> panolar, şalterler, sigortalar, fişler</li><li><b>Akışkan:</b> su, buhar, gaz ve kimyasal hatlarındaki vanalar</li><li><b>Pnömatik ve hidrolik:</b> basınçlı hava ve yağ hatları</li><li><b>Mekanik:</b> yay gerilimi, yükseltilmiş parçalar, dönen kütleler</li><li><b>Termal:</b> sıcak yüzeyler ve akışkanlar</li></ul></article></div></section>
<section class="sec sec-dark"><div class="wrap"><div class="sec-head"><div><span class="kicker">Prosedür</span><h2 class="t2">7 adım</h2></div></div><div class="steps">{steps}</div>
<p class="lead" style="margin-top:28px">İş bitince enerji ters sırayla verilir: alan kontrol edilir, çalışanlar uzaklaştırılır, her kişi kendi kilidini kendisi çıkarır ve ilgili herkes bilgilendirilir.</p></div></section>
<section class="sec"><div class="wrap"><article class="prose">
<h2 style="margin-top:0">Kilit kuralları</h2>
<ul><li><b>Bir kişi, bir kilit, bir anahtar.</b> Her çalışan kendi kişisel kilidini takar; anahtarı yalnızca kendisinde durur.</li><li>Emniyet asma kilitleri yalnızca LOTO için kullanılır; dolap ya da kapı kilidi olarak kullanılmaz.</li><li>Kilidi yalnızca takan kişi çıkarır. Kişi yerinde değilse yazılı bir kilit çıkarma prosedürü uygulanır.</li><li>Renk kodu, kilidin hangi departmana ya da ekibe ait olduğunu uzaktan gösterir.</li></ul>
<h2>Grup kilitleme</h2>
<p>Çok sayıda kişinin çok sayıda noktada çalıştığı işlerde yetkili kişi tüm izolasyon noktalarını aynı anahtarlı ortak kilitlerle kilitler, anahtarları grup kilitleme kutusuna koyar. Her çalışan kutuya kendi kilidini takar; son kilit çıkmadan anahtarlara ulaşılamaz. <a href="{cat_url("grup-kilitleme-kutulari-ve-cantalar")}">Grup kilitleme kutularını inceleyin.</a></p>
<h2>Mevzuat</h2>
<p>LOTO prosedürlerinin temel referansı ABD İş Güvenliği ve Sağlığı İdaresi'nin <b>OSHA 29 CFR 1910.147</b> standardıdır. Türkiye'de <b>6331 sayılı İş Sağlığı ve Güvenliği Kanunu</b> işverene risk değerlendirmesi yapma ve tehlikelere karşı önlem alma yükümlülüğü getirir; bakım ve onarım sırasında tehlikeli enerjinin kontrolü bu önlemlerin başında gelir.</p>
<p class="muted" style="font-size:16px">Bu sayfa genel bilgilendirme amaçlıdır; tesisinize özel prosedür iş güvenliği uzmanınızla birlikte hazırlanmalıdır.</p></article></div></section>
{faq(FAQ)}{cta()}'''
    page("loto-rehberi.html", "LOTO Rehberi", "EKED / LOTO nedir, hangi enerjiler kilitlenir, 7 adımlık prosedür, kilit kuralları, grup kilitleme ve mevzuat.", body, "loto-rehberi.html")

def build_blog():
    first = POSTS[0]
    body = f'''{band([("", "Blog")], "Blog", "Güvenli çalışma notları", "Ürün seçimi, prosedür ve saha uygulamaları hakkında kısa ve uygulanabilir yazılar.")}
<section class="sec"><div class="wrap"><div class="posts">{"".join(post_card(p) for p in POSTS[:6])}</div>
{('<div class="posts" style="margin-top:18px">%s</div>' % "".join(post_card(p) for p in POSTS[6:])) if len(POSTS) > 6 else ''}</div></section>{cta()}'''
    page("blog.html", "Blog", "Lockout Turkey blog: LOTO ürün seçimi, prosedür ve saha uygulamaları.", body, "blog.html")
    for p in POSTS:
        others = [x for x in POSTS if x is not p][:3]
        prods = [P(c) for c in p["products"]][:4]
        body = f'''<section class="ph-band"><div class="wrap" style="max-width:920px">{crumbs(("blog.html", "Blog"), ("", p["title"]))}
<div class="meta"><span class="tg">{e(p["tag"])}</span><span>{tr_date(p["date"])}</span><span>{p["minutes"]} dk okuma</span></div>
<h1 class="t1" style="font-size:clamp(34px,4vw,52px)">{e(p["title"])}</h1><p class="lead">{e(p["summary"])}</p></div></section>
<section class="sec" style="padding-top:48px"><div class="wrap" style="max-width:920px"><div class="prose">{render_body(p["body"])}</div>
<div class="card card-soft" style="margin-top:36px;max-width:74ch"><b class="t3">Doğru ürünü birlikte seçelim</b><span class="muted">Kilitleyeceğiniz noktanın fotoğrafını gönderin, uygun ekipmanı bildirelim.</span>
<a class="btn btn-red" style="align-self:flex-start" href="{wa("Merhaba, " + p["title"] + " yazınızı okudum, bilgi almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp’tan yazın</a></div></div></section>
<section class="sec sec-soft"><div class="wrap"><div class="sec-head"><div><span class="kicker">Yazıda geçen ürünler</span><h2 class="t2">İlgili ürünler</h2></div></div><div class="grid">{"".join(pcard(x) for x in prods)}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="kicker">Blog</span><h2 class="t2">Diğer yazılar</h2></div><a class="btn btn-line" href="blog.html">Tüm yazılar</a></div><div class="posts">{"".join(post_card(x) for x in others)}</div></div></section>'''
        page(post_url(p), p["title"], p["summary"], body, "blog.html")

def build_contact():
    body = f'''{band([("", "İletişim")], "İletişim", "Size destek olmak için buradayız.", "Ürün kodu, fotoğraf ya da sadece ihtiyacınızı yazın; size dönüş yapalım.")}
<section class="sec"><div class="wrap two">{contact_form()}{info_card()}</div></section>'''
    page("iletisim.html", "İletişim", "Lockout Turkey iletişim bilgileri: telefon, WhatsApp, e-posta ve adres.", body, "iletisim.html")

def build_cart():
    body = f'''{band([("", "Teklif sepeti")], "Teklif sepeti", "Teklif sepetiniz", "Adetleri düzenleyin, bilgilerinizi ekleyin; listeyi WhatsApp ya da e-posta ile gönderin.")}
<section class="sec"><div class="wrap">
<div class="empty" id="teklif-bos"><b class="t3">Sepetiniz boş.</b><p class="muted">Ürün sayfalarından ya da kategori listelerinden ürün ekleyebilirsiniz.</p><a class="btn btn-red" href="urunler.html">Ürünlere göz at</a></div>
<div class="two" id="teklif-root" hidden>
<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;gap:12px"><h2 class="t3">Ürünler</h2><button class="btn btn-line btn-sm" type="button" id="teklif-temizle">Sepeti temizle</button></div><div id="teklif-satir"></div><a href="urunler.html" style="font-weight:700">+ Ürün ekle</a></div>
<form class="card card-soft" id="teklif-form" novalidate><h2 class="t3">Bilgileriniz</h2>
<div class="field"><label for="t-firma">Firma</label><input id="t-firma" name="firma" autocomplete="organization"></div>
<div class="fields-2"><div class="field"><label for="t-ad">Ad Soyad</label><input id="t-ad" name="ad" autocomplete="name"></div><div class="field"><label for="t-tel">Telefon</label><input id="t-tel" name="telefon" type="tel" autocomplete="tel"></div></div>
<div class="fields-2"><div class="field"><label for="t-mail">E-posta</label><input id="t-mail" name="eposta" type="email" autocomplete="email"></div><div class="field"><label for="t-sehir">Şehir</label><input id="t-sehir" name="sehir" autocomplete="address-level1"></div></div>
<div class="field"><label for="t-not">Not</label><textarea id="t-not" name="not" placeholder="Renk, anahtar sistemi, baskı isteği…"></textarea></div>
<button class="btn btn-red" type="submit" style="align-self:flex-start">Teklif talebini hazırla</button>
<div class="output-box" id="teklif-cikti" hidden><p class="notice">Talebiniz hazır. WhatsApp ya da e-posta ile gönderin; açılmazsa metni kopyalayıp yapıştırın.</p>
<label class="sr-only" for="teklif-metin">Talep metni</label><textarea id="teklif-metin" readonly></textarea>
<div style="display:flex;flex-wrap:wrap;gap:10px"><a class="btn btn-dark" id="teklif-wa" href="#" target="_blank" rel="noopener">WhatsApp ile gönder</a><a class="btn btn-line" id="teklif-mail" href="#">E-posta ile gönder</a><button class="btn btn-line" type="button" data-copy="#teklif-metin">Metni kopyala</button></div></div></form></div></div></section>'''
    page("teklif.html", "Teklif Sepeti", "Seçtiğiniz LOTO ürünleri için teklif talebi oluşturun.", body, "")

def build_kvkk():
    owner = SITE.get("legal_name") or SITE["brand"]
    body = f'''{band([("", "KVKK ve gizlilik")], "Yasal", "KVKK ve gizlilik")}
<section class="sec"><div class="wrap"><article class="prose">
<p>6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında kişisel verilerinizin nasıl işlendiğini aşağıda bulabilirsiniz.</p>
<h2>Veri sorumlusu</h2><p>Kişisel verileriniz, veri sorumlusu sıfatıyla {e(owner)}, {e(SITE["address"])} tarafından işlenmektedir. İletişim: {e(SITE["email"])}</p>
<h2>İşlenen kişisel veriler</h2><p>Teklif, iletişim ve bilgi talepleriniz sırasında bize ilettiğiniz ad soyad, firma adı, telefon numarası, e-posta adresi, şehir ve mesaj içeriği.</p>
<h2>İşleme amaçları</h2><ul><li>Teklif ve bilgi taleplerinizi yanıtlamak, sizinle iletişime geçmek</li><li>Sipariş, satış ve teslimat süreçlerini yürütmek</li><li>Fatura düzenlemek ve yasal yükümlülükleri yerine getirmek</li></ul>
<h2>Toplama yöntemi ve hukuki sebep</h2><p>Verileriniz; sitedeki formlar aracılığıyla hazırlanıp sizin tarafınızdan WhatsApp veya e-posta ile gönderilen mesajlar ve telefon görüşmeleri yoluyla toplanır. Kanun'un 5. maddesindeki bir sözleşmenin kurulması veya ifasıyla doğrudan ilgili olması, hukuki yükümlülüğün yerine getirilmesi ve meşru menfaat hukuki sebeplerine dayanılarak işlenir.</p>
<h2>Aktarım</h2><p>Kişisel verileriniz, yasal zorunluluklar dışında üçüncü kişilerle paylaşılmaz; yalnızca kargo, muhasebe ve mali müşavirlik gibi hizmetlerin yürütülmesi için gerekli olduğu ölçüde ilgili hizmet sağlayıcılara aktarılabilir.</p>
<h2>Haklarınız</h2><p>Kanun'un 11. maddesi uyarınca verilerinizin işlenip işlenmediğini öğrenme, bilgi talep etme, düzeltilmesini veya silinmesini isteme, aktarıldığı kişileri öğrenme ve işlemeye itiraz etme haklarına sahipsiniz. Taleplerinizi {e(SITE["email"])} adresine iletebilirsiniz.</p>
<h2>Çerezler ve tarayıcı depolama</h2><p>Bu site reklam veya takip çerezi kullanmaz. Yazı tipleri Google Fonts üzerinden yüklenir. Teklif sepetiniz yalnızca kendi tarayıcınızda saklanır ve siz göndermedikçe bize ulaşmaz.</p>
</article></div></section>'''
    page("kvkk.html", "KVKK ve Gizlilik", "Lockout Turkey KVKK aydınlatma metni ve gizlilik bilgileri.", body, "")

def write_assets():
    shutil.copy(os.path.join(HERE, "style.css"), os.path.join(OUT, "style.css"))
    shutil.copy(os.path.join(HERE, "app.js"), os.path.join(OUT, "app.js"))
    shutil.copy(os.path.join(HERE, "extra.js"), os.path.join(OUT, "extra.js"))
    data = {"site": {k: SITE[k] for k in ("whatsapp_num", "email")}, "icons": {},
            "products": {i: {"name": p["name"], "code": p["code"], "cat": CAT[p["cat"]]["name"], "url": p["url"], "img": (imgs(p) or [""])[0]} for i, p in PROD.items()},
            "points": [], "refs": {}}
    open(os.path.join(OUT, "data.js"), "w", encoding="utf-8").write("window.BOSS = " + json.dumps(data, ensure_ascii=False) + ";\n")
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="16" fill="#D0121F"/><path d="M11.5 14.5V11a4.5 4.5 0 0 1 9 0v3.5" fill="none" stroke="#fff" stroke-width="2.8" stroke-linecap="round"/><rect x="8" y="13.5" width="16" height="12" rx="3" fill="#fff"/></svg>')
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE["domain"])
    today = date.today().isoformat()
    urls = "".join("<url><loc>%s/%s</loc><lastmod>%s</lastmod></url>" % (SITE["domain"], "" if p == "index.html" else p, today) for p in PAGES if p != "teklif.html")
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>' % urls)

if __name__ == "__main__":
    os.makedirs(IMG_DIR, exist_ok=True)
    for name in os.listdir(OUT):
        if name in KEEP: continue
        path = os.path.join(OUT, name)
        shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
    build_index(); build_products(); build_categories(); build_product_pages(); build_about(); build_guide()
    build_blog(); build_contact(); build_cart(); build_kvkk(); write_assets()
    print("%d sayfa üretildi → %s" % (len(PAGES), os.path.normpath(OUT)))
