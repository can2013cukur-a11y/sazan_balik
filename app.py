import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import json
import os

# --- 1. AYARLAR VE CONFIG OKUMA ---
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"admin_message": "", "global_model": "Filozof Sazan"}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config = load_config()

# --- 2. SAYFA VE API ---
st.set_page_config(page_title="Sazan Balık AI", page_icon="🐟")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 3. ADMIN PANELİ ---
with st.expander("👑 Admin Paneli"):
    password = st.text_input("Admin Şifresi:", type="password")
    if password == "dünyanın en iyi balığı":
        st.success("Yönetici girişi başarılı!")
        new_msg = st.text_input("Herkese Duyuru (Mesaj):", config.get("admin_message", ""))
        new_model = st.selectbox("Modeli Değiştir:", 
                                 ["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"],
                                 index=["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"].index(config.get("global_model", "Filozof Sazan")))
        
        if st.button("Ayarları Kaydet"):
            config["admin_message"] = new_msg
            config["global_model"] = new_model
            save_config(config)
            st.rerun()
    elif password:
        st.error("😡 Sazan Balık: 'Haddini bil, yanlış şifre!'")

# --- 4. ARAYÜZ VE DUYURU ---
if config.get("admin_message"):
    st.info(f"📢 **Admin Duyurusu:** {config['admin_message']}")

st.title(f"🐟 Sazan Balık ({config.get('global_model')})")

mod_input = st.radio("İletişim Modu:", ["Yazışarak", "Sesli"], horizontal=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. SOHBET MOTORU ---
def get_ai_response(text):
    prompts = {
        "Filozof Sazan": "Sen derin sularda yaşayan bilge bir sazan balığısın. Sadece Türkçe konuş.",
        "Derin Düşünce Sazan": "Sen analitik, detaycı bir sazan balığısın. Sadece Türkçe konuş.",
        "Matematik Sazan": "Sen rasyonel, matematiksel terimler kullanan bir sazan balığısın. Sadece Türkçe konuş.",
        "Komik Sazan": "Sen çok esprili, kelime oyunları yapan bir sazan balığısın. Sadece Türkçe konuş."
    }
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompts.get(config['global_model'])}] + st.session_state.messages[-5:] + [{"role": "user", "content": text}]
    )
    return completion.choices[0].message.content

# Mesajları Ekrana Yazdır
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. İŞLEM (YAZI/SES) ---
if prompt := st.chat_input("Sazan'a bir şey yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sazan düşünüyor..."):
            response = get_ai_response(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Eğer mod Sesli ise seslendir
            if mod_input == "Sesli":
                tts = gTTS(text=response, lang='tr')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                st.audio(audio_fp, format="audio/mp3", autoplay=True)
