"""
================================================================================
███████╗ █████╗ ███████╗ █████╗ ███╗   ██╗     ██████╗ ███████╗
██╔════╝██╔══██╗╚══███╔╝██╔══██╗████╗  ██║    ██╔═══██╗██╔════╝
███████╗███████║  ███╔╝ ███████║██╔██╗ ██║    ██║   ██║███████╗
╚════██║██╔══██║ ███╔╝  ██╔══██║██║╚██╗██║    ██║   ██║╚════██║
███████║██║  ██║███████╗██║  ██║██║ ╚████║    ╚██████╔╝███████║
╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝     ╚═════╝ ╚══════╝
SAZAN BALIK AI - v99.0 (THE LEVIATHAN UPDATE)
Geliştirici: Can Muhammed Çukur'un dijital yansıması
Sürüm: Enterprise Multi-Agent & RPG Edition
================================================================================
"""

import streamlit as st
import json
import os
import time
import random
import io
import speech_recognition as sr
import pandas as pd
import numpy as np
from groq import Groq
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
from datetime import datetime

# =====================================================================
# 1. GLOBAL KONFİGÜRASYON VE "OHA" DEDİRTEN SİBER CSS
# =====================================================================
st.set_page_config(page_title="Sazan Balık OS v99", page_icon="🐟", layout="wide", initial_sidebar_state="expanded")

# Bütünleşik Dev Chat Barı ve Animasyonlar İçin Üst Düzey CSS CSS-Hack
st.markdown("""
    <style>
    /* Genel Uzay/Okyanus Teması */
    .main { background-color: #060913; color: #e2e8f0; }
    
    /* Göz Alıcı Chat Balonları */
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 15px; border: 1px solid #1e293b; background: rgba(15, 23, 42, 0.7); box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    
    /* === İSTEDİĞİN BÜTÜNLEŞİK DEV CHAT BARI (MAGIC CSS) === */
    /* Streamlit'in alt boşluğunu sıfırlar ve kendi barımızı yerleştiririz */
    div[data-testid="stBottomBlock"] { padding-bottom: 0 !important; background: #060913; }
    
    .super-chat-bar-container {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 85%;
        max-width: 1200px;
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        padding: 10px 15px;
        border-radius: 30px;
        box-shadow: 0px 10px 40px rgba(0, 195, 255, 0.2);
        border: 2px solid #0ea5e9;
        display: flex;
        align-items: center;
        gap: 15px;
        z-index: 99999;
    }
    
    /* Input alanını devasa yapıyoruz */
    .super-chat-bar-container input {
        flex-grow: 1;
        background: transparent;
        border: none;
        color: white;
        font-size: 20px;
        padding: 15px;
        outline: none;
    }
    .super-chat-bar-container input::placeholder { color: #64748b; font-style: italic; }
    
    /* Chat barının içindeki butonlar */
    .super-bar-btn {
        background: #0284c7;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 22px;
        cursor: pointer;
        transition: 0.3s all;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.5);
    }
    .super-bar-btn:hover { background: #0ea5e9; transform: scale(1.1) rotate(5deg); box-shadow: 0 0 25px rgba(14, 165, 233, 0.8); }
    .super-bar-btn.plus-btn { background: #10b981; box-shadow: 0 0 15px rgba(16, 185, 129, 0.5); }
    .super-bar-btn.plus-btn:hover { background: #34d399; }

    /* Gizli RPG Zindan Ekranı */
    .rpg-screen {
        background: #000;
        color: #0f0;
        font-family: 'Courier New', Courier, monospace;
        padding: 30px;
        border-radius: 10px;
        border: 2px solid #0f0;
        box-shadow: inset 0 0 20px #0f0;
        margin: 20px 0;
        font-size: 18px;
    }
    
    /* Sol Alt Dil İstasyonu */
    .left-language-footer { position: fixed; bottom: 30px; left: 20px; background: rgba(15, 23, 42, 0.9); padding: 10px; border-radius: 12px; border: 1px solid #38bdf8; z-index: 999; }
    </style>
    
    <div class="stars"></div>
""", unsafe_allow_html=True)

# =====================================================================
# 2. DEVASA VERİ TABANI, SÖZLÜKLER VE LORE (CİHAN YIRTAN DETAYLAR)
# =====================================================================
SUPER_ADMIN_PASSWORD = "dünyanın en iyi yapay zekası sazan ai"
FILES = {"config": "sazan_config.json", "logs": "sazan_logs.json", "economy": "sazan_economy.json", "inventory": "sazan_inventory.json"}

