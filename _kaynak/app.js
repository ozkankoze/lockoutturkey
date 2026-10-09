/* Lockout Turkey — teklif listesi, nokta seçici, set oluşturucu, filtreler */
(function () {
  'use strict';
  var D = window.BOSS || { products: {}, points: [], site: {} };
  var KEY = 'lockoutTurkeyTeklif';
  var R = D.refs || {};
  var cart = null;

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  /* ---------- Teklif listesi ---------- */
  function load() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || '[]'); return Array.isArray(v) ? v : []; }
    catch (e) { return []; }
  }
  function getCart() { if (cart === null) cart = load(); return cart; }
  function save(c) {
    cart = c;
    try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) { /* depolama kapalı */ }
    renderCount();
    if ($('#teklif-root')) renderCartPage();
  }
  function addItems(items) {
    var c = getCart().slice();
    items.forEach(function (it) {
      var key = it.id || it.name;
      var found = c.filter(function (x) { return x.key === key; })[0];
      if (found) found.qty += it.qty || 1;
      else c.push({ key: key, id: it.id || '', name: it.name, qty: it.qty || 1 });
    });
    save(c);
    var n = items.length;
    toast(n === 1 ? items[0].name + ' listeye eklendi' : n + ' ürün listeye eklendi');
  }
  function renderCount() {
    var n = getCart().length;
    $$('[data-cart-count]').forEach(function (el) { el.textContent = n; });
  }

  var toastEl, toastTimer;
  function toast(msg) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'toast';
      toastEl.setAttribute('role', 'status');
      document.body.appendChild(toastEl);
    }
    toastEl.innerHTML = '<span>' + esc(msg) + '</span><a href="teklif.html">Listeyi gör</a>';
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 3200);
  }

  function productName(id) { return (D.products[id] && D.products[id].name) || id; }
  function productUrl(id) { return id && D.products[id] ? D.products[id].url : ''; }

  /* Tıklama yönetimi */
  document.addEventListener('click', function (e) {
    var add = e.target.closest('[data-add]');
    if (add) {
      e.preventDefault();
      var id = add.getAttribute('data-add');
      var qty = 1;
      var qSel = add.getAttribute('data-qty-from');
      if (qSel && $(qSel)) qty = Math.max(1, parseInt($(qSel).value, 10) || 1);
      addItems([{ id: id, name: productName(id), qty: qty }]);
      return;
    }
    var step = e.target.closest('[data-step]');
    if (step) {
      var input = $(step.getAttribute('data-target'));
      if (input) {
        var v = (parseInt(input.value, 10) || 1) + parseInt(step.getAttribute('data-step'), 10);
        input.value = Math.min(999, Math.max(1, v));
      }
      return;
    }
    var th = e.target.closest('.thumb-btn');
    if (th) {
      var main = $('#pd-main');
      if (main) main.src = th.getAttribute('data-img');
      $$('.thumb-btn').forEach(function (b) { b.setAttribute('aria-pressed', b === th ? 'true' : 'false'); });
      return;
    }
    var tog = e.target.closest('[data-nav-toggle]');
    if (tog) {
      var h = $('.header');
      var open = h.classList.toggle('open');
      tog.setAttribute('aria-expanded', open ? 'true' : 'false');
      return;
    }
    var copy = e.target.closest('[data-copy]');
    if (copy) {
      var src = $(copy.getAttribute('data-copy'));
      if (!src) return;
      var text = src.value || src.textContent;
      var done = function () { var t = copy.textContent; copy.textContent = 'Kopyalandı'; setTimeout(function () { copy.textContent = t; }, 1600); };
      try {
        navigator.clipboard.writeText(text).then(done, function () { src.select && src.select(); });
      } catch (err) { src.select && src.select(); }
    }
  });

  /* ---------- Nokta seçici (kroki) ---------- */
  function initFinder() {
    var root = $('#kroki');
    if (!root) return;
    var panel = $('#nokta-panel');
    var current = D.points[0];
    function show(id) {
      current = D.points.filter(function (p) { return p.id === id; })[0] || D.points[0];
      $$('.hot, .pt-chip').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-point') === current.id ? 'true' : 'false'); });
      $('[data-f="meta"]', panel).textContent = 'Nokta ' + current.no + ' · ' + current.zone;
      $('[data-f="energy"]', panel).textContent = current.energy;
      $('[data-f="name"]', panel).textContent = current.name;
      $('[data-f="tip"]', panel).textContent = current.tip;
      $('[data-f="list"]', panel).innerHTML = current.products.map(function (id) {
        var p = D.products[id];
        return '<a class="panel-item" href="' + esc(p.url) + '"><span class="thumb">' + (p.img ? '<img src="img/urunler/' + esc(p.img) + '" alt="" loading="lazy">' : (D.icons[p.icon] || '')) + '</span><span><b>' + esc(p.name) + '</b><small>' + esc(p.code + ' · ' + p.cat) + '</small></span></a>';
      }).join('');
    }
    $$('.pt-chip').forEach(function (c) { c.addEventListener('click', function () { show(c.getAttribute('data-point')); if (window.innerWidth < 760) panel.scrollIntoView({ behavior: 'smooth', block: 'start' }); }); });
    root.addEventListener('click', function (e) {
      var b = e.target.closest('.hot');
      if (b) show(b.getAttribute('data-point'));
    });
    $('[data-f="add"]', panel).addEventListener('click', function () {
      addItems(current.products.map(function (id) { return { id: id, name: productName(id), qty: 1 }; }));
    });
    show(current.id);
  }

  /* ---------- Set oluşturucu ---------- */
  var ENERGY = [
    { id: 'elektrik', label: 'Pano / şalter', hint: 'Sigorta, MCCB, kaçak akım', ref: 'elektrik', item: 'Şalter / devre kesici kilidi' },
    { id: 'vana', label: 'Vana', hint: 'Küresel, kelebek, sürgülü', ref: 'vana', item: 'Vana kilidi' },
    { id: 'pnomatik', label: 'Basınçlı hava', hint: 'Hızlı bağlantı, kaplin', ref: 'pnomatik', item: 'Pnömatik / fiş kilidi' },
    { id: 'fis', label: 'Elektrik fişi', hint: 'Prizli makineler', ref: 'fis', item: 'Elektrik fişi kilidi' },
    { id: 'kablo', label: 'Standart dışı nokta', hint: 'Redüktörlü vana, vana grubu', ref: 'kablo', item: 'Ayarlanabilir kablo kilidi' }
  ];
  var KEYS = {
    farkli: { label: 'Farklı anahtar', note: 'Her kilidin kendi anahtarı olur; kilidi yalnızca takan kişi açabilir. Kişisel kilitler için standart seçimdir.' },
    ayni: { label: 'Aynı anahtar', note: 'Bir gruptaki tüm kilitler tek anahtarla açılır. Grup kilitleme kutusundaki ortak kilitler için uygundur, kişisel kilitlerde kullanılmaz.' },
    master: { label: 'Master anahtar', note: 'Her kilit farklı anahtarlıdır, ayrıca tek bir yetkili anahtar hepsini açar. Master anahtarın kullanımı yazılı acil durum prosedürüne bağlanmalıdır.' }
  };

  function initBuilder() {
    var root = $('#kit');
    if (!root) return;
    var st = { workers: 4, counts: { elektrik: 2, vana: 1, pnomatik: 0, fis: 0, kablo: 0 }, key: 'farkli' };
    var rows = $('[data-k="energy"]', root);
    rows.innerHTML = ENERGY.map(function (en) {
      return '<div class="energy-row" data-row="' + en.id + '"><div><b>' + esc(en.label) + '</b><small>' + esc(en.hint) + '</small></div>' +
        '<div class="stepper stepper--sm"><button type="button" data-e="' + en.id + '" data-d="-1" aria-label="' + esc(en.label) + ' azalt">−</button>' +
        '<output aria-live="polite" data-out="' + en.id + '">0</output>' +
        '<button type="button" data-e="' + en.id + '" data-d="1" aria-label="' + esc(en.label) + ' arttır">+</button></div></div>';
    }).join('');

    root.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      if (b.hasAttribute('data-e')) {
        var id = b.getAttribute('data-e');
        st.counts[id] = Math.min(20, Math.max(0, st.counts[id] + parseInt(b.getAttribute('data-d'), 10)));
      } else if (b.hasAttribute('data-w')) {
        st.workers = Math.min(50, Math.max(1, st.workers + parseInt(b.getAttribute('data-w'), 10)));
      } else if (b.hasAttribute('data-key')) {
        st.key = b.getAttribute('data-key');
      } else if (b.hasAttribute('data-kit-add')) {
        addItems(compute().map(function (k) { return { id: k.id, name: k.cartName || k.name, qty: k.qty }; }));
        return;
      } else return;
      render();
    });

    function compute() {
      var n = st.workers, pc = 0;
      ENERGY.forEach(function (en) { pc += st.counts[en.id]; });
      var pcn = Math.max(pc, 1);
      var kit = [];
      if (n > 3) {
        kit.push({ qty: n, id: R.padlock, name: 'Kişisel emniyet asma kilidi', note: 'Her çalışana bir kilit; grup kutusuna takılır' });
        kit.push({ qty: pcn, id: R.padlock, name: 'Ortak izolasyon kilidi', cartName: 'Ortak izolasyon kilidi (aynı anahtarlı)', note: 'Her enerji noktasına bir adet, aynı anahtarlı' });
        kit.push({ qty: 1, id: R.groupbox, name: 'Grup kilitleme kutusu', note: 'İzolasyon anahtarları kutuya konur, ekip kutuyu kilitler' });
      } else {
        kit.push({ qty: n * pcn, id: R.padlock, name: 'Kişisel emniyet asma kilidi', note: 'Her çalışan her noktaya kendi kilidini takar' });
        if (n > 1) kit.push({ qty: pcn, id: R.hasp, name: 'Kilit çoklandırıcı', note: 'Bir noktaya birden fazla kilit takmak için' });
      }
      kit.push({ qty: n, id: R.tag, name: 'Kişisel kilitleme etiketi', note: 'Ad, tarih ve departman yazılır' });
      ENERGY.forEach(function (en) {
        if (st.counts[en.id] > 0) kit.push({ qty: st.counts[en.id], id: R[en.ref], name: en.item, note: 'Seçtiğiniz nokta sayısı kadar' });
      });
      if (n <= 5) kit.push({ qty: 1, id: R.bag, name: 'Taşınabilir EKED çantası', note: 'Ekipmanı sahaya taşımak için' });
      else kit.push({ qty: 1, id: R.station, name: 'Kapaklı LOTO istasyonu', note: 'Kilit ve etiketlerin sabit yeri' });
      return kit;
    }

    function render() {
      $('[data-k="workers"]', root).textContent = st.workers;
      ENERGY.forEach(function (en) {
        $('[data-out="' + en.id + '"]', root).textContent = st.counts[en.id];
        $('[data-row="' + en.id + '"]', root).classList.toggle('on', st.counts[en.id] > 0);
      });
      $$('[data-key]', root).forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-key') === st.key ? 'true' : 'false'); });
      $('[data-k="keynote"]', root).textContent = KEYS[st.key].note;
      var kit = compute(), total = 0;
      kit.forEach(function (k) { total += k.qty; });
      $('[data-k="summary"]', root).textContent = total + ' parça · ' + KEYS[st.key].label;
      $('[data-k="list"]', root).innerHTML = kit.map(function (k) {
        return '<div class="kit-row"><span class="qty">' + k.qty + '</span><div><a href="' + esc(productUrl(k.id)) + '">' + esc(k.name) + '</a><small>' + esc(k.note) + '</small></div></div>';
      }).join('');
      $('[data-k="keyinfo"]', root).textContent = st.key === 'farkli' ? '' : 'Anahtar sistemi: ' + KEYS[st.key].label + ' (teklif notuna eklenir)';
    }
    render();
  }

  /* ---------- Ürün filtresi ---------- */
  function trLower(s) { return String(s).toLocaleLowerCase('tr-TR'); }
  function initFilter() {
    var input = $('#urun-ara');
    if (!input) return;
    var cat = 'tumu';
    var cards = $$('[data-card]');
    function apply() {
      var q = trLower(input.value.trim());
      var shown = 0;
      cards.forEach(function (c) {
        var ok = (cat === 'tumu' || c.getAttribute('data-cat') === cat) && (!q || trLower(c.getAttribute('data-text')).indexOf(q) > -1);
        c.hidden = !ok;
        if (ok) shown++;
      });
      $('#urun-sayi').textContent = shown + ' ürün';
      $('#urun-bos').hidden = shown > 0;
    }
    input.addEventListener('input', apply);
    $$('[data-filter]').forEach(function (b) {
      b.addEventListener('click', function () {
        cat = b.getAttribute('data-filter');
        $$('[data-filter]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        apply();
      });
    });
    var h = (location.hash || '').replace('#', '');
    if (h) { var pre = $('[data-filter="' + h + '"]'); if (pre) pre.click(); }
    apply();
  }

  /* ---------- Teklif sayfası ---------- */
  function renderCartPage() {
    var root = $('#teklif-root');
    var c = getCart();
    var empty = $('#teklif-bos');
    empty.hidden = c.length > 0;
    root.hidden = c.length === 0;
    $('#teklif-satir').innerHTML = c.map(function (it, i) {
      var url = productUrl(it.id);
      var name = url ? '<a href="' + esc(url) + '">' + esc(it.name) + '</a>' : esc(it.name);
      return '<div class="cart-row"><div class="name">' + name + '</div>' +
        '<div class="stepper stepper--sm"><button type="button" data-ci="' + i + '" data-cd="-1" aria-label="Azalt">−</button>' +
        '<output>' + it.qty + '</output><button type="button" data-ci="' + i + '" data-cd="1" aria-label="Arttır">+</button></div>' +
        '<button type="button" class="remove" data-cr="' + i + '">Kaldır</button></div>';
    }).join('');
  }
  function buildMessage(form) {
    var f = function (n) { var el = form.elements[n]; return el ? el.value.trim() : ''; };
    var lines = ['Merhaba, aşağıdaki ürünler için teklif almak istiyorum.', ''];
    getCart().forEach(function (it) { lines.push('• ' + it.name + ' — ' + it.qty + ' adet'); });
    lines.push('');
    if (f('firma')) lines.push('Firma: ' + f('firma'));
    if (f('ad')) lines.push('Ad Soyad: ' + f('ad'));
    if (f('telefon')) lines.push('Telefon: ' + f('telefon'));
    if (f('eposta')) lines.push('E-posta: ' + f('eposta'));
    if (f('sehir')) lines.push('Şehir: ' + f('sehir'));
    if (f('not')) { lines.push(''); lines.push('Not: ' + f('not')); }
    return lines.join('\n');
  }
  function waLink(text) {
    var num = (D.site.whatsapp_num || '').replace(/\D/g, '');
    return 'https://wa.me/' + num + '?text=' + encodeURIComponent(text);
  }
  function mailLink(subject, text) {
    return 'mailto:' + (D.site.email || '') + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(text);
  }
  function initCartPage() {
    if (!$('#teklif-root')) return;
    renderCartPage();
    $('#teklif-satir').addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      var c = getCart().slice();
      if (b.hasAttribute('data-cd')) {
        var i = +b.getAttribute('data-ci');
        c[i] = Object.assign({}, c[i], { qty: Math.max(1, c[i].qty + parseInt(b.getAttribute('data-cd'), 10)) });
      } else if (b.hasAttribute('data-cr')) {
        c.splice(+b.getAttribute('data-cr'), 1);
      } else return;
      save(c);
    });
    var form = $('#teklif-form');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var text = buildMessage(form);
      var out = $('#teklif-cikti');
      out.hidden = false;
      $('#teklif-metin').value = text;
      $('#teklif-wa').href = waLink(text);
      $('#teklif-mail').href = mailLink('Teklif talebi', text);
      out.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
    $('#teklif-temizle').addEventListener('click', function () { save([]); });
  }

  /* ---------- İletişim formu ---------- */
  function initContact() {
    var form = $('#iletisim-form');
    if (!form) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = function (n) { return form.elements[n].value.trim(); };
      var text = 'Merhaba, ben ' + f('ad') + (f('firma') ? ' (' + f('firma') + ')' : '') + '.\n' + f('mesaj') + '\n\nTelefon: ' + f('telefon') + '\nE-posta: ' + f('eposta');
      var out = $('#iletisim-cikti');
      out.hidden = false;
      $('#iletisim-metin').value = text;
      $('#iletisim-wa').href = waLink(text);
      $('#iletisim-mail').href = mailLink('İletişim formu', text);
    });
  }

  renderCount();
  initFinder();
  initBuilder();
  initFilter();
  initCartPage();
  initContact();
})();
