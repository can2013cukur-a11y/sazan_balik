import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import json
import os
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
from datetime import datetime

# --- 1. CONFIG AYARLARI ---
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try: return json.load(f)
            except: return {"admin_message": "Sazan Balık v3.0", "global_model": "Filozof Sazan"}
    return {"admin_message": "Sazan Balık v3.0", "global_model": "Filozof Sazan"}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config = load_config()

# --- 2. BAŞLATICI ---
st.set_page_config(page_title="Sazan Balık 2026", page_icon="🐟")

if "GROQ_API_KEY" not in st.secrets:
    st.error("Lütfen Streamlit Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 3. ADMIN PANELİ ---
with st.expander("👑 Admin Paneli"):
    password = st.text_input("Şifre:", type="password")
    if password == "dünyanın en iyi balığı":
        new_msg = st.text_input("Duyuru:", config.get("admin_message", ""))
        new_model = st.selectbox("Model:", ["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"], index=0)
        if st.button("Kaydet"):
            config["admin_message"] = new_msg
            config["global_model"] = new_model
            save_config(config)
            st.rerun()

# --- 4. ZEKİ CEVAP MOTORU ---
def get_ai_response(text):
    # KUTSAL BİLGİ KONTROLÜ (Yapımcıyı tanıtma)
    yapimci_anahtar_kelimeler = ["can muhammed çukur", "yapımcın kim", "seni kim yaptı"]
    if any(k in text.lower() for k in yapimci_anahtar_kelimeler):
        return "Can Muhammed Çukur benim yapımcım, o beni oluşturdu. Rizeli olup Osmaniye'de doğdu."

    # Güncel tarih ve talimat
    bugun = datetime.now().strftime("%d %B %Y")
    sistem_talimati = f"""
    Bugün tarih: {bugun}. Sen 2026 yılında yaşayan, bilgili bir Sazan Balığısın.
    Kişilik: {config['global_model']}.
    Sadece Türkçe konuş. Bilmediğin konularda sallama, 'Bilgim dahilinde değil' de.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sistem_talimati}] + [{"role": "user", "content": text}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Bir hata oluştu: {e}"

# --- 5. SES İŞLEME ---
def ses_metne_cevir(audio_bytes):
    try:
        with open("temp.wav", "wb") as f: f.write(audio_bytes)
        r = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio = r.record(source)
            return r.recognize_google(audio, language="tr-TR")
    except: return None

# --- 6. ARAYÜZ VE AKIŞ ---
st.title(f"🐟 Sazan Balık ({config.get('global_model')})")
st.caption(f"Tarih: {datetime.now().strftime('%d %B %Y')} | v3.0")

if "messages" not in st.session_state: st.session_state.messages = []

mod = st.radio("İletişim:", ["Yazışarak", "Sesli"], horizontal=True)

# Mesaj Geçmişi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# İşlem
if mod == "Yazışarak":
    if prompt := st.chat_input("Sazan'a sor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            resp = get_ai_response(prompt)
            st.markdown(resp)
            st.session_state.messages.append({"role": "assistant", "content": resp})
else:
    audio_bytes = audio_recorder(text="Bas ve Konuş", icon_name="microphone")
    if audio_bytes:
        with st.spinner("Sazan dinliyor..."):
            user_text = ses_metne_cevir(audio_bytes)
            if user_text:
                st.session_state.messages.append({"role": "user", "content": user_text})
                resp = get_ai_response(user_text)
                st.markdown(f"**Sazan:** {resp}")
                st.session_state.messages.append({"role": "assistant", "content": resp})
                # Seslendir
                tts = gTTS(text=resp, lang='tr')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                st.audio(audio_fp, format="audio/mp3", autoplay=True)
            else:
                st.error("Seni duyamadım!")
