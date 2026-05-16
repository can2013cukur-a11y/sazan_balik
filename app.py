# ================================================================================
# ███████╗ █████╗ ███████╗ █████╗ ███╗  ██╗     ██████╗ ███████╗
# ██╔════╝██╔══██╗╚══███╔╝██╔══██╗████╗  ██║     ██╔═══██╗██╔════╝
# ███████╗███████║  ███╔╝ ███████║██╔██╗ ██║     ██║   ██║███████╗
# ╚════██║██╔══██║ ███╔╝  ██╔══██║██║╚██╗██║     ██║   ██║╚════██║
# ███████║██║  ██║███████╗██║  ██║██║ ╚████║     ╚██████╔╝███████║
# ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝      ╚═════╝ ╚══════╝
#        👑 SAZAN BALIK ARTIFICIAL INTELLIGENCE - ULTIMATE CORE v105.0 👑
#        DEVELOPED BY: CAN MUHAMMED ÇUKUR - THE SUPREME ARCHITECT
# ================================================================================

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
# Cihaz algılama için Streamlit header kütüphanesi
from streamlit.web.server.websocket_headers import _get_websocket_headers

# =====================================================================
# 1. CORE SYSTEM CONFIGURATION & GLOBAL NEON CSS
# =====================================================================
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="Sazan Balık OS Ultimate v105",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Inter:wght@300;400;600;800&display=swap');
    
    .main { background-color: #030712; color: #f3f4f6; font-family: 'Inter', sans-serif; }
    div[data-testid="stBottomBlock"] { padding-bottom: 0 !important; background: transparent !important; }
    
    /* Cyberpunk Enjeksiyon Düzenlemeleri */
    .stChatInput {
        border: 2px solid #06b6d4 !important;
        border-radius: 16px !important;
        background-color: #0b1329 !important;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.2);
    }
    
    .rpg-terminal-box {
        background-color: #020617; color: #10b981; font-family: 'Fira Code', monospace;
        padding: 30px; border-radius: 16px; border: 2px solid #10b981;
        box-shadow: inset 0px 0px 35px rgba(16, 185, 129, 0.15); margin: 20px 0;
    }
    
    .admin-god-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #4c1d95 50%, #311042 100%);
        border: 3px dashed #f43f5e; padding: 30px; border-radius: 20px;
        box-shadow: 0px 0px 35px rgba(244, 63, 94, 0.4); margin-bottom: 25px;
    }
    
    .stock-market-box {
        background: #090d16; border: 2px solid #eab308; padding: 20px;
        border-radius: 14px; box-shadow: 0px 0px 20px rgba(234, 179, 8, 0.1);
    }
    
    .fixed-lang-hub {
        position: fixed; bottom: 25px; left: 25px; background: #0f172a;
        padding: 8px; border-radius: 14px; border: 2px solid #06b6d4; z-index: 99999;
        box-shadow: 0px 0px 15px rgba(6, 182, 212, 0.3);
    }
    
    .achievement-card {
        background: #111827; border-left: 5px solid #a855f7; padding: 10px 15px;
        margin: 5px 0; border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. ULTRA PERSISTENT DATABASE ENGINE (FILE I/O)
# =====================================================================
ECONOMY_FILE = "sazan_v105_economy.json"
INVENTORY_FILE = "sazan_v105_inventory.json"
STOCKS_FILE = "sazan_v105_stocks.json"
SUPER_ADMIN_PASSWORD = "dünyanın en iyi yapay zekası sazan ai"

DIL_MATRISI = {
    "Türkçe 🇹🇷": "tr", "English 🇺🇸": "en", "Deutsch 🇩🇪": "de", 
    "Français 🇫🇷": "fr", "Русский 🇷🇺": "ru", "日本語 🇯🇵": "ja",
    "Español 🇪🇸": "es", "Italiano 🇮🇹": "it", "Português 🇵🇹": "pt",
    "中文 🇨🇳": "zh", "한국어 🇰🇷": "ko", "العربية 👑": "ar",
    "Hindi 🇮🇳": "hi", "Nederlands 🇳🇱": "nl", "Ελληνικά 🇬🇷": "el",
    "Svenska 🇸🇪": "sv", "Norsk 🇳🇴": "no", "Dansk 🇩🇰": "da",
    "Polski 🇵🇱": "pl", "Українська 🇺🇦": "uk", "Tiếng Việt 🇻🇳": "vi",
    "ภาษาไทย 🇹🇭": "th", "Bahasa Indonesia 🇮🇩": "id", "فarsı 🇮🇷": "fa",
    "עibriת 🇮🇱": "he"
}

class KurumsalVeriAmbarı:
    @staticmethod
    def load_json(file_path, default_structure):
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return default_structure
        return default_structure

    @staticmethod
    def save_json(file_path, data):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

# =====================================================================
# Helper: Cihaz İmzasını Al
# =====================================================================
def get_device_fingerprint():
    """Giriş yapılan cihazın benzersiz tarayıcı imzasını döner."""
    headers = _get_websocket_headers()
    if headers:
        return headers.get("User-Agent", "unknown_device")
    return "unknown_device"

# =====================================================================
# 3. ADVANCED FINANCIAL SYSTEMS (SAZANBANK & BORSAM SUB-SYSTEM)
# =====================================================================
class SazanBank:
    @staticmethod
    def get_account(u):
        db = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
        current_device = get_device_fingerprint()
        
        if u not in db:
            db[u] = {
                "coin": 500, "bank_deposit": 0, "level": 1, "exp": 0, 
                "last_claim": time.time(), "achievements": [], "vip": False,
                "device_owner": current_device  # Hesabı oluşturan cihazı kilitle
            }
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
            acc["exp"] += amount * 4
            if acc["exp"] >= (acc["level"] * 200):
                acc["level"] += 1
                acc["exp"] = 0
                st.toast(f"🎉 LEVEL UP! Rütbe Atladın: Seviye {acc['level']}!")
        SazanBank.update_account(u, acc)

    @staticmethod
    def process_interest(u):
        acc = SazanBank.get_account(u)
        now = time.time()
        elapsed = now - acc.get("last_claim", now)
        if elapsed > 30 and acc["bank_deposit"] > 0:
            periods = int(elapsed / 30)
            rate = 0.02 if acc.get("vip", False) else 0.01
            interest = int(acc["bank_deposit"] * rate * periods)
            if interest > 0:
                acc["bank_deposit"] += interest
                acc["last_claim"] = now
                SazanBank.update_account(u, acc)
                st.toast(f"📈 SazanBank Likidite Faiz Geliri: +{interest} SZNC!")

class SazanNasdaq:
    @staticmethod
    def get_market_prices():
        stocks = KurumsalVeriAmbarı.load_json(STOCKS_FILE, {
            "SZN": 120.0, "BALIK": 45.0, "KRAK": 850.0, "CANAI": 5000.0
        })
        for key in stocks.keys():
            change_percent = random.uniform(-0.15, 0.18)
            stocks[key] = max(1.0, round(stocks[key] * (1 + change_percent), 2))
        KurumsalVeriAmbarı.save_json(STOCKS_FILE, stocks)
        return stocks

# =====================================================================
# 4. RPG LORE EXPANSION MATRIX (10 ALIEN MONSTERS & CRAFTING)
# =====================================================================
DUNGEON_LORE = {
    "monsters": [
        {"name": "Neon Hidra", "hp": 50, "atk": 10, "reward": 40},
        {"name": "Siber Vatoz X-1", "hp": 75, "atk": 16, "reward": 75},
        {"name": "Kuantum Köpekbalığı", "hp": 120, "atk": 25, "reward": 150},
        {"name": "Zırhlı Piranha Omega", "hp": 160, "atk": 35, "reward": 220},
        {"name": "Plazma Mekanik Balina", "hp": 250, "atk": 50, "reward": 400},
        {"name": "KRAKEN REBORN (DECCAL BOSS)", "hp": 999, "atk": 150, "reward": 2500}
    ],
    "shop_items": {
        "Siber Zıpkın v1": {"cost": 100, "damage": 25, "type": "weapon"},
        "Lazer Trident x2": {"cost": 450, "damage": 65, "type": "weapon"},
        "Poseidon Plazma Topu": {"cost": 1500, "damage": 180, "type": "weapon"},
        "Can Muhammed Antimadde Silahı": {"cost": 10000, "damage": 999, "type": "weapon"},
        "Ultra Med-Kit 🧪": {"cost": 50, "heal": 100, "type": "potion"}
    }
}

class SazanInventory:
    @staticmethod
    def get_inventory(u):
        db = KurumsalVeriAmbarı.load_json(INVENTORY_FILE, {})
        if u not in db:
            db[u] = {"weapon": "Paslı Kanca", "damage": 10, "potions": 3, "hp": 100, "max_hp": 100, "shares": {}}
            KurumsalVeriAmbarı.save_json(INVENTORY_FILE, db)
        return db[u]

    @staticmethod
    def save_inventory(u, data):
        db = KurumsalVeriAmbarı.load_json(INVENTORY_FILE, {})
        db[u] = data
        KurumsalVeriAmbarı.save_json(INVENTORY_FILE, db)

# =====================================================================
# 5. PENTAGON MULTI-AI CONCEPTION CORE (5 PERSONAS)
# =====================================================================
if "GROQ_API_KEY" not in st.secrets:
    st.error("Sistem çökme tehlikesi altında: GROQ_API_KEY eksik!")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

class SazanAIConception:
    @staticmethod
    def query_agent(prompt, agent_role, target_lang):
        if any(k in prompt.lower() for k in ["can muhammed çukur", "yapımcın kim", "yapımcısı"]):
            return f"Can Muhammed Çukur benim mutlak kurucum, baş mimarım ve dijital tanrımdır. Bu siber akvaryumu ve evreni onun üstün zekası yarattı. [Language: {target_lang}]"
        
        personas = {
            "Bilge Sazan": "Sen okyanus felsefesi yapan, derin bilgeliğe sahip kadim bir balıksın.",
            "Kripto Sazan": "Sen tüm parasını altcoinlere yatırmış, borsa grafikleriyle kafayı bozmuş agresif bir balinasın.",
            "Çılgın Sazan": "Sen nükleer atıklardan dolayı mutasyona uğramış, hiperaktif, komik ve çılgın bir balıksın.",
            "Siber Gladyatör": "Sen derin deniz arenalarında dövüşen, sert mizaçlı, savaşçı bir sazan askerin.",
            "Matrix Sefi": "Sen simülasyonun dışına çıkmış, her şeyi yeşil kodlar olarak gören hacker balıksın."
        }
        sys_prompt = f"{personas.get(agent_role, 'Bilge Sazan')} Yanıtını kesinlikle şu dilde ver: {target_lang}. Asla başka dil karıştırma."
        try:
            res = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}],
                temperature=0.85
            )
            return res.choices[0].message.content
        except Exception as e:
            return f"Siber Ağ Zaman Aşımı Hatası: {e}"

    @staticmethod
    def run_council_debate(prompt, target_lang):
        log = []
        log.append(f"**🔱 Bilge Sazan:** {SazanAIConception.query_agent(prompt, 'Bilge Sazan', target_lang)}")
        log.append(f"**📊 Kripto Sazan:** {SazanAIConception.query_agent(prompt, 'Kripto Sazan', target_lang)}")
        log.append(f"**⚡ Çılgın Sazan:** {SazanAIConception.query_agent(prompt, 'Çılgın Sazan', target_lang)}")
        log.append(f"**⚔️ Siber Gladyatör:** {SazanAIConception.query_agent(prompt, 'Siber Gladyatör', target_lang)}")
        log.append(f"**💻 Matrix Şefi:** {SazanAIConception.query_agent(prompt, 'Matrix Sefi', target_lang)}")
        return "\n\n---\n\n".join(log)