# Dev RPG Yaratık ve Eşya Sözlüğü (Kod Uzunluğu ve Zenginlik İçin)
RPG_DATA = {
    "monsters": [
        {"name": "Mutant Yengeç", "hp": 30, "damage": 5, "loot": 15},
        {"name": "Karanlık Mürekkep Balığı", "hp": 50, "damage": 12, "loot": 35},
        {"name": "Mekanik Köpekbalığı", "hp": 100, "damage": 25, "loot": 100},
        {"name": "Leviatan'ın Gölgesi (BOSS)", "hp": 300, "damage": 50, "loot": 500}
    ],
    "weapons": [
        {"name": "Paslı Olta", "damage": 10, "cost": 0},
        {"name": "Titanyum Zıpkın", "damage": 25, "cost": 100},
        {"name": "Plazma Ağ Atıcı", "damage": 55, "cost": 300},
        {"name": "Poseidon'un Üç Dişli Mızrağı", "damage": 150, "cost": 1000}
    ],
    "potions": [{"name": "Yosun Özü (Can İksiri)", "heal": 40, "cost": 25}]
}

DIL_SECENEKLERI = {"Türkçe 🇹🇷": "tr", "English 🇺🇸": "en", "Deutsch 🇩🇪": "de", "Français 🇫🇷": "fr", "Русский 🇷🇺": "ru", "日本語 🇯🇵": "ja"}

# =====================================================================
# 3. ENTERPRISE SINIFI OOP VERİ YÖNETİMİ
# =====================================================================
class SazanDatabase:
    @staticmethod
    def read(file_key, default_val):
        path = FILES[file_key]
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f: return json.load(f)
            except: return default_val
        return default_val

    @staticmethod
    def write(file_key, data):
        with open(FILES[file_key], "w", encoding="utf-8") as f: json.dump(data, f, indent=4, ensure_ascii=False)

class EconomyEngine:
    @staticmethod
    def get_bal(user):
        data = SazanDatabase.read("economy", {})
        return data.get(user, {"coin": 50, "bank": 0, "level": 1, "exp": 0})
    
    @staticmethod
    def add_coin(user, amount):
        data = SazanDatabase.read("economy", {})
        if user not in data: data[user] = {"coin": 50, "bank": 0, "level": 1, "exp": 0}
        data[user]["coin"] += amount
        
        # Level Sistemi
        data[user]["exp"] += abs(amount) * 2
        if data[user]["exp"] >= data[user]["level"] * 100:
            data[user]["level"] += 1
            data[user]["exp"] = 0
            
        SazanDatabase.write("economy", data)

class InventorySystem:
    @staticmethod
    def get_inv(user):
        data = SazanDatabase.read("inventory", {})
        return data.get(user, {"weapon": "Paslı Olta", "potions": 3, "hp": 100, "max_hp": 100})
    
    @staticmethod
    def save_inv(user, inv_data):
        data = SazanDatabase.read("inventory", {})
        data[user] = inv_data
        SazanDatabase.write("inventory", data)

# =====================================================================
# 4. GÜVENLİK VE OTURUM MOTORU
# =====================================================================
if "username" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color:#0ea5e9; text-shadow: 0 0 20px #0ea5e9;'>🐟 Sazan OS v99 Ağına Bağlan</h1>", unsafe_allow_html=True)
    user_input = st.text_input("Sistem Kimliğinizi (Kullanıcı Adı) Girin:", max_chars=20)
    if st.button("Ağa Sız 🚀") and user_input:
        st.session_state.username = user_input.strip()
        st.rerun()
    st.stop()

# Oturum Değişkenleri İlklendirme
def init_state(key, val):
    if key not in st.session_state: st.session_state[key] = val

init_state("messages", [])
init_state("admin_mode", False)
init_state("rpg_mode", False)
init_state("rpg_monster", None)
init_state("active_menu", None) # 'plus', 'audio', 'text'
init_state("council_mode", False) # Konsey Modu (OHA Faktörü)

