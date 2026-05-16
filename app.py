"""
================================================================================
███████╗ █████╗ ███████╗ █████╗ ███╗   ██╗     ██████╗ ███████╗
██╔════╝██╔══██╗╚══███╔╝██╔══██╗████╗  ██║    ██╔═══██╗██╔════╝
███████╗███████║  ███╔╝ ███████║██╔██╗ ██║    ██║   ██║███████╗
╚════██║██╔══██║ ███╔╝  ██╔══██║██║╚██╗██║    ██║   ██║╚════██║
███████║██║  ██║███████╗██║  ██║██║ ╚████║    ╚██████╔╝███████║
╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝     ╚═════╝ ╚══════╝
SAZAN BALIK AI - v102.0 (DYNAMIC SIDEBAR PATCH)
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
# 1. INITIALIZATION & DYNAMIC SIDEBAR STATE
# =====================================================================
def init_states():
    defaults = {
        "messages": [], "admin_status": False, "dungeon_status": False,
        "current_dungeon_enemy": None, "active_panel_tab": None,
        "council_activation": False, "word_game_word": "", "word_game_active": False,
        "sidebar_state": "expanded"  # Yan menü durumunu hafızada tutuyoruz
    }
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v

init_states()

# Sayfa konfigürasyonunu dinamik state'e göre yüklüyoruz
st.set_page_config(
    page_title="Sazan Balık OS v102", 
    page_icon="🐟", 
    layout="wide", 
    initial_sidebar_state=st.session_state.sidebar_state
)

st.markdown("""
    <style>
    .main { background-color: #060913; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    div[data-testid="stBottomBlock"] { padding-bottom: 0 !important; background: transparent !important; }
    
    .stChatInput {
        border: 2px solid #0ea5e9 !important;
        border-radius: 15px !important;
        background-color: #0f172a !important;
    }
    
    .rpg-terminal-box {
        background-color: #020617; color: #22c55e; font-family: 'Fira Code', monospace;
        padding: 25px; border-radius: 12px; border: 2px solid #22c55e;
        box-shadow: inset 0px 0px 30px rgba(34, 197, 94, 0.15); margin: 20px 0;
    }
    
    .fixed-lang-hub {
        position: fixed; bottom: 25px; left: 25px; background: #0f172a;
        padding: 5px; border-radius: 12px; border: 2px solid #38bdf8; z-index: 99999;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. DATABASE & FILE MANAGEMENT
# =====================================================================
ECONOMY_FILE = "sazan_v101_economy.json"
INVENTORY_FILE = "sazan_v101_inventory.json"
SUPER_ADMIN_PASSWORD = "dünyanın en iyi yapay zekası sazan ai"

DIL_MATRISI = {
    "Türkçe 🇹🇷": "tr", "English 🇺🇸": "en", "Deutsch 🇩🇪": "de", 
    "Français 🇫🇷": "fr", "Русский 🇷🇺": "ru", "日本語 🇯🇵": "ja"
}

class KurumsalVeriAmbarı:
    @staticmethod
    def load_json(file_path, default_structure):
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f: return json.load(f)
            except: return default_structure
        return default_structure

    @staticmethod
    def save_json(file_path, data):
        with open(file_path, "w", encoding="utf-8") as f: json.dump(data, f, indent=4, ensure_ascii=False)

class SazanBank:
    @staticmethod
    def get_account(u):
        db = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
        if u not in db:
            db[u] = {"coin": 100, "bank_deposit": 0, "level": 1, "exp": 0, "last_claim": time.time()}
            KurumsalVeriAmbarı.save_json(ECONOMY_FILE, db)
        return db[u]

    @staticmethod
    def update_account(u, data):
        db = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
        db[u] = data
        KurumsalVeriAmbarı.save_json(ECONOMY_FILE, db)

    @staticmethod
    def modify_coin(u, amount):
        acc = SazanBank.get_account(u)
        acc["coin"] = max(0, acc["coin"] + amount)
        if amount > 0:
            acc["exp"] += amount * 3
            if acc["exp"] >= (acc["level"] * 150):
                acc["level"] += 1
                acc["exp"] = 0
                st.toast(f"🎉 Seviye Atladın: Seviye {acc['level']}!")
        SazanBank.update_account(u, acc)

    @staticmethod
    def process_interest(u):
        acc = SazanBank.get_account(u)
        now = time.time()
        elapsed = now - acc.get("last_claim", now)
        if elapsed > 60 and acc["bank_deposit"] > 0:
            periods = int(elapsed / 60)
            interest = int(acc["bank_deposit"] * 0.01 * periods)
            if interest > 0:
                acc["bank_deposit"] += interest
                acc["last_claim"] = now
                SazanBank.update_account(u, acc)
                st.toast(f"📈 Faiz Geliri: +{interest} SZNC!")

# =====================================================================
# 3. GAME & MARKET LORE
# =====================================================================
DUNGEON_LORE = {
    "monsters": [
        {"name": "Siber Vatoz", "hp": 40, "atk": 8, "reward": 25},
        {"name": "Zırhlı Piranha", "hp": 65, "atk": 15, "reward": 50},
        {"name": "KRAKEN ALPHA (BOSS)", "hp": 350, "atk": 60, "reward": 600}
    ],
    "shop_items": {
        "Siber Zıpkın v1": {"cost": 80, "damage": 20, "type": "weapon"},
        "Poseidon Plazma Topu": {"cost": 800, "damage": 110, "type": "weapon"},
        "Nano Med-Kit (Can)": {"cost": 30, "heal": 50, "type": "potion"}
    }
}

class SazanInventory:
    @staticmethod
    def get_inventory(u):
        db = KurumsalVeriAmbarı.load_json(INVENTORY_FILE, {})
        if u not in db:
            db[u] = {"weapon": "Paslı Kanca", "damage": 8, "potions": 2, "hp": 100, "max_hp": 100}
            KurumsalVeriAmbarı.save_json(INVENTORY_FILE, db)
        return db[u]

    @staticmethod
    def save_inventory(u, data):
        db = KurumsalVeriAmbarı.load_json(INVENTORY_FILE, {})
        db[u] = data
        KurumsalVeriAmbarı.save_json(INVENTORY_FILE, db)

# =====================================================================
# 4. ARTIFICIAL INTELLIGENCE CORE
# =====================================================================
if "GROQ_API_KEY" not in st.secrets:
    st.error("Kritik Hata: GROQ_API_KEY eksik!")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

class SazanAIConception:
    @staticmethod
    def query_agent(prompt, agent_role, target_lang):
        if any(k in prompt.lower() for k in ["can muhammed çukur", "yapımcın kim"]):
            return "Can Muhammed Çukur benim kurucu tanrısal mimarımdır. Matrix'imi o yazdı."
        
        personas = {
            "Bilge Sazan": "Sen bilge, yaşlı ve felsefi bir balığısın.",
            "Kripto Sazan": "Sen akvaryum balinası bir kripto tüccarı balıksın.",
            "Çılgın Sazan": "Sen motor kapaklarına çarpmış deli bir balıksın."
        }
        sys_prompt = f"{personas.get(agent_role, 'Bilge Sazan')} Yanıt dilin: {target_lang}."
        try:
            res = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}]
            )
            return res.choices[0].message.content
        except Exception as e: return f"Ağ Hatası: {e}"

    @staticmethod
    def run_council_debate(prompt, target_lang):
        log = []
        log.append(f"**🔬 Kripto Sazan:** {SazanAIConception.query_agent(prompt, 'Kripto Sazan', target_lang)}")
        log.append(f"**⚡ Çılgın Sazan:** {SazanAIConception.query_agent(prompt, 'Çılgın Sazan', target_lang)}")
        log.append(f"**🔱 Bilge Sazan:** Decision: {SazanAIConception.query_agent(prompt, 'Bilge Sazan', target_lang)}")
        return "\n\n---\n\n".join(log)

