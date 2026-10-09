# -*- coding: utf-8 -*-
"""Ürün kataloğu PDF'i üretir: python3 catalog_pdf.py  →  ../site/lockout-turkey-katalog.pdf
Önce build.py çalıştırılmış olmalı (ürün görselleri ../site/img/urunler altında)."""
import json, os, html, subprocess, tempfile, shutil
from datetime import date
from PIL import Image
from data import SITE, CATEGORIES

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.join(HERE, "..", "site")
IMG = os.path.join(SITE_DIR, "img", "urunler")
OUT = os.path.join(SITE_DIR, "lockout-turkey-katalog.pdf")
e = html.escape

cat = json.load(open(os.path.join(HERE, "catalog.json"), encoding="utf-8"))
by = {c["slug"]: [] for c in CATEGORIES}
import re
def nat(p): return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", p["code"])]
for p in sorted(cat, key=nat): by[p["cat"]].append(p)

work = tempfile.mkdtemp()
thumbs = os.path.join(work, "t"); os.makedirs(thumbs)
def thumb(p):
    if not p["images"]: return ""
    src = os.path.join(IMG, p["images"][0])
    if not os.path.exists(src): return ""
    dst = os.path.join(thumbs, p["id"] + ".jpg")
    Image.open(src).convert("RGB").resize((420, 420), Image.LANCZOS).save(dst, quality=80)
    return "file://" + dst

LOGO = ('<span class="wm"><span class="wm-top">LOCK<svg class="wm-o" viewBox="0 0 72 108"><path d="M18 34 V24 a18 18 0 0 1 36 0 V34" '
        'fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round"/><rect x="2" y="31" width="68" height="77" rx="12" fill="#C8102E"/>'
        '<circle cx="36" cy="62" r="7" fill="var(--kh)"/><rect x="33" y="64" width="6" height="18" rx="2" fill="var(--kh)"/></svg>UT</span>'
        '<span class="wm-bot"><i></i><span>TURKEY</span><i></i></span></span>')

pages = []
def foot(n):
    return ('<div class="foot"><span>Lockout Turkey · %s · %s</span><span>%d</span></div>'
            % (e(SITE["domain"].replace("https://", "")), e(SITE["phone"]), n))

def card(p):
    name = p["name"][len(p["code"]):].strip()
    lines = []
    if p["kit"]:
        if p["total"]: lines.append("Set içeriği: " + p["total"])
        lines += ["%d × %s" % (q, n) for q, n in p["kit"][:2]]
    else:
        for k, v in p["specs"]:
            if k.lower() in ("model", "ürün kodu"): continue
            lines.append("%s: %s" % (k, v))
            if len(lines) == 3: break
    lines = [l if len(l) < 56 else l[:53].rsplit(" ", 1)[0] + "…" for l in lines]
    src = thumb(p)
    img = '<img src="%s">' % src if src else ""
    return ('<div class="card"><div class="im">%s</div><div class="cd">%s</div><div class="nm">%s</div><ul>%s</ul></div>'
            % (img, e(p["code"]), e(name), "".join("<li>%s</li>" % e(l) for l in lines)))

# kapak
pages.append(f'''<section class="page cover"><div class="cover-top">{LOGO}</div>
<div class="cover-mid"><span class="eyebrow">EKED / LOTO · KİLİTLEME VE ETİKETLEME EKİPMANLARI</span>
<h1>Ürün<br>Kataloğu</h1><p>{len(cat)} ürün · {len(CATEGORIES)} ürün grubu · {date.today().year}</p></div>
<div class="cover-bot"><div><b>{e(SITE["phone"])}</b><span>Telefon / WhatsApp</span></div><div><b>{e(SITE["email"])}</b><span>E-posta</span></div>
<div><b>{e(SITE["domain"].replace("https://", ""))}</b><span>Web</span></div></div></section>''')

