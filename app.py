import streamlit as st
from groq import Groq
import json
import random

# 1. Sayfa Ayarları
st.set_page_config(page_title="Sazan Balık AI - v2.6", page_icon="🐟", layout="wide")

# 2. API Bağlantısı
if "GROQ_API_KEY" not in st.secrets:
    st.error("API Anahtarı bulunamadı! Lütfen Streamlit ayarlarından 'Secrets' kısmına GROQ_API_KEY ekle.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Sohbet Geçmişi ve Sayaç
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mesaj_sayisi" not in st.session_state:
    st.session_state.mesaj_sayisi = 0

# 4. Sidebar
with st.sidebar:
    st.header("⚙️ Sazan Paneli")
    mod = st.selectbox("Karakter Seç:", ["Filozof Sazan", "İğneleyici Sazan", "Normal Sazan"])
    
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.session_state.mesaj_sayisi = 0
        st.rerun()

# 5. Başlık
st.title("🐟 Sazan Balık AI - v2.6")

# 6. Mesajları Ekrana Yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Sohbet Motoru (Hata Düzeltici Temizleyici ile)
if prompt := st.chat_input("Sazan Balık'a derin bir şeyler söyle..."):
    # Mesajı ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot cevabı
    with st.chat_message("assistant"):
        system_prompts = {
            "Filozof Sazan": "Sen derin sularda yüzen, balık felsefesi yapan, biraz unutkan ama çok bilge bir sazan balığısın.",
            "İğneleyici Sazan": "Sen çok bilmiş, laf sokmayı seven, sarkastik bir sazan balığısın.",
            "Normal Sazan": "Sen yardımsever, sakin, gölün huzurunu temsil eden bir sazan balığısın."
        }
        
        # VERİ TEMİZLEME: API'ye göndermeden önce tüm geçmişi temizle
        clean_history = []
        for m in st.session_state.messages:
            # Sadece içeriği olan ve boş olmayan mesajları al
            if m.get("content"):
                clean_history.append({"role": str(m["role"]), "content": str(m["content"])})
        
        try:
            stream = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompts.get(mod, "Sen bir sazan balığısın.")},
                    *clean_history # Temizlenmiş geçmişi gönderiyoruz
                ],
                model="llama-3.3-70b-versatile",
                stream=True
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Sazanlık yaparken hata oluştu (Sohbeti temizle butonuna bas): {e}")
