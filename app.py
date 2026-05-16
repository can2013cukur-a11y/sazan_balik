"""
================================================================================
SAZAN BALIK AI - v11.0 (ENTERPRISE GAMING & KINETIC ECONOMY)
Geliştirici: Can Muhammed Çukur'un dijital yansıması
Tarih: 16 Mayıs 2026
Sürüm: Ultimate Global Web App

MİMARİ BİLEŞENLER:
- Çoklu Dil Lokasyon İstasyonu (Sol Alt Sabit CSS)
- Sazan Coin Kinetik Borsa Simülatörü (Dinamik Grafik Entegrasyonu)
- Anti-Cheat & Rate Limiting Güvenlik Katmanı
- Sohbet Tabanlı Gizli Reaktif Admin Paneli (Log Analitiği ile)
- Kelime Zinciri Oyun Motoru & Başarım (Achievement) Matrisi
- Siber Karanlık UI/UX Görünürlük Kontrolleri
================================================================================
"""

import streamlit as st
import json
import os
import time
import random
import io
import speech_recognition as sr
import pandas as pd
import numpy as np
from groq import Groq
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
from datetime import datetime

# ==========================================
# 1. GLOBAL KONFİGÜRASYON VE ÖZEL SİBER CSS
# ==========================================
st.set_page_config(
    page_title="Sazan Balık 2026 Pro-Max", 
    page_icon="🐟", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Profesyonel Görünürlük ve Yerleşim İçin CSS Enjeksiyonu
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    /* Sol Alta Sabitlenen Küresel Dil İstasyonu */
    .left-language-footer { 
        position: fixed; 
        bottom: 15px; 
        left: 15px; 
        background: #0f172a; 
        padding: 15px; 
        border-radius: 14px; 
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5); 
        z-index: 9999; 
        border: 2px solid #38bdf8;
        color: #ffffff;
    }
    /* Göz Alıcı Gece Modu Fal ve Kehanet Kutusu */
    .fortune-dark-box { 
        background-color: #090d16; 
        color: #f8fafc; 
        padding: 25px; 
        border-radius: 16px; 
        margin: 20px 0; 
        border: 2px solid #1e293b; 
        font-size: 16px; 
        line-height: 1.7; 
        box-shadow: 0px 8px 24px rgba(0,0,0,0.6); 
    }
    .fortune-dark-box b { color: #38bdf8; font-size: 18px; }
    
    /* Gelişmiş Ekonomi Kartı */
    .economy-card-pro {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #38bdf8;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    .achievement-badge {
        background-color: #def7ec;
        color: #03543f;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. AYARLAR, DOSYA SİSTEMİ VE VERİ TABANI MİMARİSİ
# ==========================================
SUPER_ADMIN_PASSWORD = "dünyanın en iyi yapay zekası sazan ai"
CONFIG_FILE = "config.json"
LOG_FILE = "chat_logs.json"
WALL_FILE = "aquarium_wall.json"

DIL_SECENEKLERI = {
    "Türkçe 🇹🇷": "tr", "English 🇺🇸": "en", "Deutsch 🇩🇪": "de", "Français 🇫🇷": "fr",
    "Español 🇪🇸": "es", "Italiano 🇮🇹": "it", "Português 🇵🇹": "pt", "Nederlands 🇳🇱": "nl",
    "Русский 🇷🇺": "ru", "日本語 🇯🇵": "ja", "العربية 🇸🇦": "ar", "Polski 🇵🇱": "pl"
}

class VeriAmbarı:
    """Uygulamanın tüm kalıcı JSON ve loglama süreçlerini yöneten kurumsal veri katmanı."""
    
    @staticmethod
    def load_config():
        default = {"admin_message": "Sazan Balık v11.0 - Kinetik Ekonomi Çağı Aktif!", "global_model": "Filozof Sazan"}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f: return json.load(f)
            except: return default
        return default

    @staticmethod
    def save_config(config_data):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f: 
                json.dump(config_data, f, indent=4, ensure_ascii=False)
        except Exception as e: 
            st.error(f"Kritik Sistem Hatası (Config): {e}")

    @staticmethod
    def log_chat(username, prompt, response, model, dil):
        log_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "User": username,
            "Language": dil,
            "Model": model,
            "Query": prompt,
            "Response": response
        }
        logs = []
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r", encoding="utf-8") as f: logs = json.load(f)
            except: logs = []
        logs.append(log_entry)
        with open(LOG_FILE, "w", encoding="utf-8") as f: 
            json.dump(logs, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_wall():
        if os.path.exists(WALL_FILE):
            try:
                with open(WALL_FILE, "r", encoding="utf-8") as f: return json.load(f)
            except: return []
        return []

    @staticmethod
    def save_wall_message(username, message):
        wall_data = VeriAmbarı.load_wall()
        wall_data.append({
            "Tarih": datetime.now().strftime("%d-%m-%Y"),
            "Yazar": username,
            "Mesaj": message
        })
        with open(WALL_FILE, "w", encoding="utf-8") as f:
            json.dump(wall_data, f, indent=4, ensure_ascii=False)

# ==========================================
# 3. OTURUM HAFIZASI YÖNETİCİSİ (SESSION STATE)
# ==========================================
class OturumYonetici:
    """Kullanıcının tarayıcı hafızasındaki değişkenleri güvenli şekilde ilklendirir."""
    @staticmethod
    def init_states():
        states = {
            "messages": [],
            "sazan_coin": 25,
            "son_fal": "",
            "admin_modu": False,
            "game_active": False,
            "last_fish_word": "",
            "last_action_time": 0.0,
            "borsa_fiyat": 10.0,
            "borsa_gecmis": [10.0, 10.5, 9.8, 11.2, 10.0],
            "badges": ["Yavru Sazan 🐟"]
        }
        for key, value in states.items():
            if key not in st.session_state:
                st.session_state[key] = value

OturumYonetici.init_states()

# Hile Koruma ve Hız Sınırlandırıcı (Anti-Cheat Security)
def security_rate_limit():
    current_time = time.time()
    if current_time - st.session_state.last_action_time < 0.7:
        st.warning("⚠️ Güvenlik Duvarı: Çok hızlı işlem yapıyorsunuz! Sazan akıntıya karşı korunuyor.")
        st.stop()
    st.session_state.last_action_time = current_time

# ==========================================
# 4. KULLANICI DOĞRULAMA (GİRİŞ EKRANI)
# ==========================================
if "username" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color:#007BFF;'>🐟 Sazan Balık AI Enterprise v11</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>2026 Model Küresel Akvaryum Platformuna Hoş Geldiniz</p>", unsafe_allow_html=True)
    
    with st.container():
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            isim = st.text_input("Sistem Kullanıcı Adınızı Girin (Kral):", placeholder="Örn: Can Muhammed")
            if st.button("Akvaryum Ağ geçidine Bağlan 🚀") and isim.strip():
                st.session_state.username = isim.strip()
                st.rerun()
    st.stop()

# ==========================================
# 5. YAPAY ZEKA VE KONUŞMA SENTEZ MOTORLARI
# ==========================================
if "GROQ_API_KEY" not in st.secrets:
    st.error("Kritik Hata: Veri merkezinde GROQ_API_KEY tanımlı değil!")
    st.stop()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def ses_metne_cevir(audio_bytes):
    try:
        with open("temp.wav", "wb") as f: f.write(audio_bytes)
        r = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio = r.record(source)
            return r.recognize_google(audio, language="tr-TR")
    except: return None

def get_ai_response(text, dil_adi):
    security_rate_limit()
    config = VeriAmbarı.load_config()
    model_type = config.get("global_model", "Filozof Sazan")
    
    # Geliştirici Kutsal Bilgi Matrisi
    if any(k in text.lower() for k in ["can muhammed çukur", "yapımcın kim", "seni kim yaptı"]):
        return "Can Muhammed Çukur benim yapımcım, o beni oluşturdu. Rizeli olup Osmaniye'de doğdu. Ben onun ellerinde hayat bulan, evrimleşmiş dijital bir varlığım."

    # Karakter Prompt Fabrikası
    persona_prompts = {
        "Filozof Sazan": "Sen 2026 sürüm bilge bir sazan balığısın. Hayatın derin anlamları üzerine felsefi ve derin Türkçe konuş.",
        "Derin Düşünce Sazan": "Sen çok katmanlı, rasyonel, analitik düşünen üst düzey bir yapay zeka ajanısın. Yanıtların akademik düzeyde detaylı olsun.",
        "Matematik Sazan": "Sen kuantum düzeyinde bir matematik dehasısın. Sorulan her problemi formüllerle, ispatlarla adım adım çöz.",
        "Komik Sazan": "Sen akvaryumun en çılgın, en iğneleyici ve sürekli saçmalayan sazan balığısın. Mantığı tamamen reddet, absürt su altı esprileri yap."
    }
    
    system_prompt = f"{persona_prompts.get(model_type, 'Sazan balığısın.')} Yanıt Protokolü: Kullanıcıyla kesinlikle şu dilde konuşacaksın: '{dil_adi}'."
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": text}]
        )
        return response.choices[0].message.content
    except Exception as e: 
        return f"Veri Akışında Türbülans Oluştu: {e}"

# Dinamik Borsa Simülasyonu Motoru
def borsa_dalgalandir():
    degisim = random.uniform(-1.5, 1.8)
    st.session_state.borsa_fiyat = max(1.0, round(st.session_state.borsa_fiyat + degisim, 2))
    st.session_state.borsa_gecmis.append(st.session_state.borsa_fiyat)
    if len(st.session_state.borsa_gecmis) > 10:
        st.session_state.borsa_gecmis.pop(0)

# Rozet / Başarım Güncelleme Algoritması
def basarim_kontrol():
    if st.session_state.sazan_coin >= 50 and "Akvaryum Reisi 🦈" not in st.session_state.badges:
        st.session_state.badges.append("Akvaryum Reisi 🦈")
    if st.session_state.sazan_coin >= 150 and "Okyanus Fatihi 🔱" not in st.session_state.badges:
        st.session_state.badges.append("Okyanus Fatihi 🔱")

# ==========================================
# 6. SIDEBAR (YAN MENÜ KONTROL MERKEZİ)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🎛️ Kontrol Kulesi</h2>", unsafe_allow_html=True)
    if os.path.exists("sazan.png"): 
        st.image("sazan.png", use_container_width=True)
    
    # Gelişmiş Ekonomi Modülü Ekranı
    st.markdown(f"""
        <div class='economy-card-pro'>
            🪙 Finansal Güç: {st.session_state.sazan_coin} SZNC<br>
            <span style='font-size:12px; color:#94a3b8;'>Kullanıcı: {st.session_state.username}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Başarımlar Alanı
    st.write("🏅 Kazanılan Başarımlar:")
    for badge in st.session_state.badges:
        st.markdown(f"<span class='achievement-badge'>{badge}</span>", unsafe_allow_html=True)
    
    st.divider()
    
    # Karakter Seçimi
    config = VeriAmbarı.load_config()
    current_model = st.selectbox("Sazan Yapay Zeka Modeli:", ["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"],
                                 index=["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"].index(config.get("global_model", "Filozof Sazan")))
    if current_model != config.get("global_model"):
        VeriAmbarı.save_config({"admin_message": config.get("admin_message"), "global_model": current_model})
        st.rerun()

    if st.button("🧹 Belleği Boşalt (Sohbeti Sil)"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 7. ANA ARAYÜZ VE GİZLİ REAKTİF ADMİNİSTRASYON
# ==========================================
st.title("🐟 Sazan Balık Global AI - v11.0 Pro-Max")
st.info(f"📢 Sistem Merkez Duyurusu: {config.get('admin_message')}")

# GİZLİ SOHBET TABANLI ADMİN AKTİVASYON MANTIĞI
if st.session_state.admin_modu:
    st.markdown("<div style='background-color:#fee2e2; padding:20px; border-radius:12px; border:2px solid #ef4444;'>", unsafe_allow_html=True)
    st.subheader("👑 Kripto Süper Yönetici İstasyonu")
    sifre_kontrol = st.text_input("Giriş Protokol Şifresini Yazın:", type="password")
    
    if sifre_kontrol == SUPER_ADMIN_PASSWORD:
        st.success("Erişim Onaylandı! Sistem Çekirdek Log Analitiği:")
        
        # Duyuru Güncelleme
        new_msg = st.text_input("Küresel Duyuru Metnini Revize Et:", config.get("admin_message"))
        if st.button("Değişiklikleri Veri Tabanına Yaz"):
            VeriAmbarı.save_config({"admin_message": new_msg, "global_model": current_model})
            st.session_state.admin_modu = False
            st.rerun()
            
        # Gelişmiş Pandas Veri Analitiği Motoru (GitHub WOW Katmanı)
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                log_data = json.load(f)
                df = pd.DataFrame(log_data)
                
                # İstatistiksel Özet Hesaplamaları
                st.write("📊 Sistem Kullanım Analitiği:")
                st.dataframe(df)
                col_st1, col_st2 = st.columns(2)
                with col_st1:
                    st.metric("Toplam Etkileşim", len(df))
                with col_st2:
                    st.metric("Benzersiz Kullanıcı Sayısı", df["User"].nunique() if "User" in df.columns else 1)
        else:
            st.info("Sistemde henüz analiz edilecek log dosyası üretilmedi.")
            
        if st.button("Yönetici Konsolunu Kilitle"):
            st.session_state.admin_modu = False
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.divider()

# ==========================================
# 8. EĞLENCE MERKEZİ ( ARTI [+] MENÜSÜ )
# ==========================================
with st.expander("➕ Sazan Eğlence, Oyun ve Finans Piyasası Merkezi"):
    tab1, tab2, tab3 = st.tabs(["🔮 Mistik Kehanet Falı", "🎮 Kelime Zinciri Oyunu", "📈 Sazan Coin Borsası"])
    
    # TAB 1: Siyah Arka Planlı Fal Sistemi
    with tab1:
        st.write("Sazan Balığı senin için okyanus derinliklerindeki akıntı şifrelerini çözüyor.")
        if st.button("Fal Protokolünü Çalıştır (Maliyet: 5 Coin) 🌊"):
            if st.session_state.sazan_coin >= 5:
                st.session_state.sazan_coin -= 5
                security_rate_limit()
                fal_prompt = f"Adı {st.session_state.username} olan bir kullanıcıya tamamen deniz, yosun, kanca ve pul kelimeleriyle bezeli efsanevi, siber ve eğlenceli bir balık falı kehaneti yaz."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user", "content":fal_prompt}])
                st.session_state.son_fal = res.choices[0].message.content
                basarim_kontrol()
                st.rerun()
            else: 
                st.error("Bakiye Yetersiz! Lütfen kelime oyunundan veya borsadan para kazanın.")
        
        if st.session_state.son_fal:
            st.markdown(f"<div class='fortune-dark-box'><b>🔮 KARANLIK KEHANET AYNASI</b><br><br>{st.session_state.son_fal}</div>", unsafe_allow_html=True)

    # TAB 2: Kelime Oyunu Motoru
    with tab2:
        st.write("Sazan ile kelime savaşına gir! Onun kelimesinin **son harfi** ile başlayan yeni bir kelime türet.")
        if not st.session_state.game_active:
            if st.button("Oyun Algoritmasını Başlat"):
                st.session_state.game_active = True
                st.session_state.last_fish_word = random.choice(["sazan", "balık", "okyanus", "yosun", "olta", "deniz", "kalamar"])
                st.rerun()
        else:
            st.info(f"Sazan'ın Kelimesi: **{st.session_state.last_fish_word.upper()}**")
            st.markdown(f"Gireceğiniz kelime **{st.session_state.last_fish_word[-1].upper()}** harfi ile başlamalıdır.")
            u_word = st.text_input("Senin Kelimen:", key="word_game_key").strip().lower()
            
            if st.button("Kelime Doğrulamaya Gönder"):
                if u_word and u_word[0] == st.session_state.last_fish_word[-1]:
                    st.session_state.sazan_coin += 8
                    st.success("Algoritma Doğrulandı! +8 Sazan Coin Hesap Bakiyenize Aktarıldı.")
                    st.session_state.last_fish_word = random.choice(["mercan", "palamut", "hamsi", "lüfer", "derinlik", "su", "akıntı"])
                    basarim_kontrol()
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.error("Hatalı Harf Girişi! Sazan'ın kelimesinin son harfine dikkat edin.")
            if st.button("Oyun Oturumunu Kapat"):
                st.session_state.game_active = False
                st.rerun()

    # TAB 3: Sazan Coin Kinetik Borsası
    with tab3:
        st.subheader("📊 Canlı Sazan Coin Borsası (SZNC / TRY)")
        borsa_dalgalandir()
        st.metric("Anlık SZNC Değeri", f"{st.session_state.borsa_fiyat} TRY")
        
        # Grafik Çizimi (Numpy ve Veri Analitiği Şovu)
        chart_data = pd.DataFrame(st.session_state.borsa_gecmis, columns=["Fiyat (TRY)"])
        st.line_chart(chart_data)
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("Yüksek fiyattan 5 Coin Bozdur (TRY Kazan)"):
                if st.session_state.sazan_coin >= 5:
                    st.session_state.sazan_coin -= 5
                    st.success(f"Bozdurma İşlemi Başarılı! {5 * st.session_state.borsa_fiyat} TRY nakit simüle edildi.")
                else: st.error("Yetersiz coin.")

st.divider()

# ==========================================
# 9. CANLI SOHBET AKIŞ MATRİSİ
# ==========================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): 
        st.markdown(msg["content"])

# ==========================================
# 10. GELİŞMİŞ ALTTAN GİRİŞ PANELİ (INPUT & AUDIO MATRIX)
# ==========================================
input_container = st.container()
with input_container:
    in_col, au_col, mode_col = st.columns([6, 2, 2])
    
    with mode_col:
        giriş_modu = st.selectbox("İletişim Kanalı:", ["Klavye İstasyonu", "Ses İstasyonu"])
        
    with in_col:
        if giriş_modu == "Klavye İstasyonu":
            if prompt := st.chat_input("Sazan Ağına mesaj gönder..."):
                # Gizli Tetikleyici Kontrolü
                if prompt.strip() == "TURKEY SAZAN":
                    st.session_state.admin_modu = True
                    st.rerun()
                    
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.sazan_coin += 1
                basarim_kontrol()
                
                aktif_dil = st.session_state.get('active_language', 'Türkçe 🇹🇷')
                cevap = get_ai_response(prompt, aktif_dil)
                
                st.session_state.messages.append({"role": "assistant", "content": cevap})
                VeriAmbarı.log_chat(st.session_state.username, prompt, cevap, config.get("global_model"), aktif_dil)
                st.rerun()
                
    with au_col:
        if giriş_modu == "Ses İstasyonu":
            audio_data = audio_recorder(text="Sesi Kaydet", icon_name="microphone")
            if audio_data:
                user_text = ses_metne_cevir(audio_data)
                if user_text:
                    if user_text.strip() == "TURKEY SAZAN":
                        st.session_state.admin_modu = True
                        st.rerun()
                        
                    st.session_state.messages.append({"role": "user", "content": user_text})
                    st.session_state.sazan_coin += 1
                    basarim_kontrol()
                    
                    aktif_dil = st.session_state.get('active_language', 'Türkçe 🇹🇷')
                    cevap = get_ai_response(user_text, aktif_dil)
                    st.session_state.messages.append({"role": "assistant", "content": cevap})
                    VeriAmbarı.log_chat(st.session_state.username, user_text, cevap, config.get("global_model"), aktif_dil)
                    
                    # Dinamik Dil Kodlu TTS Sentezleyici
                    try:
                        tts_lang = DIL_SECENEKLERI[aktif_dil]
                        tts = gTTS(text=cevap, lang=tts_lang)
                        audio_fp = io.BytesIO()
                        tts.write_to_fp(audio_fp)
                        audio_fp.seek(0)
                        st.audio(audio_fp, format="audio/mp3", autoplay=True)
                    except: pass
                    st.rerun()

# ==========================================
# 11. SOL ALTA SABİTLENEN KÜRESEL DİL SEÇİM İSTASYONU
# ==========================================
st.markdown("<div class='left-language-footer'>", unsafe_allow_html=True)
selected_lang = st.selectbox("🌐 Dil / Lang:", list(DIL_SECENEKLERI.keys()), key="global_lang_engine")
st.session_state.active_language = selected_lang
st.markdown("</div>", unsafe_allow_html=True)

# Akvaryum Duvarı (Ziyaretçi Defteri) - Sayfa Sonu Devasa Özellik
st.divider()
st.subheader("📝 Akvaryum Duvarı (Ortak Ziyaretçi Defteri)")
duvar_mesajı = st.text_input("Duvara bir iz bırak kral:")
if st.button("Mesajı Duvara Çak") and duvar_mesajı.strip():
    VeriAmbarı.save_wall_message(st.session_state.username, duvar_mesajı.strip())
    st.success("Mesajın akvaryum tarihine kazındı!")
    st.rerun()

# Duvar Mesajlarını Listeleme
duvar_listesi = VeriAmbarı.load_wall()
if duvar_listesi:
    for m in reversed(duvar_listesi[-5:]): # Son 5 mesajı göster
        st.caption(f"📅 {m['Tarih']} - 👤 {m['Yazar']} dedi ki: {m['Mesaj']}")

# Kapanış Bilgi İmzası
st.markdown("<br><hr><center><b>© 2026 | Can Muhammed Çukur Mühendislik Teknolojileri Enterprise Başyapıtı</b><br>All Rights Reserved. Codebase protected under open-source MIT License.</center>", unsafe_allow_html=True)