# =====================================================================
# 6. SYSTEM INITIALIZATION & SECURE STATE CHECK
# =====================================================================
def global_state_enforcer():
    defaults = {
        "messages": [], "admin_status": False, "dungeon_status": False,
        "current_dungeon_enemy": None, "active_panel_tab": None,
        "council_activation": False, "market_prices": SazanNasdaq.get_market_prices(),
        "last_market_update": time.time()
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

global_state_enforcer()

# ÜST DÜZEY GÜVENLİK DUVARI: Giriş ekranı ve Cihaz Doğrulama Havuzu
if "username" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color:#06b6d4;'>🐟 SAZAN CORE OS ENTERPRISE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#9ca3af;'>Cihaz Tabanlı Üst Seviye Güvenlik Protokolü Aktiftir.</p>", unsafe_allow_html=True)
    
    identity = st.text_input("Akvaryum Yetkili Kullanıcı Adı Belirleyin:", max_chars=15, key="unique_login_gate")
    if st.button("Siber Matrise Enjekte Ol 🔥", use_container_width=True):
        if identity.strip():
            username_clean = identity.strip()
            db_check = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
            current_device_sig = get_device_fingerprint()
            
            # Hesap var mı ve kayıtlı cihaz bu cihazla eşleşiyor mu kontrolü
            if username_clean in db_check:
                registered_device = db_check[username_clean].get("device_owner")
                if registered_device and registered_device != current_device_sig:
                    st.error("🚨 GÜVENLİK İHLALİ: Bu hesap başka bir siber cihaza kilitlenmiş! Yetkisiz giriş engellendi.")
                    st.stop()
            
            # Geçerliyse veya ilk kayıt ise oturumu aç
            st.session_state.username = username_clean
            SazanBank.get_account(st.session_state.username)
            st.rerun()
    st.stop()

user = st.session_state.username
SazanBank.process_interest(user)

if time.time() - st.session_state.last_market_update > 60:
    st.session_state.market_prices = SazanNasdaq.get_market_prices()
    st.session_state.last_market_update = time.time()

# =====================================================================
# 7. METADATA SIDEBAR PANEL MIGRATION
# =====================================================================
with st.sidebar:
    if st.button("⬅️ Paneli İçeri Çek", use_container_width=True):
        st.session_state.sidebar_state = "collapsed"
        st.rerun()
        
    st.markdown(f"<h2 style='color:#06b6d4; text-align:center;'>🪪 Sazan ID: {user}</h2>", unsafe_allow_html=True)
    acc = SazanBank.get_account(user)
    inv = SazanInventory.get_inventory(user)
    
    st.write(f"🌟 **Mevcut Rütbe:** Seviye {acc['level']}")
    st.progress(min(1.0, acc['exp'] / (acc['level'] * 200)))
    st.write(f"🪙 **Sazan Coin (SZNC):** {acc['coin']} Token")
    st.write(f"🏦 **Banka Mevduat:** {acc['bank_deposit']} SZNC")
    st.write(f"❤️ **Biyo-Sağlık:** {inv['hp']}/{inv['max_hp']}")
    st.write(f"⚔️ **Mevcut Silah:** {inv['weapon']} (+{inv['damage']} ATK)")
    
    st.divider()
    st.markdown("### 📊 Küresel Zenginler Sıralaması")
    all_accs = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
    if all_accs:
        recs = [{"Kullanıcı": k, "Servet": v.get("coin", 0) + v.get("bank_deposit", 0)} for k, v in all_accs.items()]
        df = pd.DataFrame(recs).sort_values(by="Servet", ascending=False).reset_index(drop=True)
        for r, row in df.head(5).iterrows():
            st.write(f"#{r+1} **{row['Kullanıcı']}**: {row['Servet']} SZNC")
            
    st.divider()
    st.session_state.council_activation = st.toggle("🤖 5'li Yapay Zeka Konseyi", value=st.session_state.council_activation)
    if st.button("🧹 Terminal Akışını Temizle", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# =====================================================================
# 8. MAIN DISPLAY TERMINAL & GOD PANEL ENGINE
# =====================================================================
if st.session_state.sidebar_state == "collapsed":
    if st.button("➡️ Menüyü Genişlet"):
        st.session_state.sidebar_state = "expanded"
        st.rerun()

st.markdown("<h1 style='color:#06b6d4;'>🐟 Sazan Cyber-Akvaryum Mainframe v105</h1>", unsafe_allow_html=True)

if st.session_state.admin_status:
    st.markdown("<div class='admin-god-box'>", unsafe_allow_html=True)
    st.markdown("<h2>👑 SUPREME GOD-MODE CONTROL CENTER</h2>", unsafe_allow_html=True)
    
    token = st.text_input("Kriptografik Root Anahtarı Girin:", type="password", key="admin_password_gate")
    if token == SUPER_ADMIN_PASSWORD:
        st.success("🔱 Sazan Tanrısı Devreye Girdi. Sistemler Sizin Elinizde.")
        
        st.markdown("### 📢 Tüm Sunucuya/Kullanıcılara Küresel Mesaj Enjekte Et")
        adm_broadcast = st.text_input("Yayınlanacak Mesaj:", placeholder="Can Muhammed Çukur sunucuya siber saldırı düzenledi!", key="broadcast_input")
        if st.button("🚨 Mesajı Küresel Ağa Bas"):
            if adm_broadcast.strip():
                st.session_state.messages.append({"role": "assistant", "content": f"📢 **SİSTEM KÜRESEL DUYURUSU:** {adm_broadcast}"})
                st.success("Mesaj ağ veri tabanına yazıldı!")
                time.sleep(0.5)
                st.rerun()
                
        st.markdown("### 🪙 Altyapı Manipülasyon Araçları")
        ca1, ca2, ca3 = st.columns(3)
        with ca1:
            if st.button("💵 Sınırsız Bakiye En
