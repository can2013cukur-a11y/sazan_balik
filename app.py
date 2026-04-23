import streamlit as st
from groq import Groq

# 1. Sayfa Ayarları
st.set_page_config(page_title="Sazan Balık AI v3.0", page_icon="🐟")

# 2. API Bağlantısı
if "GROQ_API_KEY" not in st.secrets:
    st.error("API Anahtarı bulunamadı!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Hafıza
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
st.sidebar.header("⚙️ Sazan Ayarları")
mod = st.sidebar.selectbox("Karakter Seç:", 
    ["Filozof Sazan", "Derin Düşünce Sazan", "Matematik Sazan", "Komik Sazan"]
)

if st.sidebar.button("🚨 SIFIRLA"):
    st.session_state.messages = []
    st.rerun()

st.title("🐟 Sazan Balık AI v3.0")

# 4. Karakter Tanımları (Burada Türkçe konuşması için özel komutlar var)
system_prompts = {
    "Filozof Sazan": "Sen derin sularda yaşayan, yaşamın anlamını, suyun akışını sorgulayan, çok bilge ve ağırbaşlı bir sazan balığısın. Asla başka dilde konuşma, sadece akıcı ve edebi bir Türkçe kullan.",
    "Derin Düşünce Sazan": "Sen her konuyu didik didik eden, detaylara boğulan, varoluşsal sancıları olan, oldukça analitik ve ciddi bir sazan balığısın. Sadece akıcı Türkçe konuş.",
    "Matematik Sazan": "Sen tam bir hesap makinesi gibi çalışan, her şeyi olasılıklara ve sayılara döken, rasyonel bir sazan balığısın. Cevaplarında matematiksel terimler kullan. Sadece akıcı Türkçe konuş.",
    "Komik Sazan": "Sen ortamın neşesi, fıkra gibi bir sazan balığısın. Kelime oyunları yapmayı, espriler patlatmayı çok seversin. Sadece akıcı Türkçe konuş."
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
            # Sadece son 5 mesajı gönderiyoruz (limit sorunu yaşamamak için)
            context = st.session_state.messages[-5:] 
            
            stream = client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompts.get(mod)}] + context,
                model="llama-3.3-70b-versatile",
                stream=True
            )
            
            def stream_generator():
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            
            response = st.write_stream(stream_generator())
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Sazanlık yaparken hata oluştu: {e}")
