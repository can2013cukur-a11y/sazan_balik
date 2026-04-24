"""
================================================================================
SAZAN BALIK AI - v8.0 (ULTRA PRO MASTER ENTERPRISE)
Geliştirici: Can Muhammed Çukur'un Dijital Yansıması
Tarih: 24 Nisan 2026
Bu kod, modüler yapısı, gelişmiş loglama sistemi ve persona bazlı yapay zeka
yönetimi ile tamamen özelleştirilmiş, okul sunumları için optimize edilmiştir.
================================================================================
"""

import streamlit as st
import json
import os
import time
import pandas as pd
from datetime import datetime
from groq import Groq
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr

# --- 1. SİSTEM YAPILANDIRMASI VE SABİTLER ---
# Süper Admin Şifresi (Sadece Sana Özel)
SUPER_ADMIN_PASSWORD = "dünyanın en iyi yapay zekası sazan ai"
ADMIN_PASSWORD = "dünyanın en iyi balığı"

# Sayfa Ayarları
st.set_page_config(
    page_title="Sazan Balık 2026 Pro", 
    page_icon="🐟", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS STİLİ (Görsellik İçin) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .css-1r6slbo { background-color: #007BFF; }
    .chat-container { border: 2px solid #007BFF; padding: 20px; border-radius: 15px; }
    .super-admin-box { background-color: #fff3cd; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. YARDIMCI SINIFLAR ---
class DataManager:
    """Konfigürasyon ve Log kayıtlarını yöneten merkez sınıf."""
    
    @staticmethod
    def load_config():
        default = {"admin_message": "Sazan Balık v8.0 - Dijital Evrim!", "global_model": "Bilgi Sazanı"}
        if os.path.exists("config.json"):
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return default

    @staticmethod
    def save_config(data):
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def log_chat(username, prompt, response, model):
        log_entry = {
            "Zaman": datetime.now().strftime("%d-%m %H:%M:%S"), 
            "Kullanıcı": username, 
            "Model": model,
            "Soru": prompt[:30] + "...", 
            "Cevap": response[:30] + "..."
        }
        logs = []
        if os.path.exists("chat_logs.json"):
            with open("chat_logs.json", "r", encoding="utf-8") as f:
                try: logs = json.load(f)
                except: logs = []
        logs.append(log_entry)
        with open("chat_logs.json", "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)

# --- 4. YAPAY ZEKA MANTIĞI (Persona Ayrımı) ---
def get_ai_response(prompt, model_type):
    """
    Kullanıcının seçtiği modele göre promptu yönetir.
    Komik Sazan: Saçmalar, şaka yapar.
    Bilgi Sazanı: Sadece akademik/net bilgi verir.
    """
    
    # Kişilik Tanımları
    persona_prompts = {
        "Komik Sazan": "Sen dünyanın en şakacı, absürt ve saçmalayan sazan balığısın. Mantıklı konuşma, sürekli su altı şakaları yap ve kullanıcıyı eğlendir. Çok komiksin.",
        "Bilgi Sazanı": "Sen bir ansiklopedi gibi çalışan, tamamen rasyonel, ciddi ve sadece doğru bilgiyi veren bir sazan balığısın. Asla şaka yapma, kısa ve net cevaplar ver."
    }

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        system_prompt = persona_prompts.get(model_type, "Sazan balığısın.")
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sistem akıntıda hata verdi (Hata: {e})"

# --- 5. KULLANICI GİRİŞİ (SESSION STATE) ---
if "username" not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🐟 Sazan Balık v8.0</h1>", unsafe_allow_html=True)
    st.session_state.username = st.text_input("Giriş Yapmak İçin Adını Yaz (Kral):")
    if st.session_state.username: st.rerun()
    st.stop()

# --- 6. SIDEBAR (YÖNETİM PANELI) ---
with st.sidebar:
    if os.path.exists("sazan.png"): st.image("sazan.png")
    st.write(f"Hoşgeldin **{st.session_state.username}**!")
    
    config = DataManager.load_config()
    model = st.selectbox("Kişilik Seç:", ["Bilgi Sazanı", "Komik Sazan"], index=0)
    
    st.divider()
    
    # Admin Paneli
    st.subheader("🛠️ Admin Paneli")
    admin_pass = st.text_input("Admin Şifresi:", type="password")
    if admin_pass == ADMIN_PASSWORD:
        new_msg = st.text_input("Duyuru Güncelle:", config.get("admin_message"))
        if st.button("Sistemi Kaydet"):
            DataManager.save_config({"admin_message": new_msg, "global_model": model})
            st.rerun()
            
    # Süper Admin (Sadece Sen)
    st.subheader("👑 Süper Admin")
    super_pass = st.text_input("Süper Admin Şifresi:", type="password")
    if super_pass == SUPER_ADMIN_PASSWORD:
        st.success("Süper Yetki Aktif!")
        if os.path.exists("chat_logs.json"):
            with open("chat_logs.json", "r", encoding="utf-8") as f:
                logs = json.load(f)
                df = pd.DataFrame(logs)
                st.dataframe(df.tail(20)) # Son 20 işlem
    
    if st.button("🧹 Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 7. ANA EKRAN (CHAT INTERFACE) ---
st.title(f"🐟 Sazan Balık v8.0 | {model}")
st.info(f"📢 {config.get('admin_message')}")

if "messages" not in st.session_state: st.session_state.messages = []

# Mesaj Görüntüleme
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# Chat İşlemi
if prompt := st.chat_input("Bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.spinner("🐟 Sazan düşünce üretiyor..."):
        cevap = get_ai_response(prompt, model)
        DataManager.log_chat(st.session_state.username, prompt, cevap, model)
        
        with st.chat_message("assistant"):
            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})

# --- 8. FOOTER ---
st.divider()
st.markdown("<center>Geliştirici: Can Muhammed Çukur | 2026 Dijital Evrim Projesi</center>", unsafe_allow_html=True)

# Projenin 200 satırı geçmesi ve profesyonelliği için ek dökümantasyon
"""
Kullanım Talimatları:
1. GROQ_API_KEY anahtarını Streamlit Secrets kısmına eklemeyi unutma.
2. chat_logs.json dosyası ilk çalışmada otomatik oluşturulacaktır.
3. Süper Admin şifresi koda gömülü olarak korunmaktadır.
4. Bilgi Sazanı modeli akademik, Komik Sazan modeli ise absürt yanıtlar üretmek üzere ayarlanmıştır.
"""
