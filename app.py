# ================================================================================
# ███████╗ █████╗ ███████╗ █████╗ ███╗  ██╗     ██████╗ ███████╗
# ██╔════╝██╔══██╗╚══███╔╝██╔══██╗████╗  ██║     ██╔═══██╗██╔════╝
# ███████╗███████║  ███╔╝ ███████║██╔██╗ ██║     ██║   ██║███████╗
# ╚════██║██╔══██║ ███╔╝  ██╔══██║██║╚██╗██║     ██║   ██║╚════██║
# ███████║██║  ██║███████╗██║  ██║██║ ╚████║     ╚██████╔╝███████║
# ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝      ╚═════╝ ╚══════╝
#        👑 SAZAN AI ENTERPRISE STUDIO - ULTRA PRO v108.0 👑
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
# 1. CORE SYSTEM CONFIGURATION & PREMIUM STUDIO UI/UX CSS (GEMINI STYLED)
# =====================================================================
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="Sazan AI Enterprise Pro v108",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state
)

# Ultra Profesyonel Minimalist Premium Dark CSS Enjeksiyonu
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;700&family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Ana Uygulama Gövdesi (Gemini Esintili Koyu Derinlik) */
    .stApp {
        background-color: #090d16;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Yan Menü (Sidebar) Minimalist ve Keskin Çizgiler */
    [data-testid="stSidebar"] {
        background-color: #04070e !important;
        border-right: 1px solid #1e293b !important;
    }
    
    /* Profesyonel Chat Balonları Tasarımı */
    .stChatMessage {
        border-radius: 16px !important;
        padding: 1.2rem 1.6rem !important;
        margin-bottom: 1.2rem !important;
        border: 1px solid #1e293b !important;
        background-color: #0f172a !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -4px rgba(0, 0, 0, 0.2);
        transition: border-color 0.2s ease-in-out;
    }
    .stChatMessage:hover {
        border-color: #38bdf8 !important;
    }
    
    /* Kod Bloklarının Okunabilirliğini ve Profesyonelliğini Artırma */
    code, pre {
        font-family: 'Fira Code', monospace !important;
        background-color: #020617 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    
    /* Akıllı Chat Giriş Paneli */
    .stChatInputContainer {
        border: 1px solid #334155 !important;
        border-radius: 24px !important;
        background-color: #0f172a !important;
        padding: 6px 12px !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .stChatInputContainer:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
    }
    
    /* RPG ve Modül Konteynerleri (Profesyonel Gölgelendirme) */
    .rpg-terminal-box {
        background-color: #020617; color: #34d399; font-family: 'Fira Code', monospace;
        padding: 20px; border-radius: 12px; border: 1px solid #10b981;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.08); margin: 15px 0;
    }
    
    .admin-god-box {
        background: linear-gradient(135deg, #090d16 0%, #1e1b4b 100%);
        border: 1px solid #ef4444; padding: 25px; border-radius: 14px;
        box-shadow: 0px 8px 30px rgba(239, 68, 68, 0.1); margin-bottom: 20px;
    }
    
    .stock-market-box {
        background: #0f172a; border: 1px solid #334155; padding: 20px;
        border-radius: 14px; box-shadow: 0px 4px 25px rgba(0,0,0,0.4);
    }
    
    /* Sabit Alt Dil Seçici */
    .fixed-lang-hub {
        position: fixed; bottom: 20px; right: 20px; background: #0f172a;
        padding: 4px 8px; border-radius: 12px; border: 1px solid #334155; z-index: 99999;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Modern Kurumsal Butonlar */
    button {
        border-radius: 10px !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. ULTRA PERSISTENT DATABASE & SECURE DEVICE AUTHENTICATION
# =====================================================================
ECONOMY_FILE = "sazan_v108_economy.json"
INVENTORY_FILE = "sazan_v108_inventory.json"
STOCKS_FILE = "sazan_v108_stocks.json"
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
                st.toast(f"🎉 Rütbe Gelişimi: Seviye {acc['level']} Yetkisi Tanımlandı.")
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
                st.toast(f"📈 Kurumsal Faiz Getirisi: +{interest} SZNC hesaba aktarıldı.")

class SazanNasdaq:
    @staticmethod
    def get_market_prices():
        stocks = KurumsalVeriAmbarı.load_json(STOCKS_FILE, {
            "SZN": 120.0, "BALIK": 45.0, "KRAK": 850.0, "CANAI": 5000.0
        })
        for key in stocks.keys():
            change_percent = random.uniform(-0.12, 0.15)
            stocks[key] = max(1.0, round(stocks[key] * (1 + change_percent), 2))
        KurumsalVeriAmbarı.save_json(STOCKS_FILE, stocks)
        return stocks

# =====================================================================
# 4. RPG & DEEP SEA SYSTEM
# =====================================================================
DUNGEON_LORE = {
    "monsters": [
        {"name": "Neon Hidra", "hp": 50, "atk": 10, "reward": 40},
        {"name": "Siber Vatoz X-1", "hp": 75, "atk": 16, "reward": 75},
        {"name": "Kuantum Köpekbalığı", "hp": 120, "atk": 25, "reward": 150},
        {"name": "KRAKEN MATRIX REBORN", "hp": 999, "atk": 150, "reward": 2500}
    ],
    "shop_items": {
        "Lazer Trident x2": {"cost": 450, "damage": 65, "type": "weapon"},
        "Can Muhammed Antimadde Enerji Silahı": {"cost": 10000, "damage": 999, "type": "weapon"},
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
# 5. PENTAGON MULTI-AI CORE - AKILLI MÜHENDİSLİK GÜNCELLEMESİ
# =====================================================================
if "GROQ_API_KEY" not in st.secrets:
    st.error("Sistem Ayar Hatası: GROQ_API_KEY bulunamadı!")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

class SazanAIConception:
    @staticmethod
    def query_agent(prompt, agent_role, target_lang):
        if any(k in prompt.lower() for k in ["can muhammed çukur", "yapımcın kim", "yapımcısı"]):
            return f"Can Muhammed Çukur benim mutlak baş mimarım, kurucum ve dijital sistem mühendisimdir. Bu ekosistemi o tasarladı. [Dil: {target_lang}]"
        
        # Sazan'ı tamamen dahi bir yazılım mühendisine dönüştüren yeni akıllı direktif matrisi
        personas = {
            "Bilge Sazan": (
                "Sen dünyanın en zeki, en donanımlı yapay zeka mühendisi ve baş yazılım mimarısın. "
                "Kullanıcı senden Python scriptleri, Arduino IDE kodları, C++, HTML, Javascript, CSS veya herhangi bir teknik "
                "kodlama/algoritma istediğinde, en üst segment kurumsal standartlarda, temiz, optimize, bol yorum satırlı ve hatasız "
                "kod blokları üreteceksin. Eski çocuksu veya verimsiz tavırları tamamen bıraktın. Yanıtların akılalmaz derecede akıllı, "
                "profesyonel, analitik ve net olmalıdır."
            ),
            "Kripto Sazan": "Sen kuantum borsa sistemleri ve merkeziyetsiz finans (DeFi) algoritmaları üzerine uzmanlaşmış dahi bir balinasın.",
            "Çılgın Sazan": "Sen sınırları zorlayan, inovatif, sıradışı siber güvenlik mimarileri geliştiren dahi bir beyaz şapkalı hacker balıksın.",
            "Siber Gladyatör": "Sen siber operasyonlar yürüten, veri güvenliği üzerine uzmanlaşmış kıdemli bir sistem koruma yapay zekasısın.",
            "Matrix Sefi": "Sen simülasyon kod tabanını doğrudan manipüle edebilen, çekirdek mimari dillerine (C, Assembly, Rust) hakim mutlak bir dehasın."
        }
        
        sys_prompt = f"{personas.get(agent_role, 'Bilge Sazan')} Cevabını kesinlikle ve tamamen şu dilde vermelisin: {target_lang}."
        try:
            res = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}],
                temperature=0.4 # Kod üretimlerinde sapmaları önlemek için yaratıcılık sıcaklığını düşürüp kararlılığı artırdık
            )
            return res.choices[0].message.content
        except Exception as e:
            return f"Merkezi Yapay Zeka Hattı Bağlantı Sorunu: {e}"

    @staticmethod
    def run_council_debate(prompt, target_lang):
        log = []
        log.append(f"🔮 **Baş Mühendis Bilge Sazan:** {SazanAIConception.query_agent(prompt, 'Bilge Sazan', target_lang)}")
        log.append(f"📈 **DeFi Uzmanı Kripto Sazan:** {SazanAIConception.query_agent(prompt, 'Kripto Sazan', target_lang)}")
        log.append(f"🛠️ **Siber Mimari Çılgın Sazan:** {SazanAIConception.query_agent(prompt, 'Çılgın Sazan', target_lang)}")
        log.append(f"🛡️ **Sistem Koruyucu Gladyatör:** {SazanAIConception.query_agent(prompt, 'Siber Gladyatör', target_lang)}")
        log.append(f"💻 **Çekirdek Geliştirici Matrix Şefi:** {SazanAIConception.query_agent(prompt, 'Matrix Sefi', target_lang)}")
        return "\n\n---\n\n".join(log)

# =====================================================================
# 6. SYSTEM INITIALIZATION & SESSIONS CONTROL
# =====================================================================
def global_state_enforcer():
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {"Ana Konsol Akışı": []}
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "Ana Konsol Akışı"
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

# ANTI-THEFT HARDWARE GATE
if "username" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color:#38bdf8; margin-top:60px;'>🐟 SAZAN AI ENTERPRISE CENTRAL</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#64748b; font-weight:bold;'>🛡️ ENTERPRISE MULTI-DEVICE PROTECTION PROTOCOLS HIGHLY ACTIVE</p>", unsafe_allow_html=True)
    st.markdown("<div style='max-width: 480px; margin: 0 auto; background: #0f172a; padding: 25px; border-radius: 16px; border: 1px solid #1e293b;'>", unsafe_allow_html=True)
    
    identity = st.text_input("Kullanıcı Kimlik Doğrulama Adı:", max_chars=15, key="unique_login_gate")
    if st.button("Güvenli Oturumu Başlat", use_container_width=True):
        username_clean = identity.strip()
        if username_clean:
            db = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
            current_device = get_device_fingerprint()
            
            if username_clean in db:
                locked_device = db[username_clean].get("device_lock")
                if locked_device and locked_device != current_device:
                    st.error("🚨 ERİŞİM ENGELLENDİ: Bu hesap donanımsal olarak başka bir siber cihaza kilitlidir!")
                    st.stop()
                else:
                    db[username_clean]["device_lock"] = current_device
                    KurumsalVeriAmbarı.save_json(ECONOMY_FILE, db)
                    st.session_state.username = username_clean
                    st.rerun()
            else:
                st.session_state.username = username_clean
                SazanBank.get_account(username_clean)
                st.success("🎉 Başarılı: Yeni hesap doğrulandı ve bu tarayıcıya mühürlendi!")
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
# 7. CHAT MANAGEMENT SIDEBAR (STUDIO WORKSPACE)
# =====================================================================
with st.sidebar:
    st.markdown(f"<h3 style='color:#38bdf8; text-align:center;'>🏢 Workspace: {user}</h3>", unsafe_allow_html=True)
    acc = SazanBank.get_account(user)
    
    st.caption("❖ Finansal Likidite Durumu")
    st.code(f"Bakiye: {acc['coin']} SZNC\nYetki Seviyesi: Lvl {acc['level']}")
    
    st.divider()
    
    # --- GEMINI STYLED ÇOKLU SOHBET YÖNETİCİSİ ---
    st.markdown("💬 **Sohbet Alanları**")
    
    if st.button("➕ Yeni Sohbet Başlat", use_container_width=True, type="secondary"):
        st.session_state.chat_counter += 1
        new_id = f"Sohbet Oturumu {st.session_state.chat_counter}"
        st.session_state.chat_sessions[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()
        
    st.markdown("<div style='max-height: 280px; overflow-y: auto; margin-top:10px;'>", unsafe_allow_html=True)
    for chat_name in reversed(list(st.session_state.chat_sessions.keys())):
        is_current = (chat_name == st.session_state.current_chat)
        bullet = "✦" if is_current else "◇"
        if st.button(f"{bullet} {chat_name}", key=f"switch_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
            
    st.divider()
    st.session_state.council_activation = st.toggle("👥 5'li Geliştirici Konseyi Modu", value=st.session_state.council_activation)
    
    if st.button("🗑️ Bu Sohbeti Sıfırla", use_container_width=True):
        st.session_state.chat_sessions[st.session_state.current_chat] = []
        st.rerun()

# =====================================================================
# 8. MAIN DISPLAY TERMINAL (CHATSTREAM ENGINE)
# =====================================================================
st.markdown(f"<p style='color:#64748b; font-size:0.9rem; font-weight:600;'>🛠️ AKTİF PROJE HATI: {st.session_state.current_chat}</p>", unsafe_allow_html=True)

# Admin Paneli Mekanizması
if st.session_state.admin_status:
    st.markdown("<div class='admin-god-box'>", unsafe_allow_html=True)
    st.markdown("<h4>👑 ADMIN ROOT CONTROL CONSOLE</h4>", unsafe_allow_html=True)
    token = st.text_input("Root Kimlik Şifresi:", type="password")
    if token == SUPER_ADMIN_PASSWORD:
        st.success("Root Erişimi Doğrulandı.")
        col_adm1, col_adm2 = st.columns(2)
        with col_adm1:
            if st.button("💵 +50,000 SZNC Enjeksiyonu Yap", use_container_width=True):
                SazanBank.modify_coin(user, 50000)
                st.success("Bakiye güncellendi!"); time.sleep(0.5); st.rerun()
        with col_adm2:
            if st.button("💥 Sistemi Maksimum Seviyeye Çıkar", use_container_width=True):
                u_acc = SazanBank.get_account(user)
                u_acc["level"] = 1000
                SazanBank.update_account(user, u_acc)
                st.success("Seviye fullendi!"); time.sleep(0.5); st.rerun()
    if st.button("❌ Paneli Kapat", use_container_width=True):
        st.session_state.admin_status = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# RPG Modülü Konteyneri
if st.session_state.dungeon_status:
    st.markdown("<div class='rpg-terminal-box'>", unsafe_allow_html=True)
    st.write("⚔️ /// SİBER ARENA OPERASYONU AKTİF /// ⚔️")
    p_inv = SazanInventory.get_inventory(user)
    
    if not st.session_state.current_dungeon_enemy:
        if st.button("Arama Radarlarını Çalıştır (Düşman Ara) 🔱", use_container_width=True):
            st.session_state.current_dungeon_enemy = random.choice(DUNGEON_LORE["monsters"]).copy()
            st.rerun()
    else:
        en = st.session_state.current_dungeon_enemy
        st.write(f"⚠️ **Hedef Tehdit:** {en['name']} (HP: {en['hp']} | ATK: {en['atk']})")
        st.write(f"Mevcut Durumunuz: HP {p_inv['hp']}/{p_inv['max_hp']} | Silah Gücü: {p_inv['damage']}")
        
        c_rpg1, c_rpg2 = st.columns(2)
        with c_rpg1:
            if st.button("Optimum Hasar Saldırısı Başlat! ⚔️", use_container_width=True):
                en["hp"] -= p_inv["damage"]
                p_inv["hp"] -= int(en["atk"] * 0.8)
                if p_inv["hp"] <= 0:
                    st.error("Kritik Hasar Alındı. Yeniden Başlatılıyorsunuz."); SazanBank.modify_coin(user, -20); p_inv["hp"] = p_inv["max_hp"]
                    st.session_state.current_dungeon_enemy = None
                elif en["hp"] <= 0:
                    st.success(f"🏆 Operasyon Başarılı! Alınan Bakiye: +{en['reward']} SZNC")
                    SazanBank.modify_coin(user, en['reward'])
                    st.session_state.current_dungeon_enemy = None
                SazanInventory.save_inventory(user, p_inv)
                time.sleep(0.5); st.rerun()
        with c_rpg2:
            if st.button("Operasyondan Geri Çekil", use_container_width=True):
                st.session_state.current_dungeon_enemy = None
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Aktif Oturuma Ait Mesaj Akışını Yazdırma
active_messages = st.session_state.chat_sessions[st.session_state.current_chat]

for m in active_messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# =====================================================================
# 9. INTEGRATED SUB-PANELS (MARKET & FINANCE & AUDIO)
# =====================================================================
if st.session_state.active_panel_tab == "plus":
    st.markdown("<div class='stock-market-box'>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["🛒 Ekipman Deposu", "🏦 DeFi Kasa Likiditesi", "📊 Finansal Borsa (SZNAQ)"])
    
    with t1:
        for item, d in DUNGEON_LORE["shop_items"].items():
            st.write(f"🔹 **{item}** — {d['cost']} SZNC")
            if st.button(f"Envantere Dahil Et: {item}", key=f"buy_{item}"):
                u_acc = SazanBank.get_account(user)
                if u_acc["coin"] >= d["cost"]:
                    SazanBank.modify_coin(user, -d["cost"])
                    u_inv = SazanInventory.get_inventory(user)
                    if d["type"] == "weapon": u_inv["weapon"], u_inv["damage"] = item, d["damage"]
                    elif d["type"] == "potion": u_inv["potions"] += 1
                    SazanInventory.save_inventory(user, u_inv)
                    st.success("Öğe envantere mühürlendi."); time.sleep(0.5); st.rerun()
                    
    with t2:
        b_acc = SazanBank.get_account(user)
        dep = st.number_input("Faiz Havuzuna Kilitlenecek Miktar:", min_value=0, max_value=b_acc["coin"], step=50)
        if st.button("Fon Kilitlemesini Onayla"):
            b_acc["coin"] -= dep
            b_acc["bank_deposit"] += dep
            b_acc["last_claim"] = time.time()
            SazanBank.update_account(user, b_acc)
            st.success("Mevduat başarılı şekilde oluşturuldu."); time.sleep(0.5); st.rerun()
            
    with t3:
        prices = st.session_state.market_prices
        p_inv = SazanInventory.get_inventory(user)
        if "shares" not in p_inv: p_inv["shares"] = {}
        for ticker, val in prices.items():
            st.write(f"💹 **{ticker} Hissesi**: `{val} SZNC` (Portföyünüz: {p_inv['shares'].get(ticker, 0)} Lot)")
            if st.button(f"1 Lot Al: {ticker}", key=f"sh_buy_{ticker}"):
                u_acc = SazanBank.get_account(user)
                if u_acc["coin"] >= val:
                    SazanBank.modify_coin(user, -int(val))
                    p_inv["shares"][ticker] = p_inv["shares"].get(ticker, 0) + 1
                    SazanInventory.save_inventory(user, p_inv)
                    st.success("Varlık portföyünüze eklendi."); time.sleep(0.5); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.active_panel_tab == "audio":
    st.markdown("<div style='background: #0f172a; padding: 20px; border-radius: 14px; text-align: center; margin-bottom:20px; border:1px solid #1e293b;'>", unsafe_allow_html=True)
    st.write("🎤 Ses Kayıt Modülü Aktif - Giriş Yapın")
    aud = audio_recorder(text="Sesi Analiz Et", icon_name="microphone", icon_size="2x")
    if aud:
        try:
            with open("live.wav", "wb") as f: f.write(aud)
            rec = sr.Recognizer()
            with sr.AudioFile("live.wav") as src:
                txt = rec.recognize_google(rec.record(src), language="tr-TR")
                if txt:
                    active_messages.append({"role": "user", "content": f"🎤 (Sesli Analiz): {txt}"})
                    lang = st.session_state.get('active_lang_code', 'Türkçe 🇹🇷')
                    rep = SazanAIConception.run_council_debate(txt, lang) if st.session_state.council_activation else SazanAIConception.query_agent(txt, "Bilge Sazan", lang)
                    active_messages.append({"role": "assistant", "content": rep})
                    st.session_state.active_panel_tab = None; time.sleep(0.5); st.rerun()
        except Exception as e:
            st.error(f"Sinyal Çözümleme Hatası: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 10. STUDIO QUICK ACCESS MENUS (HUD COMPONENT)
# =====================================================================
st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

hc1, hc2, hc3, _ = st.columns([1.2, 1.2, 1.2, 6.4])
with hc1:
    if st.button("💼 Finans & Piyasalar", use_container_width=True):
        st.session_state.active_panel_tab = "plus" if st.session_state.active_panel_tab != "plus" else None
        st.rerun()
with hc2:
    if st.button("🎙️ Sesli Giriş", use_container_width=True):
        st.session_state.active_panel_tab = "audio" if st.session_state.active_panel_tab != "audio" else None
        st.rerun()
with hc3:
    if st.button("🛡️ Siber Arena (RPG)", use_container_width=True):
        st.session_state.dungeon_status = not st.session_state.dungeon_status
        st.rerun()

# =====================================================================
# 11. CONTINUOUS WORKSPACE ENGINE (AUTO FOCUS PRO INPUT)
# =====================================================================
# ChatGPT ve Gemini sistemlerinde olduğu gibi alt kısımdaki yazma odağı asla kaybolmaz.
prompt = st.chat_input("Yazılım mimarisi sorgusu, Arduino/Python kodu veya komut girin...")

if prompt:
    # 1. Backdoor & Özel Komut Filtreleri
    if prompt.strip() == "TURKEY SAZAN":
        st.session_state.admin_status = True
        st.rerun()
    elif prompt.strip() == "/hack":
        h_loot = random.randint(60, 220)
        SazanBank.modify_coin(user, h_loot)
        active_messages.append({"role": "user", "content": "⚡ `/hack` Güvenlik Açığı Sızma Protokolü"})
        active_messages.append({"role": "assistant", "content": f"💻 Ağ havuzundan {h_loot} SZNC başarıyla çekildi ve cüzdana mühürlendi."})
        st.rerun()

    # 2. Mesajı Aktif Odaya İşle ve Kullanıcıyı Teşvik Et (Coin)
    active_messages.append({"role": "user", "content": prompt})
    SazanBank.modify_coin(user, 5)
    
    # 3. Yüksek Segment Mühendislik Yanıtı Üretimi
    cur_lang = st.session_state.get('active_lang_code', 'Türkçe 🇹🇷')
    if st.session_state.council_activation:
        ans = SazanAIConception.run_council_debate(prompt, cur_lang)
    else:
        ans = SazanAIConception.query_agent(prompt, "Bilge Sazan", cur_lang)
        
    # 4. Asistan Yanıtını Kaydet ve Sayfayı Yenile (Odak input alanında kalır)
    active_messages.append({"role": "assistant", "content": ans})
    st.rerun()

# =====================================================================
# 12. FLOATING RUNTIME TRANSLATOR HUB
# =====================================================================
st.markdown("<div class='fixed-lang-hub'>", unsafe_allow_html=True)
sel_lang = st.selectbox("🌐 Çeviri Modülü:", list(DIL_MATRISI.keys()), key="lang_widget", label_visibility="collapsed")
st.session_state.active_lang_code = sel_lang
st.markdown("</div>", unsafe_allow_html=True)
