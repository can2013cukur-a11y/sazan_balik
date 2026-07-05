# 👑 Sazan AI Enterprise Studio v114.0

Groq (Llama 3.3 70B) ile çalışan, tek dosyada tam oyun üreten HTML5 oyun mimarı.
Ekonomi sistemi, RPG arenası, borsa, banka ve kişisel oyun kütüphanesiyle birlikte gelir.

## ✨ Özellikler
- **Oyun Üretici**: Sohbete yazdığın fikri tek bir `.html` dosyası olan çalışan bir oyuna dönüştürür.
- **Oyun Kütüphanem**: Ürettiğin her oyun otomatik kaydedilir; tekrar oynayabilir veya indirebilirsin.
- **İndirme Butonu**: Her oyunu `.html` dosyası olarak bilgisayarına indirebilirsin.
- **Ekonomi & Banka**: Coin (SZNC), mevduat/çekim, faiz, kredi skoru, seviye sistemi.
- **Günlük Giriş Bonusu**: Her gün giriş yaptığında artan bir bonus kazanırsın.
- **Finansal Borsa**: Simüle edilmiş hisse fiyatlarıyla al-sat yapabilirsin.
- **Siber Arena (RPG)**: Rastgele düşmanlarla savaş, ganimet topla, ekipman satın al.
- **Çoklu Proje Odaları**: Aynı anda birden fazla oyun projesi üzerinde çalışabilirsin.
- **Hızlı Şablonlar**: Tek tıkla popüler oyun türlerinden birini başlatabilirsin.
- **Çok Dilli Arayüz Desteği**: Üretilen açıklamalar seçtiğin dilde yazılır.

## 🔐 API Anahtarını Güvenli Tutma (ÇOK ÖNEMLİ)

Bu proje API anahtarını **kaynak kodun içine yazmaz**. Anahtar, Streamlit'in
`secrets` sistemi üzerinden okunur (`st.secrets["GROQ_API_KEY"]`). Bu sayede
GitHub'a yüklediğinde anahtarın herkese açık şekilde görünmesi engellenir.

### Yerelde çalıştırırken
1. `.streamlit/secrets.toml.example` dosyasını kopyala ve adını
   `.streamlit/secrets.toml` yap.
2. İçindeki `GROQ_API_KEY` ve `ADMIN_PASSWORD` değerlerini kendi bilgilerinle doldur.
3. `secrets.toml` dosyası `.gitignore` içinde olduğu için **asla** GitHub'a gitmez.

```toml
GROQ_API_KEY = "gsk_xxx..."
ADMIN_PASSWORD = "kendi-gizli-sifren"
```

### Streamlit Community Cloud'a deploy ederken
1. Projeyi GitHub'a yükle (secrets.toml dosyasını **yüklemeden**, .gitignore zaten koruyor).
2. [share.streamlit.io](https://share.streamlit.io) üzerinden yeni bir app oluştur,
   deponu ve `app.py` dosyasını seç.
3. Deploy ekranında **"Advanced settings" > "Secrets"** kısmına şunu yapıştır:

```toml
GROQ_API_KEY = "gsk_xxx..."
ADMIN_PASSWORD = "kendi-gizli-sifren"
```

4. Deploy et. Anahtarın hiçbir zaman kod içinde veya GitHub deposunda görünmez.

Groq API anahtarını buradan ücretsiz alabilirsin: https://console.groq.com/keys

## 🚀 Kurulum (Yerel)

```bash
git clone <senin-repo-linkin>
cd sazan-ai
pip install -r requirements.txt
# .streamlit/secrets.toml dosyasını yukarıdaki gibi oluştur
streamlit run app.py
```

## 📁 Proje Yapısı

```
sazan-ai/
├── app.py                          # Ana uygulama (tüm mantık burada)
├── requirements.txt                # Python bağımlılıkları
├── packages.txt                    # Streamlit Cloud sistem paketleri (opsiyonel)
├── .gitignore                      # secrets.toml ve veri klasörünü korur
├── .streamlit/
│   └── secrets.toml.example        # Kopyalanacak şablon (gerçek anahtar burada DEĞİL)
└── sazan_data/                     # Çalışma zamanında otomatik oluşur (kullanıcı verileri)
```

## ⚠️ Notlar
- Streamlit Community Cloud'daki dosya sistemi **kalıcı değildir**; uygulama
  yeniden başlatıldığında `sazan_data/` klasöründeki JSON dosyaları sıfırlanabilir.
  Kalıcı veri istiyorsan bir veritabanı (örn. Supabase, SQLite + kalıcı disk,
  veya Streamlit'in `st.connection` özelliği) kullanmanı öneririz.
- Admin paneline erişmek için sohbet kutusuna `TURKEY SAZAN` yaz, ardından
  `secrets.toml` içinde tanımladığın `ADMIN_PASSWORD` değerini gir.
