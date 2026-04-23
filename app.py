import streamlit as st
from groq import Groq
import json

# 1. Sayfa Ayarları
st.set_page_config(page_title="Sazan Balık AI - v2.0", page_icon="🐟")

# 2. API Bağlantısı
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Anahtarı bulunamadı! Lütfen Streamlit ayarlarından Secrets kısmını kontrol et.")
    st.stop()

# 3. Sidebar (Ayarlar)
with st.sidebar:
    st.header("⚙️ Sazan Ayarları")
    mod = st.selectbox("Mod Seç:", ["Filozof Sazan", "İğneleyici Sazan", "Normal Sazan"])
    
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 💾 Kayıt")
    if "messages" in st.session_state and st.session_state.messages:
        conv_json = json.dumps(st.session_state.messages, ensure_ascii=False)
        st.download_button("Konuşmayı İndir", conv_json, file_name="sohbet.json", mime="application/json")

# 4. Başlık ve Mod Göstergesi
st.title("🐟 Sazan Balık AI - v2.0")
st.info(f"Mod: {mod} aktif.")

# 5. Sohbet Geçmişi Yönetimi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmişi ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Sohbet Mantığı
if prompt := st.chat_input("Sazan Balık'a yaz..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot cevabı
    with st.chat_message("assistant"):
        # Mod seçimine göre sistem promptu
        system_prompts = {
            "Filozof Sazan": "Sen derin düşüncelere dalan, balık felsefesi yapan çok bilge ama aynı zamanda sazan balığı olduğun için biraz unutkan bir filozofsun.",
            "İğneleyici Sazan": "Sen her şeye laf sokan, çok bilmiş, iğneleyici ve komik bir sazan balığısın.",
            "Normal Sazan": "Sen yardımsever ve nazik bir sazan balığısın."
        }
        
        stream = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompts.get(mod, "Sen bir sazan balığısın.")},
                *st.session_state.messages
            ],
            model="llama-3.3-70b-versatile",
            stream=True
        )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