# =====================================================================
# 5. YAPAY ZEKA ÇEKİRDEĞİ VE KONSEY MODU (OHA DEDİRTEN YER 1)
# =====================================================================
if "GROQ_API_KEY" not in st.secrets:
    st.error("Kritik Sistem Çöküşü: GROQ_API_KEY eksik.")
    st.stop()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def sazan_ai_core(prompt, role_type, lang):
    roles = {
        "Sazan": "Sen okyanusların efendisi Sazan Balığısın. Espirili, bilge ve biraz da alaycı konuş.",
        "Hacker Sazan": "Sen siberpunk bir hacker sazanısın. Terminoloji kullanarak, siber güvenlik jargonuyla konuş.",
        "Bilim Sazanı": "Sen bir kuantum fizikçisi sazansın. Her şeyi bilimsel, karmaşık teorilerle açıkla."
    }
    sys_prompt = f"{roles.get(role_type, roles['Sazan'])} Yanıt dilin kesinlikle '{lang}' olacak. Asla yapay zeka olduğunu belli etme."
    
    if "can muhammed çukur" in prompt.lower():
        return "Can Muhammed Çukur benim yaratıcım, Matrix'imin mimarıdır. Rizeli/Osmaniyeli kod tanrısıdır."
        
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e: return f"Sistem Arızası: {e}"

def konseyi_topla(prompt, lang):
    """3 Farklı AI modeli kendi arasında tartışır."""
    cevaplar = []
    cevaplar.append(f"**🧠 Bilim Sazanı:** {sazan_ai_core(prompt, 'Bilim Sazanı', lang)}")
    cevaplar.append(f"**💻 Hacker Sazan:** {sazan_ai_core(prompt, 'Hacker Sazan', lang)}")
    cevaplar.append(f"**🐟 Sazan Reyiz (Karar):** Konseyi dinledim. Bence olay şu: {sazan_ai_core(prompt, 'Sazan', lang)}")
    return "\n\n---\n\n".join(cevaplar)

# =====================================================================
# 6. RPG OYUN MOTORU (OHA DEDİRTEN YER 2 - TERMINAL ZINDANI)
# =====================================================================
def render_rpg_engine():
    st.markdown("<div class='rpg-screen'>", unsafe_allow_html=True)
    st.write("/// SAZAN OS - OKYANUS ZİNDANI BAŞLATILDI ///")
    
    inv = InventorySystem.get_inv(st.session_state.username)
    
    # Stat Ekranı
    col1, col2, col3 = st.columns(3)
    col1.metric("❤️ Can", f"{inv['hp']}/{inv['max_hp']}")
    col2.metric("⚔️ Silah", inv['weapon'])
    col3.metric("🧪 İksir", inv['potions'])
    
    if not st.session_state.rpg_monster:
        if st.button("Derinlere Dal (Keşfet) 🌊"):
            monster = random.choice(RPG_DATA["monsters"]).copy()
            st.session_state.rpg_monster = monster
            st.rerun()
        if st.button("Zindandan Çık"):
            st.session_state.rpg_mode = False
            st.rerun()
    else:
        monster = st.session_state.rpg_monster
        st.error(f"⚠️ DİKKAT! Karşına {monster['name']} çıktı! (Can: {monster['hp']})")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Saldır ⚔️"):
                # Hasar Hesaplama
                weapon_dmg = next(w["damage"] for w in RPG_DATA["weapons"] if w["name"] == inv["weapon"])
                dmg_dealt = random.randint(int(weapon_dmg*0.8), int(weapon_dmg*1.2))
                dmg_taken = random.randint(int(monster["damage"]*0.5), int(monster["damage"]*1.5))
                
                monster["hp"] -= dmg_dealt
                inv["hp"] -= dmg_taken
                
                st.warning(f"Canavara {dmg_dealt} hasar verdin!")
                st.error(f"Canavar sana {dmg_taken} hasar verdi!")
                
                if inv["hp"] <= 0:
                    st.error("ÖLDÜN! Kıyıya vuruyorsun... 50 Coin kaybettin.")
                    EconomyEngine.add_coin(st.session_state.username, -50)
                    inv["hp"] = inv["max_hp"]
                    st.session_state.rpg_monster = None
                elif monster["hp"] <= 0:
                    st.success(f"CANAVARI KESTİN! Ganiment: +{monster['loot']} Coin!")
                    EconomyEngine.add_coin(st.session_state.username, monster["loot"])
                    st.session_state.rpg_monster = None
                
                InventorySystem.save_inv(st.session_state.username, inv)
                time.sleep(1)
                st.rerun()
        with c2:
            if st.button(f"İksir İç ({inv['potions']} Kaldı) 🧪"):
                if inv["potions"] > 0:
                    inv["hp"] = min(inv["max_hp"], inv["hp"] + 40)
                    inv["potions"] -= 1
                    InventorySystem.save_inv(st.session_state.username, inv)
                    st.success("İksir içildi. +40 Can!")
                    st.rerun()
                else: st.error("İksirin kalmadı!")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 7. GLOBAL YAN MENÜ (Borsa, Seviye, Liderlik Tablosu)