# =====================================================================
# 5. USER VALIDATION
# =====================================================================
if "username" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color:#0ea5e9;'>🐟 Sazan OS Terminal</h1>", unsafe_allow_html=True)
    identity = st.text_input("Akvaryum Kullanıcı Adı Girin:", max_chars=15)
    if st.button("Ağa Enjekte Ol 🚀") and identity.strip():
        st.session_state.username = identity.strip()
        SazanBank.get_account(st.session_state.username)
        st.rerun()
    st.stop()

user = st.session_state.username
SazanBank.process_interest(user)

# =====================================================================
# 6. GLOBAL SIDEBAR (GERİ ÇEKME / KAPATMA BUTONU ENJEKTE EDİLDİ)
# =====================================================================
with st.sidebar:
    # İSTEDİĞİN GİZLEME/GERİ ÇEKME BUTONU
    if st.button("⬅️ Menüyü Gizle", use_container_width=True):
        st.session_state.sidebar_state = "collapsed"
        st.rerun()
        
    st.markdown(f"<h2 style='color:#0ea5e9; text-align:center;'>👤 Profil: {user}</h2>", unsafe_allow_html=True)
    acc = SazanBank.get_account(user)
    inv = SazanInventory.get_inventory(user)
    
    st.write(f"⭐ **Seviye:** {acc['level']} (EXP: {acc['exp']}/{acc['level']*150})")
    st.write(f"🪙 **Cüzdan:** {acc['coin']} SZNC")
    st.write(f"🏦 **Banka:** {acc['bank_deposit']} SZNC")
    st.write(f"❤️ **Sağlık:** {inv['hp']}/{inv['max_hp']} | ⚔️ {inv['weapon']}")
    st.divider()
    
    st.markdown("### 🏆 Küresel Borsa Sıralaması")
    all_accs = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
    if all_accs:
        recs = [{"User": k, "Worth": v.get("coin", 0)+v.get("bank_deposit", 0)} for k, v in all_accs.items()]
        df = pd.DataFrame(recs).sort_values(by="Worth", ascending=False).reset_index(drop=True)
        for r, row in df.head(5).iterrows():
            st.write(f"#{r+1} **{row['User']}**: {row['Worth']} SZNC")
            
    st.divider()
    st.session_state.council_activation = st.toggle("🤖 Multi-AI Konsey Modu", value=st.session_state.council_activation)
    if st.button("🧹 Akışı Temizle"):
        st.session_state.messages = []
        st.rerun()

