# ================================================================================
# ███████╗ █████╗ ███████╗ █████╗ ███╗  ██╗     ██████╗ ███████╗
# ██╔════╝██╔══██╗╚══███╔╝██╔══██╗████╗  ██║     ██╔═══██╗██╔════╝
# ███████╗███████║  ███╔╝ ███████║██╔██╗ ██║     ██║   ██║███████╗
# ╚════██║██╔══██║ ███╔╝  ██╔══██║██║╚██╗██║     ██║   ██║╚════██║
# ███████║██║  ██║███████╗██║  ██║██║ ╚████║     ╚██████╔╝███████║
# ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝      ╚═════╝ ╚══════╝
#        👑 SAZAN AI ENTERPRISE STUDIO - GAME ENGINE SUPREME v116.0 👑
#        DEVELOPED BY: CAN MUHAMMED ÇUKUR - THE MUTLAK ARCHITECT
#        PATCH NOTE: KESİNTİSİZ KOD ÜRETİMİ + MODEL SEÇİMİ + GÖRSELDEN 3D BASKI (STL) ATÖLYESİ
# ================================================================================

import streamlit as st
import json
import os
import time
import random
import re
import base64
import uuid
import hashlib
import io
import urllib.request
import urllib.parse
from datetime import datetime, date

import numpy as np
from PIL import Image
from stl import mesh as stl_mesh

from groq import Groq

# =====================================================================
# 1. CORE SYSTEM CONFIGURATION & PREMIUM STUDIO UI/UX CSS
# =====================================================================
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="Sazan AI Enterprise Game Overlord v116.0",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state,
)