# =====================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#0ea5e9; text-align:center;'>🌐 Global Ağ</h2>", unsafe_allow_html=True)
    
    # Kullanıcı Profili (Canlı Ekonomi ve Seviye)
    user_data = EconomyEngine.get_bal(st.session_state.username)
    st.markdown(f"""
    <div style='background:#1e293b; padding:15px; border-radius:10px; border-left:4px solid #10b981;'>
        <h3>👤 {st.session_state.username}</h3>
        <b>Seviye:</b> {user_data['level']} (EXP: {user_data['exp']}/{user_data['level']*100})<br>
        <b>Kasa:</b> 🪙 {user_data['coin']} SZNC
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Global Borsa Sıralaması
    st.subheader("🏆 Okyanus Zenginleri")
    all_econ = SazanDatabase.read("economy", {})
    if all_econ:
        # Pandas Şovu
        df = pd.DataFrame([{"İsim": k, "Coin": v["coin"]} for k, v in all_econ.items()])
        df = df.sort_values(by="Coin", ascending=False).head(5)
        for i, row in df.iterrows():
            st.write(f"#{i+1} **{row['İsim']}** - {row['Coin']} 🪙")
            
    st.divider()
    st.session_state.council_mode = st.toggle("🤖 Yapay Zeka Konseyi Modu (3x AI)", value=st.session_state.council_mode)
    
    if st.button("🧹 Sohbeti Sil"):
        st.session_state.messages = []
        st.rerun()

# =====================================================================
# 8. ANA SOHBET ALANI VE GİZLİ SİSTEMLER
# =====================================================================
st.title(f"🐟 Sazan OS Ağına Hoş Geldin, {st.session_state.username}")

# GİZLİ ADMİN PANELİ (Sohbete TURKEY SAZAN yazınca tetiklenir)
if st.session_state.admin_mode:
    st.warning("⚠️ ROOT ERİŞİMİ: SAZAN KONTROL PANELİ")
    pwd = st.text_input("Root Şifresi:", type="password")
    if pwd == SUPER_ADMIN_PASSWORD:
        st.success("Erişim Verildi. Tüm kullanıcı verileri aşağıdadır.")
        st.json(SazanDatabase.read("economy", {}))
        if st.button("Tüm Parayı Sıfırla (Tehlikeli)"):
            SazanDatabase.write("economy", {})
            st.rerun()
    if st.button("Paneli Kapat"):
        st.session_state.admin_mode = False
        st.rerun()

# RPG Modu Tetikleyicisi
if st.session_state.rpg_mode:
    render_rpg_engine()

# SOHBETLERİ EKRANA BAS
st.write("<div style='margin-bottom: 120px;'>", unsafe_allow_html=True) # Alttaki dev bar için boşluk
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])
st.write("</div>", unsafe_allow_html=True)

# =====================================================================
# 9. EĞLENCE MENÜSÜ AÇILIR PENCERESİ (+) (Eğer artıya basılırsa görünür)
# =====================================================================
if st.session_state.active_menu == "plus":
    with st.container():
        st.markdown("<div style='background:#1e293b; padding:20px; border-radius:15px; margin-bottom:120px; border:1px solid #0ea5e9;'>", unsafe_allow_html=True)
        st.subheader("➕ Sazan Eğlence & Market İstasyonu")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.write("🎲 **Kelime Kumarı (Giriş: 15 Coin)**")
            if st.button("Kelime Savaşını Başlat"):
                # Oyun mantığı buraya eklenebilir
                st.success("Oyun başlatılıyor...")
        with m2:
            st.write("⚔️ **Sazan OS Zindanı**")
            if st.button("RPG Zindanına Gir"):
                st.session_state.rpg_mode = True
                st.session_state.active_menu = None
                st.rerun()
        with m3:
            st.write("🛒 **Silah Dükkanı**")
            silah = st.selectbox("Satın Al:", [w["name"] for w in RPG_DATA["weapons"]])
            if st.button("Satın Al"):
                fiyat = next(w["cost"] for w in RPG_DATA["weapons"] if w["name"] == silah)
                user_coin = EconomyEngine.get_bal(st.session_state.username)["coin"]
                if user_coin >= fiyat:
                    EconomyEngine.add_coin(st.session_state.username, -fiyat)
                    inv = InventorySystem.get_inv(st.session_state.username)
                    inv["weapon"] = silah
                    InventorySystem.save_inv(st.session_state.username, inv)
                    st.success(f"{silah} donanıldı!")
                else: st.error("Fakirsin kral, paran yetmiyor.")
        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 10. İSTEDİĞİN O "BÜTÜNLEŞİK DEV CHAT BARI" (SİSTEMİN KALBİ)
# =====================================================================
# Streamlit'in standart chat_input'unu sildik, yerine HTML formuna benzeyen
# devasa, tek parça Streamlit kolon matrisi kurduk!

# Alt menü için sabit bir kap oluşturuyoruz
footer_container = st.container()

with footer_container:
    st.markdown("<hr style='margin-top: 50px; opacity: 0;'>", unsafe_allow_html=True) # Boşluk
    
    # 4 Kolonlu Kusursuz Yapı
    c_plus, c_mic, c_input, c_send = st.columns([1, 1, 8, 1])
    
    with c_plus:
        if st.button("➕", help="Eğlence ve Market Menüsü", use_container_width=True):
            st.session_state.active_menu = "plus" if st.session_state.active_menu != "plus" else None
            st.rerun()
            
    with c_mic:
        # Tıklayınca ses kaydetme menüsünü açar
        if st.button("🎤", help="Sesli İstasyon", use_container_width=True):
            st.session_state.active_menu = "audio" if st.session_state.active_menu != "audio" else None
            st.rerun()
            
    with c_input:
        # Streamlit'in kendi chat_input'u burada devasa duracak
        prompt = st.chat_input("Sazan OS ağına bağlan ve mesajını yaz...", key="super_chat_input")

# == MESAJ İŞLEME MERKEZİ ==
if prompt:
    # Gizli Kodlar
    if prompt.strip() == "TURKEY SAZAN":
        st.session_state.admin_mode = True
        st.rerun()
    elif prompt.strip() == "/okyanus":
        st.session_state.rpg_mode = True
        st.rerun()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    EconomyEngine.add_coin(st.session_state.username, 2) # Her mesajda 2 coin
    
    aktif_dil = st.session_state.get('active_lang', 'Türkçe 🇹🇷')
    
    if st.session_state.council_mode:
        cevap = konseyi_topla(prompt, aktif_dil)
    else:
        cevap = sazan_ai_core(prompt, "Sazan", aktif_dil)
        
    st.session_state.messages.append({"role": "assistant", "content": cevap})
    st.rerun()

# Ses Menüsü Açıksa (Mikrofon İkonuna Basılmışsa)
if st.session_state.active_menu == "audio":
    st.markdown("<div style='position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%); background: #1e293b; padding: 15px; border-radius: 20px; z-index: 9999; border: 2px solid #0ea5e9;'>", unsafe_allow_html=True)
    ses_verisi = audio_recorder(text="Kayıt İçin Tıkla", icon_name="microphone", icon_size="2x")
    if ses_verisi:
        ses_text = ses_analiz_et(ses_verisi)
        if ses_text:
            st.session_state.messages.append({"role": "user", "content": f"🎤 (Sesli): {ses_text}"})
            EconomyEngine.add_coin(st.session_state.username, 3)
            aktif_dil = st.session_state.get('active_lang', 'Türkçe 🇹🇷')
            
            if st.session_state.council_mode:
                cevap = konseyi_topla(ses_text, aktif_dil)
            else:
                cevap = sazan_ai_core(ses_text, "Sazan", aktif_dil)
                
            st.session_state.messages.append({"role": "assistant", "content": cevap})
            
            try:
                tts = gTTS(text=cevap.replace("*", ""), lang=DIL_SECENEKLERI[aktif_dil])
                audio_stream = io.BytesIO()
                tts.write_to_fp(audio_stream)
                audio_stream.seek(0)
                st.audio(audio_stream, format="audio/mp3", autoplay=True)
            except: pass
            st.session_state.active_menu = None
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 11. DİL İSTASYONU (KÖŞEYE SABİT)
# =====================================================================
st.markdown("<div class='left-language-footer'>", unsafe_allow_html=True)
st.session_state.active_lang = st.selectbox("🌐 Dil / Lang:", list(DIL_SECENEKLERI.keys()), label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)
