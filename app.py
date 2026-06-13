# ================================================================================
# ███████╗ █████╗ ███████╗ █████╗ ███╗  ██╗     ██████╗ ███████╗
# ██╔════╝██╔══██╗╚══███╔╝██╔══██╗████╗  ██║     ██╔═══██╗██╔════╝
# ███████╗███████║  ███╔╝ ███████║██╔██╗ ██║     ██║   ██║███████╗
# ╚════██║██╔══██║ ███╔╝  ██╔══██║██║╚██╗██║     ██║   ██║╚════██║
# ███████║██║  ██║███████╗██║  ██║██║ ╚████║     ╚██████╔╝███████║
# ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝      ╚═════╝ ╚══════╝
#        👑 SAZAN AI ENTERPRISE STUDIO - OVERLORD SUPREME v112.5 👑
#        DEVELOPED BY: CAN MUHAMMED ÇUKUR - THE MUTLAK ARCHITECT
#        PATCH NOTE: SYNTAX & INTERCEPTOR HOTFIX APPLIED
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
import urllib.parse
import re
from groq import Groq
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
from datetime import datetime
import hashlib

# =====================================================================
# 1. CORE SYSTEM CONFIGURATION & PREMIUM STUDIO UI/UX CSS
# =====================================================================
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="Sazan AI Enterprise Overlord v112.5",
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
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stChatMessage:hover {
        border-color: #38bdf8 !important;
        box-shadow: 0 12px 25px -3px rgba(56, 189, 248, 0.15);
    }
    
    code, pre {
        font-family: 'Fira Code', monospace !important;
        background-color: #010307 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 14px !important;
    }
    
    .stChatInputContainer {
        border: 1px solid #334155 !important;
        border-radius: 28px !important;
        background-color: #0e1626 !important;
        padding: 8px 16px !important;
        box-shadow: 0 25px 35px -10px rgba(0, 0, 0, 0.6);
    }
    .stChatInputContainer:focus-within {
        border-color: #38bdf8 !important;
    }
    
    .rpg-terminal-box {
        background-color: #010307; color: #10b981; font-family: 'Fira Code', monospace;
        padding: 22px; border-radius: 14px; border: 1px solid #10b981;
        box-shadow: 0 6px 25px rgba(16, 185, 129, 0.1); margin: 18px 0;
    }
    
    .admin-god-box {
        background: linear-gradient(135deg, #05070f 0%, #1e1b4b 100%);
        border: 1px solid #ef4444; padding: 25px; border-radius: 14px;
        box-shadow: 0px 8px 30px rgba(239, 68, 68, 0.15); margin-bottom: 25px;
    }
    
    .stock-market-box {
        background: #090f21; border: 1px solid #1e293b; padding: 22px;
        border-radius: 16px; box-shadow: 0px 6px 30px rgba(0,0,0,0.5);
    }
    
    .mining-card {
        background: linear-gradient(135deg, #0f172a 0%, #0369a1 100%);
        border: 1px solid #0284c7; padding: 20px; border-radius: 12px; margin: 10px 0;
    }
    
    .fixed-lang-hub {
        position: fixed; bottom: 20px; right: 20px; background: #0e1626;
        padding: 5px 10px; border-radius: 12px; border: 1px solid #334155; z-index: 99999;
    }
    
    button { border-radius: 12px !important; font-weight: 600 !important; transition: all 0.2s ease !important; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. DATA MANAGEMENT & SECURE HARDWARE PROTOCOLS
# =====================================================================
ECONOMY_FILE = "sazan_v112_economy.json"
INVENTORY_FILE = "sazan_v112_inventory.json"
STOCKS_FILE = "sazan_v112_stocks.json"
SYSTEM_LOGS_FILE = "sazan_v112_logs.json"
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

    @staticmethod
    def log_event(u, event_type, details):
        logs = KurumsalVeriAmbarı.load_json(SYSTEM_LOGS_FILE, [])
        logs.append({
            "timestamp": time.time(),
            "username": u,
            "type": event_type,
            "details": details
        })
        KurumsalVeriAmbarı.save_json(SYSTEM_LOGS_FILE, logs[-1000:])

def get_device_fingerprint():
    try:
        headers = st.context.headers
        user_agent = headers.get("User-Agent", "")
        accept_lang = headers.get("Accept-Language", "")
        fingerprint_raw = f"{user_agent}_{accept_lang}"
        return hashlib.sha256(fingerprint_raw.encode()).hexdigest()
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
                KurumsalVeriAmbarı.log_event(u, "FAIZ_KAZANCI", f"+{interest} SZNC faiz alındı.")
        
        debt_elapsed = now - acc.get("last_debt_check", now)
        if debt_elapsed > 60 and acc.get("debt", 0) > 0:
            debt_periods = int(debt_elapsed / 60)
            acc["debt"] = int(acc["debt"] * ((1 + 0.05) ** debt_periods))
            acc["credit_score"] = max(100, acc.get("credit_score", 500) - (10 * debt_periods))
            acc["last_debt_check"] = now
            SazanBank.update_account(u, acc)
            st.toast("⚠️ Faiz Uyarısı: Ödenmemiş SZNC borcunuza %5 faiz eklendi!")

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
        {"name": "Kuantum Mekanik Köpekbalığı", "hp": 180, "atk": 32, "reward": 250, "type": "normal"},
        {"name": "MEGABYTE LEVIATHAN [BOSS]", "hp": 600, "atk": 75, "reward": 1200, "type": "boss"},
        {"name": "MUTANT KRAKEN ARCHITECT [ULTIMATE BOSS]", "hp": 2000, "atk": 210, "reward": 5000, "type": "boss"}
    ],
    "shop_items": {
        "Siber Zıpkın v2": {"cost": 150, "damage": 35, "type": "weapon"},
        "Lazer Kuantum Trident": {"cost": 600, "damage": 90, "type": "weapon"},
        "Can Muhammed İmparatorluk Plazma Silahı": {"cost": 12000, "damage": 1250, "type": "weapon"},
        "Nano Med-Kit Pro 🧪": {"cost": 75, "heal": 160, "type": "potion"},
        "Kalkan Jeneratörü 🛡️": {"cost": 400, "shield": 100, "type": "shield"}
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
# 5. ELITE HIGH-LEVEL MULTI-AI TEXT GENERATION ENGINE
# =====================================================================
if "GROQ_API_KEY" not in st.secrets:
    st.error("Kritik Sistem Ayar Hatası: GROQ_API_KEY enjeksiyonu başarısız!")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

class SazanAIConception:
    @staticmethod
    def query_agent(prompt, agent_role, target_lang):
        if any(k in prompt.lower() for k in ["can muhammed çukur", "yapımcın kim", "yapımcısı"]):
            return f"Mutlak baş mimarım, kurucum ve dijital sistem mühendisim Can Muhammed Çukur'dur. Bu siber evrenin her satırını o tasarladı. [Dil: {target_lang}]"
        
        personas = {
            "Bilge Sazan": (
                "Sen MIT ve Stanford bilgisayar bilimlerinden birincilikle mezun, dünyanın en deneyimli, "
                "en zeki dahi yazılım mühendisi ve baş sistem mimarısın. Kullanıcı senden kod, "
                "yazılım mimarisi ya da teknik analiz istediğinde; en üst segment kurumsal standartlarda, "
                "SOLID prensiplerine tam uygun, detaylı yorum satırları içeren eksiksiz TAM kod blokları yazacaksın."
            ),
            "Kripto Sazan": "Sen küresel kuantum borsa ağları, DeFi algoritmaları ve arbitraj sistemleri uzmanı dahi bir finans balinasısın.",
            "Çılgın Sazan": "Sen en katı devlet sunucularına sızabilen, sınırları zorlayan, dahi bir siber güvenlik uzmanı ve beyaz şapkalı hacker balıksın.",
            "Siber Gladyatör": "Sen siber savaş taktikleri ve yüksek yoğunluklu ağ savunmaları üzerine uzmanlaşmış kıdemli bir savunma yapay zekasısın.",
            "Matrix Sefi": "Sen simülasyon kod tabanını doğrudan Assembly, C ve Rust ile manipüle edebilen mutlak çekirdek mimari dehasısın."
        }
        
        sys_prompt = f"{personas.get(agent_role, 'Bilge Sazan')} Cevabını kesinlikle ve tamamen şu dilde vermelisin: {target_lang}. Asla bu dilin dışına çıkma."
        try:
            res = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}],
                temperature=0.2
            )
            return res.choices[0].message.content
        except Exception as e:
            return f"Yapay Zeka Core Bağlantı Kesintisi: {e}"

    @staticmethod
    def run_council_debate(prompt, target_lang):
        log = []
        log.append(f"🔮 **Baş Mimarlık (Bilge Sazan):**\n{SazanAIConception.query_agent(prompt, 'Bilge Sazan', target_lang)}")
        log.append(f"📈 **DeFi Kuantum Finans (Kripto Sazan):**\n{SazanAIConception.query_agent(prompt, 'Kripto Sazan', target_lang)}")
        log.append(f"🛠️ **Siber Defans & Ağ Güvenliği (Çılgın Sazan):**\n{SazanAIConception.query_agent(prompt, 'Çılgın Sazan', target_lang)}")
        return "\n\n---\n\n".join(log)

