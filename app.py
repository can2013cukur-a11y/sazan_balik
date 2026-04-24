"""
================================================================================
SAZAN BALIK AI - v7.0 (ULTRA PRO ENTERPRISE EDITION)
================================================================================
"""

import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import pandas as pd # Verileri tablo olarak göstermek için

# --- 1. SİSTEM YAPILANDIRMASI & CSS ---
st.set_page_config(page_title="Sazan Balık 2026 Pro", page_icon="🐟", layout="wide")

st.markdown("""
    <style>
    .big-font { font-size: 20px !important; font-weight: bold; color: #007BFF; }
    .stApp { background-color: #f0f2f6; }
    .chat-bubble { padding: 15px; border-radius: 15px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. YARDIMCI SINIFLAR (LOGGING, CONFIG) ---
class SystemManager:
    @staticmethod
    def load_config():
        default = {"admin_message": "Sazan Balık v7.0 Yayında!", "global_model": "Filozof Sazan"}
        if os.path.exists("config.json"):
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return default

    @staticmethod
    def save_config(data):
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def log_chat(username, prompt, response):
        entry = {"Zaman": datetime.now().strftime("%H:%M:%S"), "Kullanıcı": username, "Soru": prompt, "Cevap": response[:50] + "..."}
        logs = []
        if os.path.exists("chat_logs.json"):
            with open("chat_logs.json", "r", encoding="utf-8") as f:
                try: logs = json.load(f)
                except: logs = []
        logs.append(entry)
        with open("chat_logs.json", "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)

# --- 3. AI MOTORU ---
def get_ai_response(prompt, model_type):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        system_prompt = f"Sen {model_type} karakterisin. 2026 yılındayız."
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sazan şu an nefes alamıyor: {e}"

# --- 4. KULLANICI GİRİŞİ ---
if "username" not in st.session_state:
    st.markdown("<center><h1>🐟 Sazan Balık Giriş Kapısı</h1></center>", unsafe_allow_html=True)
    st.session_state.username = st.text_input("Sohbete başlamak için adını gir (Kral):")
    if st.session_state.username: st.rerun()
    st.stop()

# --- 5. SIDEBAR (YÖNETİM VE AYARLAR) ---
with st.sidebar:
    if os.path.exists("sazan.png"): st.image("sazan.png")
    st.write(f"Hoşgeldin, **{st.session_state.username}**")
    
    # Model Ayarı (Herkes için)
    config = SystemManager.load_config()
    model = st.selectbox("Modeli Seç:", ["Filozof Sazan", "Komik Sazan", "Matematik Sazan"], index=0)
    
    st.divider()
    
    # Admin Paneli
    st.subheader("🛠️ Admin Paneli")
    if st.text_input("Admin Şifresi:", type="password") == "dünyanın en iyi balığı":
        new_msg = st.text_input("Duyuru Güncelle:", config.get("admin_message"))
        if st.button("Güncelle"):
            SystemManager.save_config({"admin_message": new_msg, "global_model": model})
            st.success("Sistem güncellendi!")
    
    # Süper Admin (Sadece sen)
    st.subheader("👑 Süper Admin")
    if st.text_input("Süper Şifre:", type="password") == "kendi_özel_sifren": # BURAYI KENDİ ŞİFREN YAP
        st.warning("Veri Merkezi Erişimine Girdin.")
        if os.path.exists("chat_logs.json"):
            with open("chat_logs.json", "r", encoding="utf-8") as f:
                logs = json.load(f)
                df = pd.DataFrame(logs)
                st.dataframe(df.tail(15)) # Son 15 kayıt

# --- 6. ANA EKRAN VE SOHBET ---
st.title("🐟 Sazan Balık v7.0")
st.info(config.get("admin_message"))

if "messages" not in st.session_state: st.session_state.messages = []

# Mesaj geçmişi göster
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Sazan'a bir şey sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.spinner("🐟 Sazan düşünüyor..."):
        response = get_ai_response(prompt, model)
        SystemManager.log_chat(st.session_state.username, prompt, response)
        
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- 7. FOOTER ---
st.divider()
st.caption("2026 - Can Muhammed Çukur üretimi | Dijital Evrim Projesi")
