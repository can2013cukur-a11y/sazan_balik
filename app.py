import streamlit as st
from groq import Groq
import json
import random

# 1. Sayfa Ayarları
st.set_page_config(page_title="Sazan Balık AI - v2.5", page_icon="🐟", layout="wide")

# 2. API Bağlantısı (Kilitli Kasa)
if "GROQ_API_KEY" not in st.secrets:
    st.error("API Anahtarı bulunamadı! Lütfen Streamlit ayarlarından 'Secrets' kısmına GROQ_API_KEY ekle.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Sazan Felsefesi (Rastgele sözler için)
sazan_sozleri = [
    "Akıntıya karşı yüzmeyen balık, balık değildir.",
    "Bazen sadece suyun tadını çıkarmak gerekir, felsefe sonra gelir.",
    "Pullarımın parlaklığı, ruhumun derinliğini yansıtmaz.",
    "Yem her zaman bedava değildir, oltaya dikkat et!",
    "Beni anlamak için önce suyun içindeki sessizliği duyman lazım."
]

# 4. Sohbet Geçmişi ve Sayaç
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mesaj_sayisi" not in st.session_state:
    st.session_state.mesaj_sayisi = 0

# 5. Sidebar (Ayarlar ve İstatistikler)
with st.sidebar:
    st.header("🐟 Sazan Paneli")
    mod = st.selectbox("Karakter Seç:", ["Filozof Sazan", "İğneleyici Sazan", "Normal Sazan"])
    
    st.info(f"Sazan Bilgeliği: {random.choice(sazan_sozleri)}")
    
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.session_state.mesaj_sayisi = 0
        st.rerun()
    
    st.markdown("---")
    st.write(f"📊 Sohbet Derinliği: {st.session_state.mesaj_sayisi} mesaj")
    
    if st.session_state.messages:
        safe_messages = []
        for m in st.session_state.messages:
            safe_messages.append({"role": str(m.get("role")), "content": str(m.get("content"))})
        conv_json = json.dumps(safe_messages, ensure_ascii=False)
        st.download_button("Konuşmayı İndir", conv_json, file_name="sazan_sohbet.json", mime="application/json")

# 6. Ana Başlık
st.title("🐟 Sazan Balık AI - v2.5")
st.subheader(f"Şu anki modun: **{mod}**")

# 7. Mesaj Geçmişi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Sohbet Motoru
if prompt := st.chat_input("Sazan Balık'a derin bir şeyler söyle..."):
    # Sayaç artır
    st.session_state.mesaj_sayisi += 1
    
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot cevabı (Persona ile)
    with st.chat_message("assistant"):
        system_prompts = {
            "Filozof Sazan": "Sen derin sularda yüzen, balık felsefesi yapan, biraz unutkan ama çok bilge bir sazan balığısın. Cevaplarında hep su, akıntı, pullar ve göl kenarı metaforları kullan.",
            "İğneleyici Sazan": "Sen çok bilmiş, laf sokmayı seven, insanların oltalarına ve yemiş olduğu yemlere sinir olan, sarkastik bir sazan balığısın.",
            "Normal Sazan": "Sen yardımsever, sakin, gölün huzurunu temsil eden ve herkese iyi davranan bir sazan balığısın."
        }
        
        try:
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
        except Exception as e:
            st.error(f"Sazanlık yaparken bir hata oluştu: {e}")
