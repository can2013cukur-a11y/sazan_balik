"""
================================================================================
SAZAN BALIK AI - v9.0 (GLOBAL ULTIMATE ENTERPRISE)
Geliştirici: Can Muhammed Çukur'un dijital yansıması
Tarih: 16 Mayıs 2026
Bu uygulama; 25 bağımsız uluslararası dil desteği, gelişmiş oturum tabanlı 
ekonomi (Sazan Coin), talih çarkı, yapay zeka balık falı motoru ve çok katmanlı 
admin panelleri ile donatılmış, GitHub standartlarını altüst eden bir mimaridir.
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

# --- 1. PROJE KONFİGÜRASYON VE CSS ---
st.set_page_config(
    page_title="Sazan Balık 2026 Pro", 
    page_icon="🐟", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Profesyonel ve Küresel Görünüm İçin Stil Geliştirmeleri
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 20px; background-color: #007BFF; color: white; border: none; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #0056b3; transform: scale(1.02); }
    .stExpander { border: 2px solid #007BFF; border-radius: 10px; background: #ffffff; }
    .chat-message { padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; }
    .global-footer { position: fixed; bottom: 10px; right: 10px; background: white; padding: 10px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); z-index: 999; }
    .fortune-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 15px; margin: 15px 0; }
    .economy-card { background-color: #e0f7fa; padding: 15px; border-radius: 10px; border-left: 5px solid #00acc1; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GÜVENLİK VE AYAR SABİTLERİ ---
SUPER_ADMIN_PASSWORD = "dünyanın en iyi yapay zekası sazan ai"
ADMIN_PASSWORD = "dünyanın en iyi balığı"
CONFIG_FILE = "config.json"
LOG_FILE = "chat_logs.json"

# 25 Dil ve Bayrak Eşleştirmesi
DIL_SECENEKLERI = {
    "Türkçe 🇹🇷": "tr", "English 🇺🇸": "en", "Deutsch 🇩🇪": "de", "Français 🇫🇷": "fr",
    "Español 🇪🇸": "es", "Italiano 🇮🇹": "it", "Português 🇵🇹": "pt", "Nederlands 🇳🇱": "nl",
    "Русский 🇷🇺": "ru", "日本語 🇯🇵": "ja", "한국어 🇰🇷": "ko", "中文 🇨🇳": "zh",
    "العربية 🇸🇦": "ar", "हिन्दी 🇮🇳": "hi", "Ελληνικά 🇬🇷": "el", "Svenska 🇸🇪": "sv",
    "Norsk 🇳🇴": "no", "Dansk 🇩🇰": "da", "Suomi 𝔽🇮": "fi", "Polski 🇵🇱": "pl",
    "Čeština 🇨🇿": "cs", "Română 🇷🇴": "ro", "Magyar 🇭🇺": "hu", "Українська 🇺🇦": "uk",
    "Tiếng Việt 🇻🇳": "vi"
}

# --- 3. VERİ VE KONFİGÜRASYON YÖNETİMİ ---
class SistemMerkezi:
    @staticmethod
    def load_config():
        """Konfigürasyon dosyasını güvenli şekilde yükler."""
        default = {
            "admin_message": "Sazan Balık v9.0 - Dijital Evrim Küreselleşti!",
            "global_model": "Filozof Sazan"
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f: return json.load(f)
            except Exception: return default
        return default

    @staticmethod
    def save_config(config_data):
        """Konfigürasyonu diske yazar."""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            st.error(f"Sistem Hatası (Config): {e}")
            return False

    @staticmethod
    def log_chat(username, prompt, response, model, dil):
        """Kullanıcı verilerini ve konuşma geçmişini derinlemesine loglar."""
        log_entry = {
            "Zaman": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
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
            except Exception: logs = []
        logs.append(log_entry)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)

# --- 4. SESSİON STATE (OTURUM HAFIZASI) BAŞLATMA ---
if "messages" not in st.session_state: st.session_state.messages = []
if "sazan_coin" not in st.session_state: st.session_state.sazan_coin = 10
if "cark_hakkı" not in st.session_state: st.session_state.cark_hakkı = True
if "son_fal" not in st.session_state: st.session_state.son_fal = ""

# --- 5. KULLANICI GİRİŞ EKRANI (İSİM SORMA) ---
if "username" not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🐟 Sazan Balık Global AI Giriş Paneli</h1>", unsafe_allow_html=True)
    st.write("<center>2026 Nesil Yapay Zeka Akvaryumuna Giriş Yapıyorsunuz</center>", unsafe_allow_html=True)
    isim_input = st.text_input("Lütfen Adınızı Girin (Kral):", key="giris_isim")
    if st.button("Akvaryuma Gir 🚀"):
        if isim_input.strip() != "":
            st.session_state.username = isim_input.strip()
            st.rerun()
        else:
            st.warning("İsim alanı boş bırakılamaz!")
    st.stop()

# --- 6. İSTEMCİ VE GÜVENLİK ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ GROQ_API_KEY bulunamadı! Lütfen Streamlit ayarlarından API anahtarını ekleyin.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 7. SES İŞLEME MOTORU ---
def ses_metne_cevir(audio_bytes):
    """Ses verisini metne dönüştürür."""
    try:
        with open("temp.wav", "wb") as f: f.write(audio_bytes)
        r = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio = r.record(source)
            return r.recognize_google(audio, language="tr-TR")
    except Exception:
        return None

# --- 8. YAPAY ZEKA MANTIĞI VE KÜRESEL PERSONALAR ---
def get_ai_response(text, secilen_dil_adi):
    """Yapay zeka yanıt motoru (Çoklu Dil ve Karakter Entegrasyonu)."""
    config = SistemMerkezi.load_config()
    model_type = config.get("global_model", "Filozof Sazan")
    
    # Kutsal Bilgi Kontrolü
    if any(k in text.lower() for k in ["can muhammed çukur", "yapımcın kim", "seni kim yaptı"]):
        return f"Can Muhammed Çukur benim yapımcım, o beni oluşturdu. Rizeli olup Osmaniye'de doğdu. Ben onun ellerinde hayat bulan, evrimleşmiş dijital bir varlığım."

    # Derin Düşünme Simülasyonu
    if model_type == "Derin Düşünce Sazan":
        with st.spinner("🐟 Derin okyanuslarda veriler analiz ediliyor..."):
            time.sleep(2.5)

    # Temel Persona Şablonları
    persona_prompts = {
        "Filozof Sazan": "Sen 2026 yılının bilge sazanısın. Hayat, evren ve teknoloji üzerine derin felsefi cevaplar ver.",
        "Derin Düşünce Sazan": "Sen analitik düşünen, rasyonel bir varlıksın. Cevapların detaylı, mantıklı ve çok kapsamlı olsun.",
        "Matematik Sazan": "Sen bir matematik dehasısın. Her soruyu adım adım formüllerle açıkla. Asla sadece cevabı verme.",
        "Komik Sazan": "Sen dünyanın en iğneleyici ve saçmalayan sazanısın. Mantıksız konuş, bolca su altı şakası yap, kelime oyunları kullan ve saçmala."
    }

    # Küresel Dil Entegrasyon Komutu
    dil_talimati = f"CRITICAL: You must answer and communicate dynamicly in the selected language: '{secilen_dil_adi}'. Adapt your culture and idioms to this language."

    system_prompt = f"{persona_prompts.get(model_type, 'Sazan balığısın.')} {dil_talimati} Tarih: {datetime.now().strftime('%d %B %Y')}."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sistemde küçük bir akıntı sorunu oldu: {e}"

# --- 9. YAPAY ZEKA BALIK FALI MOTORU ---
def balık_falı_bak(isim, dil):
    """Tamamen deniz ve balık temalı, yapay zeka tabanlı fal üreticisi."""
    prompt = f"Adı {isim} olan birine tamamen deniz, akvaryum, kanca, okyanus, akıntı ve pul terimlerini kullanarak eğlenceli, gizemli ve kehanet dolu bir balık falı yaz."
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Sen mistik bir falcı balıksın. Sadece şu dilde cevap yazacaksın: {dil}"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception:
        return "Geleceğin şu an yosunlar altında, göremiyorum..."

# --- 10. ARAYÜZ: YAN MENÜ (SIDEBAR / HIERARCHY MANAGEMENT) ---
with st.sidebar:
    if os.path.exists("sazan.png"):
        st.image("sazan.png", use_container_width=True)
    else:
        st.warning("🐟 Sazan fotoğrafı bulunamadı (sazan.png dosyası eksik).")

    st.write(f"🐳 Kaptan: **{st.session_state.username}**")
    
    # Sazan Coin Göstergesi
    st.markdown(f"<div class='economy-card'>🪙 Sazan Coin bakiyeniz: {st.session_state.sazan_coin} SZNC</div>", unsafe_allow_html=True)
    st.divider()

    st.header("⚙️ Sazan Ayarları")
    config = SistemMerkezi.load_config()
    current_model = st.selectbox("Kişilik Seç:", 
                                 ["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"],
                                 index=["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"].index(config.get("global_model", "Filozof Sazan")))
    
    if current_model != config.get("global_model"):
        SistemMerkezi.save_config({"admin_message": config.get("admin_message", ""), "global_model": current_model})
        st.rerun()

    if st.button("🧹 Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # --- OYUNLAŞTIRMA MODÜLÜ: ŞANSLI SAZAN ÇARKIFELEĞİ ---
    st.subheader("🎡 Şanslı Sazan Çarkı")
    if st.session_state.cark_hakkı:
        if st.button("Çarkı Çevir (Günde 1)"):
            oduller = [5, 10, -3, 20, 0]
            cekilen = random.choice(oduller)
            st.session_state.sazan_coin += cekilen
            st.session_state.cark_hakkı = False
            if cekilen > 0: st.success(f"Harika! {cekilen} Sazan Coin Kazandın!")
            elif cekilen < 0: st.error(f"Ayy! Akıntıya kapıldın, {abs(cekilen)} Coin kaybettin!")
            else: st.info("Pas geçtin! Ödül yok.")
            time.sleep(1)
            st.rerun()
    else:
        st.caption("Bugünlük çark hakkınız bitmiştir kaptan!")

    st.divider()
    
    # --- YÖNETİCİ GİRİŞ KATMANLARI (ADMIN & SUPER ADMIN) ---
    st.subheader("🔑 Yönetim İstasyonu")
    password = st.text_input("Erişim Şifresi:", type="password")
    
    if password == ADMIN_PASSWORD:
        st.success("Standart Yönetici Yetkisi Aktif")
        new_msg = st.text_input("Duyuru Güncelle:", config.get("admin_message", ""))
        if st.button("Duyuruyu Kaydet"):
            SistemMerkezi.save_config({"admin_message": new_msg, "global_model": current_model})
            st.rerun()
            
    elif password == SUPER_ADMIN_PASSWORD:
        st.warning("👑 SÜPER ADMİN YETKİSİ AKTİF")
        st.write("Tüm Küresel Akvaryum Kayıtları Veri Tabanı:")
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
                df = pd.DataFrame(logs)
                st.dataframe(df)
        else:
            st.info("Henüz veri tabanında log kaydı yok.")

# --- 11. ANA GÖVDE (MAIN INTERFACE) ---
st.title(f"🐟 Sazan Balık v9.0 Global")
st.caption(f"Aktif Karakter: {config.get('global_model')} | Veri İletişim Protokolü: 2026 Sürüm")
st.info(f"📢 {config.get('admin_message')}")

# --- EĞLENCE MODÜLÜ: MİSTİK FAL SEKMESİ ---
with st.expander("🔮 Mistik Balık Falı Çek (Maliyeti: 5 Sazan Coin)"):
    st.write("Sazan Balığı senin için okyanus akıntılarını ve yıldızları incelesin mi?")
    if st.button("Falımı Bak 🌊"):
        if st.session_state.sazan_coin >= 5:
            st.session_state.sazan_coin -= 5
            with st.spinner("Yosunlar temizleniyor, kehanet yazılıyor..."):
                fal_sonucu = balık_falı_bak(st.session_state.username, "Türkçe")
                st.session_state.son_fal = fal_sonucu
                st.rerun()
        else:
            st.error("Yetersiz Sazan Coin! Çarkıfelekten coin kazanabilirsin.")
    if st.session_state.son_fal:
        st.markdown(f"<div class='fortune-box'><b>🔮 İşte Kehanetin:</b><br><br>{st.session_state.son_fal}</div>", unsafe_allow_html=True)

st.divider()

# Sohbet Geçmişini Ekrana Basma
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# İletişim Yöntemi Seçimi
mod_secimi = st.radio("İletişim Metodu:", ["Yazışarak", "Sesli"], horizontal=True)

# Sağ Alttaki Dünya İşareti ve 25 Dil Seçim Dünyası (İstediğin Küresel Yapı)
with st.container():
    st.markdown("<div class='global-footer'>", unsafe_allow_html=True)
    secilen_dil = st.selectbox("🌐 Dil / Language:", list(DIL_SECENEKLERI.keys()), index=0)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 12. OPERASYONEL İŞLEM BLOĞU ---
if mod_secimi == "Yazışarak":
    if prompt := st.chat_input("Sazan'a küresel dilde bir mesaj gönder..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        # Konuştuğu için kullanıcıyı ödüllendir (Ekonomi Sistemi)
        st.session_state.sazan_coin += 1
        
        with st.chat_message("assistant"):
            cevap = get_ai_response(prompt, secilen_dil)
            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})
            # Sistemi Derin Loglama Havuzuna Gönder
            SistemMerkezi.log_chat(st.session_state.username, prompt, cevap, config.get("global_model"), secilen_dil)

elif mod_secimi == "Sesli":
    audio_bytes = audio_recorder(text="Bas ve Konuş", icon_name="microphone")
    if audio_bytes:
        with st.spinner("Sazan dalgaları dinliyor..."):
            user_text = ses_metne_cevir(audio_bytes)
            if user_text:
                st.session_state.messages.append({"role": "user", "content": user_text})
                with st.chat_message("user"): st.markdown(user_text)
                
                st.session_state.sazan_coin += 1
                cevap = get_ai_response(user_text, secilen_dil)
                
                with st.chat_message("assistant"):
                    st.markdown(cevap)
                    st.session_state.messages.append({"role": "assistant", "content": cevap})
                    SistemMerkezi.log_chat(st.session_state.username, user_text, cevap, config.get("global_model"), secilen_dil)
                    
                    # Seslendirme Motoru (Seçilen Dil Koduna Göre Dinamik Ses Üretir)
                    try:
                        dil_kodu = DIL_SECENEKLERI[secilen_dil]
                        tts = gTTS(text=cevap, lang=dil_kodu)
                        audio_fp = io.BytesIO()
                        tts.write_to_fp(audio_fp)
                        audio_fp.seek(0)
                        st.audio(audio_fp, format="audio/mp3", autoplay=True)
                    except Exception:
                        st.caption("Bu dil için ses sentezleyici dalgalara takıldı.")
            else:
                st.error("Seni duyamadım kral, akıntı sesi çok fazla! Tekrar dener misin?")

# --- 13. SİSTEM KAPANIŞ BİLGİSİ (FOOTER) ---
st.divider()
st.markdown("<center>© 2026 - Can Muhammed Çukur üretimi | Küresel Dijital Evrim ve Yapay Zeka Mimari Projesi</center>", unsafe_allow_html=True)
