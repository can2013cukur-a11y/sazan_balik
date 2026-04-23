import streamlit as st
from groq import Groq

# 1. Sayfa Ayarları
st.set_page_config(page_title="Sazan Balık AI - Sıfırlandı", page_icon="🐟")

# 2. API Bağlantısı
if "GROQ_API_KEY" not in st.secrets:
    st.error("API Anahtarı bulunamadı!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Hafızayı Sıfırlama Butonu
if st.sidebar.button("🚨 TÜM HAFIZAYI SIFIRLA"):
    st.session_state.messages = []
    st.rerun()

# 4. Sohbet Geçmişi Yönetimi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Başlık
st.title("🐟 Sazan Balık AI")
st.caption("Hafıza tamamen temizlenebilir.")

# Geçmişi Ekrana Bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Sohbet Motoru
if prompt := st.chat_input("Sazan'a bir şey yaz..."):
    # Yeni mesajı ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot cevabı (Sadece son 5 mesajı göndererek hata almayı engelliyoruz)
    with st.chat_message("assistant"):
        try:
            # Geçmişi sınırla (Token limitini aşmamak için)
            context = st.session_state.messages[-5:] 
            
            stream = client.chat.completions.create(
                messages=[{"role": "system", "content": "Sen bir sazan balığısın."}] + context,
                model="llama-3.3-70b-versatile",
                stream=True
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Hata: {e}")
