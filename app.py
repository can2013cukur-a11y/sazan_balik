import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import json
import os
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder

# --- 1. AYARLAR VE CONFIG ---
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"admin_message": "Sazan Balık v1.0", "global_model": "Filozof Sazan"}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config = load_config()

# --- 2. BAŞLATICI ---
st.set_page_config(page_title="Sazan Balık AI", page_icon="🐟")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 3. ADMIN PANELİ ---
with st.expander("👑 Admin Paneli"):
    password = st.text_input("Admin Şifresi:", type="password")
    if password == "dünyanın en iyi balığı":
        new_msg = st.text_input("Duyuru:", config.get("admin_message", ""))
        new_model = st.selectbox("Model:", ["Filozof Sazan", "Komik Sazan"], index=0)
        if st.button("Kaydet"):
            config["admin_message"] = new_msg
            config["global_model"] = new_model
            save_config(config)
            st.rerun()

# --- 4. SOHBET MOTORU (CORE) ---
def get_ai_response(text):
    prompt_map = {"Filozof Sazan": "Bilge bir sazan balığısın.", "Komik Sazan": "Esprili bir sazan balığısın."}
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt_map.get(config['global_model'], "Sazan balığısın.")}] + 
                  [{"role": "user", "content": text}]
    )
    return completion.choices[0].message.content

# --- 5. SES İŞLEME ---
def ses_metne_cevir(audio_bytes):
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
    r = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio = r.record(source)
        try:
            return r.recognize_google(audio, language="tr-TR")
        except:
            return None

# --- 6. ARAYÜZ ---
st.title(f"🐟 Sazan Balık ({config.get('global_model')})")
mod = st.radio("Mod:", ["Yazışarak", "Sesli"], horizontal=True)

if "messages" not in st.session_state: st.session_state.messages = []

# Yazı Modu
if mod == "Yazışarak":
    if prompt := st.chat_input("Bir şeyler yaz..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        resp = get_ai_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": resp})
        st.rerun()

# Sesli Mod
else:
    audio_bytes = audio_recorder(text="Bas ve Konuş", icon_name="microphone")
    if audio_bytes:
        with st.spinner("Sazan dinliyor..."):
            user_text = ses_metne_cevir(audio_bytes)
            if user_text:
                st.write(f"Sen dedin ki: {user_text}")
                resp = get_ai_response(user_text)
                
                # Seslendir
                tts = gTTS(text=resp, lang='tr')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                st.audio(audio_fp, format="audio/mp3", autoplay=True)
                st.markdown(f"**Sazan:** {resp}")
            else:
                st.error("Seni duyamadım, tekrar dener misin?")

# Geçmişi Göster
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])
