import streamlit as st
from groq import Groq

# 1. Sayfa Ayarları
st.set_page_config(page_title="Sazan Balık AI", page_icon="🐟")
st.title("🐟 Sazan Balık AI")

# 2. Güvenli API Bağlantısı (Anahtar Streamlit'in kasasından çekilir)
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("Kral, anahtar kasada bulunamadı! Lütfen Streamlit ayarlarından 'Secrets' kısmına GROQ_API_KEY ekle.")
    st.stop()

# 3. Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Geçmişi Ekrana Yaz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Mesajlaşma
if prompt := st.chat_input("Sazan Balık'a bir şey yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sazan Balık düşünüyor..."):
            try:
                stream = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Sen komik ve iğneleyici bir sazan balığısın. İngilizce yasak, Türkçe konuş."},
                        *st.session_state.messages
                    ],
                    model="llama-3.3-70b-versatile",
                    stream=True
                )
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")