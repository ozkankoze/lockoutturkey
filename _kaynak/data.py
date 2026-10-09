# -*- coding: utf-8 -*-
"""Lockout Turkey site içeriği. Ürünler catalog.json dosyasından gelir."""

SITE = {
    "brand": "Lockout Turkey",
    "domain": "https://lockoutturkey.com",
    "phone": "0505 499 97 32",
    "phone_tel": "+905054999732",
    "whatsapp": "0505 499 97 32",
    "whatsapp_num": "905054999732",
    "email": "info@lockoutturkey.com",
    "address": "Şerifali Mahallesi, Ziynet Sokak No: 36A, Ümraniye / İstanbul",
    "hours": "",             # örn. "Hafta içi 08:30–18:00"
}

CATEGORIES = [
    {
        "slug": "emniyet-asma-kilitleri",
        "name": "Emniyet Asma Kilitleri",
        "icon": "padlock",
        "short": "Toz korumalı, renk kodlu, anahtarı tekil kişisel kilitler.",
        "intro": "LOTO uygulamasının temeli kişisel kilittir: her çalışan kendi kilidini takar, anahtarı yalnızca kendisinde kalır. Emniyet asma kilitleri mülk koruma için değil, enerji izolasyonu için üretilir; hafif, yalıtkan gövdeli ve renk kodludur. Tüm modellerimizde anahtar yuvası menteşeli toz kapağıyla korunur.",
        "uses": ["Toz kapaklı anahtar yuvası", "Her çalışana kişisel kilit", "Çoklandırıcı ve grup kutusu ile", "Departman bazlı renk kodlama"],
    },
    {
        "slug": "salter-kilitleri",
        "name": "Şalter ve Devre Kesici Kilitleri",
        "icon": "breaker",
        "short": "Minyatür sigorta, kompakt şalter ve evrensel devre kesici kilitleri.",
        "intro": "Elektrik enerjisi kaynağında kesilip kilitlenmeden pano içinde çalışılmaz. Şalter kilitleri devre kesicinin kolunu kapalı konumda sabitler; asma kilit takılana kadar kol yeniden kaldırılamaz.",
        "uses": ["Minyatür sigortalar (MCB)", "Kompakt şalterler (MCCB)", "Snap-on ve kelepçeli kilitler"],
    },
    {
        "slug": "vana-kilitleri",
        "name": "Vana Kilitleme Ekipmanları",
        "icon": "valve",
        "short": "Küresel, kelebek, sürgülü ve tapa vana kilitleri, kör flanş kilitleri.",
        "intro": "Buhar, su, gaz ve kimyasal hatlarında bakım öncesi vana kapatılıp kilitlenir. Doğru vana kilidi, vananın tipine ve kol ya da volan ölçüsüne göre seçilir.",
        "uses": ["Kollu küresel vanalar", "Kelebek vanalar", "Sürgülü, tapa ve flanşlı hatlar"],
    },
    {
        "slug": "kablo-kilitleri",
        "name": "Kablo Kilitleme Ekipmanları",
        "icon": "cable",
        "short": "Çok noktalı ve standart dışı izolasyon için kablo kilitleri.",
        "intro": "Standart bir kilidin uymadığı noktalarda ya da birden fazla vananın tek seferde kilitlenmesi gerektiğinde kablo kilitleri kullanılır. Kablo noktalardan geçirilir, gergin hale getirilir ve kilitlenir.",
        "uses": ["Birden fazla vana", "Redüktörlü vanalar", "Standart dışı kollar"],
    },
    {
        "slug": "coklandiricilar",
        "name": "Kilit Çoklandırıcılar",
        "icon": "hasp",
        "short": "Bir noktaya birden fazla kişinin kilit takmasını sağlar.",
        "intro": "Aynı ekipman üzerinde birden fazla kişi çalışıyorsa her biri kendi kilidini takmalıdır. Çoklandırıcı tek kilitleme noktasını çoğaltır; son kilit çıkarılmadan enerji geri verilemez.",
        "uses": ["Ekip halinde bakım", "Termik şalter kilitleme", "Yüklenici çalışmaları"],
    },
    {
        "slug": "fis-ve-pnomatik-kilitleme",
        "name": "Fiş ve Pnömatik Kilitleme",
        "icon": "plug",
        "short": "Elektrik fişleri, kanal fişleri ve pnömatik bağlantılar için kilitler.",
        "intro": "Fişle çalışan makinelerde ve basınçlı hava hatlarında enerji, bağlantı ayrılarak kesilir. Fiş ve pnömatik kilitler ayrılan bağlantının bakım bitene kadar yeniden takılmasını engeller.",
        "uses": ["Elektrik fişleri", "Elektrik ve pnömatik fişler", "Kanal fişleri"],
    },
    {
        "slug": "eked-uyari-etiketleri",
        "name": "EKED Uyarı Etiketleri",
        "icon": "tag",
        "short": "Kilidi kimin taktığını ve neden taktığını gösteren etiketler.",
        "intro": "Kilit enerjiyi fiziksel olarak keser, etiket ise kimin, ne zaman ve neden kilitlediğini söyler. Etiket tek başına kilidin yerini tutmaz; her kişisel kilidin yanında bir etiket bulunur.",
        "uses": ["Her kişisel kilitle birlikte", "Test ve devreye alma", "İskele etiketleri"],
    },
    {
        "slug": "loto-istasyonlari",
        "name": "LOTO İstasyonları",
        "icon": "station",
        "short": "Kilit, etiket ve cihazların sabit ve düzenli durduğu panolar.",
        "intro": "Kilitleme ekipmanı kullanılacağı yerin yakınında, düzenli ve eksiksiz durmalıdır. LOTO istasyonları kilitlerin, etiketlerin ve cihazların sahadaki yerini belirler; eksik ekipman bir bakışta görülür.",
        "uses": ["Üretim hatları", "Bakım atölyeleri", "Elektrik odaları"],
    },
    {
        "slug": "grup-kilitleme-kutulari-ve-cantalar",
        "name": "Grup Kilitleme Kutuları ve Çantalar",
        "icon": "box",
        "short": "Kalabalık ekipler ve saha çalışmaları için kutu ve çantalar.",
        "intro": "Çok noktalı ve kalabalık bakımlarda izolasyon noktalarının anahtarları grup kutusuna konur, her çalışan kutuya kendi kilidini takar. Böylece her çalışan her noktaya ayrı kilit takmak zorunda kalmaz.",
        "uses": ["Kalabalık bakım ekipleri", "Çok noktalı izolasyon", "Saha ve taşınabilir kullanım"],
    },
    {
        "slug": "loto-setleri",
        "name": "LOTO Setleri",
        "icon": "kit",
        "short": "Başlamak için gereken ekipmanın bir arada geldiği setler.",
        "intro": "LOTO uygulamasına yeni başlayan ya da bir ekibi hızlıca donatmak isteyen işletmeler için temel ekipmanlar tek pakette gelir. Set içeriği ihtiyaca göre değiştirilebilir.",
        "uses": ["Yeni başlayan işletmeler", "Ekip donatımı", "Elektrik ve mekanik bakım"],
    },
]