# içindekiler
n = 2
toc = "".join('<li><span>%s</span><i></i><b>%d ürün</b></li>' % (e(c["name"]), len(by[c["slug"]])) for c in CATEGORIES)
pages.append(f'''<section class="page"><div class="hd"><span class="eyebrow">İÇİNDEKİLER</span><h2>Ürün grupları</h2></div>
<ol class="toc">{toc}</ol>
<div class="howto"><h3>Nasıl teklif alırım?</h3><p>Katalogdaki ürün kodlarını (ör. LT-G01) adetleriyle birlikte WhatsApp ya da e-posta ile iletmeniz yeterli. Kilitlenecek noktanın fotoğrafını gönderirseniz uygun ürünü biz belirleriz. Kişisel kilitlerde renk, anahtar sistemi ve isim/numara baskısı seçenekleri sunulur.</p>
<p><b>{e(SITE["phone"])}</b> · <b>{e(SITE["email"])}</b> · {e(SITE["address"])}</p></div>{foot(n)}</section>''')

PER_FIRST, PER = 6, 9
for c in CATEGORIES:
    items = by[c["slug"]]
    chunks = [items[:PER_FIRST]] + [items[i:i + PER] for i in range(PER_FIRST, len(items), PER)]
    for k, ch in enumerate(chunks):
        if not ch: continue
        n += 1
        head = ""
        if k == 0:
            head = '<div class="cat-hd"><span class="eyebrow">%d ÜRÜN</span><h2>%s</h2><p>%s</p></div>' % (len(items), e(c["name"]), e(c["intro"]))
        else:
            head = '<div class="cat-run">%s <span>· devam</span></div>' % e(c["name"])
        pages.append('<section class="page">%s<div class="grid">%s</div>%s</section>' % (head, "".join(card(p) for p in ch), foot(n)))

n += 1
pages.append(f'''<section class="page back"><div>{LOGO}</div>
<div class="back-mid"><h2>Doğru kilidi birlikte seçelim.</h2><p>Kilitleme noktalarınızın fotoğrafını gönderin; nokta başına ekipman listesini hazırlayıp teklifinizi iletelim.</p></div>
<div class="cover-bot"><div><b>{e(SITE["phone"])}</b><span>Telefon / WhatsApp</span></div><div><b>{e(SITE["email"])}</b><span>E-posta</span></div>
<div><b>{e(SITE["address"])}</b><span>Adres</span></div></div></section>''')

