# -*- coding: utf-8 -*-
"""Blog yazıları. Gövdede {p:LT-KOD} ürün bağlantısına, {c:kategori-slug} kategori bağlantısına dönüşür."""

POSTS = [
    {
        "slug": "emniyet-asma-kilidi-nasil-secilir",
        "title": "Emniyet asma kilidi nasıl seçilir? Çene malzemesi, boy ve anahtar sistemi",
        "date": "2026-10-08",
        "tag": "Ürün seçimi",
        "minutes": 6,
        "cover": "LT-G11",
        "summary": "Çelik mi plastik çene mi, 38 mm mi 76 mm mi, farklı anahtar mı master anahtar mı? Kişisel LOTO kilidini seçerken bakılacak dört nokta.",
        "products": ["LT-G11", "LT-G01", "LT-G31", "LT-G21"],
        "body": """
<p>Kilitleme ve etiketleme uygulamasının en temel parçası kişisel emniyet asma kilididir. Her çalışan izolasyon noktasına kendi kilidini takar ve anahtarı yalnızca kendisinde kalır. Doğru kilidi seçmek için dört soruya cevap vermek yeterli.</p>
<h2>1. Çene malzemesi: çelik mi, plastik mi?</h2>
<p>Kilidin çenesi (kelepçesi) iki tiptir. <b>Çelik çeneli kilitler</b> mekanik bakım, vana ve genel kullanım için dayanıklı bir seçenektir. <b>Plastik (naylon) çeneli kilitler</b> ise elektrik iletmez; elektrik panolarında, şalter ve sigorta kilitleriyle birlikte kullanıldığında çarpılma riskini azaltır.</p>
<p>Elektrik bakım ekibi için plastik çeneli bir model, örneğin {p:LT-G11}, mekanik ekip için çelik çeneli {p:LT-G01} iyi bir başlangıçtır.</p>
<h2>2. Çene boyu: 38 mm mi, 76 mm mi?</h2>
<p>38 mm çene çoğu şalter, sigorta ve vana kilitleme cihazına uyar ve en yaygın kullanılan boydur. Kalın çoklandırıcılara, büyük vana kilitlerine ya da ulaşılması zor deliklere kilit takılacaksa 76 mm uzun çene ({p:LT-G31}, {p:LT-G21}) işinizi kolaylaştırır.</p>
<h2>3. Anahtar sistemi</h2>
<ul>
<li><b>Farklı anahtar:</b> Her kilidin kendi anahtarı vardır. Kişisel kilitler için standart seçimdir.</li>
<li><b>Aynı anahtar:</b> Bir gruptaki kilitler tek anahtarla açılır. Grup kilitleme kutusuna konan ortak izolasyon kilitleri için uygundur, kişisel kilitlerde kullanılmaz.</li>
<li><b>Master anahtar:</b> Her kilit farklı anahtarlıdır, ayrıca tek bir yetkili anahtar hepsini açar. Kullanımı yazılı bir acil durum prosedürüne bağlanmalıdır.</li>
</ul>
<h2>4. Renk ve kişiselleştirme</h2>
<p>Kilit rengi kimin çalıştığını uzaktan gösterir. Elektrik, mekanik, yüklenici gibi grupları farklı renklerle ayırmak sahada karışıklığı önler. Kilidin üzerine isim, sicil numarası ya da departman baskısı da yapılabilir.</p>
<p>Hangi modelin size uygun olduğundan emin değilseniz kullanacağınız kilitleme noktalarını yazın ya da fotoğrafını gönderin; uygun kilidi birlikte seçelim.</p>
""",
    },
    {
        "slug": "minyatur-devre-kesici-kilitleri-pos-pis-pow-tblo",
        "title": "Minyatür devre kesici kilitleri: POS, PIS, POW ve TBLO farkı",
        "date": "2026-10-06",
        "tag": "Elektrik",
        "minutes": 5,
        "cover": "LT-D01",
        "summary": "Sigortalar için kilit seçerken karşılaşılan POS, PIS, POW ve TBLO kısaltmaları ne anlama geliyor, hangi sigortaya hangisi uyar?",
        "products": ["LT-D01", "LT-D02", "LT-D04", "LT-D03", "LT-D05-3"],
        "body": """
<p>Elektrik panosunda bakım yapılmadan önce ilgili sigortanın kolu kapalı konuma alınır ve bir kilitleme cihazıyla sabitlenir. Minyatür devre kesici (MCB) kilitleri, sigortanın gövdesindeki deliklere ya da kolun çevresine tutunarak kolun yeniden kaldırılmasını engeller.</p>
<h2>Kısaltmalar ne anlama geliyor?</h2>
<p>Pimli MCB kilitleri, sigorta kolunun yanındaki deliklere giren pimlerin yönüne ve aralığına göre adlandırılır:</p>
<ul>
<li><b>POS (Pin Out Standard):</b> Pimler dışa doğru, standart aralıkta. {p:LT-D01}</li>
<li><b>PIS (Pin In Standard):</b> Pimler içe doğru, standart aralıkta. {p:LT-D02}</li>
<li><b>POW (Pin Out Wide):</b> Pimler dışa doğru, geniş aralıkta. {p:LT-D04}</li>
<li><b>TBLO (Tie Bar Lock Out):</b> Kolları bir bağlantı çubuğuyla birleştirilmiş çok kutuplu sigortalar için. {p:LT-D03}</li>
</ul>
<h2>Hangisini seçmeliyim?</h2>
<p>Panodaki sigortaların markası ve modeli aynı değilse tek tip pimli kilit her sigortaya uymayabilir. Bu durumda pinsiz, sıkıştırmalı evrensel modeller ({p:LT-D05-3}) farklı sigortalarda kullanılabildiği için pratik bir çözümdür. Kompakt şalterler (MCCB) gibi daha büyük kollar için kelepçeli ve geniş ağızlı kilitler tercih edilir.</p>
<h2>Uygulamada dikkat edilecekler</h2>
<ul>
<li>Kilit takılmadan önce sigorta kapalı konuma alınmalı, ardından cihaz sabitlenip asma kilit takılmalıdır.</li>
<li>Kilitleme sonrasında devrede enerji olmadığı ölçüm aletiyle doğrulanmalıdır.</li>
<li>Kilidin yanına kimin, ne zaman kilitlediğini gösteren kişisel etiket asılmalıdır.</li>
</ul>
<p>Panonuzdaki sigortanın net bir fotoğrafını WhatsApp'tan gönderirseniz hangi kilidin uyduğunu söyleyebiliriz.</p>
""",
    },
    {
        "slug": "grup-kilitleme-nasil-yapilir",
        "title": "Grup kilitleme nasıl yapılır? Grup kilit kutusuyla adım adım",
        "date": "2026-10-03",
        "tag": "Prosedür",
        "minutes": 5,
        "cover": "LT-X04",
        "summary": "Çok kişinin çok noktada çalıştığı bakımlarda her çalışanın her noktaya kilit takması pratik değildir. Grup kilit kutusu bu işi nasıl kolaylaştırır?",
        "products": ["LT-X04", "LT-LK077", "LT-K42", "LT-G11"],
        "body": """
<p>Büyük bir makinenin bakımında on farklı izolasyon noktası ve sekiz çalışan olduğunu düşünün. Her çalışan her noktaya kendi kilidini taksaydı seksen kilit gerekirdi. Grup kilitleme bu sorunu çözer.</p>
<h2>Adım adım grup kilitleme</h2>
<ol>
<li><b>İzolasyon:</b> Yetkili kişi makinenin tüm enerji kaynaklarını belirler ve her noktayı kapatır.</li>
<li><b>Ortak kilitler:</b> Her izolasyon noktasına aynı anahtarlı bir ortak kilit ve etiket takılır.</li>
<li><b>Anahtarlar kutuya:</b> Ortak kilitlerin anahtarları grup kilit kutusuna ({p:LT-X04}) konur ve kutu kapatılır.</li>
<li><b>Kişisel kilitler:</b> Bakımda çalışacak her kişi kutuya kendi kişisel kilidini takar.</li>
<li><b>Doğrulama:</b> Makineyi çalıştırma denemesiyle sıfır enerji durumu teyit edilir.</li>
</ol>
<p>Kutunun üzerinde son kişisel kilit çıkarılmadan anahtarlara ulaşılamaz. Böylece işi biten çalışan kendi kilidini alır, iş tamamen bitene kadar ortak kilitler yerinde kalır.</p>
<h2>Kutu seçerken</h2>
<p>Kutunun kilit deliği sayısı aynı anda çalışacak en kalabalık ekipten fazla olmalıdır. Çok kalabalık ekiplerde daha fazla delikli kutular ({p:LT-LK077}) ya da kutuya takılan bir çoklandırıcı ({p:LT-K42}) kullanılabilir.</p>
<p>Ekibinize kaç kilit ve hangi kutunun gerektiğini <a href="set-olusturucu.html">set oluşturucu</a> ile hızlıca hesaplayabilirsiniz.</p>
""",
    },
    {
        "slug": "vana-kilitleme-dogru-ekipman",
        "title": "Vana kilitleme: küresel, kelebek ve sürgülü vanalar için doğru ekipman",
        "date": "2026-09-29",
        "tag": "Mekanik",
        "minutes": 6,
        "cover": "LT-F01",
        "summary": "Vananın tipine, kol ya da volan ölçüsüne göre hangi kilit kullanılır? Standart kilidin uymadığı vanalarda ne yapılır?",
        "products": ["LT-F01", "LT-F02", "LT-BVL31", "LT-F16", "LT-F33/F33X"],
        "body": """
<p>Su, buhar, gaz ve kimyasal hatlarında bakım öncesi vananın kapatılıp kilitlenmesi, hatta kalan basıncın tahliye edilmesi gerekir. Doğru vana kilidi vananın tipine ve ölçüsüne göre seçilir.</p>
<h2>Küresel vanalar</h2>
<p>Çeyrek tur dönen kollu küresel vanalarda kilit, kolu kapalı konumda sabitleyerek döndürülmesini engeller. Ayarlanabilir modeller ({p:LT-F01}) farklı boru çaplarına uyar; daha büyük vanalar için büyük boy modeller ({p:LT-F02}) kullanılır.</p>
<h2>Kelebek vanalar</h2>
<p>Kollu kelebek vanalarda kolu saran ve yerinden kalkmasını engelleyen kilitler kullanılır ({p:LT-BVL31}). Redüktörlü kelebek vanalarda volanı sabitleyen kablolu çözümler daha uygundur.</p>
<h2>Sürgülü ve volanlı vanalar</h2>
<p>Volanlı vanalarda kilit, volanın dönmesini engelleyecek şekilde volanı kapatır ya da sabitler ({p:LT-F16}). Volan çapı ölçülmeden seçilen kilit volan üzerinde boşlukta dönebilir; bu da kilitlemeyi etkisiz kılar.</p>
<h2>Standart kilidin uymadığı vanalar</h2>
<p>Ulaşılması zor, standart dışı ya da yan yana birden fazla vananın aynı anda kilitlenmesi gereken durumlarda kablolu evrensel kilitler ({p:LT-F33/F33X}) ve ayarlanabilir {c:kablo-kilitleri} kullanılır.</p>
<p>Vana tipini ve boru çapını yazarsanız uygun kilidi önerebiliriz.</p>
""",
    },
    {
        "slug": "renk-kodlu-kilitlerle-loto-yonetimi",
        "title": "Renk kodlu kilitlerle LOTO yönetimi",
        "date": "2026-09-24",
        "tag": "Prosedür",
        "minutes": 4,
        "cover": "LT-G13",
        "summary": "Kilit renkleri sahada kimin çalıştığını bir bakışta gösterir. Renk planı nasıl kurulur, nelere dikkat edilir?",
        "products": ["LT-G11", "LT-G13", "LT-G12", "LT-G14"],
        "body": """
<p>Bir panonun önünde yan yana asılı beş kilit düşünün. Hepsi aynı renkteyse kimin hangi ekipten olduğunu anlamak için etiketlere tek tek bakmak gerekir. Renk kodlaması bu bilgiyi uzaktan okunur hale getirir.</p>
<h2>Renk planı nasıl kurulur?</h2>
<p>Renklerin anlamı için yasal bir zorunluluk yoktur; önemli olan tesis içinde tek bir planın uygulanmasıdır. ABD'deki OSHA 29 CFR 1910.147 standardı da kilitleme cihazlarının tesis içinde renk, şekil ya da boyut bakımından standart olmasını ister. Örnek bir plan:</p>
<ul>
<li>Kırmızı: elektrik bakım ({p:LT-G11})</li>
<li>Mavi: mekanik bakım ({p:LT-G13})</li>
<li>Sarı: yükleniciler ({p:LT-G12})</li>
<li>Yeşil: proses ve üretim ({p:LT-G14})</li>
</ul>
<h2>Dikkat edilecekler</h2>
<ul>
<li>Renk planı yazılı LOTO prosedürüne eklenmeli ve tüm çalışanlara anlatılmalıdır.</li>
<li>Renk, kişisel etiketin yerini tutmaz; her kilidin yanında kilidi takanın adı yazılı bir etiket bulunmalıdır.</li>
<li>Yüklenici firmalara giriş sırasında kendi renklerinde kilit verilmesi, sahadaki takibi kolaylaştırır.</li>
</ul>
<p>Emniyet asma kilitlerimiz sekiz renkte sunulur; renk dağılımını tesisinize göre birlikte planlayabiliriz.</p>
""",
    },
    {
        "slug": "loto-istasyonu-nereye-kurulur",
        "title": "LOTO istasyonu nereye kurulur, içinde neler olmalı?",
        "date": "2026-09-18",
        "tag": "Ürün seçimi",
        "minutes": 4,
        "cover": "LT-B101",
        "summary": "Kilitleme ekipmanı kullanılacağı yere yakın, düzenli ve eksiksiz durmalı. İstasyonun yeri ve içeriği için pratik öneriler.",
        "products": ["LT-B101", "LT-B105", "LT-X07", "LT-B201"],
        "body": """
<p>Kilitleme ekipmanı bir dolabın dibinde ya da depoda duruyorsa bakım sırasında aranır, eksik kalır ya da hiç kullanılmaz. LOTO istasyonu ekipmanın sahadaki sabit yeridir; eksik bir parça bir bakışta fark edilir.</p>
<h2>Nereye kurulmalı?</h2>
<ul>
<li>Bakımı yapılan makineye ya da elektrik odasına yakın, kolay ulaşılan bir duvara</li>
<li>Görünür ve iyi aydınlatılmış bir noktaya</li>
<li>Toz, nem ve kimyasala maruz kalan alanlarda kapaklı modeller tercih edilerek ({p:LT-B101})</li>
</ul>
<h2>İçinde neler olmalı?</h2>
<ul>
<li>Bölgede çalışan kişi sayısı kadar kişisel emniyet asma kilidi</li>
<li>Kişisel kilitleme etiketleri ve yazmak için kalem</li>
<li>Çoklandırıcılar</li>
<li>Bölgedeki enerji noktalarına uygun şalter, vana ve fiş kilitleri</li>
</ul>
<h2>Hangi model?</h2>
<p>Küçük alanlar ve tek ekip için kapaksız mini istasyonlar ({p:LT-B105}), çok sayıda kilidin tek yerde durması gereken yerlerde metal dolaplar ({p:LT-X07}) ya da kombinasyon istasyonları ({p:LT-B201}) uygundur. İstasyonlar boş ya da ekipmanla dolu olarak tedarik edilebilir.</p>
<p>İstasyonun içeriğini bölgenizdeki enerji noktalarına göre birlikte belirleyebiliriz.</p>
""",
    },
    {
        "slug": "eked-uyari-etiketi-dogru-kullanim",
        "title": "Etiket kilidin yerini tutar mı? EKED uyarı etiketlerinin doğru kullanımı",
        "date": "2026-09-12",
        "tag": "Prosedür",
        "minutes": 4,
        "cover": "LT-LT02-TR",
        "summary": "Kilit enerjiyi keser, etiket ise kimin, ne zaman ve neden kilitlediğini söyler. Etiket tek başına ne zaman yeterli değildir, üzerinde neler yazmalıdır?",
        "products": ["LT-LT02-TR", "LT-LT06", "LT-LT05", "LT-LT14"],
        "body": """
<p>Kilitleme ve etiketleme iki ayrı işi birlikte yapar. Kilit, enerji kaynağının fiziksel olarak açılmasını engeller. Etiket ise o noktada kimin çalıştığını ve neden kilitlendiğini herkese söyler. Biri olmadan diğeri eksik kalır.</p>
<h2>Etiket tek başına yeterli mi?</h2>
<p>Hayır. Etiket bir uyarıdır, engel değildir; birisi etiketi görmezden gelip şalteri kaldırabilir. Bu yüzden kilitlenebilen her enerji noktasında etiket, kilidin yanında kullanılır. OSHA 29 CFR 1910.147 de kilitlenebilen bir noktada yalnızca etiketle yetinilmesini ancak kilit kadar güvenlik sağladığı gösterilebiliyorsa kabul eder.</p>
<h2>Etikette neler yazmalı?</h2>
<ul>
<li>Kilidi takan kişinin adı ve departmanı</li>
<li>Tarih ve saat</li>
<li>Kilitleme nedeni ya da yapılan iş</li>
<li>Gerekirse ulaşılabilecek telefon numarası</li>
</ul>
<p>Kişisel kilitleme etiketi ({p:LT-LT02-TR}) bu alanları içerir ve kilitle birlikte asılır.</p>
<h2>Farklı durumlar için farklı etiketler</h2>
<p>Test ve devreye alma sırasında enerjinin geçici olarak verildiğini göstermek için ayrı bir etiket ({p:LT-LT06}) kullanmak karışıklığı önler. Bakımın sürdüğünü vardiyaya duyurmak için askılı uyarı levhaları ({p:LT-LT05}, {p:LT-LT14}) da iş görür.</p>
<h2>Dayanıklılık</h2>
<p>Sahada kullanılan etiketler yağ, nem ve sıcaklığa dayanıklı olmalı, yazılanlar silinmemelidir. Yırtılan ya da okunmayan bir etiket hiç olmamış gibidir.</p>
""",
    },
]
