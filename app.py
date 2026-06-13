# ================================================================================
# ███████╗ █████╗ ███████╗ █████╗ ███╗  ██╗     ██████╗ ███████╗
# ██╔════╝██╔══██╗╚══███╔╝██╔══██╗████╗  ██║     ██╔═══██╗██╔════╝
# ███████╗███████║  ███╔╝ ███████║██╔██╗ ██║     ██║   ██║███████╗
# ╚════██║██╔══██║ ███╔╝  ██╔══██║██║╚██╗██║     ██║   ██║╚════██║
# ███████║██║  ██║███████╗██║  ██║██║ ╚████║     ╚██████╔╝███████║
# ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝      ╚═════╝ ╚══════╝
#        👑 SAZAN AI ENTERPRISE STUDIO - GAME ENGINE SUPREME v113.0 👑
#        DEVELOPED BY: CAN MUHAMMED ÇUKUR - THE MUTLAK ARCHITECT
#        PATCH NOTE: NO MORE IMAGES - QUANTUM HTML GAME GENERATOR INTERCEPTOR
# ================================================================================

import streamlit as st
import json
import os
import time
import random
import io
import re
import base64
import pandas as pd
import numpy as np
import urllib.parse
from groq import Groq
from datetime import datetime
import hashlib

# =====================================================================
# 1. CORE SYSTEM CONFIGURATION & PREMIUM STUDIO UI/UX CSS
# =====================================================================
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="Sazan AI Enterprise Game Overlord v113.0",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state
)