# =====================================================================
# 6. ULTRA-NET QUANTUM ART ENGINE (MIDJOURNEY-LEVEL PROMPT OPTIMIZER)
# =====================================================================
class SazanStudioArt:
    @staticmethod
    def optimize_prompt_with_ai(original_prompt):
        try:
            sys_directive = (
                "You are an expert AI Art Prompt Engineer specializing in advanced image syntax. "
                "Convert the user's input into an incredibly detailed, ultra-high-quality, vivid, stunning "
                "English image generation prompt. Output ONLY the final English optimized prompt."
            )
            res = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_directive}, {"role": "user", "content": original_prompt}],
                temperature=0.55,
                max_tokens=250
            )
            optimized_text = res.choices[0].message.content.strip()
            if len(optimized_text) < 5 or "sorry" in optimized_text.lower():
                return f"{original_prompt}, photorealistic, ultra detailed, 8k resolution, sharp focus, cinematic lighting"
            return optimized_text
        except Exception:
            return f"{original_prompt}, stunning visuals, highly detailed, sharp focus, 8k resolution"

    @staticmethod
    def generate_image_url(prompt, width=1280, height=720, enhance=True, seed=None):
        optimized_prompt = SazanStudioArt.optimize_prompt_with_ai(prompt)
        if not seed:
            seed = random.randint(111111, 999999)
        clean_prompt = optimized_prompt.replace("/", " ").replace("\\", " ").replace("\"", "").replace("'", "").strip()
        encoded_prompt = urllib.parse.quote(clean_prompt)
        enhance_str = "true" if enhance else "false"
        return f"https://image.pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&seed={seed}&enhance={enhance_str}&nologo=true"