# Kroki noktaları: konumlar yüzde cinsinden
POINTS = [
    {"id": "pano", "no": "01", "name": "Elektrik panosu", "zone": "Elektrik odası", "energy": "Elektrik", "x": 12, "y": 30,
     "products": ["LT-D01", "LT-D05-3", "LT-D12X"],
     "tip": "Pano kapağı açılmadan önce ana şalter kapatılıp kilitlenmeli, ardından sıfır enerji ölçümle doğrulanmalı."},
    {"id": "fis", "no": "02", "name": "Makine fişi", "zone": "Elektrik odası", "energy": "Elektrik", "x": 31, "y": 72,
     "products": ["LT-D41", "LT-D31", "LT-D45"],
     "tip": "Fiş prizden çekildikten sonra kilitlenmeli; kablonun üzerinde kişisel etiket bulunmalı."},
    {"id": "termik", "no": "03", "name": "Motor koruma şalteri", "zone": "Üretim hattı", "energy": "Elektrik", "x": 44, "y": 30,
     "products": ["LT-K34", "LT-K46-1"],
     "tip": "Termik ve motor koruma şalterinin kolu kapalı konumda kilitlenmeli. Kumanda butonu tek başına izolasyon sayılmaz."},
    {"id": "kuresel", "no": "04", "name": "Küresel vana", "zone": "Proses ve tesisat", "energy": "Akışkan", "x": 66, "y": 24,
     "products": ["LT-F01", "LT-F03/F04", "LT-F09/F09X"],
     "tip": "Vana kapalı konumda kilitlenmeli, hattaki basınç tahliye edilerek doğrulanmalı."},
    {"id": "kelebek", "no": "05", "name": "Kelebek vana", "zone": "Proses ve tesisat", "energy": "Akışkan", "x": 84, "y": 40,
     "products": ["LT-BVL31", "LT-F20", "LT-F34"],
     "tip": "Redüktörlü kelebek vanalarda volanı sabitleyen kablo kilidi tercih edilmeli."},
    {"id": "surgulu", "no": "06", "name": "Sürgülü vana", "zone": "Proses ve tesisat", "energy": "Akışkan", "x": 70, "y": 76,
     "products": ["LT-F16", "LT-F33/F33X", "LT-L01"],
     "tip": "Volan ya da kol çapı ölçülüp kilit ona göre seçilmeli; standart kilidin uymadığı vanalarda kablolu evrensel kilit kullanılır."},
    {"id": "pnomatik", "no": "07", "name": "Basınçlı hava hattı", "zone": "Proses ve tesisat", "energy": "Pnömatik", "x": 90, "y": 60,
     "products": ["LT-D31", "LT-PS02S"],
     "tip": "Hat ayrıldıktan sonra içeride kalan hava tahliye edilmeden çalışmaya başlanmamalı."},
]

