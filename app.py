import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title="Sesli Sazan Balık", page_icon="🐟")

# API Ayarları
if "GROQ_API_KEY" not in st.secrets:
    st.error("API Anahtarı eksik!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🐟 Sesli Sazan Balık")

# Mikrofon Kaydedici (Walkie-Talkie Tarzı)
audio_bytes = audio_recorder(
    text="Bas ve Konuş",
    recording_color="#e74c3c",
    neutral_color="#6c757d",
    icon_name="microphone",
    icon_size="2x",
)

# Sohbeti tut
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ses İşleme Fonksiyonu
def ses_metne_cevir(audio_bytes):
    r = sr.Recognizer()
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
    with sr.AudioFile("temp.wav") as source:
        audio_data = r.record(source)
        try:
            return r.recognize_google(audio_data, language="tr-TR")
        except:
            return None

# Konuşma akışı
if audio_bytes:
    with st.spinner("Dinliyorum..."):
        user_text = ses_metne_cevir(audio_bytes)
        
    if user_text:
        st.success(f"Sen dedin ki: {user_text}")
        st.session_state.messages.append({"role": "user", "content": user_text})
        
        # AI Cevabı
        with st.chat_message("assistant"):
            with st.spinner("Sazan düşünüyor..."):
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": user_text}]
                )
                response_text = completion.choices[0].message.content
                st.markdown(response_text)
                
                # Sesli Yanıt
                tts = gTTS(text=response_text, lang='tr')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                st.audio(audio_fp, format="audio/mp3", autoplay=True)
                
                st.session_state.messages.append({"role": "assistant", "content": response_text})

# Geçmişi Göster
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
