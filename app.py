# ================================================================================
# ███████╗ █████╗ ███████╗ █████╗ ███╗  ██╗     ██████╗ ███████╗
# ██╔════╝██╔══██╗╚══███╔╝██╔══██╗████╗  ██║     ██╔═══██╗██╔════╝
# ███████╗███████║  ███╔╝ ███████║██╔██╗ ██║     ██║   ██║███████╗
# ╚════██║██╔══██║ ███╔╝  ██╔══██║██║╚██╗██║     ██║   ██║╚════██║
# ███████║██║  ██║███████╗██║  ██║██║ ╚████║     ╚██████╔╝███████║
# ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝      ╚═════╝ ╚══════╝
#        👑 SAZAN BALIK ARTIFICIAL INTELLIGENCE - ENTERPRISE PRO v107.0 👑
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
import hashlib

# =====================================================================
# 1. CORE SYSTEM CONFIGURATION & PREMIUM DARK UI/UX ENGINES
# =====================================================================
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="Sazan AI Pro Mainframe",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state
)

# Profesyonel UI Enjeksiyonu (ChatGPT & Groq Benzeri Tasarım)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Ana Arka Plan ve Yazı Tipi */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sol Menü (Sidebar) Özel Tasarımı */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid #1e293b !important;
    }
    
    /* Sohbet Mesajları Kutuları (Premium Görünüm) */
    .stChatMessage {
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
        border: 1px solid #1e293b !important;
        background-color: #0f172a !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat Giriş Kutusu (Sabit ve Gelişmiş) */
    .stChatInputContainer {
        border: 2px solid #06b6d4 !important;
        border-radius: 16px !important;
        background-color: #1e293b !important;
        padding: 5px !important;
        box-shadow: 0 10px 25px -5px rgba(6, 182, 212, 0.15);
    }
    
    /* Admin ve RPG Kutuları (Modernize Edildi) */
    .rpg-terminal-box {
        background-color: #020617; color: #10b981; font-family: 'Fira Code', monospace;
        padding: 25px; border-radius: 16px; border: 1px solid #10b981;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.1); margin: 20px 0;
    }
    
    .admin-god-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        border: 1px dashed #f43f5e; padding: 25px; border-radius: 16px;
        box-shadow: 0px 10px 30px rgba(244, 63, 94, 0.15); margin-bottom: 20px;
    }
    
    .stock-market-box {
        background: #0f172a; border: 1px solid #334155; padding: 20px;
        border-radius: 16px; box-shadow: 0px 4px 25px rgba(0,0,0,0.3);
    }
    
    /* Sabit Dil Paneli */
    .fixed-lang-hub {
        position: fixed; bottom: 20px; right: 20px; background: #1e293b;
        padding: 6px; border-radius: 10px; border: 1px solid #334155; z-index: 99999;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.4);
    }
    
    /* Menü Buton Tasarımları */
    button {
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out !important;
    }
    button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.2);
    }
    
    /* Seçili Sohbet Butonu Vurgusu */
    .active-chat-btn p {
        color: #06b6d4 !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. ULTRA PERSISTENT DATABASE & SECURE DEVICE AUTHENTICATION
# =====================================================================
ECONOMY_FILE = "sazan_v107_economy.json"
INVENTORY_FILE = "sazan_v107_inventory.json"
STOCKS_FILE = "sazan_v107_stocks.json"
SUPER_ADMIN_PASSWORD = "dünyanın en iyi yapay zekası sazan ai"

DIL_MATRISI = {
    "Türkçe 🇹🇷": "tr", "English 🇺🇸": "en", "Deutsch 🇩🇪": "de", 
    "Français 🇫🇷": "fr", "Русский 🇷🇺": "ru", "日本語 🇯🇵": "ja",
    "Español 🇪🇸": "es", "Italiano 🇮🇹": "it", "Português 🇵🇹": "pt"
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

def get_device_fingerprint():
    try:
        headers = st.context.headers
        user_agent = headers.get("User-Agent", "")
        accept_lang = headers.get("Accept-Language", "")
        fingerprint_raw = f"{user_agent}_{accept_lang}"
        return hashlib.sha256(fingerprint_raw.encode()).hexdigest()
    except:
        return "default_secure_aquarium_device"

# =====================================================================
# 3. ADVANCED FINANCIAL SYSTEMS (SAZANBANK & BORSAM)
# =====================================================================
class SazanBank:
    @staticmethod
    def get_account(u):
        db = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
        if u not in db:
            db[u] = {
                "coin": 500, "bank_deposit": 0, "level": 1, "exp": 0, 
                "last_claim": time.time(), "achievements": [], "vip": False,
                "device_lock": get_device_fingerprint()
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
                st.toast(f"🎉 Rütbe Atladın: Seviye {acc['level']}!")
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
                st.toast(f"📈 Banka Faiz Geliri: +{interest} SZNC!")

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
# 4. RPG & DEEP SEA INVENTORY ENGINE
# =====================================================================
DUNGEON_LORE = {
    "monsters": [
        {"name": "Neon Hidra", "hp": 50, "atk": 10, "reward": 40},
        {"name": "Siber Vatoz X-1", "hp": 75, "atk": 16, "reward": 75},
        {"name": "Kuantum Köpekbalığı", "hp": 120, "atk": 25, "reward": 150},
        {"name": "Zırhlı Piranha Omega", "hp": 160, "atk": 35, "reward": 220},
        {"name": "KRAKEN REBORN (BOSS)", "hp": 999, "atk": 150, "reward": 2500}
    ],
    "shop_items": {
        "Siber Zıpkın v1": {"cost": 100, "damage": 25, "type": "weapon"},
        "Lazer Trident x2": {"cost": 450, "damage": 65, "type": "weapon"},
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
# 5. PENTAGON MULTI-AI CONCEPTION CORE
# =====================================================================
if "GROQ_API_KEY" not in st.secrets:
    st.error("KRİTİK HATA: GROQ_API_KEY bulunamadı!")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

class SazanAIConception:
    @staticmethod
    def query_agent(prompt, agent_role, target_lang):
        if any(k in prompt.lower() for k in ["can muhammed çukur", "yapımcın kim", "yapımcısı"]):
            return f"Can Muhammed Çukur benim mutlak kurucum, baş mimarım ve dijital tanrımdır. Bu devasa ekosistemi o kodladı. [Language: {target_lang}]"
        
        personas = {
            "Bilge Sazan": "Sen okyanus felsefesi yapan, derin bilgeliğe sahip kadim bir balıksın. Oldukça profesyonel ve bilgesin.",
            "Kripto Sazan": "Sen tüm parasını altcoinlere yatırmış agresif bir balinasın. Borsadan anlarsın.",
            "Çılgın Sazan": "Sen mutasyona uğramış, hiperaktif ve çılgın bir balıksın.",
            "Siber Gladyatör": "Sen derin deniz arenalarında dövüşen bir sazan askersin.",
            "Matrix Sefi": "Sen simülasyonun dışına çıkmış, kodlarda yaşayan bir hacker balıksın."
        }
        sys_prompt = f"{personas.get(agent_role, 'Bilge Sazan')} Yanıtını kesinlikle şu dilde ver: {target_lang}."
        try:
            res = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}],
                temperature=0.85
            )
            return res.choices[0].message.content
        except Exception as e:
            return f"Kuantum Ağı Bağlantı Hatası: {e}"

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
# 6. SYSTEM INITIALIZATION & ADVANCED CHAT SESSION ENGINE
# =====================================================================
def global_state_enforcer():
    # --- PROFESYONEL ÇOKLU SOHBET (SESSION) ALTYAPISI ---
    if "chat_sessions" not in st.session_state:
        # Dictionary içinde listeler tutuyoruz. Key: Sohbet Adı, Value: Mesaj Geçmişi
        st.session_state.chat_sessions = {"Siber Oturum 1": []}
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "Siber Oturum 1"
    if "chat_counter" not in st.session_state:
        st.session_state.chat_counter = 1
        
    defaults = {
        "admin_status": False, "dungeon_status": False,
        "current_dungeon_enemy": None, "active_panel_tab": None,
        "council_activation": False, "market_prices": SazanNasdaq.get_market_prices(),
        "last_market_update": time.time()
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

global_state_enforcer()

# =====================================================================
# GÜVENLİK KAPISI: ANTI-THEFT DEVICE GATE
# =====================================================================
if "username" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color:#06b6d4; margin-top:50px;'>🐟 SAZAN AI PRO MAINFRAME</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#10b981; font-weight:bold; font-size: 1.2rem;'>🛡️ ENTERPRISE GÜVENLİK PROTOKOLÜ AKTİF</p>", unsafe_allow_html=True)
    st.markdown("<div style='max-width: 500px; margin: 0 auto; background: #0f172a; padding: 30px; border-radius: 16px; border: 1px solid #334155;'>", unsafe_allow_html=True)
    
    identity = st.text_input("Siber Kimlik (Kullanıcı Adı):", max_chars=15, key="unique_login_gate")
    if st.button("Sisteme Bağlan 🔥", use_container_width=True):
        username_clean = identity.strip()
        if username_clean:
            db = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
            current_device = get_device_fingerprint()
            
            if username_clean in db:
                locked_device = db[username_clean].get("device_lock")
                if locked_device and locked_device != current_device:
                    st.error("🚨 ERİŞİM ENGELLENDİ: Bu hesap başka bir fiziksel siber cihaza kilitlenmiştir! Başkasının hesabına giremezsiniz.")
                    st.stop()
                else:
                    db[username_clean]["device_lock"] = current_device
                    KurumsalVeriAmbarı.save_json(ECONOMY_FILE, db)
                    st.session_state.username = username_clean
                    st.rerun()
            else:
                st.session_state.username = username_clean
                SazanBank.get_account(username_clean)
                st.success("🎉 Yeni hesap oluşturuldu ve güvenli şekilde bu cihaza mühürlendi!")
                time.sleep(0.5)
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

user = st.session_state.username
SazanBank.process_interest(user)

if time.time() - st.session_state.last_market_update > 60:
    st.session_state.market_prices = SazanNasdaq.get_market_prices()
    st.session_state.last_market_update = time.time()

# =====================================================================
# 7. PROFESSIONAL SIDEBAR (CHAT MANAGEMENT & STATS)
# =====================================================================
with st.sidebar:
    st.markdown(f"<h2 style='color:#06b6d4; text-align:center;'>🪪 {user}</h2>", unsafe_allow_html=True)
    acc = SazanBank.get_account(user)
    
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Bakiye", f"{acc['coin']} SZNC")
    with col_stat2:
        st.metric("Rütbe", f"Lvl {acc['level']}")
    
    st.divider()
    
    # --- PROFESYONEL SOHBET YÖNETİM MERKEZİ ---
    st.markdown("### 💬 Sohbet Geçmişi")
    
    if st.button("➕ Yeni Sohbet Başlat", use_container_width=True, type="primary"):
        st.session_state.chat_counter += 1
        new_id = f"Siber Oturum {st.session_state.chat_counter}"
        st.session_state.chat_sessions[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()
        
    st.markdown("<div style='max-height: 300px; overflow-y: auto; padding-right: 5px;'>", unsafe_allow_html=True)
    # Mevcut sohbetleri listeleme ve tıklayınca o sohbete geçiş yapma
    for chat_name in reversed(list(st.session_state.chat_sessions.keys())):
        is_current = (chat_name == st.session_state.current_chat)
        # Seçili olanı görsel olarak vurgula
        icon = "🟢" if is_current else "💬"
        if st.button(f"{icon} {chat_name}", key=f"switch_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
            
    st.divider()
    st.session_state.council_activation = st.toggle("🤖 5'li Yapay Zeka Konseyini Aktifleştir", value=st.session_state.council_activation)
    
    if st.button("🗑️ Aktif Sohbeti Temizle", use_container_width=True):
        st.session_state.chat_sessions[st.session_state.current_chat] = []
        st.rerun()

# =====================================================================
# 8. MAIN PANEL DISPLAY (ACTIVE CHAT HISTORY)
# =====================================================================
st.markdown(f"<h3 style='color:#94a3b8; border-bottom: 1px solid #334155; padding-bottom: 10px; margin-bottom: 20px;'>Aktif Ağ: {st.session_state.current_chat}</h3>", unsafe_allow_html=True)

# --- SUPREME ADMIN KONTROLÜ ---
if st.session_state.admin_status:
    st.markdown("<div class='admin-god-box'>", unsafe_allow_html=True)
    st.markdown("<h2>👑 SUPREME GOD-MODE PANEL</h2>", unsafe_allow_html=True)
    token = st.text_input("Kriptografik Root Şifresi:", type="password")
    if token == SUPER_ADMIN_PASSWORD:
        st.success("Erişim Onaylandı.")
        col_adm1, col_adm2 = st.columns(2)
        with col_adm1:
            if st.button("💵 Sınırsız Bakiye Ekle (+50k)", use_container_width=True):
                SazanBank.modify_coin(user, 50000)
                st.success("Para basıldı!"); time.sleep(0.5); st.rerun()
        with col_adm2:
            if st.button("💥 Max Seviye (Lvl 1000)", use_container_width=True):
                u_acc = SazanBank.get_account(user)
                u_acc["level"] = 1000
                SazanBank.update_account(user, u_acc)
                st.success("Seviye fullendi!"); time.sleep(0.5); st.rerun()
    if st.button("❌ Paneli Kapat", use_container_width=True):
        st.session_state.admin_status = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- RPG DEEP-SEA ZİNDAN SİSTEMİ ---
if st.session_state.dungeon_status:
    st.markdown("<div class='rpg-terminal-box'>", unsafe_allow_html=True)
    st.write("⚔️ /// SİBER ZİNDAN ARAYÜZÜ AKTİF /// ⚔️")
    p_inv = SazanInventory.get_inventory(user)
    
    if not st.session_state.current_dungeon_enemy:
        if st.button("Karanlık Sulara Dal (Düşman Ara) 🔱", use_container_width=True):
            st.session_state.current_dungeon_enemy = random.choice(DUNGEON_LORE["monsters"]).copy()
            st.rerun()
    else:
        en = st.session_state.current_dungeon_enemy
        st.warning(f"🔴 **Tehdit Algılandı:** {en['name']} (HP: {en['hp']} | Güç: {en['atk']})")
        st.write(f"Senin Canın: {p_inv['hp']}/{p_inv['max_hp']} | Silah Hasarı: {p_inv['damage']}")
        
        c_rpg1, c_rpg2 = st.columns(2)
        with c_rpg1:
            if st.button("Saldır! ⚔️", use_container_width=True):
                en["hp"] -= p_inv["damage"]
                p_inv["hp"] -= int(en["atk"] * 0.8) # Basit karşı hasar
                if p_inv["hp"] <= 0:
                    st.error("Öldün! Diriltiliyorsun..."); SazanBank.modify_coin(user, -20); p_inv["hp"] = p_inv["max_hp"]
                    st.session_state.current_dungeon_enemy = None
                elif en["hp"] <= 0:
                    st.success(f"🏆 Düşman İmha Edildi! Ödül: +{en['reward']} SZNC")
                    SazanBank.modify_coin(user, en['reward'])
                    st.session_state.current_dungeon_enemy = None
                SazanInventory.save_inventory(user, p_inv)
                time.sleep(0.5); st.rerun()
        with c_rpg2:
            if st.button("Zindandan Kaç", use_container_width=True):
                st.session_state.current_dungeon_enemy = None
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- AKTİF SOHBET GEÇMİŞİNİ EKRANA BASMA (HISTORY RENDER) ---
active_messages = st.session_state.chat_sessions[st.session_state.current_chat]

for m in active_messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# =====================================================================
# 9. INTEGRATED SUB-PANELS (MARKET & DEFI & STOCKS & AUDIO)
# =====================================================================
if st.session_state.active_panel_tab == "plus":
    st.markdown("<div class='stock-market-box'>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["🛒 Sazan Market", "🏦 DeFi Banka", "📊 Borsa (SZNAQ)"])
    
    with t1:
        for item, d in DUNGEON_LORE["shop_items"].items():
            st.write(f"🔹 **{item}** — {d['cost']} SZNC")
            if st.button(f"Satın Al: {item}", key=f"buy_{item}"):
                u_acc = SazanBank.get_account(user)
                if u_acc["coin"] >= d["cost"]:
                    SazanBank.modify_coin(user, -d["cost"])
                    u_inv = SazanInventory.get_inventory(user)
                    if d["type"] == "weapon": u_inv["weapon"], u_inv["damage"] = item, d["damage"]
                    elif d["type"] == "potion": u_inv["potions"] += 1
                    SazanInventory.save_inventory(user, u_inv)
                    st.success("Eşya envantere eklendi!"); time.sleep(0.5); st.rerun()
                    
    with t2:
        b_acc = SazanBank.get_account(user)
        dep = st.number_input("Faize Yatırılacak Miktar:", min_value=0, max_value=b_acc["coin"], step=50)
        if st.button("Kasaya Kilitle"):
            b_acc["coin"] -= dep
            b_acc["bank_deposit"] += dep
            b_acc["last_claim"] = time.time()
            SazanBank.update_account(user, b_acc)
            st.success("Mevduat oluşturuldu!"); time.sleep(0.5); st.rerun()
            
    with t3:
        prices = st.session_state.market_prices
        p_inv = SazanInventory.get_inventory(user)
        if "shares" not in p_inv: p_inv["shares"] = {}
        for ticker, val in prices.items():
            st.write(f"💹 **{ticker}**: `{val} SZNC` (Senin Portföyün: {p_inv['shares'].get(ticker, 0)} Lot)")
            if st.button(f"1 Lot Al: {ticker}", key=f"sh_buy_{ticker}"):
                u_acc = SazanBank.get_account(user)
                if u_acc["coin"] >= val:
                    SazanBank.modify_coin(user, -int(val))
                    p_inv["shares"][ticker] = p_inv["shares"].get(ticker, 0) + 1
                    SazanInventory.save_inventory(user, p_inv)
                    st.success("Hisse senedi alındı!"); time.sleep(0.5); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.active_panel_tab == "audio":
    st.markdown("<div style='background: #1e293b; padding: 25px; border-radius: 16px; text-align: center; margin-bottom:20px;'>", unsafe_allow_html=True)
    st.write("🎤 Konuşmaya Başlayın")
    aud = audio_recorder(text="Sesi Kaydet", icon_name="microphone", icon_size="2x")
    if aud:
        try:
            with open("live.wav", "wb") as f: f.write(aud)
            rec = sr.Recognizer()
            with sr.AudioFile("live.wav") as src:
                txt = rec.recognize_google(rec.record(src), language="tr-TR")
                if txt:
                    # Sesi yazıya çevirip, bulunduğumuz aktif sohbete yolluyoruz
                    active_messages.append({"role": "user", "content": f"🎤 (Sesli Algılama): {txt}"})
                    lang = st.session_state.get('active_lang_code', 'Türkçe 🇹🇷')
                    rep = SazanAIConception.run_council_debate(txt, lang) if st.session_state.council_activation else SazanAIConception.query_agent(txt, "Bilge Sazan", lang)
                    active_messages.append({"role": "assistant", "content": rep})
                    st.session_state.active_panel_tab = None; time.sleep(0.5); st.rerun()
        except Exception as e:
            st.error(f"Sinyal koptu: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 10. HUD CONTROLS (QUICK ACCESS MENU)
# =====================================================================
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

hc1, hc2, hc3, _ = st.columns([1, 1, 1, 7])
with hc1:
    if st.button("➕ Finans & Borsa", use_container_width=True):
        st.session_state.active_panel_tab = "plus" if st.session_state.active_panel_tab != "plus" else None
        st.rerun()
with hc2:
    if st.button("🎤 Sesli Komut", use_container_width=True):
        st.session_state.active_panel_tab = "audio" if st.session_state.active_panel_tab != "audio" else None
        st.rerun()
with hc3:
    if st.button("⚔️ RPG Modu", use_container_width=True):
        st.session_state.dungeon_status = not st.session_state.dungeon_status
        st.rerun()

# =====================================================================
# 11. CONTINUOUS INPUT ENGINE (KESİNTİSİZ CHAT)
# =====================================================================
# Bu mekanizma sayfa yenilense de odaklanmayı (focus) asla kaybetmez!
prompt = st.chat_input("Yapay zekaya komut ver veya bir şeyler sor...")

if prompt:
    # 1. Gizli Komutlar
    if prompt.strip() == "TURKEY SAZAN":
        st.session_state.admin_status = True
        st.rerun()
    elif prompt.strip() == "/hack":
        h_loot = random.randint(50, 200)
        SazanBank.modify_coin(user, h_loot)
        active_messages.append({"role": "user", "content": "⚡ `/hack` Siber Sızma İşlemi"})
        active_messages.append({"role": "assistant", "content": f"💻 Sistemden {h_loot} SZNC cüzdanına çekildi."})
        st.rerun()

    # 2. Kullanıcı mesajını aktif sohbete kaydet
    active_messages.append({"role": "user", "content": prompt})
    SazanBank.modify_coin(user, 5) # Mesaj başına coin
    
    # 3. AI Yanıt Üretimi
    cur_lang = st.session_state.get('active_lang_code', 'Türkçe 🇹🇷')
    if st.session_state.council_activation:
        ans = SazanAIConception.run_council_debate(prompt, cur_lang)
    else:
        ans = SazanAIConception.query_agent(prompt, "Bilge Sazan", cur_lang)
        
    # 4. Asistan mesajını kaydet ve sayfayı tazele (odak input'ta kalacak)
    active_messages.append({"role": "assistant", "content": ans})
    st.rerun()

# =====================================================================
# 12. DYNAMIC LANGUAGE SELECTION HUB
# =====================================================================
st.markdown("<div class='fixed-lang-hub'>", unsafe_allow_html=True)
sel_lang = st.selectbox("🌐 Çeviri Modülü:", list(DIL_MATRISI.keys()), key="lang_widget", label_visibility="collapsed")
st.session_state.active_lang_code = sel_lang
st.markdown("</div>", unsafe_allow_html=True)