COLORS = [
    ("Kırmızı", "#C8102E", "Elektrik bakım"),
    ("Mavi", "#1F5FAD", "Mekanik bakım"),
    ("Sarı", "#F2C230", "Yükleniciler"),
    ("Yeşil", "#2E8B57", "Proses / üretim"),
    ("Turuncu", "#E8731C", "Otomasyon"),
    ("Mor", "#6B3FA0", "Kalite / laboratuvar"),
    ("Siyah", "#1A1414", "Vardiya amiri"),
    ("Beyaz", "#FFFFFF", "Misafir / stajyer"),
]

SECTORS = [
    {"id": "enerji", "name": "Enerji ve dağıtım", "tags": ["Trafo hücreleri", "OG/AG panolar", "Ayırıcılar"],
     "text": "Dağıtım tesislerinde bakım ekipleri çoğu zaman birden fazla hücrede aynı anda çalışır. Yanlış hücrenin enerjilenmesi en ağır sonuçlu risktir; her ayırıcı ve şalter ayrı ayrı kilitlenmeli, anahtarlar grup kutusunda toplanmalıdır.",
     "cats": ["salter-kilitleri", "LT-G11", "grup-kilitleme-kutulari-ve-cantalar"]},
    {"id": "cimento", "name": "Çimento ve maden", "tags": ["Konveyörler", "Değirmen tahrikleri", "Silo vanaları"],
     "text": "Konveyör ve değirmenlerde yerçekimi ve gerilmiş bantlar gibi depolanmış enerji kaynakları vardır. Elektrik kesilse bile bu enerjiler boşaltılmadan makineye girilmemelidir. Toz ve darbeye dayanıklı metal gövdeli kilitler bu ortamda öne çıkar.",
     "cats": ["salter-kilitleri", "kablo-kilitleri", "LT-K11"]},
    {"id": "gida", "name": "Gıda ve içecek", "tags": ["Buhar hatları", "Dolum makineleri", "CIP vanaları"],
     "text": "Gıda tesislerinde sık yapılan temizlik ve ürün değişimleri en çok kilitleme ihtiyacı doğuran işlerdir. Buhar ve sıcak su hatlarındaki vanalar ile dolum makinelerinin panoları birlikte kilitlenmelidir.",
     "cats": ["vana-kilitleri", "salter-kilitleri", "loto-istasyonlari"]},
    {"id": "otomotiv", "name": "Otomotiv ve yan sanayi", "tags": ["Presler", "Robot hücreleri", "Basınçlı hava"],
     "text": "Pres ve robot hücrelerinde elektrik, hidrolik ve pnömatik enerji bir arada bulunur. Kalıp değişimi ve arıza müdahalelerinde tüm enerji kaynakları kesilmeli; hücre kapısı açılmadan önce kilitleme tamamlanmalıdır.",
     "cats": ["fis-ve-pnomatik-kilitleme", "salter-kilitleri", "coklandiricilar"]},
    {"id": "kimya", "name": "Kimya ve petrokimya", "tags": ["Proses vanaları", "Pompalar", "Flanşlı hatlar"],
     "text": "Proses hatlarında bir pompa bakımı birkaç vananın kapatılmasını gerektirir. Kablo kilitleri vana gruplarını tek seferde kilitler; flanş kilitleri körlenmiş hatların açılmasını engeller.",
     "cats": ["vana-kilitleri", "kablo-kilitleri", "eked-uyari-etiketleri"]},
    {"id": "lojistik", "name": "Lojistik ve depo", "tags": ["Forkliftler", "Kapı motorları", "Şarj istasyonları"],
     "text": "Depolarda bakım işleri çoğunlukla taşınabilir ekipman ve şarj noktalarında yapılır. Fiş kilitleri ve taşınabilir çantalar küçük ekiplerin sahada hızlı kilitleme yapmasını sağlar.",
     "cats": ["fis-ve-pnomatik-kilitleme", "grup-kilitleme-kutulari-ve-cantalar", "eked-uyari-etiketleri"]},
]

