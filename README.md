# Sentiment Analysis Dashboard

Modern ve responsive bir Sentiment Analysis (Duygu Analizi) Dashboard uygulaması.

## 📋 Özellikler

- ✅ Responsive tasarım (Mobil, Tablet, Desktop)
- ✅ Bootstrap 5 framework
- ✅ Chart.js ile interaktif grafikler
- ✅ Font Awesome ikonları
- ✅ Modern ve temiz UI/UX
- ✅ Statik veri gösterimi

## 🎨 Dashboard İçeriği

### Ana Sayfa (index.html) - Sentiment Analysis

1. **Sentiment Insight Bölümü**
   - Ürün/marka arama çubuğu
   - Tarih aralığı seçimi (Last 30 days)
   - Model seçimi (BERT-base)

2. **İstatistik Kartları**
   - Pozitif İncelemeler: 64%
   - Nötr İncelemeler: 21%
   - Negatif İncelemeler: 15%
   - Ortalama Puan: 4.1/5

3. **Grafikler**
   - Sentiment Distribution (Pasta Grafiği)
   - Sentiment Trend (Çizgi Grafiği)

### Price Manipulation Sayfası (price-manipulation.html)

1. **İstatistik Kartları**
   - Manipulative Posts: 1,245
   - Inflation Price: 30%
   - Suspicious Accounts: 65%
   - Fake Discount Rate: 28%

2. **Grafikler**
   - Top Manipulated Products (Yatay Bar Grafiği)
   - Before-After Price Trend (Çizgi Grafiği)

### Product Detail Sayfası (product-detail.html)

1. **Ürün Bilgileri**
   - Ürün adı ve görseli (New Balance 530)
   - Overall Sentiment durumu
   - Model Confidence (Accuracy 91%)

2. **Review Sentiment**
   - Bar chart ile sentiment dağılımı
   - Positive, Neutral, Negative oranları

3. **Most Frequent Keywords**
   - Pozitif anahtar kelimeler (yeşil: comfortable, light, durable)
   - Negatif anahtar kelimeler (kırmızı: tight fit, narrow, size issue)

4. **Diğer Ürünler**
   - Benzer ürünlerin kartları
   - Sentiment durumları ve istatistikler

### Manipulation Campaigns Sayfası (manipulation-campaigns.html)

1. **Manipulation Types**
   - Pasta grafiği ile manipülasyon türlerinin dağılımı
   - Fake Discounts: 37%
   - Limited Stock Press: 23%
   - Bot Activity: 22%
   - Fake Coupons: 18%

2. **Most Manipulative Campaigns**
   - Kampanya listesi tablosu
   - Kampanya adları ve türleri
   - Güven skoru (Confidence) bar'ları

3. **İstatistik Kartları**
   - Her manipülasyon türü için detaylı yüzdeler
   - İkonlu kart gösterimleri

## 🧭 Navigasyon

Üst menüden sayfalar arası geçiş yapabilirsiniz:
- **Sentiment Analysis** - Duygu analizi dashboard'u
- **Price Manipulation** - Fiyat manipülasyonu analizi
- **Product Detail** - Ürün detay sayfası ve anahtar kelime analizi
- **Campaigns** - Manipülasyon kampanyaları analizi

## 📁 Proje Yapısı

```
Dashboard/
│
├── index.html                       # Ana sayfa - Sentiment Analysis
├── price-manipulation.html          # Price Manipulation Dashboard
├── product-detail.html              # Product Detail View
├── manipulation-campaigns.html      # Manipulation Campaigns Analysis
├── css/
│   ├── style.css                   # Genel CSS stilleri ve navigasyon
│   ├── price-manipulation.css      # Price Manipulation özel stilleri
│   ├── product-detail.css          # Product Detail özel stilleri
│   └── manipulation-campaigns.css  # Campaigns özel stilleri
├── js/
│   ├── charts.js                   # Sentiment Analysis grafikleri
│   ├── price-manipulation.js       # Price Manipulation grafikleri
│   ├── product-detail.js           # Product Detail grafikleri
│   └── manipulation-campaigns.js   # Campaigns grafikleri ve interaktivite
└── README.md                       # Proje dokümantasyonu
```

## 🚀 Kullanım

1. `index.html` dosyasını tarayıcınızda açın
2. Dashboard otomatik olarak yüklenecektir
3. İnternet bağlantısı gereklidir (Bootstrap, Chart.js ve Font Awesome CDN'den yüklenir)

## 🛠️ Kullanılan Teknolojiler

- **HTML5** - Sayfa yapısı
- **CSS3** - Özel stiller ve animasyonlar
- **Bootstrap 5.3.0** - Responsive framework
- **Chart.js 4.4.0** - Grafik kütüphanesi
- **Font Awesome 6.4.0** - İkonlar

## 📱 Responsive Tasarım

Dashboard tüm cihazlarda düzgün çalışır:
- 🖥️ Desktop (1200px+)
- 💻 Laptop (992px - 1199px)
- 📱 Tablet (768px - 991px)
- 📱 Mobile (< 768px)

## 🎯 Sonraki Adımlar

Proje genişletilebilir:
- Yeni sayfalar eklenebilir
- Backend entegrasyonu yapılabilir
- Gerçek-zamanlı veri akışı eklenebilir
- Kullanıcı giriş sistemi entegre edilebilir

## 📝 Notlar

- Tüm veriler statiktir
- Grafikler Chart.js ile oluşturulmuştur
- Renkler ve stil değişkenleri CSS dosyasında tanımlıdır

---

**Geliştirme Tarihi:** Ocak 2026

