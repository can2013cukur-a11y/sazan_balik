import streamlit as st
from groq import Groq

# 1. Sayfa Ayarları
st.set_page_config(page_title="Sazan Balık AI", page_icon="🐟")

# 2. API Bağlantısı
if "GROQ_API_KEY" not in st.secrets:
    st.error("API Anahtarı bulunamadı! Ayarlardan ekle.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Hafıza Yönetimi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar (Sıfırlama Butonu)
if st.sidebar.button("🚨 SIFIRLA VE YENİDEN BAŞLAT"):
    st.session_state.messages = []
    st.rerun()

st.title("🐟 Sazan Balık AI")

# Sohbeti Ekrana Bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Sohbet Motoru (Hata Geçirmez)
if prompt := st.chat_input("Sazan'a yaz..."):
    # Mesajı ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot cevabı
    with st.chat_message("assistant"):
        try:
            # API'den cevap al
            stream = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                stream=True
            )
            
            # Gelen veriyi sadece metin olarak ayıkla ve ekrana yaz
            def stream_generator():
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            
            response = st.write_stream(stream_generator())
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Sazanlık yaparken teknik bir sorun oldu: {e}")