STEPS = [
    ("Hazırlık", "Makinenin tüm enerji kaynaklarını ve izolasyon noktalarını belirleyin: elektrik, hidrolik, pnömatik, mekanik, termal."),
    ("Bildirim", "Duruştan etkilenecek tüm çalışanları bilgilendirin; kimin, ne kadar süre çalışacağını açıklayın."),
    ("Kapatma", "Ekipmanı normal durdurma prosedürüyle kapatın. Acil stop ile durdurmak izolasyon yerine geçmez."),
    ("İzolasyon", "Şalter, vana ve bağlantılarla enerjiyi kaynağında kesin."),
    ("Kilitleme ve etiketleme", "Her çalışan izolasyon noktasına kendi kilidini ve kişisel etiketini takar."),
    ("Depolanmış enerjiyi boşaltma", "Basınç, yay gerilimi, kondansatör yükü ve yükseltilmiş parçalar gibi kalan enerjileri güvenli hale getirin."),
    ("Doğrulama", "Makineyi çalıştırmayı deneyerek ve ölçüm yaparak sıfır enerji durumunu teyit edin; sonra kumandayı kapalıya getirin."),
]

FAQ = [
    ("EKED (LOTO) nedir?", "EKED; Enerji Kesme, Kilitleme, Etiketleme ve Doğrulama adımlarının kısaltmasıdır, uluslararası adı Lockout / Tagout'tur. Bakım, onarım ve temizlik sırasında makinenin enerjisinin kaynağında kesilip kilitlenmesini, etiketlenmesini ve enerjinin gerçekten kesildiğinin doğrulanmasını kapsar."),
    ("Hangi standarda dayanır?", "Temel referans ABD İş Güvenliği ve Sağlığı İdaresi'nin OSHA 29 CFR 1910.147 standardıdır. Türkiye'de 6331 sayılı İş Sağlığı ve Güvenliği Kanunu işverene risk değerlendirmesi yapma ve önlem alma yükümlülüğü getirir; bakım sırasında tehlikeli enerjinin kontrolü bu önlemlerin başında gelir."),
    ("Emniyet asma kilidinin normal kilitten farkı nedir?", "Emniyet asma kilitleri yalnızca kilitleme ve etiketleme için kullanılır, mülk korumada kullanılmaz. Genellikle yalıtkan gövdeli, hafif ve renk kodludur. Farklı anahtar, aynı anahtar ve master anahtar sistemleriyle her kilidi yalnızca yetkili kişinin açması sağlanır."),
    ("Şalterime hangi kilit uyar?", "Şalterin marka ve modelini ya da net bir fotoğrafını WhatsApp üzerinden gönderin; uygun kilitleme ekipmanını size bildirelim."),
    ("Kilitlere isim veya numara baskısı yapılabilir mi?", "Evet. Kişisel kilitlere isim, sicil numarası veya departman baskısı yapılabilir; renk ve anahtar sistemi de ihtiyaca göre belirlenir."),
    ("Teklif nasıl alırım?", "Ürünleri teklif listesine ekleyip listeyi WhatsApp ya da e-posta ile gönderebilirsiniz. Ürün kodunu doğrudan yazmanız da yeterli."),
]

# Set oluşturucu ve teklif hesaplarında kullanılan ürünler (ürün kodu)
REFS = {
    "padlock": "LT-G11", "hasp": "LT-K42", "tag": "LT-LT02-TR", "groupbox": "LT-X04",
    "bag": "LT-Z02", "station": "LT-B101",
    "elektrik": "LT-D05-3", "vana": "LT-F01", "pnomatik": "LT-D31", "fis": "LT-D41", "kablo": "LT-L01",
}

FOOTER_TEXT = "Emniyet asma kilitlerinden şalter ve vana kilitlerine, LOTO istasyonlarından hazır setlere kadar işletmelere EKED / LOTO ekipmanı tedarik ediyoruz."