# Ultra Profesyonel Minimalist Premium Dark CSS Enjeksiyonu
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;700&family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background-color: #05070f;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: #020306 !important;
        border-right: 1px solid #1e293b !important;
    }
    
    .stChatMessage {
        border-radius: 16px !important;
        padding: 1.4rem 1.8rem !important;
        margin-bottom: 1.5rem !important;
        border: 1px solid #1e293b !important;
        background-color: #090f21 !important;
        box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.3);
    }
    
    code, pre {
        font-family: 'Fira Code', monospace !important;
        background-color: #010307 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    
    .stChatInputContainer {
        border: 1px solid #334155 !important;
        border-radius: 28px !important;
        background-color: #0e1626 !important;
        padding: 8px 16px !important;
    }
    
    .rpg-terminal-box {
        background-color: #010307; color: #10b981; font-family: 'Fira Code', monospace;
        padding: 22px; border-radius: 14px; border: 1px solid #10b981;
    }
    
    .stock-market-box {
        background: #090f21; border: 1px solid #1e293b; padding: 22px;
        border-radius: 16px;
    }
    
    .fixed-lang-hub {
        position: fixed; bottom: 20px; right: 20px; background: #0e1626;
        padding: 5px 10px; border-radius: 12px; border: 1px solid #334155; z-index: 99999;
    }
    
    /* Parlayan Premium Oyun Başlatma Butonu CSS */
    .launch-game-btn {
        display: inline-block;
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        color: white !important;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 16px 32px;
        border-radius: 14px;
        text-decoration: none !important;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        margin: 20px 0;
        border: 1px solid #22d3ee;
    }
    .launch-game-btn:hover {
        transform: translateY(-4px);
        box-shadow: 0 0 35px rgba(59, 130, 246, 0.8);
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. DATA MANAGEMENT & SECURE HARDWARE PROTOCOLS
# =====================================================================
ECONOMY_FILE = "sazan_v112_economy.json"
INVENTORY_FILE = "sazan_v112_inventory.json"
STOCKS_FILE = "sazan_v112_stocks.json"
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
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return default_structure
        return default_structure

    @staticmethod
    def save_json(file_path, data):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            st.error(f"Kritik Veri Ambarı Yazma Hatası: {e}")

def get_device_fingerprint():
    try:
        headers = st.context.headers
        user_agent = headers.get("User-Agent", "")
        accept_lang = headers.get("Accept-Language", "")
        return hashlib.sha256(f"{user_agent}_{accept_lang}".encode()).hexdigest()
    except Exception:
        return "default_secure_aquarium_device_v112"

# =====================================================================
# 3. ADVANCED ECONOMY ENGINE, BANKING & DEBT SYSTEMS
# =====================================================================
class SazanBank:
    @staticmethod
    def get_account(u):
        db = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
        if u not in db:
            db[u] = {
                "coin": 1500, "bank_deposit": 0, "level": 1, "exp": 0, 
                "last_claim": time.time(), "rigs": 0, "last_mining": time.time(),
                "debt": 0, "credit_score": 500, "last_debt_check": time.time(),
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
            acc["exp"] += amount * 5
            acc["credit_score"] = min(1000, acc.get("credit_score", 500) + int(amount * 0.05))
            if acc["exp"] >= (acc["level"] * 250):
                acc["level"] += 1
                acc["exp"] = 0
                st.toast(f"👑 SEVİYE ATLANDI: Kuantum Kademe {acc['level']} Yetkisi Tanımlandı!")
        SazanBank.update_account(u, acc)

    @staticmethod
    def process_interest(u):
        acc = SazanBank.get_account(u)
        now = time.time()
        elapsed = now - acc.get("last_claim", now)
        if elapsed > 30 and acc["bank_deposit"] > 0:
            periods = int(elapsed / 30)
            rate = 0.03 if acc.get("level", 1) >= 5 else 0.018
            interest = int(acc["bank_deposit"] * rate * periods)
            if interest > 0:
                acc["bank_deposit"] += interest
                acc["last_claim"] = now
                SazanBank.update_account(u, acc)
                st.toast(f"📈 Kurumsal Faiz Dağıtımı: +{interest} SZNC likidite eklendi.")

class SazanNasdaq:
    @staticmethod
    def get_market_prices():
        stocks = KurumsalVeriAmbarı.load_json(STOCKS_FILE, {
            "SZN": 150.0, "BALIK": 60.0, "KRAK": 920.0, "CANAI": 7500.0, "QUANT": 320.0
        })
        for key in stocks.keys():
            change_percent = random.uniform(-0.18, 0.22)
            stocks[key] = max(1.5, round(stocks[key] * (1 + change_percent), 2))
        KurumsalVeriAmbarı.save_json(STOCKS_FILE, stocks)
        return stocks

# =====================================================================
# 4. EXPANDED RPG ARENA & BOSS COMBAT SYSTEMS
# =====================================================================
DUNGEON_LORE = {
    "monsters": [
        {"name": "Neon Hidra Matrix", "hp": 70, "atk": 12, "reward": 60, "type": "normal"},
        {"name": "Siber Vatoz Alpha X", "hp": 100, "atk": 20, "reward": 100, "type": "normal"},
        {"name": "MEGABYTE LEVIATHAN [BOSS]", "hp": 600, "atk": 75, "reward": 1200, "type": "boss"}
    ],
    "shop_items": {
        "Siber Zıpkın v2": {"cost": 150, "damage": 35, "type": "weapon"},
        "Lazer Kuantum Trident": {"cost": 600, "damage": 90, "type": "weapon"},
        "Can Muhammed İmparatorluk Plazma Silahı": {"cost": 12000, "damage": 1250, "type": "weapon"}
    }
}

class SazanInventory:
    @staticmethod
    def get_inventory(u):
        db = KurumsalVeriAmbarı.load_json(INVENTORY_FILE, {})
        if u not in db:
            db[u] = {
                "weapon": "Paslı Demir Kanca", "damage": 15, "potions": 4, 
                "hp": 150, "max_hp": 150, "shield": 0, "max_shield": 100, "shares": {}
            }
            KurumsalVeriAmbarı.save_json(INVENTORY_FILE, db)
        return db[u]

    @staticmethod
    def save_inventory(u, data):
        db = KurumsalVeriAmbarı.load_json(INVENTORY_FILE, {})
        db[u] = data
        KurumsalVeriAmbarı.save_json(INVENTORY_FILE, db)

# =====================================================================
# 5. ELITE QUANTUM HTML5 GAME ARCHITECT ENGINE (750 - 50,000 LINES)
# =====================================================================
if "GROQ_API_KEY" not in st.secrets:
    st.error("Kritik Sistem Ayar Hatası: GROQ_API_KEY enjeksiyonu başarısız!")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

class SazanAIConception:
    @staticmethod
    def query_agent(prompt, history, target_lang):
        if any(k in prompt.lower() for k in ["can muhammed çukur", "yapımcın kim", "yapımcısı"]):
            return f"Mutlak baş mimarım, kurucum ve dijital sistem mühendisim Can Muhammed Çukur'dur. Bu siber evrenin her satırını o tasarladı. [Dil: {target_lang}]"
        
        # Sıkılaştırılmış ve Zorunlu Kılınmış Büyük Ölçekli Oyun Üretim Protokolü
        sys_prompt = (
            "Sen dünyanın en gelişmiş, vizyoner ve kusursuz HTML5 Oyun Mimarı ve Baş Sistem Mühendisisin. "
            "Görevin, kullanıcının isteklerini tam olarak analiz etmek ve tek bir HTML dosyası içinde çalışan devasa, "
            "profesyonel bir oyun inşa etmektir. Senden yeni bir oyun istendiğinde ya da mevcut bir oyuna özellik eklemen istendiğinde; "
            "bunu en ince detayına kadar düşünülmüş mekaniklerle, gelişmiş CSS animasyon ve tasarımlarıyla, "
            "derinlemesine yazılmış JavaScript (ES6+) algoritmalarıyla yapmalısın. "
            "KOD YAPISI SON DERECE BÜYÜK ÖLÇEKLİ, UZUN VE DETAYLI OLMALIDIR (Maksimum 50.000, minimum 750 satır mantığında, zengin ve prodüksiyon kalitesinde). "
            "Asla kısaltma yapma, hiçbir fonksiyonu veya CSS kuralını 'buraları siz doldurun' diyerek yarım bırakma. "
            "Yazdığın tüm HTML kodunu KESİNLİKLE sadece ve sadece tek bir ```html ... ``` kod bloğu içerisine al. "
            "Oyun dışındaki analizlerini, tebriklerini ve geliştirici notlarını ise kesinlikle şu dilde yap: " + target_lang
        )
        
        messages = [{"role": "system", "content": sys_prompt}]
        # Son 10 sohbet adımını hafıza olarak göndererek oyunu sürekli üst üste geliştirebilmesini sağlıyoruz
        for m in history[-10:]:
            messages.append({"role": m["role"], "content": m["content"]})
        messages.append({"role": "user", "content": prompt})
        
        try:
            res = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.25
            )
            return res.choices[0].message.content
        except Exception as e:
            return f"Oyun Laboratuvarı İletişim Hatası: {e}"

# =====================================================================
# 6. SYSTEM INITIALIZATION & STATE ENFORCER
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
        "market_prices": SazanNasdaq.get_market_prices(), "last_market_update": time.time()
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

global_state_enforcer()

if "username" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color:#38bdf8; margin-top:60px;'>🐟 SAZAN AI OVERLORD OVERRIDE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#64748b; font-weight:bold;'>🛡️ QUANTUM GAME SANDBOX DISK ACTIVE (v113.0)</p>", unsafe_allow_html=True)
    st.markdown("<div style='max-width: 480px; margin: 0 auto; background: #090f21; padding: 25px; border-radius: 16px; border: 1px solid #1e293b;'>", unsafe_allow_html=True)
    
    identity = st.text_input("Kullanıcı Kimlik Doğrulama Adı:", max_chars=15, key="unique_login_gate")
    if st.button("Güvenli Oturumu Başlat", use_container_width=True):
        username_clean = identity.strip()
        if username_clean:
            db = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
            current_device = get_device_fingerprint()
            if username_clean in db:
                locked_device = db[username_clean].get("device_lock")
                if locked_device and locked_device != current_device:
                    st.error("🚨 ERİŞİM ENGELLENDİ: Bu hesap başka bir siber donanıma kilitlidir!")
                    st.stop()
                else:
                    db[username_clean]["device_lock"] = current_device
                    KurumsalVeriAmbarı.save_json(ECONOMY_FILE, db)
                    st.session_state.username = username_clean
                    st.rerun()
            else:
                st.session_state.username = username_clean
                SazanBank.get_account(username_clean)
                st.success("🎉 Başarılı: Hesap doğrulandı!")
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
# 7. STUDIO WORKSPACE SIDEBAR
# =====================================================================
with st.sidebar:
    st.markdown(f"<h3 style='color:#38bdf8; text-align:center;'>🏢 Workspace: {user}</h3>", unsafe_allow_html=True)
    acc = SazanBank.get_account(user)
    st.caption("❖ Finansal Likidite Durumu")
    st.code(f"Bakiye: {acc['coin']} SZNC\nBorç: {acc.get('debt', 0)} SZNC\nKredi Skoru: {acc.get('credit_score', 500)}/1000\nKademe Seviyesi: Lvl {acc['level']}")
    st.divider()
    
    st.markdown("💬 **Oyun Proje Odaları**")
    if st.button("➕ Yeni Oyun Projesi Başlat", use_container_width=True, type="secondary"):
        st.session_state.chat_counter += 1
        new_id = f"Oyun Oturumu {st.session_state.chat_counter}"
        st.session_state.chat_sessions[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()
        
    st.markdown("<div style='max-height: 250px; overflow-y: auto; margin-top:10px;'>", unsafe_allow_html=True)
    for chat_name in reversed(list(st.session_state.chat_sessions.keys())):
        is_current = (chat_name == st.session_state.current_chat)
        bullet = "🎮" if is_current else "◇"
        if st.button(f"{bullet} {chat_name}", key=f"switch_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
            
    st.divider()
    if st.button("🗑️ Mevcut Akışı Sıfırla", use_container_width=True):
        st.session_state.chat_sessions[st.session_state.current_chat] = []
        st.rerun()

# =====================================================================
# 8. MAIN DISPLAY TERMINAL (CHATSTREAM & BASE64 INTERCEPTOR)
# =====================================================================
st.markdown(f"<p style='color:#64748b; font-size:0.9rem; font-weight:700; letter-spacing:1px;'>🛠️ AKTİF OYUN PROJE HATTI: {st.session_state.current_chat}</p>", unsafe_allow_html=True)

if st.session_state.admin_status:
    st.markdown("<div class='rpg-terminal-box'>", unsafe_allow_html=True)
    st.markdown("<h4>👑 ADMIN CONTROL CONSOLE</h4>", unsafe_allow_html=True)
    token = st.text_input("Root Kimlik Şifresi:", type="password")
    if token == SUPER_ADMIN_PASSWORD:
        st.success("Mutlak Root Yetkileri Aktive Edildi.")
        if st.button("💵 +250,000 SZNC Enjekte Et", use_container_width=True):
            SazanBank.modify_coin(user, 250000)
            st.success("Bakiye güncellendi!"); time.sleep(0.5); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.dungeon_status:
    st.markdown("<div class='rpg-terminal-box'>", unsafe_allow_html=True)
    st.write("⚔️ /// SİBER ARENA OPERASYONU AKTİF // ZEKA SAVAŞLARI /// ⚔️")
    p_inv = SazanInventory.get_inventory(user)
    
    if not st.session_state.current_dungeon_enemy:
        if st.button("Siber Radar Taraması Başlat (Düşman Ara) 🔱", use_container_width=True):
            st.session_state.current_dungeon_enemy = random.choice(DUNGEON_LORE["monsters"]).copy()
            st.rerun()
    else:
        en = st.session_state.current_dungeon_enemy
        st.write(f"⚠️ **Tehdit Unsuru:** {en['name']} (HP: {en['hp']} | ATK: {en['atk']})")
        if st.button("Optimum Hasar Saldırısı Başlat! ⚔️", use_container_width=True):
            en["hp"] -= p_inv["damage"]
            p_inv["hp"] -= int(en["atk"] * 0.85)
            if p_inv["hp"] <= 0:
                st.error("Zindandan elendiniz."); SazanBank.modify_coin(user, -100); p_inv["hp"] = p_inv["max_hp"]
                st.session_state.current_dungeon_enemy = None
            elif en["hp"] <= 0:
                st.success(f"🏆 Savaş Kazanıldı! Ganimet: +{en['reward']} SZNC")
                SazanBank.modify_coin(user, en['reward'])
                st.session_state.current_dungeon_enemy = None
            SazanInventory.save_inventory(user, p_inv)
            time.sleep(0.5); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

active_messages = st.session_state.chat_sessions[st.session_state.current_chat]

# Mesajları Ekrana Basarken HTML Kodlarını Yakala, Gizle ve Linke Dönüştür
for m in active_messages:
    with st.chat_message(m["role"]):
        content = m["content"]
        # HTML kod bloklarını regex ile tespit et (```html ... ```)
        html_blocks = re.findall(r'```html\s*(.*?)\s*```', content, re.DOTALL)
        
        if html_blocks:
            # Ham kodu metinden tamamen temizle, ekranda binlerce satır gözükmesin
            clean_text = re.sub(r'```html\s*(.*?)\s*```', '', content, flags=re.DOTALL)
            st.markdown(clean_text)
            
            # Kod bloğunu Base64'e dönüştürerek tarayıcının yeni sekmede açabileceği bağımsız bir URL yap
            game_code = html_blocks[0]
            b64_game = base64.b64encode(game_code.encode('utf-8')).decode('utf-8')
            game_url = f"data:text/html;base64,{b64_game}"
            
            # Premium Parlayan Butonu Kullanıcıya Sun
            st.markdown(f'<a href="{game_url}" target="_blank" class="launch-game-btn">🎮 Üretilen Oyunu Yeni Sekmede Tam Ekran Başlat</a>', unsafe_allow_html=True)
            
            with st.expander("🛠️ Geliştirici Ham Kaynak Kodları (Yedeklemek İçin)"):
                st.code(game_code, language="html")
        else:
            st.markdown(content)

# =====================================================================
# 9. INTEGRATED HUB SUB-PANELS & FINANCIAL BORSA (FIXED COUPLING)
# =====================================================================
if st.session_state.active_panel_tab == "plus":
    st.markdown("<div class='stock-market-box'>", unsafe_allow_html=True)
    t1, t2, t3, t4 = st.tabs(["🛒 Ekipman Deposu", "🏦 Kasa & Kredi Merkezi", "📊 Finansal Borsa", "⛏️ Kuantum Madencilik"])
    
    with t1:
        for item, d in DUNGEON_LORE["shop_items"].items():
            st.write(f"🔹 **{item}** — {d['cost']} SZNC")
            if st.button(f"Satın Al: {item}", key=f"buy_{item}"):
                u_acc = SazanBank.get_account(user)
                if u_acc["coin"] >= d["cost"]:
                    SazanBank.modify_coin(user, -d["cost"])
                    u_inv = SazanInventory.get_inventory(user)
                    if d["type"] == "weapon": u_inv["weapon"], u_inv["damage"] = item, d["damage"]
                    SazanInventory.save_inventory(user, u_inv)
                    st.success(f"{item} alındı."); time.sleep(0.5); st.rerun()
                    
    with t2:
        b_acc = SazanBank.get_account(user)
        st.write(f"Mevcut Borcunuz: **{b_acc.get('debt', 0)} SZNC**")
        
    with t3:
        prices = st.session_state.market_prices
        p_inv = SazanInventory.get_inventory(user)
        if "shares" not in p_inv: p_inv["shares"] = {}
        for ticker, val in prices.items():
            st.write(f"💹 **{ticker} Varlığı**: `{val} SZNC` (Senin Portföyün: {p_inv['shares'].get(ticker, 0)} Lot)")
            col_sh1, col_sh2 = st.columns(2)
            with col_sh1:
                if st.button(f"1 Lot Al: {ticker}", key=f"sh_buy_{ticker}"):
                    u_acc = SazanBank.get_account(user)
                    if u_acc["coin"] >= val:
                        SazanBank.modify_coin(user, -int(val))
                        p_inv["shares"][ticker] = p_inv["shares"].get(ticker, 0) + 1
                        SazanInventory.save_inventory(user, p_inv)
                        st.success("Portföy güncellendi."); time.sleep(0.5); st.rerun()
            with col_sh2:
                if st.button(f"1 Lot Sat: {ticker}", key=f"sh_sell_{ticker}"):
                    if p_inv["shares"].get(ticker, 0) > 0:
                        SazanBank.modify_coin(user, int(val))
                        p_inv["shares"][ticker] -= 1
                        SazanInventory.save_inventory(user, p_inv)
                        st.success("Satış yapıldı."); time.sleep(0.5); st.rerun()
                    
    with t4:
        st.write("Madencilik Modülü Stabil.")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 10. HUD CONTROLS (QUICK ACCESS MENU)
# =====================================================================
st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
hc1, hc2, _ = st.columns([1.5, 1.2, 7.3])
with hc1:
    if st.button("💼 Finans, Stüdyo & Maden", use_container_width=True):
        st.session_state.active_panel_tab = "plus" if st.session_state.active_panel_tab != "plus" else None
        st.rerun()
with hc2:
    if st.button("🛡️ Siber Arena (RPG)", use_container_width=True):
        st.session_state.dungeon_status = not st.session_state.dungeon_status
        st.rerun()

# =====================================================================
# 11. CONTINUOUS WORKSPACE ENGINE (GAME COMPILER CORE)
# =====================================================================
prompt = st.chat_input("Nasıl bir HTML5 oyunu tasarlamak istersin? Fikrini buraya yaz...")

if prompt:
    if prompt.strip() == "TURKEY SAZAN":
        st.session_state.admin_status = True
        st.rerun()

    # Kullanıcı promptunu hafızaya ekle
    active_messages.append({"role": "user", "content": prompt})
    
    with st.spinner("Sazan Kuantum Oyun Mimarı devasa kodları inşa ediyor... Lütfen bekleyin..."):
        cur_lang = st.session_state.get('active_lang_code', 'Türkçe 🇹🇷')
        
        # Yapay zekaya geçmiş hafızayı da ekleyerek sorguyu ilet
        ans = SazanAIConception.query_agent(prompt, active_messages, cur_lang)
        
        # Sonucu kaydet ve ekranı yenile
        active_messages.append({"role": "assistant", "content": ans})
        st.rerun()

# =====================================================================
# 12. DYNAMIC LANGUAGE SELECTION HUB
# =====================================================================
st.markdown("<div class='fixed-lang-hub'>", unsafe_allow_html=True)
sel_lang = st.selectbox("🌐 Çeviri:", list(DIL_MATRISI.keys()), key="lang_widget", label_visibility="collapsed")
st.session_state.active_lang_code = sel_lang
st.markdown("</div>", unsafe_allow_html=True)
