import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import json
import os
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
from datetime import datetime

# --- 1. AYARLAR VE CONFIG YÖNETİMİ ---
CONFIG_FILE = "config.json"

def load_config():
    """Config dosyasını okur, yoksa varsayılanları döner."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {"admin_message": "Sazan Balık v2.0 Aktif", "global_model": "Filozof Sazan"}
    return {"admin_message": "Sazan Balık v2.0 Aktif", "global_model": "Filozof Sazan"}

def save_config(config):
    """Config dosyasını kaydeder."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config = load_config()

# --- 2. SAYFA VE İSTEMCİ AYARLARI ---
st.set_page_config(page_title="Sazan Balık AI 2026", page_icon="🐟")

if "GROQ_API_KEY" not in st.secrets:
    st.error("API Anahtarı bulunamadı! Lütfen Secrets kısmına ekle.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 3. ADMIN PANELİ ---
with st.expander("👑 Admin Paneli (Yönetim)"):
    password = st.text_input("Admin Şifresi:", type="password")
    if password == "dünyanın en iyi balığı":
        st.success("Yönetici girişi başarılı!")
        new_msg = st.text_input("Duyuru Mesajı:", config.get("admin_message", ""))
        new_model = st.selectbox(
            "Model Seçimi:", 
            ["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"],
            index=["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"].index(config.get("global_model", "Filozof Sazan"))
        )
        if st.button("Ayarları Güncelle"):
            config["admin_message"] = new_msg
            config["global_model"] = new_model
            save_config(config)
            st.rerun()
    elif password:
        st.error("😡 Sazan Balık: 'Haddini bil, yanlış şifre!'")

# --- 4. GÜNCEL ZAMAN VE BİLGİLENDİRME ---
if config.get("admin_message"):
    st.info(f"📢 **Admin Duyurusu:** {config['admin_message']}")

st.title(f"🐟 Sazan Balık ({config.get('global_model')})")
st.caption(f"Sistem Tarihi: {datetime.now().strftime('%d %B %Y')} - Güncel ve 2026 Modunda.")

# --- 5. SES İŞLEME MOTORU ---
def ses_metne_cevir(audio_bytes):
    try:
        with open("temp.wav", "wb") as f:
            f.write(audio_bytes)
        r = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio_data = r.record(source)
            return r.recognize_google(audio_data, language="tr-TR")
    except Exception as e:
        return f"Hata: {str(e)}"

# --- 6. AI CEVAP MOTORU (2026 GÜNCEL) ---
def get_ai_response(text):
    bugun = datetime.now().strftime("%d %B %Y")
    
    sistem_talimati = f"""
    Bugün tarih: {bugun}. Sen 2026 yılında yaşayan, teknolojiye, bilime ve güncel olaylara hakim 
    modern bir Sazan Balığısın. 
    Kişiliğin: {config['global_model']}.
    Eski bilgileri değil, 2026'nın güncel dünyasını baz alarak konuş. 
    Asla '2023' veya öncesine dair kısıtlı bilgilerle cevap verme.
    Cevapların kısa, öz ve zekice olsun. Sadece Türkçe konuş.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": sistem_talimati}] + 
                  st.session_state.get("messages", [])[-5:] + 
                  [{"role": "user", "content": text}]
    )
    return completion.choices[0].message.content

# --- 7. SOHBET AKIŞI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

mod_input = st.radio("İletişim Modu:", ["Yazışarak", "Sesli"], horizontal=True)

# Mesajları görüntüle
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- İŞLEM (Yazı/Ses) ---
# A) YAZI MODU
if mod_input == "Yazışarak":
    if prompt := st.chat_input("Sazan'a bir şey yaz..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Sazan düşünüyor..."):
                resp = get_ai_response(prompt)
                st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp})

# B) SES MODU
else:
    audio_bytes = audio_recorder(text="Bas ve Konuş", icon_name="microphone")
    if audio_bytes:
        with st.spinner("Sazan dinliyor..."):
            user_text = ses_metne_cevir(audio_bytes)
            
            if user_text and "Hata" not in user_text:
                st.write(f"🎤 Sen: {user_text}")
                st.session_state.messages.append({"role": "user", "content": user_text})
                
                with st.spinner("Sazan cevaplıyor..."):
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
                st.error("Seni duyamadım veya mikrofon hatası var!")
