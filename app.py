import streamlit as st
from groq import Groq
from gtts import gTTS  # Ses için yeni kütüphane
import os

# 1. Sayfa Ayarları
st.set_page_config(page_title="Sazan Balık AI v4.0", page_icon="🐟")

# 2. API Bağlantısı
if "GROQ_API_KEY" not in st.secrets:
    st.error("API Anahtarı bulunamadı!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Hafıza
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MOBİL İÇİN DÜZENLEME (Ana sayfaya taşıdık) ---
st.title("🐟 Sazan Balık AI v4.0")

# Mod seçimi ve temizleme butonu artık sidebar'da değil, üstte!
col1, col2 = st.columns([3, 1])
with col1:
    mod = st.selectbox("Karakterini Seç:", 
        ["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"]
    )
with col2:
    if st.button("Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# 4. Karakter Tanımları
system_prompts = {
    "Filozof Sazan": "Sen derin sularda yaşayan bilge bir sazan balığısın. Sadece akıcı Türkçe konuş.",
    "Derin Düşünce Sazan": "Sen analitik ve ciddi bir sazan balığısın. Sadece akıcı Türkçe konuş.",
    "Matematik Sazan": "Sen hesap makinesi gibi çalışan rasyonel bir sazan balığısın. Sadece akıcı Türkçe konuş.",
    "Komik Sazan": "Sen neşeli, esprili bir sazan balığısın. Sadece akıcı Türkçe konuş."
}

# Sohbeti Ekrana Bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Sohbet Motoru
if prompt := st.chat_input("Sazan'a bir şey yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompts.get(mod)}] + st.session_state.messages[-5:],
                model="llama-3.3-70b-versatile",
                stream=True
            )
            
            # Cevabı birleştir
            full_response = ""
            response_placeholder = st.empty()
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # --- SESLENDİRME ---
            tts = gTTS(text=full_response, lang='tr')
            tts.save("cevap.mp3")
            st.audio("cevap.mp3", format="audio/mp3")

        except Exception as e:
            st.error(f"Sazanlık yaparken hata oluştu: {e}")