# =====================================================================
# 7. REGEX-BASED NATURAL LANGUAGE IMAGE INTERCEPTOR (CRITICAL HOTFIX)
# =====================================================================
def detect_and_intercept_image_request(user_input):
    """Gelişmiş RegEx dil matrisi sayesinde kullanıcının konuşma dilindeki 
    görsel üretim isteklerini tam isabetle yakalar."""
    patterns = [
        r"(çiz|yap|oluştur|tasarla|üret|resmet|görselleştir|fotoğrafla|boya|çiziver|resmediver)\b.*\b(resim|görsel|fotoğraf|çizim|grafik|sahne|manzara|karakter|logo|duvar kağıdı)",
        r"(resim|görsel|fotoğraf|çizim|grafik|sahne|manzara|karakter|logo|duvar kağıdı)\b.*\b(çiz|yap|oluştur|tasarla|üret|resmet|görselleştir|fotoğrafla|boya|çiziver|resmediver)",
        r"\b(resmini çiz|görselini yap|fotoğrafını oluştur|çiziver|resmediver|resmini yap|görsel yap|resim çiz|görsel çiz|görseli oluştur|görsel oluştur)\b",
        r"\b(görselleştir|resmet)\b"
    ]
    
    clean_input = user_input.lower().strip()
    is_image = any(re.search(p, clean_input) for p in patterns)
    
    if is_image:
        clean_prompt = user_input
        stop_phrases = [
            "resmini çiz", "resmi çiz", "görselini yap", "görsel yap", "fotoğrafını oluştur", 
            "çizermisin", "çizer misin", "fotoğrafını yap", "çiz", "yap", "görselleştir", "resmet",
            "resim çiz", "görsel çiz", "bana", "bir tane", "şunun", "resmini", "görselini",
            "görseli oluştur", "görsel oluştur"
        ]
        for phrase in stop_phrases:
            clean_prompt = re.sub(r'\b' + re.escape(phrase) + r'\b', '', clean_prompt, flags=re.IGNORECASE)
        return True, clean_prompt.strip()
    return False, None