CSS = '''
@page { size: A4; margin: 0; }
:root { --red: #C8102E; --ink: #1A1414; --muted: #5E5651; --line: #E2DBD4; --ground: #F6F4F1; --kh: #F6F4F1; }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Barlow', Arial, sans-serif; color: var(--ink); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; padding: 16mm 14mm 20mm; position: relative; overflow: hidden; page-break-after: always; background: #FFFFFF; display: flex; flex-direction: column; gap: 7mm; }
.eyebrow { font-family: 'IBM Plex Mono', monospace; font-size: 8.5pt; font-weight: 600; letter-spacing: .12em; color: var(--red); }
h1, h2, h3 { font-family: 'Barlow Condensed', Arial, sans-serif; font-weight: 700; margin: 0; }
.wm { display: inline-flex; flex-direction: column; gap: .14em; font-family: 'Archivo', sans-serif; font-size: 30pt; color: var(--ink); }
.wm-top { display: flex; align-items: baseline; font-weight: 900; font-stretch: 110%; letter-spacing: -.02em; line-height: 1; }
.wm-o { width: .643em; height: .964em; margin: 0 .03em; }
.wm-bot { display: flex; align-items: center; gap: .16em; }
.wm-bot i { flex: 1; height: .045em; background: var(--red); }
.wm-bot span { font-size: .232em; font-weight: 700; font-stretch: 110%; letter-spacing: .85em; margin-right: -.85em; line-height: 1; }
.cover, .back { background: var(--ink); color: #FFFFFF; justify-content: space-between; padding: 22mm 18mm; --kh: #1A1414; }
.cover .wm, .back .wm { color: #FFFFFF; font-size: 40pt; }
.cover-mid { display: flex; flex-direction: column; gap: 8mm; border-left: 3mm solid var(--red); padding-left: 8mm; }
.cover-mid .eyebrow { color: #F2B8B5; }
.cover h1 { font-size: 96pt; line-height: .88; }
.cover-mid p { margin: 0; font-size: 14pt; color: #D9D0C9; }
.cover-bot { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6mm; border-top: 1px solid #4A3F3B; padding-top: 7mm; }
.cover-bot div { display: flex; flex-direction: column; gap: 1.5mm; }
.cover-bot b { font-size: 12pt; }
.cover-bot span { font-family: 'IBM Plex Mono', monospace; font-size: 7.5pt; letter-spacing: .12em; color: #B9AEA6; text-transform: uppercase; }
.back-mid h2 { font-size: 48pt; line-height: .95; }
.back-mid p { font-size: 14pt; color: #D9D0C9; max-width: 140mm; }
.hd h2 { font-size: 40pt; margin-top: 2mm; }
.toc { list-style: none; margin: 0; padding: 0; border-top: 2px solid var(--ink); }
.toc li { display: flex; align-items: baseline; gap: 4mm; padding: 4.2mm 0; border-bottom: 1px solid var(--line); font-size: 14pt; }
.toc li span { font-family: 'Barlow Condensed', sans-serif; font-weight: 700; font-size: 17pt; }
.toc li i { flex: 1; border-bottom: 1px dotted #CFC4BA; }
.toc li b { font-family: 'IBM Plex Mono', monospace; font-size: 10pt; color: var(--red); }
.howto { margin-top: auto; background: var(--ground); border-radius: 4mm; padding: 7mm; display: flex; flex-direction: column; gap: 3mm; font-size: 11pt; line-height: 1.5; }
.howto h3 { font-size: 20pt; }
.howto p { margin: 0; }
.cat-hd { display: flex; flex-direction: column; gap: 2mm; padding-bottom: 5mm; border-bottom: 2px solid var(--ink); }
.cat-hd h2 { font-size: 34pt; line-height: 1; }
.cat-hd p { margin: 0; font-size: 10.5pt; line-height: 1.45; color: var(--muted); max-width: 165mm; }
.cat-run { font-family: 'Barlow Condensed', sans-serif; font-weight: 700; font-size: 16pt; padding-bottom: 3mm; border-bottom: 2px solid var(--ink); }
.cat-run span { color: var(--muted); font-weight: 500; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); grid-auto-rows: 79mm; gap: 5mm; }
.card { border: 1px solid var(--line); border-radius: 3mm; padding: 3mm; display: flex; flex-direction: column; gap: 1.4mm; overflow: hidden; }
.card .im { height: 40mm; display: flex; align-items: center; justify-content: center; }
.card .im img { max-width: 100%; max-height: 100%; }
.card .cd { font-family: 'IBM Plex Mono', monospace; font-size: 8.5pt; font-weight: 600; color: var(--red); margin-top: 1mm; }
.card .nm { font-family: 'Barlow Condensed', sans-serif; font-weight: 700; font-size: 11.5pt; line-height: 1.08; }
.card ul { margin: 0; padding: 0; list-style: none; font-size: 7.6pt; line-height: 1.35; color: var(--muted); }
.foot { position: absolute; left: 14mm; right: 14mm; bottom: 9mm; display: flex; justify-content: space-between; font-family: 'IBM Plex Mono', monospace; font-size: 7.5pt; color: #8A7F77; border-top: 1px solid var(--line); padding-top: 3mm; }
'''
doc = ('<!doctype html><html lang="tr"><head><meta charset="utf-8">'
       '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,800..900&family=Barlow+Condensed:wght@500;700&family=Barlow:wght@400;600&family=IBM+Plex+Mono:wght@500;600&display=swap">'
       '<style>%s</style></head><body>%s</body></html>' % (CSS, "".join(pages)))
html_path = os.path.join(work, "katalog.html")
open(html_path, "w", encoding="utf-8").write(doc)
js = os.path.join(work, "pdf.js")
open(js, "w").write("""const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
 await p.goto('file://%s', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
 await p.pdf({ path: '%s', format: 'A4', printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } }); await b.close(); })();""" % (html_path, os.path.abspath(OUT)))
env = dict(os.environ)
env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
subprocess.run(["node", js], check=True, env=env)
shutil.rmtree(work)
print("%d sayfa → %s (%.1f MB)" % (n, os.path.normpath(OUT), os.path.getsize(OUT) / 1e6))
