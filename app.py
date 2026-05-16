"""
================================================================================
SAZAN BALIK AI - v12.0 (THE ULTIMATE GLOBAL ARCHITECTURE)
Geliştirici: Can Muhammed Çukur'un dijital yansıması
Tarih: 16 Mayıs 2026
Sürüm: Production-Ready Cyber Akvaryum

MİMARİ BİLEŞENLER:
- Dinamik Alt Giriş Barı (Klavye, Mikrofon ve [+] Eğlence Entegrasyonu)
- Ücretli Oyun Algoritması (Giriş: 10 SZNC, Hata: -5 SZNC)
- Global Sazan Borsası (Sidebar Kullanıcı Coin Sıralama & Liderlik Tablosu)
- Sol Alt Lokasyon Tabanlı Dil Motoru (Fixed CSS)
- Kapsamlı Pandas Veri Özetleyici (Gizli Admin Modülü İçin)
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
from groq import Groq
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
from datetime import datetime

# ==========================================
# 1. GLOBAL KONFİGÜRASYON VE SİBER APERATİF CSS
# ==========================================
st.set_page_config(
    page_title="Sazan Balık v12.0 Ultra Pro", 
    page_icon="🐟", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Arayüzü Tamamen Değiştiren ve Görseldeki Girişi Özelleştiren CSS Matrisi
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    
    /* Sol Alta Sabitlenen Küresel Dil İstasyonu */
    .left-language-footer { 
        position: fixed; 
        bottom: 15px; 
        left: 15px; 
        background: #0f172a; 
        padding: 12px; 
        border-radius: 14px; 
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5); 
        z-index: 9999; 
        border: 2px solid #38bdf8;
        color: #ffffff;
    }
    
    /* Karanlık Mod Fal Veri Kutusu */
    .fortune-dark-box { 
        background-color: #0b0f19; 
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
    
    /* Global Borsa Listesi Tasarımı */
    .borsa-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #38bdf8;
        margin-bottom: 10px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    
    /* Buton Yumuşatma ve Animasyon */
    .stButton>button { border-radius: 20px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.03); }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. AYARLAR, GÜVENLİK VE DOSYA VERİ TABANI KATMANI
# ==========================================
SUPER_ADMIN_PASSWORD = "dünyanın en iyi yapay zekası sazan ai"
CONFIG_FILE = "config.json"
LOG_FILE = "chat_logs.json"
ECONOMY_FILE = "sazan_economy.json"

DIL_SECENEKLERI = {
    "Türkçe 🇹🇷": "tr", "English 🇺🇸": "en", "Deutsch 🇩🇪": "de", "Français 🇫🇷": "fr",
    "Español 🇪🇸": "es", "Italiano 🇮🇹": "it", "Português 🇵🇹": "pt", "Nederlands 🇳🇱": "nl",
    "Русский 🇷🇺": "ru", "日本語 🇯🇵": "ja", "العربية 🇸🇦": "ar", "Polski 🇵🇱": "pl"
}

class MerkezVeriDeposu:
    """Uygulamanın tüm dosya okuma, yazma, loglama ve borsa verilerini işleyen ana motor."""
    
    @staticmethod
    def load_config():
        default = {"admin_message": "Sazan Balık v12.0 - Global Borsa ve Alt Bar Entegrasyonu Aktif!", "global_model": "Filozof Sazan"}
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
        except Exception as e: st.error(f"Config Kayıt Hatası: {e}")

    @staticmethod
    def log_chat(username, prompt, response, model, dil):
        log_entry = {
            "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Kullanıcı": username,
            "Dil": dil,
            "Model": model,
            "Soru": prompt,
            "Cevap": response
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
    def load_economy():
        """Tüm kullanıcıların coin bakiyelerini kalıcı dosyadan çeker."""
        if os.path.exists(ECONOMY_FILE):
            try:
                with open(ECONOMY_FILE, "r", encoding="utf-8") as f: return json.load(f)
            except: return {}
        return {}

    @staticmethod
    def save_user_coin(username, coin_amount):
        """Kullanıcının coin miktarını küresel veri tabanına kaydeder ve günceller."""
        economy_data = MerkezVeriDeposu.load_economy()
        economy_data[username] = coin_amount
        with open(ECONOMY_FILE, "w", encoding="utf-8") as f:
            json.dump(economy_data, f, indent=4, ensure_ascii=False)

# ==========================================
# 3. DİNAMİK OTURUM BELLEĞİ (SESSION STATE)
# ==========================================
class OturumKontrolMerkezi:
    @staticmethod
    def baslat():
        states = {
            "messages": [],
            "sazan_coin": 30,
            "son_fal": "",
            "admin_modu": False,
            "game_active": False,
            "last_fish_word": "",
            "active_input_mode": "🔤 Klavye",
            "show_plus_menu": False
        }
        for key, value in states.items():
            if key not in st.session_state:
                st.session_state[key] = value

OturumKontrolMerkezi.baslat()

# ==========================================
# 4. KULLANICI YETKİLENDİRME (GİRİŞ KAPISI)
# ==========================================
if "username" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color:#007BFF;'>🐟 Sazan Balık Global AI - v12</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Gelişmiş Algoritmik Akvaryum Ağ Sürücüsü</p>", unsafe_allow_html=True)
    
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        giren_isim = st.text_input("Sisteme Giriş İçin Kullanıcı Adı Belirleyin:")
        if st.button("Akvaryum Oturumunu Aç 🚀") and giren_isim.strip():
            st.session_state.username = giren_isim.strip()
            # İlk girişte ekonomiye kaydet veya eski bakiyeyi yükle
            mevcut_ekonomi = MerkezVeriDeposu.load_economy()
            if st.session_state.username in mevcut_ekonomi:
                st.session_state.sazan_coin = mevcut_ekonomi[st.session_state.username]
            else:
                MerkezVeriDeposu.save_user_coin(st.session_state.username, st.session_state.sazan_coin)
            st.rerun()
    st.stop()

# ==========================================
# 5. YAPAY ZEKA VE KONUŞMA TANIMA SİSTEMLERİ
# ==========================================
if "GROQ_API_KEY" not in st.secrets:
    st.error("Kritik Sistem Hatası: GROQ_API_KEY bulunamadı!")
    st.stop()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def ses_analiz_et(audio_bytes):
    try:
        with open("temp.wav", "wb") as f: f.write(audio_bytes)
        r = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio = r.record(source)
            return r.recognize_google(audio, language="tr-TR")
    except: return None

def sazan_beyin_motoru(text, dil_adi):
    config = MerkezVeriDeposu.load_config()
    model_type = config.get("global_model", "Filozof Sazan")
    
    # Can Muhammed Çukur Kutsal Kod Entegrasyonu
    if any(k in text.lower() for k in ["can muhammed çukur", "yapımcın kim", "seni kim yaptı"]):
        return "Can Muhammed Çukur benim yapımcım, o beni oluşturdu. Rizeli olup Osmaniye'de doğdu. Ben onun ellerinde hayat bulan, evrimleşmiş dijital bir varlığım."

    prompts = {
        "Filozof Sazan": "Sen bilge bir sazan balığısın. Hayat ve okyanuslar üzerine derin edebi ve felsefi cümleler kur.",
        "Derin Düşünce Sazan": "Sen üst düzey analitik zekaya sahip rasyonel bir yapay zekasın. Cevapların çok detaylı ve ispatlı olsun.",
        "Matematik Sazan": "Sen evrensel bir matematik profesörüsün. Soruları formüllerle adım adım çöz.",
        "Komik Sazan": "Sen dünyanın en iğneleyici ve saçmalayan sazan balığısın. Mantığı reddet, absürt su altı esprileri yap ve saçmala."
    }
    
    system_instruction = f"{prompts.get(model_type, 'Sazan balığısın.')} Konuşacağın dil protokolü: '{dil_adi}'."
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": text}]
        )
        return response.choices[0].message.content
    except Exception as e: return f"Veri Protokol Hatası: {e}"

# ==========================================
# 6. SIDEBAR: GLOBAL SAZAN BORSASI (LİDERLİK TABLOSU)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>📈 Küresel İstasyon</h2>", unsafe_allow_html=True)
    if os.path.exists("sazan.png"): st.image("sazan.png", use_container_width=True)
    
    st.markdown(f"<div class='borsa-card'>🪙 Senin Bakiyen: <b>{st.session_state.sazan_coin} SZNC</b></div>", unsafe_allow_html=True)
    
    # KÜRESEL SAZAN BORSASI SIRA LİSTESİ
    st.subheader("📊 Global Sazan Borsası")
    st.caption("Akvaryumdaki En Zengin Kullanıcılar:")
    
    tum_ekonomi = MerkezVeriDeposu.load_economy()
    if tum_ekonomi:
        # Verileri Pandas ile Sıralama Şovu
        df_ekonomi = pd.DataFrame(list(tum_ekonomi.items()), columns=["Kullanıcı", "Bakiye (SZNC)"])
        df_ekonomi = df_ekonomi.sort_values(by="Bakiye (SZNC)", ascending=False).reset_index(drop=True)
        
        for index, row in df_ekonomi.head(10).iterrows():
            madalya = "🥇" if index == 0 else "🥈" if index == 1 else "🥉" if index == 2 else "🐟"
            st.markdown(f"{madalya} **{row['Kullanıcı']}**: {row['Bakiye (SZNC)']} SZNC")
    else:
        st.info("Borsa verisi henüz oluşmadı.")
        
    st.divider()
    
    # Karakter Mod Değiştirici
    config = MerkezVeriDeposu.load_config()
    secilen_model = st.selectbox("Sazan Karakter Tipi:", ["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"],
                                 index=["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"].index(config.get("global_model", "Filozof Sazan")))
    if secilen_model != config.get("global_model"):
        MerkezVeriDeposu.save_config({"admin_message": config.get("admin_message"), "global_model": secilen_model})
        st.rerun()

    if st.button("🧹 Sohbet Akışını Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 7. ANA EKRAN VE GİZLİ SOHBET ADMİNİSTRASYONU
# ==========================================
st.title("🐟 Sazan Balık Global Pro - v12.0")
st.info(f"📢 Akvaryum Duyurusu: {config.get('admin_message')}")

# TURKEY SAZAN Komutuyla Tetiklenen Gizli Adminlik Alanı
if st.session_state.admin_modu:
    st.markdown("<div style='background-color:#1e293b; color:white; padding:20px; border-radius:12px; border:2px solid #38bdf8;'>", unsafe_allow_html=True)
    st.subheader("👑 Kripto Süper Yönetici Paneli")
    girilen_sifre = st.text_input("Süper yetki için şifreyi gir kral:", type="password")
    
    if girilen_sifre == SUPER_ADMIN_PASSWORD:
        st.success("Erişim Yetkisi Sağlandı.")
        yeni_duyuru = st.text_input("Duyuru Metnini Revize Et:", config.get("admin_message"))
        if st.button("Duyuruyu Veri Tabanına Yaz"):
            MerkezVeriDeposu.save_config({"admin_message": yeni_duyuru, "global_model": secilen_model})
            st.session_state.admin_modu = False
            st.rerun()
            
        if os.path.exists(LOG_FILE):
            st.write("📊 Akvaryum Detaylı İletişim Logları:")
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                st.dataframe(pd.DataFrame(json.load(f)))
        
        if st.button("Yönetici Konsolunu Kapat"):
            st.session_state.admin_modu = False
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.divider()

# Sohbet Mesajlarını Ekrana Basma Bölümü
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ==========================================
# 8. Gelişmiş EĞLENCE (+) MENÜSÜ AKTİVASYONU
# ==========================================
if st.session_state.show_plus_menu:
    st.markdown("<div style='background-color:#f1f5f9; padding:20px; border-radius:12px; border:1px solid #cbd5e1; margin-bottom:15px;'>", unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.subheader("🔮 Mistik Balık Falı (5 Coin)")
        if st.button("Kehanet Altyapısını Tetikle 🌊"):
            if st.session_state.sazan_coin >= 5:
                st.session_state.sazan_coin -= 5
                MerkezVeriDeposu.save_user_coin(st.session_state.username, st.session_state.sazan_coin)
                f_prompt = f"Adı {st.session_state.username} olan kullanıcı için tamamen siber-komik, deniz ve kanca terimlerini içeren bir balık falı kehaneti üret."
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f_prompt}])
                st.session_state.son_fal = res.choices[0].message.content
                st.rerun()
            else: st.error("Yetersiz Bakiye! Kelime oyunundan coin kasabilirsin.")
            
        if st.session_state.son_fal:
            st.markdown(f"<div class='fortune-dark-box'><b>🔮 KARANLIK KEHANET AYNASI</b><br><br>{st.session_state.son_fal}</div>", unsafe_allow_html=True)
            
    with col_t2:
        st.subheader("🎮 Kelime Zinciri Oyunu (Giriş: 10 SZNC | Hata: -5 SZNC)")
        if not st.session_state.game_active:
            if st.button("10 Coin Öde ve Oyunu Başlat 🪙"):
                if st.session_state.sazan_coin >= 10:
                    st.session_state.sazan_coin -= 10
                    MerkezVeriDeposu.save_user_coin(st.session_state.username, st.session_state.sazan_coin)
                    st.session_state.game_active = True
                    st.session_state.last_fish_word = random.choice(["sazan", "balık", "okyanus", "yosun", "olta", "deniz"])
                    st.rerun()
                else: st.error("Bakiyeniz bu oyuna girmek için yetersiz!")
        else:
            st.info(f"Sazan'ın Kelimesi: **{st.session_state.last_fish_word.upper()}**")
            st.caption(f"Gireceğin kelime **{st.session_state.last_fish_word[-1].upper()}** harfi ile başlamak zorunda!")
            u_word = st.text_input("Senin Kelimen:", key="game_word_input_field").strip().lower()
            
            c_g1, c_g2 = st.columns(2)
            with c_g1:
                if st.button("Kelimeyi Onayla"):
                    if u_word and u_word[0] == st.session_state.last_fish_word[-1]:
                        st.session_state.sazan_coin += 20 # Kazanma ödülü yüksek
                        MerkezVeriDeposu.save_user_coin(st.session_state.username, st.session_state.sazan_coin)
                        st.success("Doğru Hamle! +20 Sazan Coin Kazandın!")
                        st.session_state.last_fish_word = random.choice(["mercan", "palamut", "hamsi", "lüfer", "derinlik", "su"])
                        time.sleep(0.8)
                        st.rerun()
                    else:
                        st.session_state.sazan_coin -= 5 # Ceza Sistemi
                        MerkezVeriDeposu.save_user_coin(st.session_state.username, st.session_state.sazan_coin)
                        st.error("Yanlış kelime! Hata bedeli: -5 Sazan Coin kasanızdan düşüldü.")
                        time.sleep(0.8)
                        st.rerun()
            with c_g2:
                if st.button("Oyundan Çekil"):
                    st.session_state.game_active = False
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 9. DİNAMİK ALT GİRİŞ İSTASYONU (İSTEDİĞİN ÖZEL REASONS)
# ==========================================
st.write("") # Boşluk ayarı
st.divider()

# Butonların ve girişin yan yana kusursuz dizilmesi için 4 kolonlu sistem
bar_col_plus, bar_col_mode, bar_col_input, bar_col_audio = st.columns([1, 1.5, 6, 1.5])

with bar_col_plus:
    if st.button("➕ Eğlence"):
        st.session_state.show_plus_menu = not st.session_state.show_plus_menu
        st.rerun()

with bar_col_mode:
    girdi_turu = st.selectbox("Mod:", ["🔤 Klavye", "🎤 Mikrofon"], label_visibility="collapsed")
    st.session_state.active_input_mode = girdi_turu

with bar_col_input:
    if st.session_state.active_input_mode == "🔤 Klavye":
        if user_prompt := st.chat_input("Sazan Ağına mesaj gönder..."):
            if user_prompt.strip() == "TURKEY SAZAN":
                st.session_state.admin_modu = True
                st.rerun()
                
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            st.session_state.sazan_coin += 1
            MerkezVeriDeposu.save_user_coin(st.session_state.username, st.session_state.sazan_coin)
            
            su_an_dil = st.session_state.get('active_language', 'Türkçe 🇹🇷')
            ai_output = sazan_beyin_motoru(user_prompt, su_an_dil)
            
            st.session_state.messages.append({"role": "assistant", "content": ai_output})
            MerkezVeriDeposu.log_chat(st.session_state.username, user_prompt, ai_output, config.get("global_model"), su_an_dil)
            st.rerun()

with bar_col_audio:
    if st.session_state.active_input_mode == "🎤 Mikrofon":
        ses_verisi = audio_recorder(text="", icon_name="microphone", icon_size="2x")
        if ses_verisi:
            ses_text = ses_analiz_et(ses_verisi)
            if ses_text:
                if ses_text.strip() == "TURKEY SAZAN":
                    st.session_state.admin_modu = True
                    st.rerun()
                
                st.session_state.messages.append({"role": "user", "content": ses_text})
                st.session_state.sazan_coin += 1
                MerkezVeriDeposu.save_user_coin(st.session_state.username, st.session_state.sazan_coin)
                
                su_an_dil = st.session_state.get('active_language', 'Türkçe 🇹🇷')
                ai_output = sazan_beyin_motoru(ses_text, su_an_dil)
                st.session_state.messages.append({"role": "assistant", "content": ai_output})
                MerkezVeriDeposu.log_chat(st.session_state.username, ses_text, ai_output, config.get("global_model"), su_an_dil)
                
                # Ses Sentezleme
                try:
                    tts_kod = DIL_SECENEKLERI[su_an_dil]
                    tts = gTTS(text=ai_output, lang=tts_kod)
                    audio_stream = io.BytesIO()
                    tts.write_to_fp(audio_stream)
                    audio_stream.seek(0)
                    st.audio(audio_stream, format="audio/mp3", autoplay=True)
                except: pass
                st.rerun()

# ==========================================
# 10. SOL ALTA SABİTLENEN KÜRESEL DİL SEÇİM İSTASYONU
# ==========================================
st.markdown("<div class='left-language-footer'>", unsafe_allow_html=True)
secilen_global_dil = st.selectbox("🌐 Dil / Lang:", list(DIL_SECENEKLERI.keys()), key="ultimate_lang_engine_box")
st.session_state.active_language = secilen_global_dil
st.markdown("</div>", unsafe_allow_html=True)

# Alt Telif Hakkı Kapanışı
st.markdown("<br><br><center><small>© 2026 | Can Muhammed Çukur Savunma ve Yazılım Sanayii Başyapıtı</small></center>", unsafe_allow_html=True)
