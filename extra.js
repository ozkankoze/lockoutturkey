/* 2. tasarıma özel etkileşimler: renk seçici, sekmeler, mega menü, arama odağı */
(function () {
  'use strict';
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  // Renk seçici
  $$('[data-pick]').forEach(function (b) {
    b.addEventListener('click', function () {
      $$('[data-pick]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      var im = $('#pick-img'); if (im) im.src = b.getAttribute('data-img');
      $('#pick-name').textContent = b.getAttribute('data-color') + ' · ' + b.getAttribute('data-code');
      $('#pick-role').textContent = 'Örnek kullanım: ' + b.getAttribute('data-role');
      $('#pick-link').href = b.getAttribute('data-url');
    });
  });

  // Ana sayfa kategori sekmeleri
  var tabs = $$('[data-tab]');
  function showTab(id) {
    tabs.forEach(function (t) { t.setAttribute('aria-selected', t.getAttribute('data-tab') === id ? 'true' : 'false'); });
    $$('[data-tabitem]').forEach(function (c) { c.hidden = c.getAttribute('data-tabitem') !== id; });
  }
  tabs.forEach(function (t) { t.addEventListener('click', function () { showTab(t.getAttribute('data-tab')); }); });
  if (tabs.length) showTab(tabs[0].getAttribute('data-tab'));

  // Ürün sayfası sekmeleri
  $$('[data-ptab]').forEach(function (t) {
    t.addEventListener('click', function () {
      var id = t.getAttribute('data-ptab');
      $$('[data-ptab]').forEach(function (x) { x.setAttribute('aria-selected', x === t ? 'true' : 'false'); });
      $$('[role="tabpanel"]').forEach(function (p) { p.hidden = p.id !== 'p-' + id; });
    });
  });

  // Arama bağlantısı ile gelindiyse arama kutusuna odaklan
  if (location.hash === '#ara') { var s = $('#urun-ara'); if (s) setTimeout(function () { s.focus(); }, 50); }
})();