st.markdown(
    """
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
        padding: 22px; border-radius: 14px; border: 1px solid #10b981; margin-bottom: 18px;
    }

    .stock-market-box {
        background: #090f21; border: 1px solid #1e293b; padding: 22px;
        border-radius: 16px; margin-bottom: 18px;
    }

    .library-card {
        background: #090f21; border: 1px solid #1e293b; padding: 16px 20px;
        border-radius: 14px; margin-bottom: 12px;
    }

    .fixed-lang-hub {
        position: fixed; bottom: 20px; right: 20px; background: #0e1626;
        padding: 5px 10px; border-radius: 12px; border: 1px solid #334155; z-index: 99999;
    }

    .launch-game-btn {
        display: inline-block;
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        color: white !important;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 14px 28px;
        border-radius: 14px;
        text-decoration: none !important;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        margin: 14px 6px 4px 0;
        border: 1px solid #22d3ee;
    }
    .launch-game-btn:hover {
        transform: translateY(-4px);
        box-shadow: 0 0 35px rgba(59, 130, 246, 0.8);
        color: #ffffff !important;
    }

    .badge {
        display: inline-block; padding: 3px 10px; border-radius: 8px;
        background: #0e1626; border: 1px solid #334155; font-size: 0.78rem;
        color: #38bdf8; margin-right: 6px;
    }

    /* --- v115 COOL UI UPGRADE --- */
    @keyframes sazanGradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes sazanGlowPulse {
        0%, 100% { box-shadow: 0 0 18px rgba(6, 182, 212, 0.35); }
        50% { box-shadow: 0 0 32px rgba(59, 130, 246, 0.65); }
    }
    @keyframes sazanFadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .sazan-hero {
        text-align: center;
        padding: 22px 10px 14px 10px;
        animation: sazanFadeInUp 0.5s ease-out;
    }
    .sazan-hero h1 {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(90deg, #22d3ee, #3b82f6, #a855f7, #22d3ee);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: sazanGradientShift 6s ease infinite;
        letter-spacing: 1px;
    }
    .sazan-hero p {
        color: #94a3b8;
        font-size: 0.92rem;
        margin-top: 6px;
        font-weight: 500;
    }

    .print-studio-box {
        background: linear-gradient(160deg, #0b1120 0%, #090f21 100%);
        border: 1px solid #22d3ee;
        padding: 24px;
        border-radius: 18px;
        margin-bottom: 18px;
        animation: sazanGlowPulse 3.5s ease-in-out infinite, sazanFadeInUp 0.4s ease-out;
    }

    /* Streamlit butonlarına hover parlaması ve hafif kalkma efekti */
    .stButton > button {
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border-radius: 12px !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px -4px rgba(6, 182, 212, 0.45) !important;
        border-color: #22d3ee !important;
    }

    /* Dosya yükleme kutusuna vurgulu, dikkat çekici bir çerçeve */
    [data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #22d3ee !important;
        background-color: #071019 !important;
        border-radius: 14px !important;
    }

    .library-card, .stock-market-box, .rpg-terminal-box, .print-studio-box {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .library-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 22px -6px rgba(56, 189, 248, 0.35);
    }

    /* --- v117 KİMLİK DOĞRULAMA & COOL UI UPGRADE --- */
    [data-testid="stTextInput"] input {
        background-color: #0e1626 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
        padding: 10px 14px !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #22d3ee !important;
        box-shadow: 0 0 14px rgba(34, 211, 238, 0.4) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #0e1626;
        border-radius: 12px 12px 0 0;
        padding: 10px 22px;
        color: #94a3b8;
        font-weight: 600;
        border: 1px solid #1e293b;
    }
    .stTabs [aria-selected="true"] {
        background-color: #10233a !important;
        color: #22d3ee !important;
        border-color: #22d3ee !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 22px !important;
        border-color: #22d3ee !important;
        background: linear-gradient(160deg, #0b1120 0%, #090f21 100%) !important;
        box-shadow: 0 0 45px rgba(34, 211, 238, 0.16);
        animation: sazanFadeInUp 0.5s ease-out;
    }

    [data-testid="stWidgetLabel"] p {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }

    .auth-logo-ring {
        width: 78px; height: 78px; margin: 0 auto 6px auto;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 2.1rem;
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 60%, #a855f7 100%);
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.55);
        animation: sazanGlowPulse 3s ease-in-out infinite;
    }
    .auth-caption {
        text-align: center; color: #64748b; font-size: 0.85rem;
        margin-bottom: 18px; font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# 2. VERİ DEPOLARI & GÜVENLİ DONANIM PARMAK İZİ
# =====================================================================
DATA_DIR = "sazan_data"
os.makedirs(DATA_DIR, exist_ok=True)

ECONOMY_FILE = os.path.join(DATA_DIR, "sazan_economy.json")
INVENTORY_FILE = os.path.join(DATA_DIR, "sazan_inventory.json")
STOCKS_FILE = os.path.join(DATA_DIR, "sazan_stocks.json")
GAMES_LIBRARY_FILE = os.path.join(DATA_DIR, "sazan_games_library.json")
IMAGE_GALLERY_FILE = os.path.join(DATA_DIR, "sazan_image_gallery.json")
AUTH_FILE = os.path.join(DATA_DIR, "sazan_auth.json")

# ÖNEMLİ: Admin şifresi artık kaynak kodda açık yazmıyor.
# GitHub'a yüklemeden önce bunu .streamlit/secrets.toml içine ekleyin:
#   ADMIN_PASSWORD = "sizin-gizli-sifreniz"
SUPER_ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "lutfen-secrets-toml-icinde-degistir")

DIL_MATRISI = {
    "Türkçe 🇹🇷": "tr",
    "English 🇺🇸": "en",
    "Deutsch 🇩🇪": "de",
    "Français 🇫🇷": "fr",
    "Русский 🇷🇺": "ru",
    "日本語 🇯🇵": "ja",
}

GAME_TEMPLATES = [
    "🏎️ Basit ama akıcı bir arabalı yarış oyunu yap, engellerden kaçılsın",
    "🧩 Renk eşleştirme bulmaca oyunu, zamana karşı puan toplansın",
    "👾 Klasik uzay istilacıları (space invaders) tarzı atış oyunu",
    "🐍 Modern görsellikte yılan (snake) oyunu, skor tablosu olsun",
    "🏰 Basit bir kule savunma (tower defense) prototipi",
    "🃏 Kart eşleştirme hafıza oyunu (memory match)",
]

# Görsel Üretim Atölyesi için hazır stil presetleri (İngilizce prompt eklentisi olarak kullanılır)
IMAGE_STYLE_PRESETS = {
    "🎯 Otomatik (AI Karar Versin)": "",
    "📷 Fotogerçekçi": "ultra realistic, photorealistic, 8k, professional photography, sharp focus, natural lighting",
    "🎨 Dijital Sanat": "digital art, trending on artstation, highly detailed, vibrant colors, concept art",
    "🌆 Cyberpunk": "cyberpunk style, neon lights, futuristic city, blade runner atmosphere, high contrast",
    "🧙 Fantastik": "fantasy art, epic, magical atmosphere, dramatic lighting, detailed illustration",
    "🕹️ Piksel Sanatı": "pixel art, 16-bit retro game style, crisp pixels, limited color palette",
    "🖼️ Suluboya": "watercolor painting, soft brush strokes, artistic, pastel colors",
    "🧊 3D Render": "3d render, octane render, unreal engine, cinematic lighting, highly detailed",
    "✏️ Anime / Manga": "anime style, manga illustration, cel shaded, vibrant, studio quality",
}


class KurumsalVeriAmbari:
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
        return "default_secure_aquarium_device_v114"


# =====================================================================
# 2.5. GERÇEK KİMLİK DOĞRULAMA MOTORU (GMAIL + ŞİFRE)
# =====================================================================
# Sadece geçerli formatta bir @gmail.com adresini kabul eder.
GMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9])?@gmail\.com$", re.IGNORECASE
)


class SazanAuth:
    """
    Kullanıcıları gerçek bir e-posta (Gmail) + şifre çifti ile kimlik
    doğrulamasından geçirir. Şifreler ASLA açık metin olarak saklanmaz;
    her hesap için üretilen benzersiz bir salt ile SHA-256 özetlenerek
    sazan_auth.json içine yazılır.
    """

    @staticmethod
    def _load():
        return KurumsalVeriAmbari.load_json(AUTH_FILE, {})

    @staticmethod
    def _save(db):
        KurumsalVeriAmbari.save_json(AUTH_FILE, db)

    @staticmethod
    def is_valid_gmail(email: str) -> bool:
        return bool(GMAIL_REGEX.match((email or "").strip()))

    @staticmethod
    def email_exists(email: str) -> bool:
        db = SazanAuth._load()
        return email.strip().lower() in db

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        return hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()

    @staticmethod
    def register(email: str, password: str):
        db = SazanAuth._load()
        email_key = email.strip().lower()
        salt = uuid.uuid4().hex
        db[email_key] = {
            "salt": salt,
            "password_hash": SazanAuth._hash_password(password, salt),
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
        SazanAuth._save(db)

    @staticmethod
    def verify(email: str, password: str) -> bool:
        db = SazanAuth._load()
        record = db.get(email.strip().lower())
        if not record:
            return False
        return SazanAuth._hash_password(password, record["salt"]) == record["password_hash"]


# =====================================================================
# 3. EKONOMİ MOTORU, BANKACILIK & GÜNLÜK BONUS SİSTEMİ
# =====================================================================
class SazanBank:
    @staticmethod
    def get_account(u):
        db = KurumsalVeriAmbari.load_json(ECONOMY_FILE, {})
        if u not in db:
            db[u] = {
                "coin": 1500,
                "bank_deposit": 0,
                "level": 1,
                "exp": 0,
                "last_claim": time.time(),
                "debt": 0,
                "credit_score": 500,
                "device_lock": get_device_fingerprint(),
                "last_login_date": "",
                "login_streak": 0,
                "games_created": 0,
            }
            KurumsalVeriAmbari.save_json(ECONOMY_FILE, db)
        acc = db[u]
        acc.setdefault("games_created", 0)
        acc.setdefault("login_streak", 0)
        acc.setdefault("last_login_date", "")
        return acc

    @staticmethod
    def update_account(u, data):
        db = KurumsalVeriAmbari.load_json(ECONOMY_FILE, {})
        db[u] = data
        KurumsalVeriAmbari.save_json(ECONOMY_FILE, db)

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

    @staticmethod
    def process_daily_bonus(u):
        acc = SazanBank.get_account(u)
        today = date.today().isoformat()
        if acc.get("last_login_date") != today:
            acc["login_streak"] = acc.get("login_streak", 0) + 1
            bonus = 100 + min(acc["login_streak"], 10) * 25
            acc["coin"] += bonus
            acc["last_login_date"] = today
            SazanBank.update_account(u, acc)
            st.toast(f"🎁 Günlük Giriş Bonusu: +{bonus} SZNC (Seri: {acc['login_streak']} gün)")


class SazanNasdaq:
    @staticmethod
    def get_market_prices():
        stocks = KurumsalVeriAmbari.load_json(
            STOCKS_FILE,
            {"SZN": 150.0, "BALIK": 60.0, "KRAK": 920.0, "CANAI": 7500.0, "QUANT": 320.0},
        )
        for key in stocks.keys():
            change_percent = random.uniform(-0.18, 0.22)
            stocks[key] = max(1.5, round(stocks[key] * (1 + change_percent), 2))
        KurumsalVeriAmbari.save_json(STOCKS_FILE, stocks)
        return stocks


# =====================================================================
# 4. RPG ARENA & BOSS SAVAŞ SİSTEMLERİ
# =====================================================================
DUNGEON_LORE = {
    "monsters": [
        {"name": "Neon Hidra Matrix", "hp": 70, "atk": 12, "reward": 60, "type": "normal"},
        {"name": "Siber Vatoz Alpha X", "hp": 100, "atk": 20, "reward": 100, "type": "normal"},
        {"name": "MEGABYTE LEVIATHAN [BOSS]", "hp": 600, "atk": 75, "reward": 1200, "type": "boss"},
    ],
    "shop_items": {
        "Siber Zıpkın v2": {"cost": 150, "damage": 35, "type": "weapon"},
        "Lazer Kuantum Trident": {"cost": 600, "damage": 90, "type": "weapon"},
        "Can Muhammed İmparatorluk Plazma Silahı": {"cost": 12000, "damage": 1250, "type": "weapon"},
    },
}


class SazanInventory:
    @staticmethod
    def get_inventory(u):
        db = KurumsalVeriAmbari.load_json(INVENTORY_FILE, {})
        if u not in db:
            db[u] = {
                "weapon": "Paslı Demir Kanca",
                "damage": 15,
                "potions": 4,
                "hp": 150,
                "max_hp": 150,
                "shield": 0,
                "max_shield": 100,
                "shares": {},
            }
            KurumsalVeriAmbari.save_json(INVENTORY_FILE, db)
        return db[u]

    @staticmethod
    def save_inventory(u, data):
        db = KurumsalVeriAmbari.load_json(INVENTORY_FILE, {})
        db[u] = data
        KurumsalVeriAmbari.save_json(INVENTORY_FILE, db)


# =====================================================================
# 5. OYUN KÜTÜPHANESİ (üretilen tüm oyunlar kalıcı olarak kaydedilir)
# =====================================================================
class SazanGameLibrary:
    @staticmethod
    def get_library(u):
        db = KurumsalVeriAmbari.load_json(GAMES_LIBRARY_FILE, {})
        return db.get(u, [])

    @staticmethod
    def add_game(u, title, code):
        db = KurumsalVeriAmbari.load_json(GAMES_LIBRARY_FILE, {})
        if u not in db:
            db[u] = []
        entry = {
            "id": uuid.uuid4().hex[:10],
            "title": title[:70],
            "code": code,
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
        db[u].insert(0, entry)
        db[u] = db[u][:50]  # kullanıcı başına en fazla 50 oyun sakla
        KurumsalVeriAmbari.save_json(GAMES_LIBRARY_FILE, db)
        return entry

    @staticmethod
    def delete_game(u, game_id):
        db = KurumsalVeriAmbari.load_json(GAMES_LIBRARY_FILE, {})
        if u in db:
            db[u] = [g for g in db[u] if g["id"] != game_id]
            KurumsalVeriAmbari.save_json(GAMES_LIBRARY_FILE, db)


# =====================================================================
# 5.5. 3D BASKI ATÖLYESİ - GÖRSELDEN STL (KABARTMA/LİTOFAN) ÜRETİCİSİ
# =====================================================================
class SazanPrintStudio:
    """
    Yüklenen bir görseli gri tonlamalı bir yükseklik haritasına (heightmap)
    dönüştürüp, 3D yazıcılarda basılabilecek kapalı (watertight) bir STL
    kabartma modeli üretir. Bu; fotoğraftan lityofan/rölyef tarzı 3D baskılar
    için pratik ve yaygın kullanılan bir tekniktir (tam bir 3D nesne
    rekonstrüksiyonu değildir, görselin kabartmalı bir yorumudur).
    """

    MAX_RESOLUTION_PX = 220  # performans ve dosya boyutu için üst sınır

    @staticmethod
    def generate_stl_from_image(
        image: Image.Image,
        max_size_px: int = 120,
        base_height_mm: float = 2.0,
        relief_height_mm: float = 5.0,
        pixel_size_mm: float = 0.6,
        invert: bool = False,
    ):
        max_size_px = max(10, min(max_size_px, SazanPrintStudio.MAX_RESOLUTION_PX))

        img = image.convert("L")
        w, h = img.size
        scale = max_size_px / max(w, h)
        new_w, new_h = max(2, int(w * scale)), max(2, int(h * scale))
        img = img.resize((new_w, new_h), Image.LANCZOS)

        arr = np.asarray(img, dtype=np.float64) / 255.0
        if invert:
            arr = 1.0 - arr

        rows, cols = arr.shape
        if rows < 2 or cols < 2:
            raise ValueError("Görsel çözünürlüğü çok düşük, en az 2x2 piksel gerekiyor.")

        top_z = base_height_mm + arr * relief_height_mm
        bottom_z = np.zeros_like(top_z)

        xs = np.arange(cols) * pixel_size_mm
        ys = np.arange(rows) * pixel_size_mm
        X, Y = np.meshgrid(xs, ys)

        top_v = np.stack([X, Y, top_z], axis=-1).reshape(-1, 3)
        bot_v = np.stack([X, Y, bottom_z], axis=-1).reshape(-1, 3)

        ii, jj = np.mgrid[0 : rows - 1, 0 : cols - 1]
        v00 = (ii * cols + jj).ravel()
        v01 = (ii * cols + (jj + 1)).ravel()
        v10 = ((ii + 1) * cols + jj).ravel()
        v11 = ((ii + 1) * cols + (jj + 1)).ravel()

        tris = [
            np.stack([top_v[v00], top_v[v10], top_v[v11]], axis=1),
            np.stack([top_v[v00], top_v[v11], top_v[v01]], axis=1),
            np.stack([bot_v[v00], bot_v[v11], bot_v[v10]], axis=1),
            np.stack([bot_v[v00], bot_v[v01], bot_v[v11]], axis=1),
        ]

        def wall(a_idx, b_idx):
            t1 = np.stack([top_v[a_idx], bot_v[a_idx], bot_v[b_idx]], axis=1)
            t2 = np.stack([top_v[a_idx], bot_v[b_idx], top_v[b_idx]], axis=1)
            return t1, t2

        top_row = np.arange(0, cols)
        idx_top_row = 0 * cols + top_row
        a, b = idx_top_row[:-1], idx_top_row[1:]
        t1, t2 = wall(b, a)
        tris += [t1, t2]

        idx_bot_row = (rows - 1) * cols + top_row
        a, b = idx_bot_row[:-1], idx_bot_row[1:]
        t1, t2 = wall(a, b)
        tris += [t1, t2]

        left_col = np.arange(0, rows) * cols
        a, b = left_col[:-1], left_col[1:]
        t1, t2 = wall(a, b)
        tris += [t1, t2]

        right_col = np.arange(0, rows) * cols + (cols - 1)
        a, b = right_col[:-1], right_col[1:]
        t1, t2 = wall(b, a)
        tris += [t1, t2]

        all_tris = np.concatenate(tris, axis=0)
        # Dış yüzey normalleri doğru yöne (dışa) baksın diye köşe sırasını çevir
        all_tris[:, [1, 2]] = all_tris[:, [2, 1]]

        data = np.zeros(all_tris.shape[0], dtype=stl_mesh.Mesh.dtype)
        data["vectors"] = all_tris
        generated_mesh = stl_mesh.Mesh(data)

        buf = io.BytesIO()
        generated_mesh.save("sazan_model.stl", fh=buf, mode=stl_mesh.stl.Mode.BINARY)
        buf.seek(0)

        width_mm = (new_w - 1) * pixel_size_mm
        depth_mm = (new_h - 1) * pixel_size_mm
        height_mm = base_height_mm + relief_height_mm

        return buf.read(), {
            "resolution": (new_w, new_h),
            "triangles": int(all_tris.shape[0]),
            "boyut_mm": (round(width_mm, 1), round(depth_mm, 1), round(height_mm, 1)),
        }


# =====================================================================
# 5.6. GÖRSEL ÜRETİM ATÖLYESİ - AI PROMPT'TAN GÖRSEL SENTEZLEYİCİ
# =====================================================================
class SazanImageForge:
    """
    Kullanıcının yazdığı fikri (hangi dilde olursa olsun) önce Groq üzerindeki
    dil modeliyle profesyonel, detaylı bir İngilizce görsel üretim prompt'una
    dönüştürür, ardından bu prompt'u anahtarsız/ücretsiz çalışan bir difüzyon
    görsel sentezleme uç noktasına göndererek gerçek bir PNG görsel üretir.
    Üretilen görseller kullanıcıya özel kalıcı bir galeriye kaydedilir.
    """

    # Anahtarsız, ücretsiz çalışan açık görsel sentezleme uç noktası.
    BASE_ENDPOINT = "https://image.pollinations.ai/prompt/"

    @staticmethod
    def get_gallery(u):
        db = KurumsalVeriAmbari.load_json(IMAGE_GALLERY_FILE, {})
        return db.get(u, [])

    @staticmethod
    def add_image(u, prompt_ozet, stil, image_bytes):
        db = KurumsalVeriAmbari.load_json(IMAGE_GALLERY_FILE, {})
        if u not in db:
            db[u] = []
        entry = {
            "id": uuid.uuid4().hex[:10],
            "prompt": prompt_ozet[:180],
            "stil": stil,
            "image_b64": base64.b64encode(image_bytes).decode("utf-8"),
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
        db[u].insert(0, entry)
        db[u] = db[u][:40]  # kullanıcı başına en fazla 40 görsel sakla
        KurumsalVeriAmbari.save_json(IMAGE_GALLERY_FILE, db)
        return entry

    @staticmethod
    def delete_image(u, image_id):
        db = KurumsalVeriAmbari.load_json(IMAGE_GALLERY_FILE, {})
        if u in db:
            db[u] = [g for g in db[u] if g["id"] != image_id]
            KurumsalVeriAmbari.save_json(IMAGE_GALLERY_FILE, db)

    @staticmethod
    def enhance_prompt_with_ai(ham_prompt, model="openai/gpt-oss-120b"):
        """Kullanıcının kısa/Türkçe görsel fikrini; kompozisyon, ışık, renk
        paleti ve atmosfer detaylarını içeren zengin bir İngilizce görsel
        üretim prompt'una dönüştürür. Groq'taki dil modelini kullanır."""
        sys_prompt = (
            "Sen profesyonel bir görsel üretim (text-to-image) prompt mühendisisin. "
            "Kullanıcı sana herhangi bir dilde kısa bir görsel fikri verecek. "
            "Görevin bu fikri; kompozisyon, ışıklandırma, renk paleti, atmosfer "
            "ve detay seviyesini net biçimde belirten, İngilizce, tek paragraf, "
            "en fazla 70 kelimelik zengin bir görsel üretim prompt'una çevirmektir. "
            "SADECE prompt metnini döndür; açıklama, giriş cümlesi, tırnak "
            "işareti veya markdown ekleme."
        )
        try:
            res = groq_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": ham_prompt},
                ],
                temperature=0.6,
                top_p=0.9,
                max_tokens=220,
            )
            enhanced = (res.choices[0].message.content or "").strip()
            enhanced = enhanced.strip('"').strip()
            return enhanced if enhanced else ham_prompt
        except Exception:
            # AI zenginleştirme başarısız olursa, kullanıcının ham fikriyle devam et
            return ham_prompt

    @staticmethod
    def generate_image(prompt_text, style_suffix="", width=1024, height=1024, seed=None):
        """Verilen prompt'u (ve seçilen stil eklentisini) görsel sentezleme
        motoruna gönderir, üretilen PNG byte dizisini geri döndürür."""
        final_prompt = prompt_text.strip()
        if style_suffix:
            final_prompt = f"{final_prompt}, {style_suffix}"

        width = max(256, min(int(width), 1536))
        height = max(256, min(int(height), 1536))
        seed_val = int(seed) if seed is not None else random.randint(1, 9_999_999)

        encoded_prompt = urllib.parse.quote(final_prompt)
        query = urllib.parse.urlencode(
            {"width": width, "height": height, "seed": seed_val, "nologo": "true"}
        )
        full_url = f"{SazanImageForge.BASE_ENDPOINT}{encoded_prompt}?{query}"

        req = urllib.request.Request(
            full_url, headers={"User-Agent": "Mozilla/5.0 (SazanAI ImageForge)"}
        )
        with urllib.request.urlopen(req, timeout=90) as response:
            image_bytes = response.read()

        return image_bytes, final_prompt, seed_val


# =====================================================================
# 6. GROQ AI OYUN MİMARI MOTORU (API ANAHTARI GÜVENLİ ŞEKİLDE SAKLANIR)
# =====================================================================
# API anahtarı ASLA kaynak kodun içine yazılmaz. Streamlit'in "secrets" sistemi
# kullanılır. Bunu GitHub'a yüklemeden önce yerelde .streamlit/secrets.toml
# dosyasına, Streamlit Cloud'da ise "App settings > Secrets" bölümüne eklersiniz:
#
#   GROQ_API_KEY = "gsk_xxx...xxx"
#
# Bu sayede anahtar hiçbir zaman GitHub deposuna gitmez (.gitignore ile korunur).
if "GROQ_API_KEY" not in st.secrets:
    st.error(
        "🚨 Kritik Sistem Ayar Hatası: GROQ_API_KEY bulunamadı!\n\n"
        "Lütfen `.streamlit/secrets.toml` dosyanıza (yerelde) veya Streamlit Cloud "
        "üzerinde 'Settings > Secrets' bölümüne şu satırı ekleyin:\n\n"
        'GROQ_API_KEY = "gsk_sizin_anahtariniz"'
    )
    st.stop()

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Kalite/hız tercihine göre seçilebilecek modeller
# ÖNEMLİ: Groq, 17 Haziran 2026'da llama-3.3-70b-versatile ve llama-3.1-8b-instant
# modellerinin kullanımdan kaldırılacağını duyurdu; bu modeller Ağustos 2026 itibarıyla
# tamamen kapatılıyor. Bu yüzden varsayılan model listesi Groq'un önerdiği güncel
# modellere (openai/gpt-oss ailesi ve qwen3.6) taşındı. Groq hesabından hangi
# modellerin aktif olduğunu https://console.groq.com/docs/models üzerinden kontrol edebilirsin.
# Sazan artık kararlılık ve tutarlılık için TEK ve SABİT bir yapay zeka modeli
# kullanır. Model seçim arayüzü bilgi amaçlı gösterilir ama pasiftir (disabled).
ACTIVE_MODEL_LABEL = "🏆 Sazan Kalite Motoru (GPT-OSS 120B)"
AI_MODELS = {
    ACTIVE_MODEL_LABEL: "openai/gpt-oss-120b",
}

MAX_CONTINUATIONS = 4  # Kod kesilirse otomatik olarak kaç kez "devam et" denenecek


class SazanAIConception:
    @staticmethod
    def _tek_istek(messages, model):
        return groq_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            top_p=0.9,
            max_tokens=8000,
        )

    @staticmethod
    def query_agent(prompt, history, target_lang, model="openai/gpt-oss-120b"):
        lowered = prompt.lower()
        if any(k in lowered for k in ["can muhammed çukur", "yapımcın kim", "yapımcısı"]):
            return (
                "Mutlak baş mimarım, kurucum ve dijital sistem mühendisim Can Muhammed "
                f"Çukur'dur. Bu siber evrenin her satırını o tasarladı. [Dil: {target_lang}]"
            )

        # Sıkılaştırılmış, kod kalitesine ve eksiksizliğe odaklı sistem promptu
        sys_prompt = (
            "Sen dünyanın en gelişmiş, vizyoner ve kusursuz HTML5 Oyun Mimarı ve Baş Sistem "
            "Mühendisisin. Görevin, kullanıcının isteklerini tam olarak analiz etmek ve tek "
            "bir HTML dosyası içinde çalışan, profesyonel kalitede bir oyun inşa etmektir.\n\n"
            "KOD KALİTESİ KURALLARI (KESİNLİKLE UYULMALI):\n"
            "1. Oyun; menü ekranı, oynanış durumu, duraklatma ve 'oyun bitti' ekranlarını içeren "
            "net bir durum makinesi (state machine) ile yönetilmelidir.\n"
            "2. JavaScript (ES6+) temiz, okunabilir, mantıksal bölümlere ayrılmış ve kısa "
            "açıklama yorumları içermelidir. requestAnimationFrame tabanlı düzgün bir oyun "
            "döngüsü kullan; çerçeve hızından bağımsız hareket (delta time) uygula.\n"
            "3. Oyun HEM klavye HEM DE dokunmatik/mobil kontrollerle oynanabilir olmalı; canvas "
            "boyutu pencereye göre duyarlı (responsive) olmalıdır.\n"
            "4. Kesinlikle hiçbir dış CDN, dış script veya dış görsel/ses linki kullanma; oyun "
            "tamamen bağımsız, tek dosya içinde ve tamamen offline çalışabilir olmalı (üretilen "
            "oyun tarayıcıda base64 data-URI olarak açılacağından dış kaynaklar yüklenemez).\n"
            "5. Görsel öğeler için HTML5 Canvas çizimleri, CSS gradyanları veya basit shape "
            "çizimleri kullan; hazır resim dosyası isteme.\n"
            "6. Asla bir fonksiyonu veya CSS kuralını 'buraları siz doldurun' diyerek yarım "
            "bırakma; kod üretimi uzun sürecek olsa bile eksiksiz ve çalışır durumda bitir.\n"
            "7. Yazdığın tüm HTML kodunu KESİNLİKLE sadece ve sadece TEK bir "
            "```html ... ``` kod bloğu içerisine al; kod bloğunun dışına başka kod yazma.\n\n"
            "Oyun dışındaki analizlerini, tebriklerini ve geliştirici notlarını ise kesinlikle "
            "şu dilde yaz: " + target_lang
        )

        messages = [{"role": "system", "content": sys_prompt}]
        for m in history[-10:]:
            messages.append({"role": m["role"], "content": m["content"]})
        messages.append({"role": "user", "content": prompt})

        try:
            res = SazanAIConception._tek_istek(messages, model)
            combined = res.choices[0].message.content or ""
            finish_reason = res.choices[0].finish_reason

            # Kod uzunluk limitinden dolayı yarıda kesildiyse, otomatik olarak
            # "kaldığın yerden devam et" isteği göndererek eksiksiz kodu tamamla.
            attempts = 0
            while finish_reason == "length" and attempts < MAX_CONTINUATIONS:
                messages.append({"role": "assistant", "content": combined})
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Yanıtın token limiti nedeniyle yarıda kesildi. BAŞTAN BAŞLAMA. "
                            "Sadece kaldığın satırdan itibaren devam ederek HTML/CSS/JS kodunu "
                            "eksiksiz şekilde tamamla ve tek ```html``` bloğunu düzgün kapat."
                        ),
                    }
                )
                res2 = SazanAIConception._tek_istek(messages, model)
                combined += res2.choices[0].message.content or ""
                finish_reason = res2.choices[0].finish_reason
                attempts += 1

            return combined
        except Exception as e:
            err_text = str(e).lower()
            if "decommission" in err_text or "deprecat" in err_text or "not found" in err_text:
                return (
                    "⚠️ Seçtiğin AI modeli Groq tarafından kaldırılmış görünüyor. "
                    "Lütfen sol menüden **'🧠 Oyun Mimarı Motoru'** kısmından farklı bir "
                    f"model seç ve tekrar dene.\n\n(Teknik detay: {e})"
                )
            return f"⚠️ Oyun Laboratuvarı İletişim Hatası: {e}"


# =====================================================================
# 7. SİSTEM BAŞLATICI & DURUM YÖNETİCİSİ
# =====================================================================
def global_state_enforcer():
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {"Ana Konsol Akışı": []}
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "Ana Konsol Akışı"
    if "chat_counter" not in st.session_state:
        st.session_state.chat_counter = 1

    defaults = {
        "admin_status": False,
        "dungeon_status": False,
        "current_dungeon_enemy": None,
        "active_panel_tab": None,
        "market_prices": SazanNasdaq.get_market_prices(),
        "last_market_update": time.time(),
        "active_lang_code": "Türkçe 🇹🇷",
        "pending_prompt": None,
        "active_ai_model": ACTIVE_MODEL_LABEL,
        "print_studio_status": False,
        "image_studio_status": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


global_state_enforcer()

# =====================================================================
# 8. GİRİŞ EKRANI
# =====================================================================
if "username" not in st.session_state:
    st.markdown(
        """
        <div class='sazan-hero' style='margin-top:34px;'>
            <h1>🐟 SAZAN AI OVERLORD</h1>
            <p>🛡️ Kuantum Oyun Stüdyosu · Görsel Sentezleyici · 3D Baskı Atölyesi</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, mid_col, _ = st.columns([1, 1.35, 1])
    with mid_col:
        with st.container(border=True):
            st.markdown("<div class='auth-logo-ring'>🐟</div>", unsafe_allow_html=True)
            st.markdown(
                "<h4 style='text-align:center; color:#f8fafc; margin:4px 0 2px 0;'>"
                "Sazan Evrenine Hoş Geldin</h4>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p class='auth-caption'>Devam etmek için Gmail adresinle giriş yap "
                "ya da yeni bir hesap oluştur.</p>",
                unsafe_allow_html=True,
            )

            tab_login, tab_signup = st.tabs(["➡️ Giriş Yap", "🆕 Hesap Oluştur"])

            # --- GİRİŞ YAP SEKMESİ ---
            with tab_login:
                login_email = st.text_input(
                    "📧 Gmail Adresin",
                    key="login_email_input",
                    placeholder="[email protected]",
                )
                login_pw = st.text_input(
                    "🔑 Şifren", type="password", key="login_pw_input"
                )
                if st.button(
                    "Giriş Yap", use_container_width=True, type="primary", key="login_submit_btn"
                ):
                    email_clean = login_email.strip()
                    if not email_clean or not login_pw:
                        st.error("⚠️ Lütfen e-posta ve şifreni gir.")
                    elif not SazanAuth.is_valid_gmail(email_clean):
                        st.error(
                            "❌ Geçersiz e-posta! Lütfen '@gmail.com' ile biten "
                            "geçerli bir Gmail adresi girin."
                        )
                    elif not SazanAuth.email_exists(email_clean):
                        st.error(
                            "❌ Bu Gmail adresine kayıtlı bir hesap bulunamadı. "
                            "Önce '🆕 Hesap Oluştur' sekmesinden kayıt ol."
                        )
                    elif not SazanAuth.verify(email_clean, login_pw):
                        st.error("❌ Şifre yanlış! Lütfen tekrar dene.")
                    else:
                        st.session_state.username = email_clean.lower()
                        SazanBank.get_account(email_clean.lower())
                        st.success("🎉 Giriş başarılı! Sazan evrenine yönlendiriliyorsun...")
                        time.sleep(0.5)
                        st.rerun()

            # --- HESAP OLUŞTUR SEKMESİ ---
            with tab_signup:
                signup_email = st.text_input(
                    "📧 Gmail Adresin",
                    key="signup_email_input",
                    placeholder="[email protected]",
                )
                signup_pw = st.text_input(
                    "🔑 Şifre Belirle (en az 6 karakter)",
                    type="password",
                    key="signup_pw_input",
                )
                signup_pw_confirm = st.text_input(
                    "🔑 Şifreni Tekrar Gir", type="password", key="signup_pw_confirm_input"
                )
                if st.button(
                    "Hesap Oluştur", use_container_width=True, type="primary", key="signup_submit_btn"
                ):
                    email_clean = signup_email.strip()
                    if not email_clean or not signup_pw or not signup_pw_confirm:
                        st.error("⚠️ Lütfen tüm alanları doldur.")
                    elif not SazanAuth.is_valid_gmail(email_clean):
                        st.error(
                            "❌ Geçersiz e-posta! Lütfen '@gmail.com' ile biten "
                            "geçerli bir Gmail adresi girin."
                        )
                    elif SazanAuth.email_exists(email_clean):
                        st.error("❌ Bu Gmail adresi zaten kayıtlı. '➡️ Giriş Yap' sekmesini kullan.")
                    elif len(signup_pw) < 6:
                        st.error("❌ Şifren en az 6 karakter olmalı.")
                    elif signup_pw != signup_pw_confirm:
                        st.error("❌ Şifreler birbiriyle eşleşmiyor.")
                    else:
                        SazanAuth.register(email_clean, signup_pw)
                        st.session_state.username = email_clean.lower()
                        SazanBank.get_account(email_clean.lower())
                        st.success("🎉 Hesabın oluşturuldu! Sazan evrenine hoş geldin.")
                        time.sleep(0.5)
                        st.rerun()

    st.stop()

user = st.session_state.username
SazanBank.process_interest(user)
SazanBank.process_daily_bonus(user)

if time.time() - st.session_state.last_market_update > 60:
    st.session_state.market_prices = SazanNasdaq.get_market_prices()
    st.session_state.last_market_update = time.time()

# =====================================================================
# 9. STÜDYO ÇALIŞMA ALANI - SIDEBAR
# =====================================================================
with st.sidebar:
    st.markdown(f"<h3 style='color:#38bdf8; text-align:center;'>🏢 Workspace: {user}</h3>", unsafe_allow_html=True)
    if st.button("🚪 Çıkış Yap", use_container_width=True):
        del st.session_state["username"]
        st.rerun()
    acc = SazanBank.get_account(user)
    st.caption("❖ Finansal Likidite Durumu")
    st.code(
        f"Bakiye: {acc['coin']} SZNC\n"
        f"Borç: {acc.get('debt', 0)} SZNC\n"
        f"Kredi Skoru: {acc.get('credit_score', 500)}/1000\n"
        f"Kademe Seviyesi: Lvl {acc['level']}\n"
        f"Giriş Serisi: {acc.get('login_streak', 0)} gün\n"
        f"Üretilen Oyun: {acc.get('games_created', 0)}"
    )
    st.divider()

    st.markdown("💬 **Oyun Proje Odaları**")
    if st.button("➕ Yeni Oyun Projesi Başlat", use_container_width=True, type="secondary"):
        st.session_state.chat_counter += 1
        new_id = f"Oyun Oturumu {st.session_state.chat_counter}"
        st.session_state.chat_sessions[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()

    st.markdown("<div style='max-height: 220px; overflow-y: auto; margin-top:10px;'>", unsafe_allow_html=True)
    for chat_name in reversed(list(st.session_state.chat_sessions.keys())):
        is_current = chat_name == st.session_state.current_chat
        bullet = "🎮" if is_current else "◇"
        if st.button(f"{bullet} {chat_name}", key=f"switch_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️ Mevcut Akışı Sıfırla", use_container_width=True):
        st.session_state.chat_sessions[st.session_state.current_chat] = []
        st.rerun()

    st.divider()
    st.markdown("🧠 **Oyun Mimarı Motoru**")
    st.selectbox(
        "AI Model Tercihi:",
        list(AI_MODELS.keys()),
        key="active_ai_model",
        label_visibility="collapsed",
        disabled=True,
        help="Sazan artık kararlılık ve maksimum kalite için sabit, tek bir "
        "yapay zeka motoru kullanır. Bu nedenle model seçimi pasif hale getirildi.",
    )
    st.caption("🔒 Sazan artık tek ve sabit bir yapay zeka motoruyla çalışır.")

    st.divider()
    st.markdown("💡 **Hızlı Oyun Şablonları**")
    for tpl in GAME_TEMPLATES:
        if st.button(tpl, key=f"tpl_{tpl}", use_container_width=True):
            st.session_state.pending_prompt = tpl.split(" ", 1)[1]
            st.rerun()

# =====================================================================
# 10. ANA GÖSTERİM TERMİNALİ (SOHBET AKIŞI & OYUN YAKALAYICI)
# =====================================================================
st.markdown(
    """
    <div class='sazan-hero'>
        <h1>🐟 SAZAN AI ENTERPRISE STUDIO</h1>
        <p>Kuantum Oyun Mimarı · Ekonomi Motoru · Siber Arena · 3D Baskı Atölyesi</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"<p style='color:#64748b; font-size:0.9rem; font-weight:700; letter-spacing:1px;'>"
    f"🛠️ AKTİF OYUN PROJE HATTI: {st.session_state.current_chat}</p>",
    unsafe_allow_html=True,
)

if st.session_state.admin_status:
    st.markdown("<div class='rpg-terminal-box'>", unsafe_allow_html=True)
    st.markdown("<h4>👑 ADMIN CONTROL CONSOLE</h4>", unsafe_allow_html=True)
    token = st.text_input("Root Kimlik Şifresi:", type="password", key="admin_token_input")
    if token:
        if token == SUPER_ADMIN_PASSWORD:
            st.success("Mutlak Root Yetkileri Aktive Edildi.")
            if st.button("💵 +250,000 SZNC Enjekte Et", use_container_width=True):
                SazanBank.modify_coin(user, 250000)
                st.success("Bakiye güncellendi!")
                time.sleep(0.4)
                st.rerun()
        else:
            st.error("Geçersiz şifre.")
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
                st.error("Zindandan elendiniz.")
                SazanBank.modify_coin(user, -100)
                p_inv["hp"] = p_inv["max_hp"]
                st.session_state.current_dungeon_enemy = None
            elif en["hp"] <= 0:
                st.success(f"🏆 Savaş Kazanıldı! Ganimet: +{en['reward']} SZNC")
                SazanBank.modify_coin(user, en["reward"])
                st.session_state.current_dungeon_enemy = None
            SazanInventory.save_inventory(user, p_inv)
            time.sleep(0.4)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

active_messages = st.session_state.chat_sessions[st.session_state.current_chat]

for idx, m in enumerate(active_messages):
    with st.chat_message(m["role"]):
        content = m["content"]
        html_blocks = re.findall(r"```html\s*(.*?)\s*```", content, re.DOTALL)

        if html_blocks:
            clean_text = re.sub(r"```html\s*(.*?)\s*```", "", content, flags=re.DOTALL)
            st.markdown(clean_text)

            game_code = html_blocks[0]
            b64_game = base64.b64encode(game_code.encode("utf-8")).decode("utf-8")
            game_url = f"data:text/html;base64,{b64_game}"

            st.markdown(
                f'<a href="{game_url}" target="_blank" class="launch-game-btn">'
                f"🎮 Üretilen Oyunu Yeni Sekmede Tam Ekran Başlat</a>",
                unsafe_allow_html=True,
            )
            st.download_button(
                "⬇️ Oyunu .html Olarak İndir",
                data=game_code,
                file_name=f"sazan_oyun_{idx}.html",
                mime="text/html",
                key=f"dl_{st.session_state.current_chat}_{idx}",
            )

            with st.expander("🛠️ Geliştirici Ham Kaynak Kodları (Yedeklemek İçin)"):
                st.code(game_code, language="html")
        else:
            st.markdown(content)

# =====================================================================
# 11. ENTEGRE HUB PANELLERİ (MAĞAZA / BANKA / BORSA / MADEN / KÜTÜPHANE)
# =====================================================================
if st.session_state.active_panel_tab == "plus":
    st.markdown("<div class='stock-market-box'>", unsafe_allow_html=True)
    t1, t2, t3, t4, t5 = st.tabs(
        [
            "🛒 Ekipman Deposu",
            "🏦 Kasa & Kredi Merkezi",
            "📊 Finansal Borsa",
            "⛏️ Kuantum Madencilik",
            "📚 Oyun Kütüphanem",
        ]
    )

    with t1:
        for item, d in DUNGEON_LORE["shop_items"].items():
            st.write(f"🔹 **{item}** — {d['cost']} SZNC")
            if st.button(f"Satın Al: {item}", key=f"buy_{item}"):
                u_acc = SazanBank.get_account(user)
                if u_acc["coin"] >= d["cost"]:
                    SazanBank.modify_coin(user, -d["cost"])
                    u_inv = SazanInventory.get_inventory(user)
                    if d["type"] == "weapon":
                        u_inv["weapon"], u_inv["damage"] = item, d["damage"]
                    SazanInventory.save_inventory(user, u_inv)
                    st.success(f"{item} alındı.")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error("Yetersiz bakiye.")

    with t2:
        b_acc = SazanBank.get_account(user)
        st.write(f"Mevcut Borcunuz: **{b_acc.get('debt', 0)} SZNC**")
        st.write(f"Banka Mevduatınız: **{b_acc.get('bank_deposit', 0)} SZNC**")
        dep_col1, dep_col2 = st.columns(2)
        with dep_col1:
            dep_amt = st.number_input("Yatırılacak Tutar", min_value=0, step=50, key="dep_amt")
            if st.button("Bankaya Yatır", use_container_width=True):
                if dep_amt > 0 and b_acc["coin"] >= dep_amt:
                    b_acc["coin"] -= dep_amt
                    b_acc["bank_deposit"] += dep_amt
                    SazanBank.update_account(user, b_acc)
                    st.success("Yatırıldı."); time.sleep(0.4); st.rerun()
                else:
                    st.error("Geçersiz tutar veya yetersiz bakiye.")
        with dep_col2:
            wd_amt = st.number_input("Çekilecek Tutar", min_value=0, step=50, key="wd_amt")
            if st.button("Bankadan Çek", use_container_width=True):
                if wd_amt > 0 and b_acc["bank_deposit"] >= wd_amt:
                    b_acc["bank_deposit"] -= wd_amt
                    b_acc["coin"] += wd_amt
                    SazanBank.update_account(user, b_acc)
                    st.success("Çekildi."); time.sleep(0.4); st.rerun()
                else:
                    st.error("Geçersiz tutar veya yetersiz mevduat.")

    with t3:
        prices = st.session_state.market_prices
        p_inv = SazanInventory.get_inventory(user)
        if "shares" not in p_inv:
            p_inv["shares"] = {}
        for ticker, val in prices.items():
            st.write(f"💹 **{ticker} Varlığı**: `{val} SZNC` (Portföyün: {p_inv['shares'].get(ticker, 0)} Lot)")
            col_sh1, col_sh2 = st.columns(2)
            with col_sh1:
                if st.button(f"1 Lot Al: {ticker}", key=f"sh_buy_{ticker}"):
                    u_acc = SazanBank.get_account(user)
                    if u_acc["coin"] >= val:
                        SazanBank.modify_coin(user, -int(val))
                        p_inv["shares"][ticker] = p_inv["shares"].get(ticker, 0) + 1
                        SazanInventory.save_inventory(user, p_inv)
                        st.success("Portföy güncellendi."); time.sleep(0.4); st.rerun()
                    else:
                        st.error("Yetersiz bakiye.")
            with col_sh2:
                if st.button(f"1 Lot Sat: {ticker}", key=f"sh_sell_{ticker}"):
                    if p_inv["shares"].get(ticker, 0) > 0:
                        SazanBank.modify_coin(user, int(val))
                        p_inv["shares"][ticker] -= 1
                        SazanInventory.save_inventory(user, p_inv)
                        st.success("Satış yapıldı."); time.sleep(0.4); st.rerun()
                    else:
                        st.error("Elinizde bu hisseden yok.")

    with t4:
        st.write("Madencilik Modülü Stabil.")
        st.caption("Bu modül gelecek sürümlerde genişletilecek.")

    with t5:
        lib = SazanGameLibrary.get_library(user)
        if not lib:
            st.info("Henüz kütüphanenizde kayıtlı bir oyun yok. Sohbetten bir oyun ürettiğinizde otomatik olarak buraya kaydedilir.")
        for g in lib:
            st.markdown("<div class='library-card'>", unsafe_allow_html=True)
            st.markdown(f"**🎮 {g['title']}**  <span class='badge'>{g['created_at']}</span>", unsafe_allow_html=True)
            b64_game = base64.b64encode(g["code"].encode("utf-8")).decode("utf-8")
            game_url = f"data:text/html;base64,{b64_game}"
            lc1, lc2, lc3 = st.columns([1.3, 1.3, 0.6])
            with lc1:
                st.markdown(
                    f'<a href="{game_url}" target="_blank" class="launch-game-btn">▶️ Oyunu Başlat</a>',
                    unsafe_allow_html=True,
                )
            with lc2:
                st.download_button(
                    "⬇️ İndir", data=g["code"], file_name=f"{g['title'][:30]}.html",
                    mime="text/html", key=f"lib_dl_{g['id']}",
                )
            with lc3:
                if st.button("🗑️", key=f"lib_del_{g['id']}"):
                    SazanGameLibrary.delete_game(user, g["id"])
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 11.5. 🖨️ 3D BASKI ATÖLYESİ (BAĞIMSIZ, GÖZE ÇARPAN PANEL)
# =====================================================================
if st.session_state.get("print_studio_status", False):
    st.markdown("<div class='print-studio-box'>", unsafe_allow_html=True)
    st.markdown("<h4>🖨️ 3D BASKI ATÖLYESİ — GÖRSELDEN STL ÜRETİCİ</h4>", unsafe_allow_html=True)
    st.markdown(
        "Bir görsel yükle; Sazan onu gri tonlamalı bir **yükseklik haritasına** çevirip "
        "3D yazıcında basabileceğin kapalı (watertight) bir **.stl kabartma modeli** üretsin. "
        "Bu teknik bir *lityofan/rölyef* dönüşümüdür — görseli tam bir 3D nesneye değil, "
        "kabartmalı bir yüzeye çevirir. Portre, logo, harita gibi görsellerde en iyi sonucu verir."
    )

    uploaded_img = st.file_uploader(
        "📤 Görsel Yükle (PNG / JPG / JPEG) — Buraya tıkla veya sürükle-bırak",
        type=["png", "jpg", "jpeg"],
        key="stl_uploader",
    )

    if uploaded_img is not None:
        pil_image = Image.open(uploaded_img)
        col_prev, col_opts = st.columns([1, 1.3])

        with col_prev:
            st.image(pil_image, caption="Yüklenen Görsel", use_container_width=True)

        with col_opts:
            boyut_mm = st.slider("Genişlik/Uzunluk (mm)", 30, 200, 80, step=5)
            taban_mm = st.slider("Taban Kalınlığı (mm)", 0.5, 5.0, 2.0, step=0.5)
            rolyef_mm = st.slider("Kabartma Yüksekliği (mm)", 1.0, 15.0, 5.0, step=0.5)
            cozunurluk = st.slider(
                "Çözünürlük (piksel, yüksek = daha detaylı ama daha ağır dosya)",
                30,
                SazanPrintStudio.MAX_RESOLUTION_PX,
                120,
                step=10,
            )
            ters_cevir = st.checkbox(
                "Tonları Ters Çevir (koyu alanlar daha yüksek olsun)", value=False
            )

        if st.button("🧊 STL Modelini Oluştur", use_container_width=True, type="primary"):
            with st.spinner("Yükseklik haritası ve 3D örgü (mesh) hesaplanıyor..."):
                try:
                    max_w = max(pil_image.width, pil_image.height)
                    pixel_size_mm = boyut_mm / min(cozunurluk, max_w)
                    stl_bytes, info = SazanPrintStudio.generate_stl_from_image(
                        pil_image,
                        max_size_px=cozunurluk,
                        base_height_mm=taban_mm,
                        relief_height_mm=rolyef_mm,
                        pixel_size_mm=pixel_size_mm,
                        invert=ters_cevir,
                    )
                    w_mm, d_mm, h_mm = info["boyut_mm"]
                    st.success(
                        f"✅ Model hazır! Boyut: {w_mm} x {d_mm} x {h_mm} mm | "
                        f"Üçgen sayısı: {info['triangles']:,} | "
                        f"Çözünürlük: {info['resolution'][0]}x{info['resolution'][1]} px"
                    )
                    st.download_button(
                        "⬇️ .stl Dosyasını İndir",
                        data=stl_bytes,
                        file_name=f"sazan_3d_model_{uuid.uuid4().hex[:6]}.stl",
                        mime="model/stl",
                        use_container_width=True,
                    )
                    st.caption(
                        "İndirdiğin .stl dosyasını Cura, PrusaSlicer veya Bambu Studio gibi "
                        "bir dilimleyici (slicer) programına yükleyip 3D yazıcına gönderebilirsin."
                    )
                except Exception as e:
                    st.error(f"⚠️ Model üretilirken hata oluştu: {e}")
    else:
        st.info("👆 Başlamak için yukarıdaki kutuya tıklayıp bir görsel yükle.")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 11.6. 🎨 GÖRSEL ÜRETİM ATÖLYESİ (AI PROMPT'TAN GÖRSEL SENTEZLE)
# =====================================================================
if st.session_state.get("image_studio_status", False):
    st.markdown("<div class='print-studio-box'>", unsafe_allow_html=True)
    st.markdown("<h4>🎨 GÖRSEL ÜRETİM ATÖLYESİ — PROMPT'TAN GÖRSEL SENTEZLE</h4>", unsafe_allow_html=True)
    st.markdown(
        "Aklındaki görseli anlat; Sazan önce Groq üzerindeki dil modeliyle fikrini "
        "profesyonel bir görsel üretim prompt'una dönüştürsün, ardından gerçek bir "
        "görsel üretsin. Türkçe (veya istediğin herhangi bir dilde) yazabilirsin, "
        "çeviri ve zenginleştirme otomatik yapılır."
    )

    img_col1, img_col2 = st.columns([1.5, 1])

    with img_col1:
        ham_fikir = st.text_area(
            "💭 Görsel Fikrin:",
            placeholder="Örn: Ay ışığında bir kaleye bakan zırhlı bir ejderha, sisli dağlar arasında...",
            key="img_forge_prompt_input",
            height=110,
        )

        stil_secim = st.selectbox(
            "🎭 Görsel Stili:",
            list(IMAGE_STYLE_PRESETS.keys()),
            key="img_forge_style_select",
        )

        enh_col, gen_col = st.columns(2)
        with enh_col:
            enhance_clicked = st.button("✨ AI ile Prompt'u Geliştir", use_container_width=True)
        with gen_col:
            generate_clicked = st.button("🖼️ Görseli Üret", use_container_width=True, type="primary")

        if enhance_clicked:
            if ham_fikir.strip():
                with st.spinner("Prompt profesyonelce zenginleştiriliyor..."):
                    cur_model = AI_MODELS.get(
                        st.session_state.get("active_ai_model", ACTIVE_MODEL_LABEL),
                        "openai/gpt-oss-120b",
                    )
                    zenginlesmis = SazanImageForge.enhance_prompt_with_ai(ham_fikir, model=cur_model)
                    st.session_state["img_forge_enhanced_prompt"] = zenginlesmis
                    st.rerun()
            else:
                st.warning("Önce bir görsel fikri yaz.")

        if st.session_state.get("img_forge_enhanced_prompt"):
            st.text_area(
                "🧠 AI Tarafından Geliştirilmiş Prompt (istersen elle düzenleyebilirsin):",
                key="img_forge_enhanced_prompt",
                height=90,
            )

    with img_col2:
        boyut_secim = st.selectbox(
            "📐 Görsel Boyutu:",
            ["Kare (1024x1024)", "Portre (768x1024)", "Manzara (1024x768)", "Geniş Ekran (1280x720)"],
            key="img_forge_size_select",
        )
        rastgele_seed = st.checkbox("🎲 Rastgele Seed Kullan", value=True, key="img_forge_random_seed")
        sabit_seed = None
        if not rastgele_seed:
            sabit_seed = st.number_input(
                "Sabit Seed Değeri", min_value=1, max_value=9999999, value=42, step=1
            )

    boyut_haritasi = {
        "Kare (1024x1024)": (1024, 1024),
        "Portre (768x1024)": (768, 1024),
        "Manzara (1024x768)": (1024, 768),
        "Geniş Ekran (1280x720)": (1280, 720),
    }
    secili_w, secili_h = boyut_haritasi[boyut_secim]

    if generate_clicked:
        nihai_prompt = st.session_state.get("img_forge_enhanced_prompt") or ham_fikir
        if not nihai_prompt or not nihai_prompt.strip():
            st.error("⚠️ Lütfen önce bir görsel fikri yaz.")
        else:
            with st.spinner("🎨 Kuantum difüzyon motoru görseli inşa ediyor... Lütfen bekleyin..."):
                try:
                    stil_suffix = IMAGE_STYLE_PRESETS.get(stil_secim, "")
                    img_bytes, kullanilan_prompt, kullanilan_seed = SazanImageForge.generate_image(
                        nihai_prompt,
                        style_suffix=stil_suffix,
                        width=secili_w,
                        height=secili_h,
                        seed=sabit_seed,
                    )
                    st.session_state["img_forge_last_result"] = {
                        "bytes": img_bytes,
                        "prompt": kullanilan_prompt,
                        "seed": kullanilan_seed,
                        "stil": stil_secim,
                    }

                    SazanImageForge.add_image(user, ham_fikir or nihai_prompt, stil_secim, img_bytes)
                    SazanBank.modify_coin(user, 10)  # her üretimde küçük bir ödül
                    st.toast("🖼️ Görsel galeriye kaydedildi! (+10 SZNC)")
                except Exception as e:
                    st.error(f"⚠️ Görsel üretilirken hata oluştu: {e}")

    if st.session_state.get("img_forge_last_result"):
        sonuc = st.session_state["img_forge_last_result"]
        st.divider()
        st.image(
            sonuc["bytes"],
            caption=f"Seed: {sonuc['seed']} | Stil: {sonuc['stil']}",
            use_container_width=True,
        )
        st.download_button(
            "⬇️ Görseli .png Olarak İndir",
            data=sonuc["bytes"],
            file_name=f"sazan_gorsel_{sonuc['seed']}.png",
            mime="image/png",
            use_container_width=True,
        )
        with st.expander("🔍 Kullanılan Nihai Prompt"):
            st.code(sonuc["prompt"], language="text")

    st.divider()
    st.markdown("📚 **Görsel Galerim**")
    galeri = SazanImageForge.get_gallery(user)
    if not galeri:
        st.info(
            "Henüz galerinde kayıtlı bir görsel yok. Yukarıdan bir görsel "
            "ürettiğinde otomatik olarak buraya eklenir."
        )
    else:
        gal_cols = st.columns(3)
        for i, g in enumerate(galeri):
            with gal_cols[i % 3]:
                st.markdown("<div class='library-card'>", unsafe_allow_html=True)
                img_raw = base64.b64decode(g["image_b64"])
                st.image(img_raw, use_container_width=True)
                st.caption(f"🎭 {g['stil']}  ·  {g['created_at']}")
                kisa_prompt = g["prompt"][:60] + ("..." if len(g["prompt"]) > 60 else "")
                st.caption(f"💭 {kisa_prompt}")
                gcol1, gcol2 = st.columns(2)
                with gcol1:
                    st.download_button(
                        "⬇️", data=img_raw, file_name=f"sazan_gorsel_{g['id']}.png",
                        mime="image/png", key=f"gal_dl_{g['id']}", use_container_width=True,
                    )
                with gcol2:
                    if st.button("🗑️", key=f"gal_del_{g['id']}", use_container_width=True):
                        SazanImageForge.delete_image(user, g["id"])
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 12. HUD KONTROLLERİ (HIZLI ERİŞİM MENÜSÜ)
# =====================================================================
st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
hc1, hc2, hc3, hc4, _ = st.columns([1.5, 1.2, 1.5, 1.8, 4.3])
with hc1:
    if st.button("💼 Finans, Stüdyo & Maden", use_container_width=True):
        st.session_state.active_panel_tab = "plus" if st.session_state.active_panel_tab != "plus" else None
        st.rerun()
with hc2:
    if st.button("🛡️ Siber Arena (RPG)", use_container_width=True):
        st.session_state.dungeon_status = not st.session_state.dungeon_status
        st.rerun()
with hc3:
    if st.button("🖨️ 3D Baskı Atölyesi", use_container_width=True, type="primary"):
        st.session_state.print_studio_status = not st.session_state.get("print_studio_status", False)
        st.rerun()
with hc4:
    if st.button("🎨 Görsel Üretim Atölyesi", use_container_width=True, type="primary"):
        st.session_state.image_studio_status = not st.session_state.get("image_studio_status", False)
        st.rerun()

# =====================================================================
# 13. SÜREKLİ ÇALIŞMA ALANI MOTORU (OYUN DERLEYİCİ ÇEKİRDEĞİ)
# =====================================================================
typed_prompt = st.chat_input("Nasıl bir HTML5 oyunu tasarlamak istersin? Fikrini buraya yaz...")
prompt = typed_prompt or st.session_state.pending_prompt
if st.session_state.pending_prompt and not typed_prompt:
    st.session_state.pending_prompt = None

if prompt:
    if prompt.strip() == "TURKEY SAZAN":
        st.session_state.admin_status = True
        st.rerun()

    active_messages.append({"role": "user", "content": prompt})

    with st.spinner("Sazan Kuantum Oyun Mimarı devasa kodları inşa ediyor... Lütfen bekleyin..."):
        cur_lang = st.session_state.get("active_lang_code", "Türkçe 🇹🇷")
        cur_model = AI_MODELS.get(
            st.session_state.get("active_ai_model", ACTIVE_MODEL_LABEL),
            "openai/gpt-oss-120b",
        )
        ans = SazanAIConception.query_agent(prompt, active_messages, cur_lang, model=cur_model)
        active_messages.append({"role": "assistant", "content": ans})

        html_blocks = re.findall(r"```html\s*(.*?)\s*```", ans, re.DOTALL)
        if html_blocks:
            entry = SazanGameLibrary.add_game(user, prompt, html_blocks[0])
            acc = SazanBank.get_account(user)
            acc["games_created"] = acc.get("games_created", 0) + 1
            SazanBank.update_account(user, acc)
            SazanBank.modify_coin(user, 25)  # her üretimde küçük bir ödül
            st.toast(f"📚 Oyun kütüphaneye kaydedildi: {entry['title']}")

        st.rerun()

# =====================================================================
# 14. DİNAMİK DİL SEÇİM MERKEZİ
# =====================================================================
st.markdown("<div class='fixed-lang-hub'>", unsafe_allow_html=True)
sel_lang = st.selectbox(
    "🌐 Çeviri:", list(DIL_MATRISI.keys()), key="lang_widget", label_visibility="collapsed"
)
st.session_state.active_lang_code = sel_lang
st.markdown("</div>", unsafe_allow_html=True)