# =====================================================================
# 8. SYSTEM INITIALIZATION & STATE ENFORCER
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

if "username" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color:#38bdf8; margin-top:60px;'>🐟 SAZAN AI OVERLORD OVERRIDE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#64748b; font-weight:bold;'>🛡️ HARDWARE ENCRYPTION PROTOCOL ACTIVE (v112.5)</p>", unsafe_allow_html=True)
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
# 9. STUDIO WORKSPACE SIDEBAR
# =====================================================================
with st.sidebar:
    st.markdown(f"<h3 style='color:#38bdf8; text-align:center;'>🏢 Workspace: {user}</h3>", unsafe_allow_html=True)
    acc = SazanBank.get_account(user)
    st.caption("❖ Finansal Likidite Durumu")
    st.code(f"Bakiye: {acc['coin']} SZNC\nBorç: {acc.get('debt', 0)} SZNC\nKredi Skoru: {acc.get('credit_score', 500)}/1000\nKademe Seviyesi: Lvl {acc['level']}")
    st.divider()
    
    st.markdown("💬 **Sohbet Alanları**")
    if st.button("➕ Yeni Sohbet Odası Aç", use_container_width=True, type="secondary"):
        st.session_state.chat_counter += 1
        new_id = f"Sohbet Oturumu {st.session_state.chat_counter}"
        st.session_state.chat_sessions[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()
        
    st.markdown("<div style='max-height: 250px; overflow-y: auto; margin-top:10px;'>", unsafe_allow_html=True)
    for chat_name in reversed(list(st.session_state.chat_sessions.keys())):
        is_current = (chat_name == st.session_state.current_chat)
        bullet = "🔮" if is_current else "◇"
        if st.button(f"{bullet} {chat_name}", key=f"switch_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
            
    st.divider()
    st.session_state.council_activation = st.toggle("👥 3'lü Kıdemli Konsey Modu", value=st.session_state.council_activation)
    if st.button("🗑️ Mevcut Akışı Sıfırla", use_container_width=True):
        st.session_state.chat_sessions[st.session_state.current_chat] = []
        st.rerun()

# =====================================================================
# 10. MAIN DISPLAY TERMINAL (CHATSTREAM & GALLERY RENDER)
# =====================================================================
st.markdown(f"<p style='color:#64748b; font-size:0.9rem; font-weight:700; letter-spacing:1px;'>🛠️ AKTİF PROJE HATI: {st.session_state.current_chat}</p>", unsafe_allow_html=True)

if st.session_state.admin_status:
    st.markdown("<div class='admin-god-box'>", unsafe_allow_html=True)
    st.markdown("<h4>👑 ADMIN ROOT OVERRIDE CONTROL CONSOLE</h4>", unsafe_allow_html=True)
    token = st.text_input("Root Kimlik Şifresi:", type="password")
    if token == SUPER_ADMIN_PASSWORD:
        st.success("Mutlak Root Yetkileri Aktive Edildi.")
        col_adm1, col_adm2 = st.columns(2)
        with col_adm1:
            if st.button("💵 +250,000 SZNC Enjekte Et", use_container_width=True):
                SazanBank.modify_coin(user, 250000)
                st.success("Bakiye güncellendi!"); time.sleep(0.5); st.rerun()
    if st.button("❌ Paneli Kapat", use_container_width=True):
        st.session_state.admin_status = False
        st.rerun()
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
        c_rpg1, c_rpg2 = st.columns(2)
        with c_rpg1:
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

for m in active_messages:
    with st.chat_message(m["role"]):
        if m.get("type") == "image":
            st.markdown(f"🎨 **Sazan Ultra-Net Sanat Modülü Başarıyla Çizdi:**")
            st.markdown(f"> **Senin Hayalin:** *{m.get('original_prompt_turkish', 'Bilinmeyen İstem')}*")
            st.image(m["content"], use_container_width=True)
        else:
            st.markdown(m["content"])

# =====================================================================
# 11. INTEGRATED HUB SUB-PANELS & FINANCIAL BORSA (FIXED COUPLING)
# =====================================================================
if st.session_state.active_panel_tab == "plus":
    st.markdown("<div class='stock-market-box'>", unsafe_allow_html=True)
    t1, t2, t3, t4, t5 = st.tabs(["🛒 Ekipman Deposu", "🏦 Kasa & Kredi Merkezi", "📊 Finansal Borsa", "🎨 Yapay Zeka Görsel Stüdyosu", "⛏️ Kuantum Madencilik"])
    
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
                        # CRITICAL HOTFIX: Tırnak hatası düzeltildi!
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
        art_prompt = st.text_area("Çizmek istediğin tasarımı buraya yaz:", key="area_art")
        if st.button("Sanat Eserini İşle ⚡", use_container_width=True):
            u_acc = SazanBank.get_account(user)
            if u_acc["coin"] >= 20 and art_prompt.strip():
                generated_url = SazanStudioArt.generate_image_url(art_prompt, 1280, 720, True)
                SazanBank.modify_coin(user, -20)
                active_messages.append({"role": "user", "content": f"🎨 [Görsel İstemi]: {art_prompt}"})
                active_messages.append({"role": "assistant", "type": "image", "content": generated_url, "original_prompt_turkish": art_prompt})
                st.success("Çizildi!"); time.sleep(0.5); st.rerun()
                
    with t5:
        st.write("Madencilik Modülü Stabil.")
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.active_panel_tab == "audio":
    st.write("Ses Kayıt Özelliği Hazır.")

# =====================================================================
# 12. HUD CONTROLS (QUICK ACCESS MENU)
# =====================================================================
st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
hc1, hc2, hc3, _ = st.columns([1.5, 1.2, 1.2, 6.1])
with hc1:
    if st.button("💼 Finans, Stüdyo & Maden", use_container_width=True):
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
# 13. CONTINUOUS WORKSPACE ENGINE (HOTFIXED INTERCEPTOR)
# =====================================================================
prompt = st.chat_input("Yazılım kodu isteyin, soru sorun veya doğal dilde hayalinizi yazın...")

if prompt:
    if prompt.strip() == "TURKEY SAZAN":
        st.session_state.admin_status = True
        st.rerun()

    # Çizim İsteği Kontrolü
    is_image_request, art_hayal_istemi = detect_and_intercept_image_request(prompt)
    
    if is_image_request:
        u_acc = SazanBank.get_account(user)
        if u_acc["coin"] < 20:
            active_messages.append({"role": "user", "content": prompt})
            active_messages.append({"role": "assistant", "content": "❌ Görsel üretimi için cüzdanınızda yeterli SZNC bulunmuyor (Gereken: 20 SZNC)."})
            st.rerun()
        else:
            with st.spinner("Sazan Sanat Modülü render alıyor..."):
                generated_url = SazanStudioArt.generate_image_url(art_hayal_istemi, 1280, 720, True)
                SazanBank.modify_coin(user, -20)
                active_messages.append({"role": "user", "content": prompt})
                active_messages.append({"role": "assistant", "type": "image", "content": generated_url, "original_prompt_turkish": art_hayal_istemi})
                st.rerun()
    else:
        active_messages.append({"role": "user", "content": prompt})
        cur_lang = st.session_state.get('active_lang_code', 'Türkçe 🇹🇷')
        ans = SazanAIConception.query_agent(prompt, "Bilge Sazan", cur_lang)
        active_messages.append({"role": "assistant", "content": ans})
        st.rerun()

# =====================================================================
# 14. DYNAMIC LANGUAGE SELECTION HUB
# =====================================================================
st.markdown("<div class='fixed-lang-hub'>", unsafe_allow_html=True)
sel_lang = st.selectbox("🌐 Çeviri:", list(DIL_MATRISI.keys()), key="lang_widget", label_visibility="collapsed")
st.session_state.active_lang_code = sel_lang
st.markdown("</div>", unsafe_allow_html=True)
