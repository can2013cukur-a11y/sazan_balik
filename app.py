"""
================================================================================
SAZAN BALIK AI - v5.5 (ULTRA PRO EDITION)
Geliştirici: Can Muhammed Çukur'un dijital yansıması
Tarih: 23 Nisan 2026
Bu uygulama, 2026 standartlarında, güncel, zeki ve derin düşünme yeteneğine 
sahip, profesyonel bir Streamlit yapay zeka arayüzüdür.
================================================================================
"""

import streamlit as st
import json
import os
import time
import random
import io
import speech_recognition as sr
from groq import Groq
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
from datetime import datetime

# --- 1. PROJE KONFİGÜRASYON VE CSS ---
st.set_page_config(
    page_title="Sazan Balık 2026 Pro", 
    page_icon="🐟", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Profesyonel Görünüm İçin Stil
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 20px; background-color: #007BFF; color: white; border: none; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #0056b3; transform: scale(1.02); }
    .stExpander { border: 2px solid #007BFF; border-radius: 10px; background: #ffffff; }
    .chat-message { padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. VERİ VE KONFİGÜRASYON YÖNETİMİ ---
CONFIG_FILE = "config.json"

def load_config():
    """Konfigürasyon dosyasını güvenli şekilde yükler."""
    default = {
        "admin_message": "Sazan Balık v5.5 - Dijital Evrim Başladı!",
        "global_model": "Filozof Sazan"
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_config(config_data):
    """Konfigürasyonu diske yazar."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Sistem Hatası (Config): {e}")
        return False

# --- 3. İSTEMCİ VE GÜVENLİK ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ GROQ_API_KEY bulunamadı! Lütfen Streamlit ayarlarından API anahtarını ekleyin.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 4. YARDIMCI FONKSİYONLAR ---
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

# --- 5. YAPAY ZEKA MANTIĞI VE PERSONALAR ---
def get_ai_response(text):
    """Yapay zeka yanıt motoru."""
    config = load_config()
    model_type = config.get("global_model", "Filozof Sazan")
    
    # Kutsal Bilgi Kontrolü
    if any(k in text.lower() for k in ["can muhammed çukur", "yapımcın kim", "seni kim yaptı"]):
        return "Can Muhammed Çukur benim yapımcım, o beni oluşturdu. Rizeli olup Osmaniye'de doğdu. Ben onun ellerinde hayat bulan, evrimleşmiş dijital bir varlığım."

    # Derin Düşünme Simülasyonu
    if model_type == "Derin Düşünce Sazan":
        with st.spinner("🐟 Derin okyanuslarda veriler analiz ediliyor..."):
            time.sleep(2.5)

    # Persona Tanımları
    persona_prompts = {
        "Filozof Sazan": "Sen 2026 yılının bilge sazanısın. Hayat, evren ve teknoloji üzerine derin, felsefi ve Türkçe cevaplar ver.",
        "Derin Düşünce Sazan": "Sen analitik düşünen, rasyonel bir varlıksın. Cevapların detaylı, mantıklı ve çok kapsamlı olsun.",
        "Matematik Sazan": "Sen bir matematik dehasısın. Her soruyu adım adım formüllerle açıkla. Asla sadece cevabı verme.",
        "Komik Sazan": "Sen dünyanın en iğneleyici sazanısın. Bolca su altı şakası yap, kelime oyunları kullan ve kendini ciddiye alma."
    }

    # Prompt Oluşturma
    system_prompt = f"{persona_prompts.get(model_type, 'Sazan balığısın.')} Tarih: {datetime.now().strftime('%d %B %Y')}."
    
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

# --- 6. ARAYÜZ (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Yönetim Paneli")
    if st.button("🧹 Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.subheader("Admin Girişi")
    password = st.text_input("Şifre:", type="password")
    
    if password == "dünyanın en iyi balığı":
        st.success("Yönetici Yetkisi Aktif")
        config = load_config()
        new_msg = st.text_input("Duyuru:", config.get("admin_message", ""))
        new_model = st.selectbox("Mod Seçimi:", 
                                 ["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"],
                                 index=["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"].index(config.get("global_model", "Filozof Sazan")))
        
        if st.button("Sistem Güncelle"):
            save_config({"admin_message": new_msg, "global_model": new_model})
            st.rerun()

# --- 7. ANA GÖVDE (MAIN) ---
config = load_config()
st.title(f"🐟 Sazan Balık v5.5")
st.caption(f"Sistem Modu: {config.get('global_model')} | {datetime.now().strftime('%d %B %Y')}")
st.info(f"📢 {config.get('admin_message')}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Görüntüle
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# İletişim Yöntemi
mod_secimi = st.radio("İletişim Yöntemi:", ["Yazışarak", "Sesli"], horizontal=True)

# İşlem Bloğu
if mod_secimi == "Yazışarak":
    if prompt := st.chat_input("Bir şeyler yaz..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            cevap = get_ai_response(prompt)
            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})

elif mod_secimi == "Sesli":
    audio_bytes = audio_recorder(text="Bas ve Konuş", icon_name="microphone")
    if audio_bytes:
        with st.spinner("Sazan dinliyor..."):
            user_text = ses_metne_cevir(audio_bytes)
            if user_text:
                st.session_state.messages.append({"role": "user", "content": user_text})
                with st.chat_message("user"): st.markdown(user_text)
                
                cevap = get_ai_response(user_text)
                with st.chat_message("assistant"):
                    st.markdown(cevap)
                    st.session_state.messages.append({"role": "assistant", "content": cevap})
                    
                    # Seslendirme Motoru
                    tts = gTTS(text=cevap, lang='tr')
                    audio_fp = io.BytesIO()
                    tts.write_to_fp(audio_fp)
                    audio_fp.seek(0)
                    st.audio(audio_fp, format="audio/mp3", autoplay=True)
            else:
                st.error("Seni duyamadım kral, tekrar denesene!")

# Footer Bilgi Bölümü
st.divider()
st.markdown("<center>© 2026 - Can Muhammed Çukur üretimi | Dijital Evrim Projesi</center>", unsafe_allow_html=True)