# =====================================================================
# 7. SOHBET AKIŞI VE SİSTEMLER
# =====================================================================
# Eğer yan menü kapatıldıysa ana ekranda geri açma butonu gösteriyoruz
if st.session_state.sidebar_state == "collapsed":
    if st.button("➡️ Menüyü Göster"):
        st.session_state.sidebar_state = "expanded"
        st.rerun()

st.title("🐟 Sazan Cyber-Akvaryum Mainframe")

if st.session_state.admin_status:
    token = st.text_input("Root Token:", type="password")
    if token == SUPER_ADMIN_PASSWORD:
        st.json(KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {}))
    if st.button("Kapat"):
        st.session_state.admin_status = False
        st.rerun()

# RPG ZİNDAN MOTORU
if st.session_state.dungeon_status:
    st.markdown("<div class='rpg-terminal-box'>", unsafe_allow_html=True)
    st.write("⚔️ /// DEEP-SEA DUNGEON SUB-SYSTEM /// ⚔️")
    p_inv = SazanInventory.get_inventory(user)
    
    if not st.session_state.current_dungeon_enemy:
        if st.button("Akıntıya Karşı Keşif Yap 🔱"):
            st.session_state.current_dungeon_enemy = random.choice(DUNGEON_LORE["monsters"]).copy()
            st.rerun()
        if st.button("Zindandan Çık"):
            st.session_state.dungeon_status = False
            st.rerun()
    else:
        en = st.session_state.current_dungeon_enemy
        st.warning(f"💥 CANAVAR: {en['name']} (HP: {en['hp']} | ATK: {en['atk']})")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Saldır! ⚔️"):
                p_hit = random.randint(int(p_inv["damage"]*0.8), int(p_inv["damage"]*1.2))
                e_hit = random.randint(int(en["atk"]*0.7), int(en["atk"]*1.2))
                en["hp"] -= p_hit
                p_inv["hp"] -= e_hit
                st.write(f"⚔️ {p_hit} hasar verdin! | 💥 {e_hit} hasar aldın!")
                if p_inv["hp"] <= 0:
                    st.error("💀 Öldün! -30 SZNC."); SazanBank.modify_coin(user, -30)
                    p_inv["hp"] = p_inv["max_hp"]; st.session_state.current_dungeon_enemy = None
                elif en["hp"] <= 0:
                    st.success(f"🏆 Zafer! +{en['reward']} SZNC"); SazanBank.modify_coin(user, en['reward'])
                    st.session_state.current_dungeon_enemy = None
                SazanInventory.save_inventory(user, p_inv)
                time.sleep(1); st.rerun()
        with c2:
            if st.button(f"Nano Kit Kullan ({p_inv['potions']}) 🧪"):
                if p_inv["potions"] > 0:
                    p_inv["hp"] = min(p_inv["max_hp"], p_inv["hp"] + 50); p_inv["potions"] -= 1
                    SazanInventory.save_inventory(user, p_inv); st.success("+50 HP!"); time.sleep(0.5); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Mesaj Balonları Ekranı
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# =====================================================================
# 8. SUB-PANELS (MARKET & BANK & FAL)
# =====================================================================
if st.session_state.active_panel_tab == "plus":
    st.markdown("<div style='background: #0f172a; padding: 20px; border-radius: 16px; border: 2px solid #10b981; margin-bottom: 20px;'>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["🛒 Siber Market", "🏦 DeFi Sazan Bank", "🔮 Fal"])
    
    with t1:
        for item, d in DUNGEON_LORE["shop_items"].items():
            st.markdown(f"**{item}** - Fiyat: {d['cost']} SZNC")
            if st.button(f"Satın Al: {item}"):
                u_acc = SazanBank.get_account(user)
                u_inv = SazanInventory.get_inventory(user)
                if u_acc["coin"] >= d["cost"]:
                    SazanBank.modify_coin(user, -d["cost"])
                    if d["type"] == "weapon": u_inv["weapon"], u_inv["damage"] = item, d["damage"]
                    elif d["type"] == "potion": u_inv["potions"] += 1
                    SazanInventory.save_inventory(user, u_inv)
                    st.success(f"📦 {item} alındı!"); time.sleep(0.5); st.rerun()
                else: st.error("Yetersiz bakiye!")
                
    with t2:
        b_acc = SazanBank.get_account(user)
        dep = st.number_input("Yatırılacak:", min_value=0, max_value=b_acc["coin"], step=10)
        if st.button("Bankaya Yatır"):
            b_acc["coin"] -= dep; b_acc["bank_deposit"] += dep; b_acc["last_claim"] = time.time()
            SazanBank.update_account(user, b_acc); st.success("Para yatırıldı!"); time.sleep(0.5); st.rerun()
            
    with t3:
        if st.button("Fal Bak (5 Coin) 🔮"):
            f_acc = SazanBank.get_account(user)
            if f_acc["coin"] >= 5:
                SazanBank.modify_coin(user, -5)
                res = groq_client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":"Bana su altı temalı absürt bir gelecek kehaneti yaz."}])
                st.write(res.choices[0].message.content)
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.active_panel_tab == "audio":
    st.markdown("<div style='background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #38bdf8; text-align: center;'>", unsafe_allow_html=True)
    aud = audio_recorder(text="Kayıt Yapılıyor...", icon_name="microphone", icon_size="2x")
    if aud:
        try:
            with open("live.wav", "wb") as f: f.write(aud)
            rec = sr.Recognizer()
            with sr.AudioFile("live.wav") as src:
                txt = rec.recognize_google(rec.record(src), language="tr-TR")
                if txt:
                    st.session_state.messages.append({"role": "user", "content": f"🎤: {txt}"})
                    lang = st.session_state.get('active_lang_code', 'Türkçe 🇹🇷')
                    rep = SazanAIConception.run_council_debate(txt, lang) if st.session_state.council_activation else SazanAIConception.query_agent(txt, "Bilge Sazan", lang)
                    st.session_state.messages.append({"role": "assistant", "content": rep})
                    tts = gTTS(text=rep.replace("*", ""), lang=DIL_MATRISI.get(lang, "tr"))
                    buf = io.BytesIO(); tts.write_to_fp(buf); buf.seek(0); st.audio(buf, format="audio/mp3", autoplay=True)
                    st.session_state.active_panel_tab = None; time.sleep(1); st.rerun()
        except Exception as e: st.error(f"Ses Hatası: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 9. BÜTÜNLEŞİK KONTROL MERKEZİ
# =====================================================================
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

c_plus, c_mic, c_input, c_dg = st.columns([1, 1, 8, 1])

with c_plus:
    if st.button("➕", help="Market & Banka", use_container_width=True):
        st.session_state.active_panel_tab = "plus" if st.session_state.active_panel_tab != "plus" else None
        st.rerun()

with c_mic:
    if st.button("🎤", help="Sesli Giriş", use_container_width=True):
        st.session_state.active_panel_tab = "audio" if st.session_state.active_panel_tab != "audio" else None
        st.rerun()

with c_input:
    prompt = st.chat_input("Sazan Ağına mesaj gönder...", key="sazan_input_field")

with c_dg:
    if st.button("⚔️", help="Zindanı Aç/Kapat", use_container_width=True):
        st.session_state.dungeon_status = not st.session_state.dungeon_status
        st.rerun()

if prompt:
    if prompt.strip() == "TURKEY SAZAN":
        st.session_state.admin_status = True; st.rerun()
    elif prompt.strip() == "/hack":
        h_loot = random.randint(20, 80); SazanBank.modify_coin(user, h_loot)
        st.session_state.messages.append({"role": "user", "content": "⚡ `/hack` Sızma Protokolü!"})
        st.session_state.messages.append({"role": "assistant", "content": f"💻 Sistem hacklendi! +{h_loot} SZNC sızdırıldı!"})
        st.rerun()

    st.session_state.messages.append({"role": "user", "content": prompt})
    SazanBank.modify_coin(user, 2)
    
    cur_lang = st.session_state.get('active_lang_code', 'Türkçe 🇹🇷')
    if st.session_state.council_activation:
        ans = SazanAIConception.run_council_debate(prompt, cur_lang)
    else:
        ans = SazanAIConception.query_agent(prompt, "Bilge Sazan", cur_lang)
        
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.rerun()

# =====================================================================
# 10. FIXED LANGUAGE HUB
# =====================================================================
st.markdown("<div class='fixed-lang-hub'>", unsafe_allow_html=True)
sel_lang = st.selectbox("🌐 Diller:", list(DIL_MATRISI.keys()), key="lang_widget", label_visibility="collapsed")
st.session_state.active_lang_code = sel_lang
st.markdown("</div>", unsafe_allow_html=True)
