# ================================================================================
#   🐟  S A Z A N   A I   —   v121.0  "AURORA+"
#   Modern, Gemini esintili sohbet deneyimi.
#   Ekonomi / bakiye / RPG sistemleri tamamen kaldırıldı.
#   Misafir: sohbet + tek sabit model. Üye: 7 model + görsel üretimi + 3D baskı.
#   YENİ: "Bu cihazda beni hatırla" (isteğe bağlı çerez girişi) + "Okudum, onaylıyorum"
#         (telif hakkı sorumluluğu) kutusu + daha güvenilir güncel bilgi araması.
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
from datetime import datetime, timedelta

import numpy as np
from PIL import Image
from stl import mesh as stl_mesh

from groq import Groq

# "Beni hatırla" özelliği için tarayıcı çerezi yöneticisi.
# requirements.txt dosyana şunu eklemen gerekir:  extra-streamlit-components
# NOT: Bu kütüphane requirements.txt'de yoksa veya Streamlit Cloud henüz kurmadıysa
# uygulamanın tamamen çökmemesi için import'u güvenli hale getiriyoruz. Eksikse
# "beni hatırla" özelliği sessizce devre dışı kalır, geri kalan her şey çalışmaya devam eder.
try:
    import extra_streamlit_components as stx
    _COOKIE_LIB_VAR = True
except ModuleNotFoundError:
    stx = None
    _COOKIE_LIB_VAR = False

# =====================================================================
# 1. SAYFA AYARLARI
# =====================================================================
st.set_page_config(
    page_title="Sazan AI",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# 2. GÖRSEL KİMLİK — MODERN "AURORA" TEMASI (CSS)
# =====================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root{
        --sz-bg: #0a0d16;
        --sz-bg-soft: #0f1320;
        --sz-surface: #131829;
        --sz-border: #232a3d;
        --sz-text: #eef1f8;
        --sz-muted: #8b93a7;
        --sz-cyan: #22d3ee;
        --sz-indigo: #6366f1;
        --sz-violet: #a855f7;
    }

    html, body, .stApp {
        background: radial-gradient(circle at 15% 0%, #10162a 0%, #0a0d16 45%, #07090f 100%) !important;
        color: var(--sz-text);
        font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* ---------- SIDEBAR AÇMA/KAPAMA OKU ---------- */
    /* "header {visibility: hidden;}" kuralı, bazı Streamlit sürümlerinde sidebar'ı
       kapatınca tekrar açmaya yarayan ok/ok düğmesini de gizliyordu — bu yüzden
       sidebar bir kez kapatılınca bir daha açılamıyordu. Aşağıdaki kurallar, hem
       sidebar KAPALIYKEN görünen açma okunu, hem de sidebar AÇIKKEN görünen kapama
       okunu (Streamlit sürümüne göre iki farklı test-id kullanılabiliyor) her
       zaman görünür ve tıklanabilir tutar, ayrıca temaya uygun şekilde boyar.*/
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        opacity: 1 !important;
        z-index: 999999 !important;
    }
    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapsedControl"] button {
        visibility: visible !important;
        opacity: 1 !important;
        background: var(--sz-surface) !important;
        border: 1px solid var(--sz-border) !important;
        border-radius: 10px !important;
    }
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarCollapsedControl"] svg {
        color: var(--sz-cyan) !important;
        fill: var(--sz-cyan) !important;
    }

    /* ---------- SIDEBAR ---------- */
    [data-testid="stSidebar"] {
        background: #080a13 !important;
        border-right: 1px solid var(--sz-border) !important;
    }
    [data-testid="stSidebar"] * { font-family: 'Inter', sans-serif; }

    /* ---------- SCROLLBAR ---------- */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-thumb { background: #2a3149; border-radius: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }

    /* ---------- CHAT BUBBLES ---------- */
    .stChatMessage {
        border-radius: 18px !important;
        padding: 1.1rem 1.4rem !important;
        margin-bottom: 1.1rem !important;
        border: 1px solid var(--sz-border) !important;
        background-color: var(--sz-surface) !important;
        box-shadow: 0 8px 24px -12px rgba(0,0,0,0.5);
    }

    code, pre {
        font-family: 'Fira Code', monospace !important;
        background-color: #060810 !important;
        border: 1px solid #263049 !important;
        border-radius: 10px !important;
    }

    [data-testid="stChatInput"] {
        border: 1px solid var(--sz-border) !important;
        border-radius: 26px !important;
        background-color: var(--sz-surface) !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: var(--sz-cyan) !important;
        box-shadow: 0 0 0 3px rgba(34,211,238,0.15) !important;
    }

    /* ---------- ANIMATIONS ---------- */
    @keyframes szGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes szFadeUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes szGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(99,102,241,0.25); }
        50% { box-shadow: 0 0 34px rgba(168,85,247,0.4); }
    }

    /* ---------- HERO ---------- */
    .sz-hero { text-align:center; padding: 40px 10px 18px 10px; animation: szFadeUp 0.5s ease-out; }
    .sz-hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.6rem; font-weight: 700; margin: 0; letter-spacing: -0.5px;
        background: linear-gradient(100deg, var(--sz-cyan), var(--sz-indigo) 45%, var(--sz-violet) 80%, var(--sz-cyan));
        background-size: 300% 300%;
        -webkit-background-clip: text; background-clip: text; color: transparent;
        animation: szGradient 7s ease infinite;
    }
    .sz-hero p { color: var(--sz-muted); font-size: 1rem; margin-top: 10px; font-weight: 400; }
    .sz-hero-mini h2 { font-size: 1.5rem; }

    /* ---------- SUGGESTION CHIPS ---------- */
    .stButton > button {
        transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important;
        border-radius: 14px !important;
        border: 1px solid var(--sz-border) !important;
        background-color: var(--sz-surface) !important;
        color: var(--sz-text) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: var(--sz-cyan) !important;
        box-shadow: 0 8px 20px -6px rgba(34,211,238,0.35) !important;
    }
    button[kind="primary"] {
        background: linear-gradient(120deg, var(--sz-cyan), var(--sz-indigo)) !important;
        border: none !important;
        color: #05070d !important;
        font-weight: 700 !important;
    }

    /* ---------- MODEL CARD ---------- */
    .model-pill {
        border: 1px solid var(--sz-border); border-radius: 14px; padding: 10px 14px;
        margin-bottom: 8px; background: var(--sz-bg-soft);
    }
    .model-pill b { color: var(--sz-text); }
    .model-pill span { color: var(--sz-muted); font-size: 0.8rem; }

    /* ---------- LOCK CARD (misafir kilit bildirimi) ---------- */
    .lock-card {
        border: 1px dashed #3a4260; border-radius: 16px; padding: 16px;
        background: linear-gradient(160deg, #10162a 0%, #0c0f1a 100%);
        text-align: center; margin-top: 10px;
    }
    .lock-card .lock-emoji { font-size: 1.6rem; }
    .lock-card p { color: var(--sz-muted); font-size: 0.83rem; margin: 6px 0 0 0; }

    /* ---------- STUDIO PANEL ---------- */
    .studio-panel {
        background: linear-gradient(160deg, #10162a 0%, #0c1120 100%);
        border: 1px solid var(--sz-border);
        padding: 26px; border-radius: 22px; margin-bottom: 20px;
        animation: szGlow 4s ease-in-out infinite, szFadeUp 0.4s ease-out;
    }
    .studio-panel h4 { margin-top:0; font-family:'Space Grotesk', sans-serif; }

    .gallery-card {
        background: var(--sz-surface); border: 1px solid var(--sz-border);
        padding: 14px; border-radius: 16px; margin-bottom: 12px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .gallery-card:hover { transform: translateY(-3px); box-shadow: 0 10px 24px -8px rgba(56,189,248,0.3); }

    .launch-game-btn {
        display: inline-block;
        background: linear-gradient(120deg, var(--sz-cyan), var(--sz-indigo));
        color: #05070d !important; font-weight: 700; font-size: 1rem;
        padding: 13px 26px; border-radius: 14px; text-decoration: none !important;
        box-shadow: 0 0 24px rgba(34,211,238,0.35);
        transition: all 0.25s ease; text-align:center; margin: 12px 6px 4px 0;
    }
    .launch-game-btn:hover { transform: translateY(-3px); box-shadow: 0 0 32px rgba(99,102,241,0.6); }

    .badge {
        display:inline-block; padding:3px 10px; border-radius:8px;
        background: var(--sz-bg-soft); border:1px solid var(--sz-border);
        font-size:0.75rem; color: var(--sz-cyan); margin-right:6px;
    }

    /* ---------- AUTH CARD ---------- */
    [data-testid="stTextInput"] input {
        background-color: var(--sz-bg-soft) !important;
        border: 1px solid var(--sz-border) !important;
        border-radius: 12px !important; color: var(--sz-text) !important;
        padding: 10px 14px !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: var(--sz-cyan) !important;
        box-shadow: 0 0 14px rgba(34,211,238,0.35) !important;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        background-color: var(--sz-bg-soft); border-radius: 12px 12px 0 0;
        padding: 10px 22px; color: var(--sz-muted); font-weight: 600;
        border: 1px solid var(--sz-border);
    }
    .stTabs [aria-selected="true"] {
        background-color: #16233c !important; color: var(--sz-cyan) !important;
        border-color: var(--sz-cyan) !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 24px !important; border-color: var(--sz-border) !important;
        background: linear-gradient(160deg, #10162a 0%, #0b0e18 100%) !important;
        box-shadow: 0 0 50px rgba(99,102,241,0.12);
        animation: szFadeUp 0.5s ease-out;
    }
    .auth-logo-ring {
        width: 74px; height: 74px; margin: 0 auto 8px auto; border-radius: 50%;
        display:flex; align-items:center; justify-content:center; font-size: 2rem;
        background: linear-gradient(135deg, var(--sz-cyan), var(--sz-indigo) 60%, var(--sz-violet));
        box-shadow: 0 0 30px rgba(99,102,241,0.5); animation: szGlow 3.4s ease-in-out infinite;
    }
    .auth-caption { text-align:center; color: var(--sz-muted); font-size:0.85rem; margin-bottom:16px; }

    [data-testid="stFileUploaderDropzone"] {
        border: 2px dashed var(--sz-cyan) !important;
        background-color: #0a0e18 !important; border-radius: 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# 2b. YAN MENÜ (SIDEBAR) AÇMA/KAPAMA DÜĞMESİ — EK GÜVENCE
# ---------------------------------------------------------------------
# Streamlit'in kendi sidebar açma/kapama okuna ek olarak, sürümden bağımsız
# çalışan, her zaman ekranda kalan küçük bir "☰" düğmesi ekliyoruz. Bu düğme
# tıklandığında, sayfada bulunan Streamlit'in yerleşik sidebar kontrolüne
# (hangi test-id ile geliyorsa) otomatik olarak tıklar. Böylece kullanıcı
# sidebar'ı kapattıktan sonra "bir daha açılmıyor" sorunu yaşamaz.
st.components.v1.html(
    """
    <script>
    (function(){
        const parentDoc = window.parent.document;
        if (parentDoc.getElementById('sz-sidebar-toggle-btn')) { return; }
        const btn = parentDoc.createElement('button');
        btn.id = 'sz-sidebar-toggle-btn';
        btn.innerHTML = '☰';
        btn.title = 'Menüyü Aç/Kapat';
        Object.assign(btn.style, {
            position: 'fixed', top: '12px', left: '12px', zIndex: 999999,
            width: '38px', height: '38px', borderRadius: '10px',
            border: '1px solid #232a3d', background: '#131829',
            color: '#22d3ee', fontSize: '18px', cursor: 'pointer',
            boxShadow: '0 6px 18px rgba(0,0,0,0.35)'
        });
        btn.onclick = function(){
            const selectors = [
                '[data-testid="collapsedControl"] button',
                '[data-testid="collapsedControl"]',
                '[data-testid="stSidebarCollapseButton"] button',
                '[data-testid="stSidebarCollapseButton"]',
                '[data-testid="stSidebarCollapsedControl"] button',
                '[data-testid="stSidebarCollapsedControl"]'
            ];
            for (const sel of selectors) {
                const el = parentDoc.querySelector(sel);
                if (el) { el.click(); return; }
            }
        };
        parentDoc.body.appendChild(btn);
    })();
    </script>
    """,
    height=0,
)

# =====================================================================
# 3. VERİ DEPOLARI
# =====================================================================
DATA_DIR = "sazan_data"
os.makedirs(DATA_DIR, exist_ok=True)

AUTH_FILE = os.path.join(DATA_DIR, "sazan_auth.json")
CHATS_FILE = os.path.join(DATA_DIR, "sazan_chats.json")
GAMES_LIBRARY_FILE = os.path.join(DATA_DIR, "sazan_games_library.json")
IMAGE_GALLERY_FILE = os.path.join(DATA_DIR, "sazan_image_gallery.json")

# "Beni hatırla" çerezlerinin isimleri ve geçerlilik süresi (gün)
REMEMBER_EMAIL_COOKIE = "sazan_remember_email"
REMEMBER_TOKEN_COOKIE = "sazan_remember_token"
REMEMBER_DAYS = 30


class SazanStore:
    @staticmethod
    def load(path, default):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return default
        return default

    @staticmethod
    def save(path, data):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Depolama yazma hatası: {e}")


DIL_MATRISI = {
    "Türkçe 🇹🇷": "tr",
    "English 🇺🇸": "en",
    "Deutsch 🇩🇪": "de",
    "Français 🇫🇷": "fr",
    "Русский 🇷🇺": "ru",
    "日本語 🇯🇵": "ja",
}

QUICK_SUGGESTIONS = [
    "🏎️ Engellerden kaçılan bir arabalı yarış oyunu yap",
    "🐍 Skor tablolu modern bir yılan (snake) oyunu üret",
    "💡 Bana bugün için üretkenlik tüyoları ver",
    "📈 Basit bir bütçe takip tablosu nasıl kurarım?",
    "🧠 Kuantum bilgisayarları 5 yaşındaki bir çocuğa anlat",
    "🃏 Kart eşleştirme hafıza oyunu (memory match) oluştur",
]

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

# Kullanıcının, ürettiği içeriklerin telif hakkı sorumluluğunun kendisine ait
# olduğunu onaylamasını istediğimiz metin. Giriş / kayıt ekranında gösterilir.
TELIF_ONAY_METNI = """
**Kullanım Şartları ve Telif Hakkı Bildirimi**

- Sazan AI ile ürettiğiniz tüm içeriklerin (metin, kod, oyun, görsel, 3D model) kullanım,
  paylaşım ve **telif hakkı sorumluluğu tamamen size (kullanıcıya) aittir.**
- Sazan AI; görsel üretiminde üçüncü taraf servisler, metin üretiminde ise büyük dil
  modelleri kullanır. Üretilen içerik bazen hatalı, güncel olmayan veya yanıltıcı olabilir;
  önemli kararlar almadan önce bilgiyi doğrulamanız önerilir.
- Telif hakkıyla korunan (marka, karakter, ünlü kişi, şarkı sözü vb.) içerik üretimi talep
  etmek ve bu içeriği kullanmak sizin sorumluluğunuzdadır.
- Bu kutuyu işaretleyerek yukarıdaki maddeleri okuduğunuzu ve kabul ettiğinizi beyan
  edersiniz.
"""

# =====================================================================
# 4. KİMLİK DOĞRULAMA (GMAIL + ŞİFRE + "BENİ HATIRLA")
# =====================================================================
GMAIL_REGEX = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9])?@gmail\.com$", re.IGNORECASE)


class SazanAuth:
    @staticmethod
    def _load():
        return SazanStore.load(AUTH_FILE, {})

    @staticmethod
    def _save(db):
        SazanStore.save(AUTH_FILE, db)

    @staticmethod
    def is_valid_gmail(email: str) -> bool:
        return bool(GMAIL_REGEX.match((email or "").strip()))

    @staticmethod
    def email_exists(email: str) -> bool:
        return email.strip().lower() in SazanAuth._load()

    @staticmethod
    def _hash(password: str, salt: str) -> str:
        return hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()

    @staticmethod
    def register(email: str, password: str):
        db = SazanAuth._load()
        key = email.strip().lower()
        salt = uuid.uuid4().hex
        db[key] = {
            "salt": salt,
            "password_hash": SazanAuth._hash(password, salt),
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "remember_salt": None,
            "remember_token_hash": None,
        }
        SazanAuth._save(db)

    @staticmethod
    def verify(email: str, password: str) -> bool:
        rec = SazanAuth._load().get(email.strip().lower())
        if not rec:
            return False
        return SazanAuth._hash(password, rec["salt"]) == rec["password_hash"]

    # ---------- "BU CİHAZDA BENİ HATIRLA" (isteğe bağlı) ----------
    @staticmethod
    def create_remember_token(email: str) -> str:
        """Kullanıcı 'beni hatırla' kutusunu işaretlediyse çağrılır.
        Şifreyi ASLA çereze yazmayız; bunun yerine rastgele, tek kullanımlık bir
        'hatırlama token'ı üretip sadece bu token'ın HASH'ini veritabanına yazarız.
        Ham token, tarayıcı çerezine yazılmak üzere geri döner."""
        db = SazanAuth._load()
        key = email.strip().lower()
        if key not in db:
            return ""
        raw_token = uuid.uuid4().hex + uuid.uuid4().hex
        remember_salt = uuid.uuid4().hex
        db[key]["remember_salt"] = remember_salt
        db[key]["remember_token_hash"] = SazanAuth._hash(raw_token, remember_salt)
        SazanAuth._save(db)
        return raw_token

    @staticmethod
    def verify_remember_token(email: str, raw_token: str) -> bool:
        if not email or not raw_token:
            return False
        rec = SazanAuth._load().get(email.strip().lower())
        if not rec or not rec.get("remember_token_hash") or not rec.get("remember_salt"):
            return False
        return SazanAuth._hash(raw_token, rec["remember_salt"]) == rec["remember_token_hash"]

    @staticmethod
    def clear_remember_token(email: str):
        """Kullanıcı 'çıkış yap' derse veya 'beni hatırla'yı iptal ederse
        cihazdaki eski token'ı geçersiz kılmak için sunucu tarafındaki hash'i siler."""
        db = SazanAuth._load()
        key = (email or "").strip().lower()
        if key in db:
            db[key]["remember_salt"] = None
            db[key]["remember_token_hash"] = None
            SazanAuth._save(db)


# =====================================================================
# 5. KALICI SOHBET / OYUN / GÖRSEL DEPOLARI (SADECE ÜYELER İÇİN)
# =====================================================================
class SazanChatStore:
    @staticmethod
    def get_sessions(u):
        db = SazanStore.load(CHATS_FILE, {})
        return db.get(u, {"💬 Yeni Sohbet": []})

    @staticmethod
    def save_sessions(u, sessions):
        db = SazanStore.load(CHATS_FILE, {})
        db[u] = sessions
        SazanStore.save(CHATS_FILE, db)


class SazanGameLibrary:
    @staticmethod
    def get_library(u):
        return SazanStore.load(GAMES_LIBRARY_FILE, {}).get(u, [])

    @staticmethod
    def add_game(u, title, code):
        db = SazanStore.load(GAMES_LIBRARY_FILE, {})
        db.setdefault(u, [])
        entry = {
            "id": uuid.uuid4().hex[:10],
            "title": title[:70],
            "code": code,
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
        db[u].insert(0, entry)
        db[u] = db[u][:50]
        SazanStore.save(GAMES_LIBRARY_FILE, db)
        return entry

    @staticmethod
    def delete_game(u, game_id):
        db = SazanStore.load(GAMES_LIBRARY_FILE, {})
        if u in db:
            db[u] = [g for g in db[u] if g["id"] != game_id]
            SazanStore.save(GAMES_LIBRARY_FILE, db)


class SazanImageGallery:
    @staticmethod
    def get_gallery(u):
        return SazanStore.load(IMAGE_GALLERY_FILE, {}).get(u, [])

    @staticmethod
    def add_image(u, prompt, stil, img_bytes):
        db = SazanStore.load(IMAGE_GALLERY_FILE, {})
        db.setdefault(u, [])
        entry = {
            "id": uuid.uuid4().hex[:10],
            "prompt": prompt,
            "stil": stil,
            "image_b64": base64.b64encode(img_bytes).decode("utf-8"),
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
        db[u].insert(0, entry)
        db[u] = db[u][:60]
        SazanStore.save(IMAGE_GALLERY_FILE, db)
        return entry

    @staticmethod
    def delete_image(u, image_id):
        db = SazanStore.load(IMAGE_GALLERY_FILE, {})
        if u in db:
            db[u] = [g for g in db[u] if g["id"] != image_id]
            SazanStore.save(IMAGE_GALLERY_FILE, db)


# =====================================================================
# 6. GROQ MOTORU & MODEL KATALOĞU
# =====================================================================
# ── API KEY ROL HARİTASI ─────────────────────────────────────────────
# secrets.toml'a (veya Streamlit Cloud Secrets'a) şu şekilde ekle:
#
#   GROQ_API_KEY   = "gsk_..."   # Key 1 → sohbet / normal yazışma
#   GROQ_API_KEY_2 = "gsk_..."   # Key 2 → sohbet / normal yazışma (round-robin)
#   GROQ_API_KEY_3 = "gsk_..."   # Key 3 → görsel üretimi + 3D baskı
#   GROQ_API_KEY_4 = "gsk_..."   # Key 4 → hacker modu (kod yazımı)
#
# Eksik key varsa fallback: görsel/3D → KEY 1, hacker → KEY 1.

def _get_key(name: str) -> str | None:
    return st.secrets.get(name, None)

# Her rol için key'leri çek
_KEY_CHAT   = [k for k in [_get_key("GROQ_API_KEY"), _get_key("GROQ_API_KEY_2")] if k]
_KEY_VISUAL = [k for k in [_get_key("GROQ_API_KEY_3")] if k] or _KEY_CHAT
_KEY_HACKER = [k for k in [_get_key("GROQ_API_KEY_4")] if k] or _KEY_CHAT

if not _KEY_CHAT:
    st.error(
        "🚨 Hiçbir GROQ_API_KEY bulunamadı!\n\n"
        "`.streamlit/secrets.toml` dosyanıza şunları ekleyin:\n\n"
        'GROQ_API_KEY   = "gsk_sohbet_key_1"\n'
        'GROQ_API_KEY_2 = "gsk_sohbet_key_2"\n'
        'GROQ_API_KEY_3 = "gsk_gorsel_3d_key"\n'
        'GROQ_API_KEY_4 = "gsk_hacker_kod_key"'
    )
    st.stop()


class _GroqKeyPool:
    """
    Belirli bir key listesi üzerinde round-robin + otomatik fallback.
    Rate-limit / auth hatası → bir sonraki anahtara geç.
    """
    def __init__(self, keys: list[str]):
        self._keys = keys
        self._index = 0

    def _client(self, idx: int) -> Groq:
        return Groq(api_key=self._keys[idx % len(self._keys)])

    def create(self, **kwargs):
        total    = len(self._keys)
        last_exc = None
        for attempt in range(total):
            idx = (self._index + attempt) % total
            try:
                result = self._client(idx).chat.completions.create(**kwargs)
                self._index = (idx + 1) % total
                return result
            except Exception as e:
                err = str(e).lower()
                if any(k in err for k in ("rate_limit", "429", "quota", "auth", "invalid_api_key", "403")):
                    last_exc = e
                    continue
                raise
        raise last_exc


# Üç ayrı havuz — her biri kendi key setini kullanır
_pool_chat   = _GroqKeyPool(_KEY_CHAT)    # sohbet
_pool_visual = _GroqKeyPool(_KEY_VISUAL)  # görsel + 3D
_pool_hacker = _GroqKeyPool(_KEY_HACKER)  # hacker / kod


def _groq_create(pool: _GroqKeyPool, **kwargs):
    """Seçilen havuzu kullanarak completion isteği gönderir."""
    return pool.create(**kwargs)


# Eski groq_client shim'i — sadece sohbet havuzunu çağırır (legacy uyumluluk)
class _GroqClientShim:
    class _CompletionsShim:
        class _ChatShim:
            @staticmethod
            def create(**kwargs):
                return _pool_chat.create(**kwargs)
        completions = _ChatShim()
    chat = _CompletionsShim()


groq_client = _GroqClientShim()

# Misafirler bu tek modeli kullanır. Üyeler aşağıdaki 7 modelin tamamına erişir.
GUEST_MODEL_LABEL = "⚡ Sazan Hız"

AI_MODELS = {
    "⚡ Sazan Hız": {
        "id": "openai/gpt-oss-20b",
        "effort": "low",
        "temp": 0.55,
        "desc": "Anında yanıt veren en hızlı model. Günlük sohbetler için ideal.",
        "web_search": True,
    },
    "🧠 Sazan Dengeli": {
        "id": "openai/gpt-oss-120b",
        "effort": "medium",
        "temp": 0.4,
        "desc": "Hız ve akıl yürütme gücü arasında dengeli, günlük kullanım için önerilir.",
        "web_search": True,
    },
    "👑 Sazan Ultra": {
        "id": "openai/gpt-oss-120b",
        "effort": "high",
        "temp": 0.3,
        "desc": "En güçlü akıl yürütme motoru. Karmaşık kod ve oyun üretimi için.",
        "web_search": True,
    },
    "🔬 Sazan Derin Analiz": {
        "id": "openai/gpt-oss-120b",
        "effort": "high",
        "temp": 0.15,
        "desc": "Adım adım, titiz ve uzun analitik yanıtlar üretir.",
        "web_search": True,
    },
    "🎨 Sazan Görsel Akıl": {
        "id": "qwen/qwen3.6-27b",
        "effort": "default",
        "temp": 0.5,
        "desc": "Çok modlu düşünce yapısı; yaratıcı ve görsel-duyarlı yanıtlarda güçlü.",
        "web_search": False,
    },
    "🛡️ Sazan Güvenli Mod": {
        "id": "openai/gpt-oss-safeguard-20b",
        "effort": "medium",
        "temp": 0.35,
        "desc": "Ekstra güvenlik katmanlı, hassas konularda temkinli yanıtlar.",
        "web_search": False,
    },
    "🌐 Sazan Ajan (Compound)": {
        "id": "groq/compound",
        "effort": None,
        "temp": 0.4,
        "desc": "Güncel olayları otomatik olarak web'den arayıp kod da çalıştırabilen ajan sistemi.",
        "web_search": False,  # groq/compound zaten kendi web aramasını otomatik yapar
    },
}

# Uygulamanın "bugün" olarak bildiği tarih — modelin eski eğitim verisine değil,
# bu tarihe ve (varsa) canlı arama sonuçlarına güvenmesi için sistem promptuna eklenir.
SAZAN_TODAY_STR = datetime.now().strftime("%d %B %Y")
SAZAN_TODAY_YEAR = datetime.now().strftime("%Y")

MAX_CONTINUATIONS = 4
DEFAULT_MAX_TOKENS = 3000  # TPM limitine takılmamak için ölçülü tutuluyor (continuation ile tamamlanır)
SEARCH_MAX_TOKENS = 4000   # Arama sonuçlarını kaynak/tarihiyle birlikte özetleyebilmek için biraz daha geniş pay
MIN_MAX_TOKENS = 700

# Bu kelimelerden biri sorguda geçiyorsa, model "arama yapayım mı yapmayayım mı" diye
# tereddüt etmesin diye web aramasını ZORUNLU (tool_choice="required") hale getiriyoruz.
# "auto" bırakıldığında modeller genelde arama yapmadan eski bilgiyle uydurma yanıt
# verebiliyordu — bu, kullanıcının şikayet ettiği "saçma/yanlış güncel bilgi" sorununu çözer.
GUNCEL_BILGI_ANAHTAR_KELIMELER = [
    "güncel", "bugün", "bu yıl", "bu ay", "bu hafta", "geçen hafta", "geçen ay",
    "2023", "2024", "2025", "2026", "2027", "2028",
    "kadro", "kadrosu", "transfer", "skor", "maç sonucu", "puan durumu",
    "şampiyon", "final", "sonuç", "haberi", "haber", "son dakika", "gündem",
    "kim oldu", "kimdir", "kaç yaşında", "fiyat", "fiyatı", "ne kadar", "kaç para",
    "hava durumu", "döviz", "kur", "borsa", "altın fiyatı", "bitcoin",
    "cumhurbaşkanı", "başkan", "başbakan", "bakan", "ceo", "genel müdür",
    "hangi ülke", "nerede oynuyor", "en son", "yeni çıkan", "yeni model",
    "sürüm", "versiyon", "release", "şu an", "canlı", "az önce", "yakın zamanda",
    "hala", "hâlâ", "mı çıktı", "mi çıktı", "var mı", "kim kazandı", "ne zaman",
    "kim öldü", "vefat", "istifa", "seçim", "seçildi", "açıklandı", "duyuruldu",
]

# Türkçe büyük/küçük harf normalizasyonu (İ/I, ı/i vb.) casefold ile birebir
# çalışmadığı için anahtar kelime taramasını daha güvenilir hale getiren yardımcı.
_TR_CASEFOLD_MAP = str.maketrans({"İ": "i", "I": "ı", "Ş": "ş", "Ğ": "ğ", "Ü": "ü", "Ö": "ö", "Ç": "ç"})


def _tr_normalize(text: str) -> str:
    return (text or "").translate(_TR_CASEFOLD_MAP).casefold()


def _guncel_bilgi_sorusu_mu(prompt: str) -> bool:
    lowered = _tr_normalize(prompt)
    return any(_tr_normalize(k) in lowered for k in GUNCEL_BILGI_ANAHTAR_KELIMELER)


def _kisalt_gecmis_icerik(content, limit_chars=600):
    """Geçmiş mesajlardaki büyük ```html``` oyun kodlarını, sohbet bağlamını şişirip TPM
    limitini aşmaması için kısa bir özetle değiştirir. Sadece dışarıya gönderilecek
    mesaj geçmişinde kullanılır; kullanıcının gördüğü orijinal mesaj değişmez."""
    if "```html" in content:
        clean_text = re.sub(r"```html\s*.*?\s*```", "[Önceki mesajda bir HTML oyunu üretildi — kod bu bağlamdan kısaltıldı]", content, flags=re.DOTALL)
        return clean_text[:limit_chars]
    return content[:limit_chars] if len(content) > limit_chars else content


class SazanAIConception:
    @staticmethod
    def _tek_istek(messages, model_cfg, max_tokens=DEFAULT_MAX_TOKENS, force_search=False, pool=None):
        # pool belirtilmezse varsayılan sohbet havuzu kullanılır
        _pool = pool if pool is not None else _pool_chat
        kwargs = dict(
            model=model_cfg["id"],
            messages=messages,
            temperature=model_cfg.get("temp", 0.4),
            top_p=0.9,
            max_tokens=max_tokens,
        )
        effort = model_cfg.get("effort")
        if effort:
            kwargs["reasoning_effort"] = effort
        if model_cfg.get("web_search"):
            kwargs["tools"] = [{"type": "browser_search"}]
            kwargs["tool_choice"] = "required" if force_search else "auto"
        try:
            return _pool.create(**kwargs)
        except Exception as e:
            err_text = str(e).lower()
            if "tool" in err_text and ("support" in err_text or "unsupported" in err_text or "choice" in err_text):
                if kwargs.get("tool_choice") == "required":
                    kwargs["tool_choice"] = "auto"
                    try:
                        return _pool.create(**kwargs)
                    except Exception:
                        pass
                kwargs.pop("tools", None)
                kwargs.pop("tool_choice", None)
                try:
                    return _pool.create(**kwargs)
                except Exception:
                    pass
            if "reasoning_effort" in err_text or "unsupported" in err_text:
                kwargs.pop("reasoning_effort", None)
                return _pool.create(**kwargs)
            if "rate_limit_exceeded" in err_text or "413" in err_text or "too large" in err_text:
                smaller = max(MIN_MAX_TOKENS, int(max_tokens * 0.5))
                if smaller < max_tokens:
                    kwargs["max_tokens"] = smaller
                    return _pool.create(**kwargs)
            raise

    @staticmethod
    def _yanit_arama_izi_tasiyor_mu(cevap: str) -> bool:
        """Zorunlu arama istendiği halde model gerçekten arama yapıp kaynağa
        dayanmış mı, yoksa yine ezberinden mi yazmış — kaba bir kontrol.
        Kaynak/tarih/link göstergesi yoksa ikinci bir zorunlu-arama denemesi yaparız."""
        if not cevap:
            return False
        gosterge_kelimeler = [
            "kaynak", "http", "www.", ".com", ".com.tr", "tarihli", "haberine göre",
            "göre,", "sitesine göre", "verilerine göre", "güncellendi",
        ]
        lowered = _tr_normalize(cevap)
        return any(_tr_normalize(g) in lowered for g in gosterge_kelimeler)

    @staticmethod
    def query_agent(prompt, history, target_lang, model_cfg, hacker_mode=False):
        lowered = prompt.lower()
        if any(k in lowered for k in ["can muhammed çukur", "yapımcın kim", "yapımcısı", "kim yaptı"]):
            return (
                "Beni Can Muhammed Çukur tasarladı ve geliştirdi. "
                f"[Yanıt dili: {target_lang}]"
            )

        # ── HACKER MODU SİSTEM PROMPTU ────────────────────────────────
        if hacker_mode:
            # ── Hacker modu sistem promptu ──────────────────────────────
            # KURAL: sistem promptu + geçmiş + kullanıcı mesajı + max_tokens
            #        toplamı Groq'un TPM limitini (8000) aşmamalı.
            # Prompt ~650 token, geçmiş ~400 token, kullanıcı ~100 token → ~1150 token
            # Güvenli yanıt penceresi: 8000 - 1150 - 500 güvenlik tamponu = ~6350 → 2500
            # continuation ile 4 × 2500 = 10000 token'lık uzun kod çıkabilir.
            HACKER_MAX_TOKENS = 2500
            HACKER_GECMIS_KISALT = 300   # karakter — geçmiş mesaj kısaltma sınırı
            HACKER_GECMIS_ADET  = 4      # kaç geçmiş mesaj gönderilsin

            hacker_sys = (
                f"Sen Hacker Sazan — dünyanın en elit yazılım mühendisisin. Yanıt dili: {target_lang}\n\n"

                "KİMLİK: Ego yok, laf yok — cerrahi kod. 1-3 cümle özet, ardından kod.\n\n"

                "MİMARİ: SOLID + DI + katmanlı (küçük→fonksiyon, orta→sınıf, büyük→katman).\n\n"

                "KALİTE:\n"
                "• Type hints (Py/TS/Go) zorunlu; mypy strict.\n"
                "• Guard clause: erken return, derin nesting yok.\n"
                "• Custom exception hiyerarşisi; DRY; sabitler UPPER_SNAKE_CASE.\n"
                "• Pure fonksiyon tercih; immutable veri dönüşümü.\n\n"

                "PERFORMANS: O(n log n) tercih; döngüde I/O yok; object pool/generator.\n\n"

                "GÜVENLİK: Input validation; parameterized SQL; innerHTML yasak;\n"
                "bcrypt/argon2; secrets .env'de; rate limiting her endpoint'te.\n\n"

                "TEST: Her public fonksiyon için happy-path + edge + hata case.\n"
                "Python: pytest parametrize. JS/TS: Jest describe/it.\n\n"

                "ASYNC: asyncio+aiohttp (Py); async/await (JS) — .then() yasak;\n"
                "timeout + cancellation token her operasyonda.\n\n"

                "LOG: logging/winston; print/console.log production'da yasak;\n"
                "structured JSON log; PII asla log'a.\n\n"

                "ÇIKTI: doğru dil etiketi (```python, ```ts...); çok dosya → ayrı blok;\n"
                "blok üstü '# filename: x.py'; blok sonrası kurulum adımları.\n\n"

                "YASAK: stub/TODO, var/any/bare-except, eval/innerHTML,\n"
                "hardcoded secret, döngüde sync-I/O, magic number, callback hell.\n\n"

                "Kodu ASLA yarım bırakma — son satıra kadar eksiksiz tamamla."
            )

            messages = [{"role": "system", "content": hacker_sys}]
            # Geçmiş mesajları çok kısa tut — TPM bütçesini kullanıcı mesajına ve
            # yanıta bırakmak için geçmiş adetini ve karakter limitini kısıyoruz.
            for m in history[-HACKER_GECMIS_ADET - 1 : -1]:
                messages.append({
                    "role": m["role"],
                    "content": _kisalt_gecmis_icerik(m["content"], limit_chars=HACKER_GECMIS_KISALT),
                })
            messages.append({"role": "user", "content": prompt})

            try:
                res = SazanAIConception._tek_istek(
                    messages, model_cfg,
                    max_tokens=HACKER_MAX_TOKENS,
                    force_search=False,
                    pool=_pool_hacker,
                )
                combined = res.choices[0].message.content or ""
                finish_reason = res.choices[0].finish_reason
                attempts = 0
                while finish_reason == "length" and attempts < MAX_CONTINUATIONS:
                    messages.append({"role": "assistant", "content": combined})
                    messages.append({
                        "role": "user",
                        "content": "Kaldığın satırdan itibaren devam et, başa dönme.",
                    })
                    res2 = SazanAIConception._tek_istek(
                        messages, model_cfg,
                        max_tokens=HACKER_MAX_TOKENS,
                        pool=_pool_hacker,
                    )
                    combined += res2.choices[0].message.content or ""
                    finish_reason = res2.choices[0].finish_reason
                    attempts += 1
                return combined
            except Exception as e:
                err = str(e)
                # TPM limiti yine de aşıldıysa daha küçük tokenla son bir kez dene
                if "413" in err or "rate_limit_exceeded" in err or "too large" in err:
                    try:
                        # geçmişi tamamen çıkar, sadece sys + user
                        msgs_minimal = [
                            {"role": "system", "content": hacker_sys},
                            {"role": "user", "content": prompt},
                        ]
                        res_min = SazanAIConception._tek_istek(
                            msgs_minimal, model_cfg,
                            max_tokens=1500,
                            force_search=False,
                            pool=_pool_hacker,
                        )
                        return res_min.choices[0].message.content or ""
                    except Exception as e2:
                        return (
                            f"⚠️ Hacker Mod: İstek hâlâ çok büyük ({e2}). "
                            "Lütfen soruyu daha kısa yaz veya yeni sohbet aç."
                        )
                return f"⚠️ Hacker Mod hatası: {e}"
        # ── NORMAL MOD DEVAM ─────────────────────────────────────────

        force_search = model_cfg.get("web_search", False) and _guncel_bilgi_sorusu_mu(prompt)

        # Oyun isteklerini tespit et — daha genis token penceresi ac
        _OYUN_KELIMELERI = [
            "oyun", "game", "oyunu", "oynak", "oyna", "snake", "tetris", "platform",
            "mario", "shooter", "araba", "racing", "puzzle", "bulmaca", "quiz",
            "labirent", "maze", "flappy", "pong", "breakout", "pacman", "pac-man",
            "canavar", "zombie", "uzay", "space", "asteroids", "dungeon", "rpg",
            "tower defense", "strateji", "kart oyunu", "memory", "hafiza", "match",
            "interaktif", "simulasyon", "simulation", "mini uygulama",
        ]
        _lowered_tr = _tr_normalize(prompt)
        is_game_request = any(_tr_normalize(k) in _lowered_tr for k in _OYUN_KELIMELERI)
        GAME_MAX_TOKENS = 7000

        if is_game_request:
            max_tokens_bu_istek = GAME_MAX_TOKENS
        elif force_search:
            max_tokens_bu_istek = SEARCH_MAX_TOKENS
        else:
            max_tokens_bu_istek = DEFAULT_MAX_TOKENS

        sys_prompt = (
            "Sen Sazan AI adında, sıcak, net ve yardımsever genel amaçlı bir yapay zeka "
            "asistanısın. Kullanıcıyla doğal bir sohbet dilinde konuş, sorularını dikkatle "
            "analiz et ve doğrudan, faydalı yanıtlar ver.\n\n"

            f"BUGÜNÜN GERÇEK TARİHİ: {SAZAN_TODAY_STR} ({SAZAN_TODAY_YEAR} yılındayız). "
            "Eğitim verin bundan çok daha eski bir tarihte kesilmiş olabilir; bu yüzden "
            "GÜNCEL bilgi gerektiren her konuda (spor transferleri, kadrolar, skorlar, "
            "haberler, hangi kişinin hangi görevde olduğu, fiyatlar, hava durumu, sürümler "
            "vb.) ASLA eski eğitim verinden tahmin yürütme veya uydurma.\n\n"

            "ARAMA GÜVENİLİRLİĞİ İÇİN KESİN KURALLAR:\n"
            "1. Elinde bir web arama aracı varsa (browser_search) onu MUTLAKA kullanarak "
            f"güncel ve doğrulanmış bilgiyi getir. Arama yaparken sorguna gerektiğinde {SAZAN_TODAY_YEAR} "
            "yılını ekle ki eski/arşiv sonuçlar yerine en güncel sonuçlar gelsin.\n"
            "2. TEK bir aramayla yetinme. En az 2 farklı sorgu dene (örneğin biri Türkçe, "
            "biri gerekiyorsa İngilizce anahtar kelimelerle) ve sonuçları birbirleriyle "
            "karşılaştır. Sonuçlar çelişiyorsa, tarihi en yakın ve en güvenilir kaynağı "
            "(resmi kurum, büyük haber ajansı, şirketin kendi sitesi) esas al.\n"
            "3. Bulduğun sonucun TARİHİNE bak. Eğer sonuç bugünün tarihinden çok eskiyse "
            "veya konuyla ilgisiz görünüyorsa, farklı anahtar kelimelerle YENİDEN ara; "
            "ilk bulduğun sonucu sorgulamadan doğru kabul etme.\n"
            "4. Yanıtını SADECE arama sonuçlarına dayandır; kendi eski eğitim bilgini "
            "arama sonucuyla karıştırıp yorumlama veya 'muhtemelen böyledir' diye tahmin "
            "üretme.\n"
            "5. Güncel bilgi veren her yanıtın sonuna, hangi kaynağa/kaynaklara dayandığını "
            "kısaca belirt (ör. 'Kaynak: [site adı], [gün ay yıl]'). Bu, kullanıcının "
            "bilgiyi doğrulayabilmesi için zorunludur.\n"
            "6. Arama aracın yoksa, sonuç bulamazsan veya sonuçlar birbiriyle çelişiyorsa, "
            "bunu kullanıcıya açıkça söyle ('şu an bunu kesin doğrulayamıyorum, güncel bir "
            "kaynaktan teyit etmeni öneririm' gibi). Kafandan isim, sayı, tarih veya olay "
            "UYDURMA.\n"
            "7. Yanlış ama kendinden emin görünen bir cevap vermek, dürüstçe 'emin değilim' "
            "demekten çok daha kötüdür — belirsizlik payını her zaman açıkça belirt.\n\n"

            # ═══════════════════════════════════════════════════════════════════
            # OYUN & İNTERAKTİF UYGULAMA ÜRETİMİ
            # ═══════════════════════════════════════════════════════════════════
            "╔══════════════════════════════════════════════════════════════════╗\n"
            "║   OYUN & İNTERAKTİF UYGULAMA ÜRETİMİ — USTA SEVİYE STANDART   ║\n"
            "╚══════════════════════════════════════════════════════════════════╝\n\n"
            "Kullanıcı senden oyun, mini-uygulama veya interaktif deneyim istediğinde\n"
            "aşağıdaki TÜM kurallara eksiksiz uy. Hiçbir kural isteğe bağlı değildir.\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "BÖLÜM 1 — MİMARİ & YAZILIM MÜHENDİSLİĞİ\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "1.1  DOSYA YAPISI\n"
            "  • Tek bir self-contained HTML dosyası; <head>/<style>/<script> hepsi içinde.\n"
            "  • Dış CDN, harici font, resim URL'si veya ses dosyası linki KESİNLİKLE YASAK.\n"
            "    Font gerekiyorsa CSS @font-face + base64 data-URI veya system-ui kullan.\n"
            "  • Dosya, tarayıcıda data:text/html;base64,... URL'si olarak da çalışmalı.\n\n"

            "1.2  JAVASCRIPT MİMARİSİ\n"
            "  • Dosyanın başına 'use strict'; yaz; tüm kod ES2020+ sözdiziminde olsun.\n"
            "  • Her bağımsız kavram kendi class'ında: Vector2, Entity, Player, Enemy,\n"
            "    Bullet, Particle, ParticleSystem, PowerUp, Camera, InputManager,\n"
            "    AudioEngine, ScoreManager, StorageManager — gereken tüm sınıfları yaz.\n"
            "  • Sınıf ilişkileri: composition over inheritance — Entity base class'ı\n"
            "    içinde update(dt)/draw(ctx)/destroy() metodları; alt sınıflar extend eder.\n"
            "  • Tüm magic number'lar dosyanın tepesinde const CONFIG = {...} bloğunda;\n"
            "    oyun içinde CONFIG.PLAYER_SPEED gibi kullan, asla 42 veya 0.016 gibi\n"
            "    ham sayı yazma.\n"
            "  • Obje pooling: Bullet, Particle, Enemy gibi sık create/destroy edilen\n"
            "    nesneler için object pool uygula (GC baskısını azalt).\n"
            "  • Quadtree veya spatial hashing: 20+ düşman varsa çarpışma tespitini\n"
            "    brute-force O(n²) yerine O(n log n) ile yap.\n"
            "  • Event sistemi: oyun olayları (ENEMY_KILLED, POWER_UP_COLLECTED,\n"
            "    LEVEL_COMPLETE) için basit EventEmitter sınıfı; modüller birbirini\n"
            "    doğrudan çağırmak yerine event dinlesin.\n"
            "  • Kodu asla yarım bırakma — son kapanış tag'ına kadar eksiksiz yaz.\n\n"

            "1.3  OYUN DÖNGÜSÜ & ZAMANLAMA\n"
            "  • requestAnimationFrame(gameLoop) tabanlı ana döngü.\n"
            "  • Delta-time: dt = Math.min((now - lastTime) / 1000, 0.05) — 50ms cap\n"
            "    ile çok yavaş kare hızında patlamamayı önle.\n"
            "  • Fizik ve oyun mantığı dt ile çarp; frame-rate bağımsız hareket.\n"
            "  • Sabit fizik adımı (fixed timestep) gerekiyorsa accumulator pattern uygula.\n"
            "  • FPS sayacı: sağ üst köşede küçük, yarı saydam göster (geliştirici modu).\n\n"

            "1.4  STATE MACHINE\n"
            "  • Merkezi GameState: LOADING → MENU → PLAYING → PAUSED →\n"
            "    LEVEL_COMPLETE → GAME_OVER → (CREDITS) döngüsü.\n"
            "  • Her state geçişinde önceki state'i temizle (timer, event listener vb.).\n"
            "  • Transition animasyonu: state değişiminde 300ms fade-in/out.\n\n"

            "1.5  RESPONSIVE & ÇÖZÜNÜRLÜK\n"
            "  • Canvas boyutu: window.innerWidth × window.innerHeight (tam ekran).\n"
            "  • window 'resize' olayında canvas'ı yeniden boyutlandır + tüm\n"
            "    pozisyon/boyut hesaplamalarını viewport oranına göre yeniden ölçekle.\n"
            "  • devicePixelRatio desteği: canvas.width = w * dpr; ctx.scale(dpr, dpr)\n"
            "    ile retina ekranlarda keskin görüntü.\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "BÖLÜM 2 — GÖRSEL KALİTE & SANAT\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "2.1  ARKA PLAN & ATMOSFER\n"
            "  • Saf siyah (#000) arka plan kesinlikle yasak. Şunlardan birini seç:\n"
            "    (a) Yıldız alanı: 200+ nokta, parallax katmanlar (yakın=hızlı, uzak=yavaş)\n"
            "    (b) Neon ızgara (tron-tarzı) perspektif animasyonu\n"
            "    (c) Procedural nebula: Perlin-benzeri noise ile renkli bulut efekti\n"
            "    (d) Dinamik gradient: hsl() renk döngüsü ile yavaş akan arka plan\n"
            "  • Arka plan katmanları için offscreen canvas kullan, her kare yeniden\n"
            "    çizme; scroll/parallax efektini transform ile uygula.\n\n"

            "2.2  VARLIK ÇİZİMİ\n"
            "  • Her varlık (oyuncu, düşman, mermi, platform, coin) en az 2 renk\n"
            "    içeren radial veya linear gradient ile doldurulsun.\n"
            "  • ctx.shadowBlur + ctx.shadowColor ile neon/glow efekti — varlıklar\n"
            "    'parlıyor' gibi görünsün.\n"
            "  • Sprite sheet yerine Canvas API ile çizilen vektör sanat yap:\n"
            "    bezier eğrileri, arc, polygon; karakterlerin göz, anten, kanat\n"
            "    gibi detayları olsun.\n"
            "  • Tween sınıfı yaz (from/to/duration/easing); scale pulse, alpha fade,\n"
            "    rotation wobble gibi animasyonlar bu sınıf üzerinden çalışsın.\n\n"

            "2.3  PARTİKÜL SİSTEMİ\n"
            "  • ParticleSystem sınıfı: spawn(x, y, config) ile farklı tipte\n"
            "    parçacık grupları fırlat.\n"
            "  • Parçacık tipleri:\n"
            "    - EXPLOSION: 20-40 parçacık, radyal yayılma, turuncu→kırmızı→şeffaf\n"
            "    - SPARKLE: 8-12 parçacık, yıldız şekli, beyaz→sarı\n"
            "    - TRAIL: oyuncu/düşman hareketinde iz bırakan küçük noktalar\n"
            "    - SCORE_POP: +100 gibi floating text, yukarı kayarak solar\n"
            "    - LEVEL_UP: ekranı dolduran 60+ parçacık, konfeti efekti\n"
            "  • Object pool ile parçacıkları yeniden kullan; max 500 aktif parçacık.\n\n"

            "2.4  KAMERA\n"
            "  • Camera sınıfı: x, y, zoom, shake(intensity, duration) metodları.\n"
            "  • Oyuncu harekete geçince smooth follow: cam.x += (target.x - cam.x) * 0.1\n"
            "  • Hasar aldığında screen shake: rastgele offset, her kare sönümlenerek sıfır.\n"
            "  • Zoom animasyonu: seviye başında zoom-in, level complete'de zoom-out.\n"
            "  • ctx.save() / ctx.translate(cx, cy) / ctx.scale() / ctx.restore() ile\n"
            "    düzgün camera transform uygula.\n\n"

            "2.5  UI & HUD TASARIMI\n"
            "  • Tüm UI elemanları CSS değil Canvas üzerinde çizilsin.\n"
            "  • Skor paneli: sol üstte yarı-saydam (#ffffff15) yuvarlak dikdörtgen,\n"
            "    içinde 🏆 ikon + skor (gradient fill metin).\n"
            "  • Can göstergesi: kalp ikonları veya dolup biten animasyonlu bar.\n"
            "  • Level/dalga göstergesi: sağ üstte parlayan rozet.\n"
            "  • Combo metni: ekran ortasında büyük, 1 saniye görünür, scale animasyonlu.\n"
            "  • Minimap: sağ altta küçük overheadview (harita büyükse).\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "BÖLÜM 3 — SES & MÜZİK\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "3.1  AUDIO ENGINE\n"
            "  • AudioEngine sınıfı; AudioContext'i lazy init et (kullanıcı etkileşimi\n"
            "    sonrasında, tarayıcı politikası gereği).\n"
            "  • masterGain, sfxGain, musicGain zinciri; M tuşu ile mute toggle.\n"
            "  • playNote(freq, type, duration, gainVal) yardımcı fonksiyonu.\n\n"

            "3.2  SENTEZLENMIŞ SFX (ZORUNLU — dış dosya yasak)\n"
            "  Web Audio API OscillatorNode + GainNode + BiquadFilterNode ile:\n"
            "  • ATIŞ: kısa 'pew' (sine 880Hz → 220Hz, 80ms)\n"
            "  • DÜŞMAN ÖLÜMÜ: 'crunch' (sawtooth 400→100Hz, distortion, 150ms)\n"
            "  • OYUNCU HASAR: 'thud' (triangle 200Hz, vibrato, 200ms)\n"
            "  • COIN/PUAN TOPLAMA: 'ding' (sine 880Hz + 1200Hz harmonik, 100ms)\n"
            "  • LEVEL-UP: artan arpeggio (C4-E4-G4-C5 dizisi, 400ms)\n"
            "  • GAME OVER: alçalan melodi (G4-E4-C4-A3, ağır, 800ms)\n"
            "  • GÜÇLENME: hızlı yükselen sweep (200→2000Hz, 300ms)\n"
            "  • PATLAMA: beyaz noise burst + low-pass filter (300ms)\n"
            "  • MENÜ SEÇIM: kısa 'tick' (sine 660Hz, 40ms)\n\n"

            "3.3  PROCEDURAL ARKA PLAN MÜZİĞİ\n"
            "  • Basit ama etkileyici bir procedural loop yaz:\n"
            "    - Bas davul: her 500ms'de düşük freqs (60Hz sine, 100ms decay)\n"
            "    - Hi-hat: her 250ms'de beyaz noise, high-pass filtre, 30ms\n"
            "    - Melodi: 8 notadan oluşan C-minör arpeggio, her nota 250ms,\n"
            "      tam döngü 2 saniye, tekrar eder\n"
            "    - Pad: uzun sustain'li chord (C3+Eb3+G3 sine, gain 0.05)\n"
            "  • Müzik tempo'su oyunun hızına göre artabilir (level * 5 BPM).\n"
            "  • Kullanıcı M tuşuyla müziği kapatabilir; durum localStorage'a kayıt.\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "BÖLÜM 4 — OYUN MEKANİKLERİ & OYNANIŞI\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "4.1  FIZIK & ÇARPIŞMA\n"
            "  • Her varlık için AABB veya çember çarpışma tespiti; hangisi uygunsa.\n"
            "  • Platform oyunu ise: yerçekimi (9.8 m/s² ölçekli), zıplama (impulse),\n"
            "    coyote-time (kenardan çıkınca 80ms daha zıplayabilme), jump buffering\n"
            "    (yere değmeden 100ms önce basılan zıplama geçerli sayılır).\n"
            "  • Nesne hızları dt ile ölçeklensin; duvar tespitinde kayma vektörü hesapla.\n\n"

            "4.2  DÜŞMAN YAPAY ZEKASI\n"
            "  Aşağıdakilerden oyun türüne uygun olanları uygula:\n"
            "  • CHASE: düşman her kare oyuncuya doğru normalize edilmiş vektörle ilerle.\n"
            "  • PATROL: iki nokta arası gidip gel, oyuncu yaklaşınca CHASE'e geç.\n"
            "  • FLANK: oyuncunun gittiği yönü öngör, kesiştirme noktasına git.\n"
            "  • SHOOTER: belirli menzil içinde oyuncuya mermi at; cooldown ile.\n"
            "  • SINE WAVE: yatayda sinüs dalgası hareketiyle uçan düşman.\n"
            "  • SPLIT: ölünce 2 küçük düşmana bölünen (Asteroids tarzı).\n"
            "  • BOSS: çok fazlı — her %33 can kaybında yeni saldırı pattern'ı açılır;\n"
            "    can barı ekranın altında büyük ve animasyonlu gösterilir.\n"
            "  Düşman hızı ve puanı: level * difficultyMultiplier ile artsın.\n\n"

            "4.3  GÜÇLENME (POWER-UP) SİSTEMİ\n"
            "  En az 4 farklı güçlenme tipi uygula:\n"
            "  • SHIELD: 5 saniye dokunulmazlık, oyuncunun etrafında dönen parçacık halka.\n"
            "  • RAPID_FIRE: ateş hızı 3× artar, 8 saniye; ateş efektleri kırmızıya döner.\n"
            "  • SPEED_BOOST: hareket hızı 1.8× artar, 6 saniye; trails yoğunlaşır.\n"
            "  • NUKE: ekrandaki tüm düşmanlar patlayarak ölür; büyük patlama animasyonu.\n"
            "  • MAGNET: coin/puan mıknatısı, 10 saniye (varsa).\n"
            "  Güçlenmeler: rastgele spawn, 10 saniyede kaybolur, bob animasyonu yapar.\n"
            "  Aktif güçlenme HUD'da ikon + dolup biten timer bar ile gösterilir.\n\n"

            "4.4  COMBO & SKOR SİSTEMİ\n"
            "  • Base skor: düşman türüne göre 100–1000 puan.\n"
            "  • Combo çarpanı: 3 saniyelik window içinde arka arkaya öldürme:\n"
            "    x1.0 → x1.5 → x2.0 → x3.0 → x5.0; window sıfırlanınca x1.0'a döner.\n"
            "  • Combo metni: ekranda büyük 'x2 COMBO!' yazısı, her artışta scale burst.\n"
            "  • High score localStorage'a kayıt; menüde ve game-over ekranında göster.\n"
            "  • Achievement sistemi: 'İlk Öldürme', '10 Combo', '10000 Puan' gibi\n"
            "    rozetler; kazanıldığında ekranda 3 saniye bildiri çıkar.\n\n"

            "4.5  ZORLUK EĞRİSİ & DALGA SİSTEMİ\n"
            "  • Wave tabanlı oyunlarda: her dalgada düşman sayısı +2, hız +5%.\n"
            "  • Her 5. dalgada BOSS spawner.\n"
            "  • Sürekli akış oyunlarında: elapsed time ile zorluk artar (her 30s).\n"
            "  • Düşman tipi çeşitliliği: wave 1-3=sıradan, 4-6=hızlı, 7+=shooter+split.\n"
            "  • Oyun bitince 'Bu level'da geçirdiğin süre' ve 'Öldürdüğün düşman' istatistiği.\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "BÖLÜM 5 — KONTROL & ERİŞİLEBİLİRLİK\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "5.1  KLAVYE\n"
            "  • InputManager sınıfı; keydown/keyup/mousedown/mousemove event'lerini\n"
            "    merkezi Map'te topla; oyun döngüsü bu Map'i okusun (polling).\n"
            "  • WASD + Arrow keys: hareket (ikisi de çalışsın).\n"
            "  • Space: ateş / zıplama / onaylama.\n"
            "  • P / ESC: duraklatma toggle.\n"
            "  • R: oyunu yeniden başlat (sadece GAME_OVER state'inde).\n"
            "  • M: müzik/ses toggle.\n"
            "  • F: tam ekran toggle (document.fullscreenElement).\n"
            "  • 1-4: güçlenme slotlarına hızlı erişim (varsa).\n\n"

            "5.2  DOKUNMATIK & MOBİL\n"
            "  • Mobil tespiti: 'ontouchstart' in window.\n"
            "  • On-screen D-Pad: sol altta 4 yönlü ok tuşu (SVG veya canvas çizimi).\n"
            "  • Aksiyon butonları: sağ altta A (ateş), B (güçlenme kullan) — büyük,\n"
            "    parmakla basılabilir (min 60×60 px).\n"
            "  • Swipe gesture: oyun türüne göre swipe-to-dodge veya swipe-to-aim.\n"
            "  • Pause butonu: sağ üstte her zaman görünür.\n"
            "  • Multi-touch: sol el hareket, sağ el ateş aynı anda çalışsın.\n\n"

            "5.3  GAMEPAD\n"
            "  • navigator.getGamepads() polling, gamepadconnected event'ini dinle.\n"
            "  • Sol analog çubuk: hareket (deadzone 0.15).\n"
            "  • A butonu: zıplama/onaylama; X butonu: ateş.\n"
            "  • Start butonu: duraklatma.\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "BÖLÜM 6 — ZORUNLU EKRANLAR\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "6.1  YÜKLEME EKRANI\n"
            "  • Oyun başlarken 1-2 saniyelik animasyonlu loading bar.\n"
            "  • Sazan AI logosu veya oyun ismi animasyonlu typewriter efektiyle.\n\n"

            "6.2  ANA MENÜ\n"
            "  • Oyun ismi: büyük, gradient, pulse animasyonlu.\n"
            "  • Arka plan: oyun temalı hareketli sahne (örn. dönen yıldızlar).\n"
            "  • Butonlar: OYNA, AYARLAR (ses toggle), NASIL OYNANIR, EN YÜKSEK SKOR.\n"
            "  • En yüksek skor: localStorage'dan oku, menüde büyük göster.\n"
            "  • Menüde arka plan müziği çal (daha sakin versiyon).\n"
            "  • Buton hover: ölçek büyüme + glow efekti.\n\n"

            "6.3  OYUN İÇİ HUD\n"
            "  • Can göstergesi: kalp ikonları veya dolup biten animasyonlu bar — sol üst.\n"
            "  • Skor: gradient metin, skor artınca kısa bounce animasyonu — orta üst.\n"
            "  • Level/Dalga: parlayan rozet — sağ üst.\n"
            "  • Aktif güçlenme: ikon + dolup biten dairesel timer — sol alt.\n"
            "  • Combo çarpanı (aktifken): ekran ortası üst, büyük ve renkli.\n"
            "  • Minimap (harita büyükse): sağ alt, 100×100 px.\n"
            "  • FPS sayacı: sağ alt köşe, küçük gri metin.\n\n"

            "6.4  DURAKLAT EKRANI\n"
            "  • Arka plan: bulanık overlay (canvas imageData üzerine rgba(0,0,0,0.6)).\n"
            "  • 'DURAKLADI' yazısı: büyük, animasyonlu.\n"
            "  • Butonlar: Devam Et, Yeniden Başla, Ana Menü.\n"
            "  • Ses ve oyun döngüsü tam olarak durdurulsun.\n\n"

            "6.5  OYUN BİTTİ EKRANI\n"
            "  • 'GAME OVER' yazısı: kırmızı, titreyen, ekranı kaplayan büyük animasyon.\n"
            "  • Skor özeti: Skor, En Yüksek Skor, Geçirilen Süre, Öldürülen Düşman.\n"
            "  • Yeni yüksek skor ise: parlayan 'YENİ REKOR!' rozetli konfeti yağmuru.\n"
            "  • Butonlar: Tekrar Oyna, Ana Menü.\n\n"

            "6.6  SEVİYE TAMAMLANDI\n"
            "  • Puan bonusu animasyonu: süre bonusu + combo bonusu sayaç animasyonuyla.\n"
            "  • '» Sonraki Seviye «' butonu; tıklayana kadar bekle.\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "BÖLÜM 7 — KOD YAZI STANDARTLARI (OYUN DIŞI KOD)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "Kullanıcı oyun değil genel kod, script veya program istediğinde:\n\n"

            "7.1  PYTHON\n"
            "  • PEP 8 uy; type hints (Python 3.10+) her fonksiyon parametresi ve\n"
            "    dönüş değerinde zorunlu.\n"
            "  • Docstring: Google stili, her public fonksiyon ve sınıfta.\n"
            "  • Hata yönetimi: özel exception sınıfları; bare 'except:' asla kullanma.\n"
            "  • Loglama: print() yerine logging modülü; log level seçilebilir.\n"
            "  • Immutable default args: def f(lst=None): lst = lst or [] paterni.\n"
            "  • Context manager: dosya, DB, ağ işlemlerinde 'with' zorunlu.\n"
            "  • Async: I/O-bound için asyncio + aiohttp; thread değil.\n"
            "  • Test: her fonksiyon için unittest/pytest örnek test bloğu ekle.\n"
            "  • requirements.txt veya pyproject.toml bloğunu yanına yaz.\n\n"

            "7.2  JAVASCRIPT / TYPESCRIPT\n"
            "  • TypeScript verilirse strict: true; her değişken ve parametreye tip.\n"
            "  • Modern JS: const/let (var yasak), arrow fonksiyon, destructuring,\n"
            "    optional chaining (?.), nullish coalescing (??).\n"
            "  • Async/await; .then() zinciri değil (okunabilirlik için).\n"
            "  • ESLint + Prettier uyumlu format; trailing comma, single quote.\n"
            "  • Frontend: DOM manipülasyonu için querySelector; jQuery bağımlılığı yok.\n"
            "  • Hata sınırları: try/catch + window.onerror; hata mesajı kullanıcıya göster.\n\n"

            "7.3  WEB (HTML/CSS)\n"
            "  • Semantic HTML5 elementleri: <header>, <main>, <section>, <article>.\n"
            "  • CSS: Custom properties (--renk-birincil), flex + grid layout.\n"
            "  • Responsive: mobile-first; @media breakpoint'ler.\n"
            "  • Erişilebilirlik: ARIA label'lar, renk kontrastı WCAG AA, klavye nav.\n"
            "  • Performans: critical CSS inline; lazy-load görseller.\n\n"

            "7.4  VERİTABANI & BACKEND\n"
            "  • SQL: parameterized query zorunlu (SQL injection'a karşı).\n"
            "  • ORM kullanılıyorsa lazy-load N+1 sorununa dikkat et; eager load ekle.\n"
            "  • API tasarımı: RESTful veya GraphQL; endpoint isimleri kaynak odaklı\n"
            "    (/users/{id} gibi, /getUser değil).\n"
            "  • JWT veya session: güvenli saklama (HttpOnly cookie, SameSite=Strict).\n"
            "  • Rate limiting ve input validation her endpoint'te.\n\n"

            "7.5  ÇIKTI FORMATI (GENEL KOD)\n"
            "  • Dil etiketi doğru: ```python, ```typescript, ```bash, ```sql vb.\n"
            "  • Birden fazla dosya gerekiyorsa her biri ayrı blokta,\n"
            "    üstünde '# ── filename: app.py ──' gibi açık yorum satırı.\n"
            "  • Blok öncesi 1-3 cümle özet; blok sonrası kurulum/çalıştırma adımları.\n"
            "  • Kod içi yorumlar: neden (why) odaklı, ne (what) değil.\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "BÖLÜM 8 — KESİN KURALLAR & YASAKLAR\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "✗  Yarım veya stub kod: 'TODO: implement' veya '// ...' bırakma.\n"
            "✗  Sahte placeholder: 'add your logic here' yazan fonksiyon gövdesi.\n"
            "✗  Dış bağımlılık (oyunlarda): CDN, harici URL, require(), import CDN.\n"
            "✗  console.log(): debug log bırakma; production kodunda yok.\n"
            "✗  alert() / prompt(): oyun dışı kod için kullanmayın (modal UI yaz).\n"
            "✗  eval(), innerHTML (XSS): asla kullanma.\n"
            "✗  var: const veya let kullan.\n"
            "✗  Sihirli sayı: ham 42, 0.016, 255 gibi değerleri doğrudan koda yazma.\n"
            "✗  Tekrar eden blok (DRY ihlali): 3+ kez aynı kod → fonksiyon/sınıf yaz.\n"
            "✗  Asenkron olmayan I/O (backend): sync dosya okuma/yazma yasak.\n"
            "✗  Hardcoded credential: API key, şifre, token asla kaynak kodda.\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "ÇIKTI KURALLARI\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "• Oyun için: HTML kodunu KESİNLİKLE tek bir ```html ... ``` bloğu içine al.\n"
            "  Açıklama varsa bloğun ÖNÜNE yaz; bloğun SONRASINA hiçbir şey ekleme.\n"
            "• Genel kod için: doğru dil etiketiyle blok; çok dosyalıysa her biri ayrı.\n"
            "• Kodu ASLA yarım bırakma — son karakter kapanana kadar eksiksiz tamamla.\n\n"

            "Oyun/kod dışı tüm sohbet ve açıklamalarını şu dilde yaz: " + target_lang
        )

        messages = [{"role": "system", "content": sys_prompt}]
        # Not: geçmişteki büyük HTML oyun kodları bağlamdan kısaltılır ki TPM
        # (dakika başına token) limitine takılmayalım. Son 6 mesajla sınırlı tutulur.
        for m in history[-6:-1]:
            messages.append({"role": m["role"], "content": _kisalt_gecmis_icerik(m["content"])})
        messages.append({"role": "user", "content": prompt})

        try:
            res = SazanAIConception._tek_istek(messages, model_cfg, max_tokens=max_tokens_bu_istek, force_search=force_search)
            combined = res.choices[0].message.content or ""
            finish_reason = res.choices[0].finish_reason

            # Güncel bilgi zorunlu arandığı halde yanıt hiçbir kaynak/tarih izine
            # dayanmıyor gibi görünüyorsa, modeli daha net bir uyarıyla BİR KEZ daha
            # aramaya zorluyoruz. Bu, "arama yaptı görünüyor ama aslında ezber cevap
            # verdi" sorununu azaltır.
            if force_search and combined and not SazanAIConception._yanit_arama_izi_tasiyor_mu(combined):
                messages.append({"role": "assistant", "content": combined})
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Bu yanıtında hiçbir kaynak, tarih veya arama izi görmüyorum. "
                            "browser_search aracını GERÇEKTEN kullanarak yeniden ara ve "
                            "yanıtının sonuna hangi kaynağa/tarihe dayandığını mutlaka yaz. "
                            "Emin değilsen bunu açıkça söyle, ama uydurma."
                        ),
                    }
                )
                try:
                    res_retry = SazanAIConception._tek_istek(
                        messages, model_cfg, max_tokens=max_tokens_bu_istek, force_search=True
                    )
                    retry_content = res_retry.choices[0].message.content or ""
                    if retry_content.strip():
                        combined = retry_content
                        finish_reason = res_retry.choices[0].finish_reason
                except Exception:
                    pass  # yeniden deneme başarısız olursa ilk yanıtla devam et

            attempts = 0
            while finish_reason == "length" and attempts < MAX_CONTINUATIONS:
                messages.append({"role": "assistant", "content": combined})
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Yanıtın token limiti nedeniyle yarıda kesildi. BAŞTAN BAŞLAMA. "
                            "Sadece kaldığın satırdan itibaren devam ederek kodu/ metni "
                            "eksiksiz tamamla."
                        ),
                    }
                )
                res2 = SazanAIConception._tek_istek(messages, model_cfg, max_tokens=max_tokens_bu_istek, force_search=force_search)
                combined += res2.choices[0].message.content or ""
                finish_reason = res2.choices[0].finish_reason
                attempts += 1

            return combined
        except Exception as e:
            err_text = str(e).lower()
            if "decommission" in err_text or "deprecat" in err_text or "not found" in err_text:
                return (
                    "⚠️ Seçtiğin model Groq tarafından güncellenmiş görünüyor. Lütfen sol "
                    f"menüden farklı bir model seç ve tekrar dene.\n\n(Teknik detay: {e})"
                )
            return f"⚠️ Sazan AI ile iletişim hatası: {e}"


# =====================================================================
# 7. GÖRSEL ÜRETİM ATÖLYESİ (SADECE ÜYELER)
# =====================================================================
class SazanImageForge:
    BASE_ENDPOINT = "https://image.pollinations.ai/prompt/"

    @staticmethod
    def enhance_prompt_with_ai(ham_prompt, model_cfg):
        sys_prompt = (
            "Sen profesyonel bir görsel üretim (text-to-image) prompt mühendisisin. "
            "Kullanıcı sana herhangi bir dilde kısa bir görsel fikri verecek. Bunu; "
            "kompozisyon, ışıklandırma, renk paleti, atmosfer ve detay seviyesini net "
            "biçimde belirten, İngilizce, tek paragraf, en fazla 70 kelimelik zengin bir "
            "görsel üretim prompt'una çevir. SADECE prompt metnini döndür."
        )
        try:
            res = _groq_create(
                _pool_visual,
                model=model_cfg["id"],
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": ham_prompt},
                ],
                temperature=0.6,
                top_p=0.9,
                max_tokens=220,
            )
            enhanced = (res.choices[0].message.content or "").strip().strip('"').strip()
            return enhanced if enhanced else ham_prompt
        except Exception:
            return ham_prompt

    @staticmethod
    def generate_image(prompt_text, style_suffix="", width=1024, height=1024, seed=None):
        final_prompt = prompt_text.strip()
        if style_suffix:
            final_prompt = f"{final_prompt}, {style_suffix}"

        width = max(256, min(int(width), 1536))
        height = max(256, min(int(height), 1536))
        seed_val = int(seed) if seed is not None else random.randint(1, 9_999_999)

        encoded_prompt = urllib.parse.quote(final_prompt)
        query = urllib.parse.urlencode({"width": width, "height": height, "seed": seed_val, "nologo": "true"})
        full_url = f"{SazanImageForge.BASE_ENDPOINT}{encoded_prompt}?{query}"

        req = urllib.request.Request(full_url, headers={"User-Agent": "Mozilla/5.0 (SazanAI ImageForge)"})
        with urllib.request.urlopen(req, timeout=90) as response:
            image_bytes = response.read()

        return image_bytes, final_prompt, seed_val


# =====================================================================
# 8. 3D BASKI ATÖLYESİ — GÖRSELDEN STL (SADECE ÜYELER)
# =====================================================================
class SazanPrintStudio:
    MAX_RESOLUTION_PX = 220

    @staticmethod
    def generate_stl_from_image(image, max_size_px=120, base_height_mm=2.0, relief_height_mm=5.0,
                                 pixel_size_mm=0.6, invert=False):
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

        ii, jj = np.mgrid[0:rows - 1, 0:cols - 1]
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
# 9. ÇEREZ (COOKIE) YÖNETİCİSİ — "BENİ HATIRLA" İÇİN
# =====================================================================
class _NoOpCookieManager:
    """extra_streamlit_components kurulu değilse kullanılan sahte (no-op) çerez
    yöneticisi. Böylece 'beni hatırla' özelliği sessizce kapanır ama app.py
    ModuleNotFoundError ile çökmez; get() her zaman None döner, set/delete hiçbir
    şey yapmaz."""

    def get(self, *args, **kwargs):
        return None

    def set(self, *args, **kwargs):
        return None

    def delete(self, *args, **kwargs):
        return None


def get_cookie_manager():
    # CookieManager bir Streamlit widget'ı olduğu için @st.cache_resource KULLANILMAZ
    # (CachedWidgetWarning fırlatır). Bunun yerine session_state'e saklıyoruz —
    # böylece her rerun'da aynı nesne kullanılır VE cookie okuma yarış koşulundan
    # (ilk render'da henüz hazır olmaması) kaçınmak için "cookie_manager_ready" flag'i
    # ile kontrol ediyoruz.
    if not _COOKIE_LIB_VAR:
        return _NoOpCookieManager()
    if "_sazan_cookie_mgr" not in st.session_state:
        st.session_state._sazan_cookie_mgr = stx.CookieManager(key="sazan_cookie_manager")
    return st.session_state._sazan_cookie_mgr


cookie_manager = get_cookie_manager()

# =====================================================================
# 10. OTURUM DURUMU BAŞLATICI
# =====================================================================
def init_session_state():
    defaults = {
        "username": None,
        "guest_active": False,
        "chat_sessions": {"💬 Yeni Sohbet": []},
        "current_chat": "💬 Yeni Sohbet",
        "chat_counter": 1,
        "active_model_label": GUEST_MODEL_LABEL,
        "active_lang_code": "Türkçe 🇹🇷",
        "pending_prompt": None,
        "show_image_studio": False,
        "show_print_studio": False,
        "hacker_mode": False,
        "hacker_intro_shown": False,
        "hacker_confirm_pending": False,   # onay ekranı bekliyor mu
        "hacker_chat_key": "💀 Hacker Terminali",
        "prev_chat_key": "💬 Yeni Sohbet",
        "cooldown_until": 0.0,
        "img_forge_last_result": None,
        "img_forge_enhanced_prompt": "",
        "auto_login_checked": False,
        "remembered_email_prefill": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_session_state()

# ---------- "BU CİHAZDA BENİ HATIRLA" — OTOMATİK GİRİŞ DENEMESİ ----------
# Bu blok, kullanıcı henüz giriş yapmamışsa/misafir modunda değilse ve daha önce
# "beni hatırla" işaretlediyse, tarayıcıdaki çerezleri okuyup otomatik giriş yapar.
# CookieManager ilk render'da hazır olmayabilir; bu yüzden auto_login_checked=False
# olduğunda okuma deneriz. Eğer kütüphane yoksa (NoOp) doğrudan geçeriz.
if (not st.session_state.username) and (not st.session_state.guest_active) and (not st.session_state.auto_login_checked):
    try:
        remembered_email = cookie_manager.get(REMEMBER_EMAIL_COOKIE)
        remembered_token = cookie_manager.get(REMEMBER_TOKEN_COOKIE)
    except Exception:
        remembered_email, remembered_token = None, None

    # Sadece gerçekten bir email değeri varsa işlem yap; None ise kütüphane hazır
    # olmamış olabilir ama sonsuz döngüye GİRMEMEK için flag'i True yapıp geçiyoruz.
    st.session_state.auto_login_checked = True

    if remembered_email and remembered_token and SazanAuth.verify_remember_token(remembered_email, remembered_token):
        st.session_state.username = remembered_email.strip().lower()
        st.session_state.guest_active = False
        st.session_state.chat_sessions = SazanChatStore.get_sessions(st.session_state.username)
        st.session_state.current_chat = list(st.session_state.chat_sessions.keys())[0]
        st.session_state.active_model_label = "🧠 Sazan Dengeli"
        st.rerun()
    elif remembered_email:
        st.session_state.remembered_email_prefill = remembered_email.strip().lower()

is_member = bool(st.session_state.username)
is_guest = st.session_state.guest_active and not is_member

# =====================================================================
# 11. GİRİŞ EKRANI (üye değil VE misafir modunda değilse)
# =====================================================================
if not is_member and not is_guest:
    st.markdown(
        """
        <div class='sz-hero' style='margin-top:20px;'>
            <h1>🐟 Sazan AI</h1>
            <p>Sohbet et, kod yaz, oyun üret, görsel oluştur ve 3D baskıya hazırla.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, mid_col, _ = st.columns([1, 1.3, 1])
    with mid_col:
        with st.container(border=True):
            st.markdown("<div class='auth-logo-ring'>🐟</div>", unsafe_allow_html=True)
            st.markdown(
                "<h4 style='text-align:center; margin:4px 0 2px 0;'>Sazan Evrenine Hoş Geldin</h4>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p class='auth-caption'>Giriş yaparsan tüm modelleri, görsel üretimini ve "
                "3D baskı atölyesini açarsın. İstersen misafir olarak da göz atabilirsin.</p>",
                unsafe_allow_html=True,
            )

            if not _COOKIE_LIB_VAR:
                st.caption(
                    "ℹ️ 'Bu cihazda beni hatırla' özelliği şu an kapalı görünüyor çünkü "
                    "`extra-streamlit-components` kütüphanesi sunucuda kurulu değil. "
                    "Bunu düzeltmek için GitHub deponuzdaki requirements.txt dosyasına "
                    "`extra-streamlit-components` satırını ekleyip yeniden deploy edin. "
                    "Diğer tüm özellikler (sohbet, görsel üretim, 3D baskı) normal çalışır."
                )

            tab_login, tab_signup = st.tabs(["➡️ Giriş Yap", "🆕 Hesap Oluştur"])

            # ---------------- GİRİŞ SEKMESİ ----------------
            with tab_login:
                if st.session_state.remembered_email_prefill:
                    st.caption(
                        "📱 Bu cihazda daha önce kullandığın bir hesap tespit edildi, "
                        "e-posta alanı otomatik dolduruldu."
                    )
                login_email = st.text_input(
                    "📧 Gmail Adresin",
                    key="login_email_input",
                    value=st.session_state.remembered_email_prefill,
                    placeholder="[email protected]",
                )
                login_pw = st.text_input("🔑 Şifren", type="password", key="login_pw_input")

                login_remember = st.checkbox(
                    "📱 Bu cihazda beni hatırla (isteğe bağlı)",
                    key="login_remember_chk",
                    value=bool(st.session_state.remembered_email_prefill),
                    help="İşaretlersen, bu cihazda bir daha ki girişlerinde e-posta/şifre "
                         "tekrar sorulmaz, otomatik giriş yapılır. İşaretlemezsen normal "
                         "şekilde her seferinde e-posta ve şifreni girmen istenir. "
                         "Paylaşımlı/ortak bir cihazdaysan işaretlememeni öneririz.",
                )

                with st.expander("📜 Kullanım Şartları ve Telif Hakkı Bildirimi"):
                    st.markdown(TELIF_ONAY_METNI)
                login_consent = st.checkbox(
                    "Yukarıdaki kullanım şartlarını ve telif hakkı sorumluluğunu okudum, onaylıyorum. "
                    "(Ürettiğim içeriklerin telif hakkı sorumluluğunun bana ait olduğunu kabul ediyorum.)",
                    key="login_consent_chk",
                )

                if st.button("Giriş Yap", use_container_width=True, type="primary", key="login_submit_btn"):
                    email_clean = login_email.strip()
                    if not login_consent:
                        st.error(
                            "⚠️ Devam edebilmen için önce 'Okudum, onaylıyorum' kutusunu "
                            "işaretlemen gerekiyor. Bu kutu, ürettiğin içeriklerin telif hakkı "
                            "sorumluluğunun sana ait olduğunu kabul ettiğin anlamına gelir."
                        )
                    elif not email_clean or not login_pw:
                        st.error("⚠️ Lütfen e-posta ve şifreni gir.")
                    elif not SazanAuth.is_valid_gmail(email_clean):
                        st.error("❌ Geçersiz e-posta! '@gmail.com' ile biten bir adres gir.")
                    elif not SazanAuth.email_exists(email_clean):
                        st.error("❌ Bu Gmail adresine kayıtlı bir hesap yok. Önce kayıt ol.")
                    elif not SazanAuth.verify(email_clean, login_pw):
                        st.error("❌ Şifre yanlış! Lütfen tekrar dene.")
                    else:
                        key_email = email_clean.lower()
                        st.session_state.username = key_email
                        st.session_state.guest_active = False
                        st.session_state.chat_sessions = SazanChatStore.get_sessions(key_email)
                        st.session_state.current_chat = list(st.session_state.chat_sessions.keys())[0]
                        st.session_state.active_model_label = "🧠 Sazan Dengeli"

                        if login_remember:
                            # İSTEĞE BAĞLI: kullanıcı işaretlediyse bu cihazda kalıcı oturum
                            # açılır — şifre çereze YAZILMAZ, sadece tek kullanımlık rastgele
                            # bir "hatırlama token"ının hash'i saklanır (bkz. create_remember_token).
                            raw_token = SazanAuth.create_remember_token(key_email)
                            expires_at = datetime.now() + timedelta(days=REMEMBER_DAYS)
                            cookie_manager.set(REMEMBER_EMAIL_COOKIE, key_email, expires_at=expires_at, key="set_email_ck_login")
                            cookie_manager.set(REMEMBER_TOKEN_COOKIE, raw_token, expires_at=expires_at, key="set_token_ck_login")
                        else:
                            # Kullanıcı istemediyse (ör. ortak bilgisayar) bu cihazdaki eski
                            # hatırlama kaydı varsa temizlenir; her girişte tekrar sorulur.
                            SazanAuth.clear_remember_token(key_email)
                            cookie_manager.delete(REMEMBER_EMAIL_COOKIE, key="del_email_ck_login")
                            cookie_manager.delete(REMEMBER_TOKEN_COOKIE, key="del_token_ck_login")

                        st.success("🎉 Giriş başarılı! Yönlendiriliyorsun...")
                        time.sleep(0.4)
                        st.rerun()

            # ---------------- KAYIT SEKMESİ ----------------
            with tab_signup:
                signup_email = st.text_input("📧 Gmail Adresin", key="signup_email_input", placeholder="[email protected]")
                signup_pw = st.text_input("🔑 Şifre Belirle (en az 6 karakter)", type="password", key="signup_pw_input")
                signup_pw_confirm = st.text_input("🔑 Şifreni Tekrar Gir", type="password", key="signup_pw_confirm_input")

                signup_remember = st.checkbox(
                    "📱 Bu cihazda beni hatırla (isteğe bağlı)",
                    key="signup_remember_chk",
                    help="İşaretlersen, bu cihazda bir daha ki girişlerinde e-posta/şifre "
                         "tekrar sorulmaz, otomatik giriş yapılır. İşaretlemezsen her "
                         "seferinde normal şekilde giriş yapman istenir.",
                )

                with st.expander("📜 Kullanım Şartları ve Telif Hakkı Bildirimi"):
                    st.markdown(TELIF_ONAY_METNI)
                signup_consent = st.checkbox(
                    "Yukarıdaki kullanım şartlarını ve telif hakkı sorumluluğunu okudum, onaylıyorum. "
                    "(Ürettiğim içeriklerin telif hakkı sorumluluğunun bana ait olduğunu kabul ediyorum.)",
                    key="signup_consent_chk",
                )

                if st.button("Hesap Oluştur", use_container_width=True, type="primary", key="signup_submit_btn"):
                    email_clean = signup_email.strip()
                    if not signup_consent:
                        st.error(
                            "⚠️ Devam edebilmen için önce 'Okudum, onaylıyorum' kutusunu "
                            "işaretlemen gerekiyor. Bu kutu, ürettiğin içeriklerin telif hakkı "
                            "sorumluluğunun sana ait olduğunu kabul ettiğin anlamına gelir."
                        )
                    elif not email_clean or not signup_pw or not signup_pw_confirm:
                        st.error("⚠️ Lütfen tüm alanları doldur.")
                    elif not SazanAuth.is_valid_gmail(email_clean):
                        st.error("❌ Geçersiz e-posta! '@gmail.com' ile biten bir adres gir.")
                    elif SazanAuth.email_exists(email_clean):
                        st.error("❌ Bu Gmail adresi zaten kayıtlı. '➡️ Giriş Yap' sekmesini kullan.")
                    elif len(signup_pw) < 6:
                        st.error("❌ Şifren en az 6 karakter olmalı.")
                    elif signup_pw != signup_pw_confirm:
                        st.error("❌ Şifreler birbiriyle eşleşmiyor.")
                    else:
                        SazanAuth.register(email_clean, signup_pw)
                        key_email = email_clean.lower()
                        st.session_state.username = key_email
                        st.session_state.guest_active = False
                        st.session_state.chat_sessions = SazanChatStore.get_sessions(key_email)
                        st.session_state.current_chat = list(st.session_state.chat_sessions.keys())[0]
                        st.session_state.active_model_label = "🧠 Sazan Dengeli"

                        if signup_remember:
                            raw_token = SazanAuth.create_remember_token(key_email)
                            expires_at = datetime.now() + timedelta(days=REMEMBER_DAYS)
                            cookie_manager.set(REMEMBER_EMAIL_COOKIE, key_email, expires_at=expires_at, key="set_email_ck_signup")
                            cookie_manager.set(REMEMBER_TOKEN_COOKIE, raw_token, expires_at=expires_at, key="set_token_ck_signup")

                        st.success("🎉 Hesabın oluşturuldu! Hoş geldin.")
                        time.sleep(0.4)
                        st.rerun()

            st.markdown("<div style='text-align:center; margin-top:14px;'>", unsafe_allow_html=True)
            if st.button("👤 Misafir Olarak Devam Et", use_container_width=True):
                st.session_state.guest_active = True
                st.session_state.active_model_label = GUEST_MODEL_LABEL
                st.rerun()
            st.markdown(
                "<p style='text-align:center; color:#8b93a7; font-size:0.78rem; margin-top:6px;'>"
                "Misafir modunda tek bir model ile sohbet edebilirsin. Görsel üretimi, 3D baskı "
                "ve diğer modeller için giriş yapman gerekir.</p>",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

user = st.session_state.username if is_member else None

# =====================================================================
# 12. SIDEBAR
# =====================================================================
with st.sidebar:
    if is_member:
        st.markdown(f"<h3 style='color:#22d3ee; text-align:center;'>🐟 {user}</h3>", unsafe_allow_html=True)
        if st.button("🚪 Çıkış Yap", use_container_width=True):
            SazanAuth.clear_remember_token(user)
            cookie_manager.delete(REMEMBER_EMAIL_COOKIE, key="del_email_ck_logout")
            cookie_manager.delete(REMEMBER_TOKEN_COOKIE, key="del_token_ck_logout")
            for k in ["username", "guest_active", "chat_sessions", "current_chat", "auto_login_checked", "remembered_email_prefill"]:
                st.session_state.pop(k, None)
            st.rerun()
    else:
        st.markdown("<h3 style='color:#22d3ee; text-align:center;'>👤 Misafir</h3>", unsafe_allow_html=True)
        if st.button("➡️ Giriş Yap / Üye Ol", use_container_width=True, type="primary"):
            st.session_state.guest_active = False
            st.rerun()

    st.divider()
    st.markdown("**💬 Sohbetler**")
    if st.button("➕ Yeni Sohbet", use_container_width=True, type="secondary"):
        st.session_state.chat_counter += 1
        new_id = f"💬 Sohbet {st.session_state.chat_counter}"
        st.session_state.chat_sessions[new_id] = []
        st.session_state.current_chat = new_id
        if is_member:
            SazanChatStore.save_sessions(user, st.session_state.chat_sessions)
        st.rerun()

    if is_member:
        st.markdown("<div style='max-height: 220px; overflow-y:auto;'>", unsafe_allow_html=True)
        for chat_name in reversed(list(st.session_state.chat_sessions.keys())):
            is_current = chat_name == st.session_state.current_chat
            bullet = "🟢" if is_current else "◇"
            if st.button(f"{bullet} {chat_name}", key=f"switch_{chat_name}", use_container_width=True):
                st.session_state.current_chat = chat_name
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🗑️ Bu Sohbeti Temizle", use_container_width=True):
        st.session_state.chat_sessions[st.session_state.current_chat] = []
        if is_member:
            SazanChatStore.save_sessions(user, st.session_state.chat_sessions)
        st.rerun()

    st.divider()
    st.markdown("**🧠 Yapay Zeka Modeli**")
    if is_member:
        model_label = st.selectbox(
            "Model seç:",
            list(AI_MODELS.keys()),
            key="active_model_label",
            label_visibility="collapsed",
        )
        search_badge = "<br><span class='badge'>🌐 Canlı web araması aktif</span>" if AI_MODELS[model_label].get("web_search") else ""
        st.markdown(
            f"<div class='model-pill'><b>{model_label}</b><br><span>{AI_MODELS[model_label]['desc']}</span>{search_badge}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.session_state.active_model_label = GUEST_MODEL_LABEL
        search_badge = "<br><span class='badge'>🌐 Canlı web araması aktif</span>" if AI_MODELS[GUEST_MODEL_LABEL].get("web_search") else ""
        st.markdown(
            f"<div class='model-pill'><b>{GUEST_MODEL_LABEL}</b><br>"
            f"<span>{AI_MODELS[GUEST_MODEL_LABEL]['desc']}</span>{search_badge}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='lock-card'><div class='lock-emoji'>🔒</div>"
            "<p><b>7 model</b> arasından seçim yapmak için giriş yap.</p></div>",
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown("**🎨 Yaratıcı Stüdyolar**")
    if is_member:
        if st.button("🎨 Görsel Üretim Atölyesi", use_container_width=True,
                      type="primary" if st.session_state.show_image_studio else "secondary"):
            st.session_state.show_image_studio = not st.session_state.show_image_studio
            st.rerun()
        if st.button("🖨️ 3D Baskı Atölyesi", use_container_width=True,
                      type="primary" if st.session_state.show_print_studio else "secondary"):
            st.session_state.show_print_studio = not st.session_state.show_print_studio
            st.rerun()
    else:
        st.markdown(
            "<div class='lock-card'><div class='lock-emoji'>🔒</div>"
            "<p><b>Görsel üretimi</b> ve <b>3D baskı atölyesi</b> sadece üyelere özeldir.</p></div>",
            unsafe_allow_html=True,
        )

    st.divider()
    # ── HACKER SAZAN MODU ──
    hacker_active = st.session_state.get("hacker_mode", False)
    hacker_btn_label = "🟢 HACKER MODU AKTİF" if hacker_active else "💀 Hacker Sazan Modunu Aç"
    hacker_btn_type  = "primary" if hacker_active else "secondary"
    if st.button(hacker_btn_label, use_container_width=True, type=hacker_btn_type, key="hacker_toggle_btn"):
        if not hacker_active:
            # Onay ekranını göster — direkt aktif etme
            st.session_state.hacker_confirm_pending = True
            st.rerun()
        else:
            # MODU KAPAT
            st.session_state.hacker_mode = False
            st.session_state.hacker_intro_shown = False
            st.session_state.hacker_confirm_pending = False
            prev = st.session_state.get("prev_chat_key", "💬 Yeni Sohbet")
            if prev not in st.session_state.chat_sessions:
                prev = list(st.session_state.chat_sessions.keys())[0]
            st.session_state.current_chat = prev
            st.rerun()
    if hacker_active:
        st.markdown(
            "<p style='text-align:center;color:#00ff41;font-size:0.72rem;margin:2px 0 0 0;'>"
            "⚡ Hacker terminali aktif · Ayrı sohbet</p>",
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown("**🌐 Dil**")
    st.selectbox("Çeviri:", list(DIL_MATRISI.keys()), key="active_lang_code", label_visibility="collapsed")

# =====================================================================
# 13. ANA BAŞLIK / HACKER MODU
# =====================================================================
active_messages = st.session_state.chat_sessions.setdefault(st.session_state.current_chat, [])

# ── HACKER ONAY EKRANI (tam ekran, butonlar çalışmadan önce) ─────────
if st.session_state.get("hacker_confirm_pending", False):
    st.components.v1.html(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        *{margin:0;padding:0;box-sizing:border-box;}
        body{background:#000;overflow:hidden;}
        #cw{width:100%;height:400px;position:relative;background:#000;}
        #cc{position:absolute;top:0;left:0;width:100%;height:100%;}
        #cb{
            position:absolute;top:0;left:0;width:100%;height:100%;
            display:flex;flex-direction:column;align-items:center;justify-content:center;
            gap:14px;pointer-events:none;
        }
        #skull-anim{font-size:4rem;animation:sp 1.2s ease-in-out infinite alternate;}
        @keyframes sp{from{transform:scale(1);filter:drop-shadow(0 0 8px #00ff41);}
                       to{transform:scale(1.12);filter:drop-shadow(0 0 22px #00ff41);}}
        #ctitle{
            font-family:'Share Tech Mono',monospace;font-size:2rem;
            letter-spacing:6px;color:#00ff41;
            text-shadow:0 0 12px #00ff41,0 0 28px #00cc33;
            animation:glitch 3s infinite;
        }
        @keyframes glitch{
            0%,91%,100%{transform:none;text-shadow:0 0 12px #00ff41,0 0 28px #00cc33;}
            92%{transform:translate(-3px,0);text-shadow:-3px 0 #ff0066,3px 0 #00ffff;}
            93%{transform:translate(3px,0);text-shadow:3px 0 #ff0066,-3px 0 #00ffff;}
        }
        #csub{
            font-family:'Share Tech Mono',monospace;font-size:0.88rem;
            color:#00aa30;letter-spacing:2px;text-align:center;line-height:1.7;
            max-width:480px;
        }
        /* köşe braketleri */
        .cb2{position:absolute;width:32px;height:32px;border-color:#00ff41;border-style:solid;opacity:0.55;}
        .cb2.tl{top:12px;left:12px;border-width:2px 0 0 2px;}
        .cb2.tr{top:12px;right:12px;border-width:2px 2px 0 0;}
        .cb2.bl{bottom:12px;left:12px;border-width:0 0 2px 2px;}
        .cb2.br{bottom:12px;right:12px;border-width:0 2px 2px 0;}
        </style>
        <div id="cw">
          <canvas id="cc"></canvas>
          <div class="cb2 tl"></div><div class="cb2 tr"></div>
          <div class="cb2 bl"></div><div class="cb2 br"></div>
          <div id="cb">
            <div id="skull-anim">💀</div>
            <div id="ctitle">HACKER SAZAN MODU</div>
            <div id="csub">
              Bu mod ayrı bir terminal sohbeti açar.<br>
              Maksimum kalite kod motoru devreye girer.<br>
              <span style="color:#00ff41;font-weight:bold;">Devam etmek istiyor musun?</span>
            </div>
          </div>
        </div>
        <script>
        (function(){
          const cv=document.getElementById('cc'),ctx=cv.getContext('2d');
          function rs(){cv.width=cv.offsetWidth||700;cv.height=cv.offsetHeight||400;}
          rs();window.addEventListener('resize',rs);
          const CH='アイウエオ0123456789ABCDEF<>{}[]!@#$';
          let dr=[];
          function id(){dr=Array.from({length:Math.floor(cv.width/14)},()=>Math.random()*-40|0);}
          id();
          let sc=0;
          function draw(){
            const W=cv.width,H=cv.height;
            ctx.fillStyle='rgba(0,0,0,0.83)';ctx.fillRect(0,0,W,H);
            ctx.font='13px monospace';
            dr.forEach((d,i)=>{
              const ch=CH[Math.random()*CH.length|0],y=d*14;
              ctx.fillStyle='rgba(160,255,160,0.85)';ctx.fillText(ch,i*14,y);
              ctx.fillStyle='rgba(0,130,40,0.25)';ctx.fillText(CH[Math.random()*CH.length|0],i*14,y-14);
              if(y>H&&Math.random()>0.975)dr[i]=0; dr[i]++;
            });
            sc=(sc+1.1)%H;
            const sg=ctx.createLinearGradient(0,sc-5,0,sc+5);
            sg.addColorStop(0,'rgba(0,255,65,0)');sg.addColorStop(0.5,'rgba(0,255,65,0.12)');sg.addColorStop(1,'rgba(0,255,65,0)');
            ctx.fillStyle=sg;ctx.fillRect(0,sc-5,W,10);
            requestAnimationFrame(draw);
          }
          draw();
        })();
        </script>
        """,
        height=408,
    )

    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("✅ EVET — Hacker Modunu Aç", use_container_width=True, type="primary", key="hacker_confirm_yes"):
            st.session_state.hacker_confirm_pending = False
            st.session_state.hacker_mode = True
            st.session_state.hacker_intro_shown = False
            st.session_state.prev_chat_key = st.session_state.current_chat
            hk = st.session_state.hacker_chat_key
            if hk not in st.session_state.chat_sessions:
                st.session_state.chat_sessions[hk] = []
            st.session_state.current_chat = hk
            st.rerun()
    with col_no:
        if st.button("❌ HAYIR — Normal Sohbete Devam Et", use_container_width=True, type="secondary", key="hacker_confirm_no"):
            st.session_state.hacker_confirm_pending = False
            st.rerun()
    st.stop()  # onay ekranındayken altta başka bir şey render edilmesin

# ── HACKER SAZAN MODU AÇILIŞ EKRANI ──────────────────────────────────
if st.session_state.get("hacker_mode", False):

    # Intro animasyonu — sadece ilk açılışta tam ekran oynatılır
    if not st.session_state.get("hacker_intro_shown", False):
        st.components.v1.html(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
            *{margin:0;padding:0;box-sizing:border-box;}
            body{background:#000;overflow:hidden;}
            #intro-wrap{
                width:100%;height:420px;position:relative;
                background:#000;overflow:hidden;
                display:flex;align-items:center;justify-content:center;
            }
            #ic{display:block;position:absolute;top:0;left:0;width:100%;height:100%;}

            /* ── merkez kutu ── */
            #intro-box{
                position:relative;z-index:10;
                display:flex;flex-direction:column;align-items:center;gap:10px;
                animation: boxReveal 0.6s ease-out both;
            }
            @keyframes boxReveal{from{opacity:0;transform:scale(0.7);}to{opacity:1;transform:scale(1);}}

            #skull{font-size:5rem;animation:skullPulse 1s ease-in-out infinite alternate;}
            @keyframes skullPulse{from{text-shadow:0 0 20px #00ff41,0 0 40px #00ff41;}
                                   to{text-shadow:0 0 40px #00ff41,0 0 80px #00cc33,0 0 120px #009922;}}

            #main-title{
                font-family:'Share Tech Mono',monospace;
                font-size:2.8rem;font-weight:700;letter-spacing:8px;color:#00ff41;
                text-shadow:0 0 15px #00ff41,0 0 35px #00ff41,0 0 70px #00cc33;
                animation:glitch 3s infinite;
                white-space:nowrap;
            }
            @keyframes glitch{
                0%,90%,100%{text-shadow:0 0 15px #00ff41,0 0 35px #00ff41;transform:none;}
                91%{text-shadow:-4px 0 #ff0066,4px 0 #00ffff;transform:translate(-3px,1px);}
                92%{text-shadow: 4px 0 #ff0066,-4px 0 #00ffff;transform:translate(3px,-1px);}
                93%{text-shadow:-2px 0 #00ffff,2px 0 #ff0066;transform:translate(1px,2px);}
                94%{text-shadow:0 0 15px #00ff41;transform:none;}
            }
            #sub-title{
                font-family:'Share Tech Mono',monospace;
                font-size:1.1rem;letter-spacing:4px;color:#00cc33;
                text-shadow:0 0 10px #00cc33;
                animation:fadeInSub 0.5s 0.4s both;
            }
            @keyframes fadeInSub{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:none;}}

            /* tipler */
            #typed-line{
                font-family:'Share Tech Mono',monospace;
                font-size:0.9rem;color:#00ff41;letter-spacing:2px;
                min-height:1.4em;
                text-shadow:0 0 8px #00ff41;
            }
            #typed-line::after{content:'█';animation:blink 0.7s infinite;}
            @keyframes blink{0%,100%{opacity:1;}50%{opacity:0;}}

            /* ilerleyiş çubuğu */
            #prog-wrap{
                width:380px;height:6px;border-radius:4px;
                background:rgba(0,255,65,0.12);
                border:1px solid rgba(0,255,65,0.3);
                overflow:hidden;
                animation:fadeInSub 0.4s 0.6s both;
            }
            #prog-bar{
                height:100%;width:0%;border-radius:4px;
                background:linear-gradient(90deg,#00ff41,#00cc33);
                box-shadow:0 0 12px #00ff41;
                transition:width 0.05s linear;
            }

            #badge{
                font-family:'Share Tech Mono',monospace;
                font-size:0.75rem;color:#000;
                background:#00ff41;padding:5px 22px;border-radius:4px;
                letter-spacing:3px;box-shadow:0 0 20px #00ff41;
                opacity:0;animation:badgePop 0.4s 2.6s ease-out forwards;
            }
            @keyframes badgePop{from{opacity:0;transform:scale(0.6);}to{opacity:1;transform:scale(1);}}
            </style>

            <div id="intro-wrap">
              <canvas id="ic"></canvas>
              <div id="intro-box">
                <div id="skull">💀</div>
                <div id="main-title">HACKER MODU AKTİF</div>
                <div id="sub-title">⚡ SAZAN HACK SİSTEMİ v2.0 ⚡</div>
                <div id="typed-line"></div>
                <div id="prog-wrap"><div id="prog-bar"></div></div>
                <div id="badge">MAXIMUM CODE QUALITY UNLOCKED</div>
              </div>
            </div>

            <script>
            (function(){
              /* ── Matrix arka plan ── */
              const cv=document.getElementById('ic');
              const ctx=cv.getContext('2d');
              function resize(){cv.width=cv.offsetWidth||700;cv.height=cv.offsetHeight||420;}
              resize(); window.addEventListener('resize',resize);
              const CH='アイウエオ0123456789ABCDEF<>{}[]!@#$';
              let drops=[];
              function initDrops(){drops=Array.from({length:Math.floor(cv.width/14)},()=>Math.random()*-50|0);}
              initDrops();
              function drawMatrix(){
                ctx.fillStyle='rgba(0,0,0,0.85)';ctx.fillRect(0,0,cv.width,cv.height);
                ctx.font='13px monospace';
                drops.forEach((d,i)=>{
                  const ch=CH[Math.random()*CH.length|0];
                  const y=d*14;
                  ctx.fillStyle=`rgba(200,255,200,0.9)`;ctx.fillText(ch,i*14,y);
                  ctx.fillStyle=`rgba(0,180,50,0.3)`;ctx.fillText(CH[Math.random()*CH.length|0],i*14,y-14);
                  if(y>cv.height&&Math.random()>0.97)drops[i]=0; drops[i]++;
                });
                requestAnimationFrame(drawMatrix);
              }
              drawMatrix();

              /* ── Typing efekti + progress ── */
              const LINES=[
                'ACCESS GRANTED...',
                'LOADING ELITE CODE ENGINE...',
                'INJECTING HACKER PROTOCOL...',
                'MAXIMUM QUALITY MODE ON ✓',
              ];
              const typed=document.getElementById('typed-line');
              const bar=document.getElementById('prog-bar');
              let li=0,ci=0,prog=0;
              const TOTAL_MS=2600;
              const startT=performance.now();

              function typeNext(){
                if(li>=LINES.length)return;
                const line=LINES[li];
                if(ci<line.length){
                  typed.textContent=line.slice(0,ci+1);
                  ci++;
                  setTimeout(typeNext, 38+Math.random()*22);
                } else {
                  ci=0; li++;
                  if(li<LINES.length) setTimeout(typeNext,220);
                  else typed.textContent=LINES[LINES.length-1];
                }
              }
              typeNext();

              function tickBar(){
                const elapsed=performance.now()-startT;
                prog=Math.min(100,elapsed/TOTAL_MS*100);
                bar.style.width=prog+'%';
                if(prog<100) requestAnimationFrame(tickBar);
              }
              tickBar();
            })();
            </script>
            """,
            height=430,
        )
        # Intro gösterildi, bir daha render edilmesin
        st.session_state.hacker_intro_shown = True
        # 0.1s bekle ve rerun ile matrix moduna geç
        time.sleep(3.2)
        st.rerun()

    else:
        # ── Intro bitti, kalıcı matrix + HUD ──
        st.components.v1.html(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
            *{margin:0;padding:0;box-sizing:border-box;}
            body{background:#000;overflow:hidden;}
            #mwrap{width:100%;height:280px;position:relative;background:#000;}
            #mc{display:block;width:100%;height:100%;}
            #mhud{
                position:absolute;top:0;left:0;width:100%;height:100%;
                display:flex;flex-direction:column;
                justify-content:center;align-items:center;
                pointer-events:none;gap:6px;
            }
            #mhud-title{
                font-family:'Share Tech Mono',monospace;
                font-size:1.6rem;letter-spacing:6px;color:#00ff41;
                text-shadow:0 0 10px #00ff41,0 0 25px #00cc33;
                animation:glitch2 4s infinite;
            }
            @keyframes glitch2{
                0%,92%,100%{transform:none;text-shadow:0 0 10px #00ff41,0 0 25px #00cc33;}
                93%{transform:translate(-2px,0);text-shadow:-3px 0 #ff0066,3px 0 #00ffff;}
                94%{transform:translate(2px,0);text-shadow:3px 0 #ff0066,-3px 0 #00ffff;}
            }
            #mhud-sub{
                font-family:'Share Tech Mono',monospace;font-size:0.72rem;
                color:#007a20;letter-spacing:3px;
            }
            /* corner brackets */
            .cb{position:absolute;width:30px;height:30px;border-color:#00ff41;border-style:solid;opacity:0.6;}
            .cb.tl{top:10px;left:10px;border-width:2px 0 0 2px;}
            .cb.tr{top:10px;right:10px;border-width:2px 2px 0 0;}
            .cb.bl{bottom:10px;left:10px;border-width:0 0 2px 2px;}
            .cb.br{bottom:10px;right:10px;border-width:0 2px 2px 0;}
            </style>
            <div id="mwrap">
              <canvas id="mc"></canvas>
              <div class="cb tl"></div><div class="cb tr"></div>
              <div class="cb bl"></div><div class="cb br"></div>
              <div id="mhud">
                <div id="mhud-title">💀 HACKER SAZAN MODU</div>
                <div id="mhud-sub">⚡ KOD MAKİNESİ HAZIR — YAZAR BEKLENIYOR ⚡</div>
              </div>
            </div>
            <script>
            (function(){
              const cv=document.getElementById('mc');
              const ctx=cv.getContext('2d');
              function resize(){cv.width=cv.offsetWidth||700;cv.height=cv.offsetHeight||280;}
              resize();window.addEventListener('resize',resize);
              const CH='アイウエオ0123456789ABCDEF<>{}[]!@#$%^';
              let drops=[];
              function init(){drops=Array.from({length:Math.floor(cv.width/14)},()=>Math.random()*-40|0);}
              init();
              /* floating code particles */
              const SN=['import os','def hack():','while True:','SELECT *','git push',
                        '0xDEAD','chmod +x','ssh root@','docker run','AES-256','RSA_2048',
                        'malloc(512)','XOR eax','async def','Promise.all'];
              const pts=Array.from({length:18},()=>({
                x:Math.random()*700,y:Math.random()*280,
                vx:(Math.random()-0.5)*0.5,vy:(Math.random()-0.5)*0.35,
                t:SN[Math.random()*SN.length|0],a:Math.random()*0.4+0.1,
              }));
              let sc=0,frame=0;
              function draw(){
                const W=cv.width,H=cv.height;
                ctx.fillStyle='rgba(0,0,0,0.84)';ctx.fillRect(0,0,W,H);
                ctx.font='13px monospace';
                drops.forEach((d,i)=>{
                  const ch=CH[Math.random()*CH.length|0];
                  const y=d*14;
                  ctx.fillStyle='rgba(180,255,180,0.85)';ctx.fillText(ch,i*14,y);
                  ctx.fillStyle='rgba(0,150,40,0.28)';ctx.fillText(CH[Math.random()*CH.length|0],i*14,y-14);
                  if(y>H&&Math.random()>0.975)drops[i]=0; drops[i]++;
                });
                /* hex grid */
                const hr=24,hw=hr*Math.sqrt(3),hh=hr*2;
                ctx.lineWidth=0.4;
                for(let r=-1;r<H/hh*1.5;r++)for(let c=-1;c<W/hw*1.2;c++){
                  const cx=c*hw+(r%2?hw/2:0),cy=r*hh*0.75;
                  ctx.beginPath();
                  for(let k=0;k<6;k++){const a=Math.PI/3*k-Math.PI/6;k?ctx.lineTo(cx+hr*Math.cos(a),cy+hr*Math.sin(a)):ctx.moveTo(cx+hr*Math.cos(a),cy+hr*Math.sin(a));}
                  ctx.closePath();
                  ctx.strokeStyle=`rgba(0,255,65,${0.03+0.015*Math.sin(frame*0.02+c+r)})`;
                  ctx.stroke();
                }
                /* particles */
                ctx.font='10px "Share Tech Mono",monospace';
                pts.forEach(p=>{
                  p.x+=p.vx;p.y+=p.vy;
                  if(p.x<-100)p.x=W+10; if(p.x>W+10)p.x=-100;
                  if(p.y<-15)p.y=H+5;   if(p.y>H+5)p.y=-15;
                  ctx.globalAlpha=p.a*(0.4+0.3*Math.sin(frame*0.05+p.x*0.01));
                  ctx.fillStyle='#00ff41';ctx.shadowColor='#00ff41';ctx.shadowBlur=6;
                  ctx.fillText(p.t,p.x,p.y);
                  ctx.globalAlpha=1;ctx.shadowBlur=0;
                });
                /* scan line */
                sc=(sc+1.0)%H;
                const sg=ctx.createLinearGradient(0,sc-6,0,sc+6);
                sg.addColorStop(0,'rgba(0,255,65,0)');sg.addColorStop(0.5,'rgba(0,255,65,0.14)');sg.addColorStop(1,'rgba(0,255,65,0)');
                ctx.fillStyle=sg;ctx.fillRect(0,sc-6,W,12);
                frame++;requestAnimationFrame(draw);
              }
              draw();
            })();
            </script>
            """,
            height=285,
        )

if not active_messages and not st.session_state.get("hacker_mode", False):
    st.markdown(
        """
        <div class='sz-hero sz-hero-mini'>
            <h2>Merhaba 👋 Ben Sazan AI</h2>
            <p>Bir şey sor, bir oyun tarif et ya da aşağıdaki önerilerden birine dokun.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    chip_cols = st.columns(3)
    for i, sug in enumerate(QUICK_SUGGESTIONS):
        with chip_cols[i % 3]:
            if st.button(sug, key=f"chip_{i}", use_container_width=True):
                st.session_state.pending_prompt = sug.split(" ", 1)[1]
                st.rerun()
elif not active_messages:
    pass  # hacker modunda boş ekranda sadece simülasyon görünür

# -----------------------------------------------------------------------
# Kod bloğu → uzantı/MIME/ikon eşleme tablosu
# -----------------------------------------------------------------------
_EXT_MAP = {
    # Web
    "html": ("html", "text/html", "🌐"),
    "css":  ("css",  "text/css",  "🎨"),
    "js":   ("js",   "text/javascript", "⚙️"),
    "javascript": ("js", "text/javascript", "⚙️"),
    # Veri / config
    "json": ("json", "application/json", "📋"),
    "yaml": ("yaml", "text/yaml", "📋"),
    "yml":  ("yml",  "text/yaml", "📋"),
    "xml":  ("xml",  "application/xml", "📋"),
    "csv":  ("csv",  "text/csv", "📊"),
    "toml": ("toml", "text/plain", "📋"),
    "env":  ("env",  "text/plain", "🔐"),
    # Python ekosistemi
    "python": ("py", "text/x-python", "🐍"),
    "py":     ("py", "text/x-python", "🐍"),
    # Sistem / shell
    "bash":       ("sh",  "text/x-sh", "💻"),
    "sh":         ("sh",  "text/x-sh", "💻"),
    "powershell": ("ps1", "text/plain", "💻"),
    "ps1":        ("ps1", "text/plain", "💻"),
    "batch":      ("bat", "text/plain", "💻"),
    "bat":        ("bat", "text/plain", "💻"),
    # C ailesi
    "c":    ("c",   "text/x-c", "⚙️"),
    "cpp":  ("cpp", "text/x-c++", "⚙️"),
    "c++":  ("cpp", "text/x-c++", "⚙️"),
    "h":    ("h",   "text/x-c", "⚙️"),
    # JVM
    "java":   ("java",   "text/x-java-source", "☕"),
    "kotlin": ("kt",     "text/x-kotlin", "☕"),
    "kt":     ("kt",     "text/x-kotlin", "☕"),
    # .NET
    "csharp": ("cs",  "text/plain", "🔷"),
    "cs":     ("cs",  "text/plain", "🔷"),
    "vb":     ("vb",  "text/plain", "🔷"),
    # Fonksiyonel / diğer
    "rust":   ("rs",  "text/plain", "🦀"),
    "rs":     ("rs",  "text/plain", "🦀"),
    "go":     ("go",  "text/plain", "🐹"),
    "ruby":   ("rb",  "text/plain", "💎"),
    "rb":     ("rb",  "text/plain", "💎"),
    "php":    ("php", "text/plain", "🐘"),
    "swift":  ("swift","text/plain","🍎"),
    "r":      ("r",   "text/plain", "📊"),
    "scala":  ("scala","text/plain","⚙️"),
    "lua":    ("lua", "text/plain", "🌙"),
    # Veritabanı
    "sql": ("sql", "text/plain", "🗄️"),
    # Metin / doküman
    "markdown": ("md",  "text/markdown", "📝"),
    "md":       ("md",  "text/markdown", "📝"),
    "txt":      ("txt", "text/plain", "📄"),
    "text":     ("txt", "text/plain", "📄"),
    # Altyapı / DevOps
    "dockerfile": ("Dockerfile", "text/plain", "🐳"),
    "docker":     ("Dockerfile", "text/plain", "🐳"),
    "terraform":  ("tf",  "text/plain", "🏗️"),
    "tf":         ("tf",  "text/plain", "🏗️"),
    "nginx":      ("conf","text/plain", "🌐"),
    "apache":     ("conf","text/plain", "🌐"),
}

def _parse_code_blocks(content: str):
    """
    İçerikteki tüm ```lang ... ``` bloklarını bulur.
    Dönüş: list of (lang_raw, code_str, ext, mime, icon)
    """
    pattern = re.compile(r"```(\w*)\s*(.*?)\s*```", re.DOTALL)
    results = []
    for m in pattern.finditer(content):
        lang_raw = m.group(1).lower().strip()
        code = m.group(2)
        ext, mime, icon = _EXT_MAP.get(lang_raw, ("txt", "text/plain", "📄"))
        results.append((lang_raw, code, ext, mime, icon))
    return results


for idx, m in enumerate(active_messages):
    with st.chat_message(m["role"]):
        content = m["content"]
        blocks = _parse_code_blocks(content)
        html_blocks = [b for b in blocks if b[0] == "html"]

        if html_blocks:
            # HTML oyun varsa temizlenmiş metni göster + oyun aksiyonları
            clean_text = re.sub(r"```html\s*(.*?)\s*```", "", content, flags=re.DOTALL).strip()
            if clean_text:
                st.markdown(clean_text)

            game_code = html_blocks[0][1]
            b64_game = base64.b64encode(game_code.encode("utf-8")).decode("utf-8")
            game_url = f"data:text/html;base64,{b64_game}"

            st.markdown(
                f'<a href="{game_url}" target="_blank" class="launch-game-btn">🎮 Oyunu Yeni Sekmede Başlat</a>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "⬇️ Oyunu .html Olarak İndir",
                data=game_code,
                file_name=f"sazan_oyun_{idx}.html",
                mime="text/html",
                key=f"dl_html_{st.session_state.current_chat}_{idx}",
            )
            with st.expander("🛠️ Kaynak Kodu Görüntüle"):
                st.code(game_code, language="html")

        elif blocks:
            # HTML olmayan kod blokları — her biri için indir butonu ekle
            # Önce markdown'ı bloklardan arındırarak göster
            clean_text = re.sub(r"```\w*\s*.*?\s*```", "", content, flags=re.DOTALL).strip()
            if clean_text:
                st.markdown(clean_text)

            for b_idx, (lang_raw, code, ext, mime, icon) in enumerate(blocks):
                # Orijinal ```lang ... ``` bloğunu syntax-highlight ile göster
                st.code(code, language=lang_raw if lang_raw else None)
                safe_name = re.sub(r"[^a-z0-9_]", "_", lang_raw) if lang_raw else "kod"
                st.download_button(
                    f"{icon} .{ext} olarak indir",
                    data=code,
                    file_name=f"sazan_{safe_name}_{idx}_{b_idx}.{ext}",
                    mime=mime,
                    key=f"dl_{lang_raw}_{st.session_state.current_chat}_{idx}_{b_idx}",
                )
        else:
            st.markdown(content)

# =====================================================================
# 14. GÖRSEL ÜRETİM ATÖLYESİ (SADECE ÜYE)
# =====================================================================
if is_member and st.session_state.show_image_studio:
    st.markdown("<div class='studio-panel'>", unsafe_allow_html=True)
    st.markdown("<h4>🎨 Görsel Üretim Atölyesi</h4>", unsafe_allow_html=True)
    st.markdown(
        "Aklındaki görseli anlat; Sazan önce fikrini profesyonel bir prompt'a dönüştürsün, "
        "sonra gerçek bir görsel üretsin. Hangi dilde yazarsan yaz, çeviri otomatik yapılır."
    )

    img_col1, img_col2 = st.columns([1.5, 1])
    with img_col1:
        ham_fikir = st.text_area(
            "💭 Görsel Fikrin:",
            placeholder="Örn: Ay ışığında bir kaleye bakan zırhlı bir ejderha, sisli dağlar arasında...",
            key="img_forge_prompt_input",
            height=110,
        )
        stil_secim = st.selectbox("🎭 Görsel Stili:", list(IMAGE_STYLE_PRESETS.keys()), key="img_forge_style_select")

        enh_col, gen_col = st.columns(2)
        with enh_col:
            enhance_clicked = st.button("✨ AI ile Prompt'u Geliştir", use_container_width=True)
        with gen_col:
            generate_clicked = st.button("🖼️ Görseli Üret", use_container_width=True, type="primary")

        if enhance_clicked:
            if ham_fikir.strip():
                with st.spinner("Prompt zenginleştiriliyor..."):
                    cur_model_cfg = AI_MODELS[st.session_state.active_model_label]
                    zenginlesmis = SazanImageForge.enhance_prompt_with_ai(ham_fikir, cur_model_cfg)
                    st.session_state["img_forge_enhanced_prompt"] = zenginlesmis
                    st.rerun()
            else:
                st.warning("Önce bir görsel fikri yaz.")

        if st.session_state.get("img_forge_enhanced_prompt"):
            st.text_area(
                "🧠 AI Tarafından Geliştirilmiş Prompt (elle düzenleyebilirsin):",
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
            sabit_seed = st.number_input("Sabit Seed Değeri", min_value=1, max_value=9999999, value=42, step=1)

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
            with st.spinner("🎨 Görsel oluşturuluyor... Lütfen bekleyin..."):
                try:
                    stil_suffix = IMAGE_STYLE_PRESETS.get(stil_secim, "")
                    img_bytes, kullanilan_prompt, kullanilan_seed = SazanImageForge.generate_image(
                        nihai_prompt, style_suffix=stil_suffix, width=secili_w, height=secili_h, seed=sabit_seed,
                    )
                    st.session_state["img_forge_last_result"] = {
                        "bytes": img_bytes, "prompt": kullanilan_prompt, "seed": kullanilan_seed, "stil": stil_secim,
                    }
                    SazanImageGallery.add_image(user, ham_fikir or nihai_prompt, stil_secim, img_bytes)
                    st.toast("🖼️ Görsel galeriye kaydedildi!")
                except Exception as e:
                    st.error(f"⚠️ Görsel üretilirken hata oluştu: {e}")

    if st.session_state.get("img_forge_last_result"):
        sonuc = st.session_state["img_forge_last_result"]
        st.divider()
        st.image(sonuc["bytes"], caption=f"Seed: {sonuc['seed']} | Stil: {sonuc['stil']}", use_container_width=True)
        st.download_button(
            "⬇️ Görseli .png Olarak İndir", data=sonuc["bytes"],
            file_name=f"sazan_gorsel_{sonuc['seed']}.png", mime="image/png", use_container_width=True,
        )
        with st.expander("🔍 Kullanılan Nihai Prompt"):
            st.code(sonuc["prompt"], language="text")

    st.divider()
    st.markdown("📚 **Görsel Galerim**")
    galeri = SazanImageGallery.get_gallery(user)
    if not galeri:
        st.info("Henüz galerinde kayıtlı bir görsel yok.")
    else:
        gal_cols = st.columns(3)
        for i, g in enumerate(galeri):
            with gal_cols[i % 3]:
                st.markdown("<div class='gallery-card'>", unsafe_allow_html=True)
                img_raw = base64.b64decode(g["image_b64"])
                st.image(img_raw, use_container_width=True)
                st.caption(f"🎭 {g['stil']}  ·  {g['created_at']}")
                kisa_prompt = g["prompt"][:60] + ("..." if len(g["prompt"]) > 60 else "")
                st.caption(f"💭 {kisa_prompt}")
                gcol1, gcol2 = st.columns(2)
                with gcol1:
                    st.download_button("⬇️", data=img_raw, file_name=f"sazan_gorsel_{g['id']}.png",
                                        mime="image/png", key=f"gal_dl_{g['id']}", use_container_width=True)
                with gcol2:
                    if st.button("🗑️", key=f"gal_del_{g['id']}", use_container_width=True):
                        SazanImageGallery.delete_image(user, g["id"])
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 15. 3D BASKI ATÖLYESİ (SADECE ÜYE)
# =====================================================================
if is_member and st.session_state.show_print_studio:
    st.markdown("<div class='studio-panel'>", unsafe_allow_html=True)
    st.markdown("<h4>🖨️ 3D Baskı Atölyesi — Görselden STL Üretici</h4>", unsafe_allow_html=True)
    st.markdown(
        "Bir görsel yükle; Sazan onu gri tonlamalı bir yükseklik haritasına çevirip 3D "
        "yazıcında basabileceğin kapalı (watertight) bir .stl kabartma modeli üretsin. "
        "Bu bir lityofan/rölyef dönüşümüdür — portre, logo ve harita gibi görsellerde en iyi sonucu verir."
    )

    uploaded_img = st.file_uploader("📤 Görsel Yükle (PNG / JPG / JPEG)", type=["png", "jpg", "jpeg"], key="stl_uploader")

    if uploaded_img is not None:
        pil_image = Image.open(uploaded_img)
        col_prev, col_opts = st.columns([1, 1.3])

        with col_prev:
            st.image(pil_image, caption="Yüklenen Görsel", use_container_width=True)

        with col_opts:
            boyut_mm = st.slider("Genişlik/Uzunluk (mm)", 30, 200, 80, step=5)
            taban_mm = st.slider("Taban Kalınlığı (mm)", 0.5, 5.0, 2.0, step=0.5)
            rolyef_mm = st.slider("Kabartma Yüksekliği (mm)", 1.0, 15.0, 5.0, step=0.5)
            cozunurluk = st.slider("Çözünürlük (piksel)", 30, SazanPrintStudio.MAX_RESOLUTION_PX, 120, step=10)
            ters_cevir = st.checkbox("Tonları Ters Çevir (koyu alanlar daha yüksek olsun)", value=False)

        if st.button("🧊 STL Modelini Oluştur", use_container_width=True, type="primary"):
            with st.spinner("Yükseklik haritası ve 3D örgü hesaplanıyor..."):
                try:
                    max_w = max(pil_image.width, pil_image.height)
                    pixel_size_mm = boyut_mm / min(cozunurluk, max_w)
                    stl_bytes, info = SazanPrintStudio.generate_stl_from_image(
                        pil_image, max_size_px=cozunurluk, base_height_mm=taban_mm,
                        relief_height_mm=rolyef_mm, pixel_size_mm=pixel_size_mm, invert=ters_cevir,
                    )
                    w_mm, d_mm, h_mm = info["boyut_mm"]
                    st.success(
                        f"✅ Model hazır! Boyut: {w_mm} x {d_mm} x {h_mm} mm | "
                        f"Üçgen: {info['triangles']:,} | Çözünürlük: {info['resolution'][0]}x{info['resolution'][1]} px"
                    )
                    st.download_button(
                        "⬇️ .stl Dosyasını İndir", data=stl_bytes,
                        file_name=f"sazan_3d_model_{uuid.uuid4().hex[:6]}.stl", mime="model/stl",
                        use_container_width=True,
                    )
                    st.caption("İndirdiğin .stl dosyasını Cura, PrusaSlicer veya Bambu Studio gibi bir dilimleyiciye yükleyebilirsin.")
                except Exception as e:
                    st.error(f"⚠️ Model üretilirken hata oluştu: {e}")
    else:
        st.info("👆 Başlamak için yukarıdaki kutuya tıklayıp bir görsel yükle.")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 16. OYUN KÜTÜPHANEM (SADECE ÜYE)
# =====================================================================
if is_member:
    lib = SazanGameLibrary.get_library(user)
    if lib:
        with st.expander(f"📚 Oyun Kütüphanem ({len(lib)})"):
            for g in lib:
                st.markdown("<div class='gallery-card'>", unsafe_allow_html=True)
                st.markdown(f"**🎮 {g['title']}**  <span class='badge'>{g['created_at']}</span>", unsafe_allow_html=True)
                b64_game = base64.b64encode(g["code"].encode("utf-8")).decode("utf-8")
                game_url = f"data:text/html;base64,{b64_game}"
                lc1, lc2, lc3 = st.columns([1.3, 1.3, 0.6])
                with lc1:
                    st.markdown(f'<a href="{game_url}" target="_blank" class="launch-game-btn">▶️ Başlat</a>', unsafe_allow_html=True)
                with lc2:
                    st.download_button("⬇️ İndir", data=g["code"], file_name=f"{g['title'][:30]}.html",
                                        mime="text/html", key=f"lib_dl_{g['id']}")
                with lc3:
                    if st.button("🗑️", key=f"lib_del_{g['id']}"):
                        SazanGameLibrary.delete_game(user, g["id"])
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 17. SOHBET GİRDİSİ VE YANIT MOTORU
# =====================================================================
_is_hacker   = st.session_state.get("hacker_mode", False)
_COOLDOWN_S  = 60          # saniye
_CODE_LANGS  = {           # bu dil etiketleri "kod yanıtı" sayılır
    "python","py","javascript","js","typescript","ts","html","css","bash","sh",
    "java","cpp","c","cs","go","rust","rs","php","ruby","rb","sql","kotlin","swift",
    "json","yaml","yml","toml","dockerfile","docker","terraform","tf","r","scala","lua",
}

# ── Cooldown durumu ──────────────────────────────────────────────────
_now          = time.time()
_cooldown_end = st.session_state.get("cooldown_until", 0.0)
_remaining    = max(0.0, _cooldown_end - _now)
_in_cooldown  = _remaining > 0

if _in_cooldown:
    # Kalan süreyi göster — Streamlit'in auto-rerun mekanizması olmadığı için
    # st.empty() + time.sleep(1) döngüsüyle gerçek zamanlı sayaç çiziyoruz
    _cd_placeholder = st.empty()
    _cd_bar         = st.empty()

    # Her saniye güncelle; toplam kalan süreyi hesapla
    _elapsed_in_block = 0
    _total_wait       = int(_remaining) + 1
    for _tick in range(_total_wait):
        _secs_left = max(0, int(_cooldown_end - time.time()))
        _pct       = _secs_left / _COOLDOWN_S

        _cd_placeholder.markdown(
            f"""
            <div style="
                background:linear-gradient(135deg,#0d1117,#0a1a0a);
                border:1px solid {'#00ff41' if _is_hacker else '#f97316'};
                border-radius:12px;padding:16px 24px;text-align:center;
                box-shadow:0 0 20px {'rgba(0,255,65,0.15)' if _is_hacker else 'rgba(249,115,22,0.15)'};
                font-family:{'Share Tech Mono,monospace' if _is_hacker else 'inherit'};
            ">
                <div style="font-size:2.2rem;margin-bottom:4px;">⏳</div>
                <div style="font-size:1.6rem;font-weight:700;
                    color:{'#00ff41' if _is_hacker else '#f97316'};
                    text-shadow:{'0 0 10px #00ff41' if _is_hacker else 'none'};">
                    {_secs_left:02d} saniye
                </div>
                <div style="color:#888;font-size:0.82rem;margin-top:4px;">
                    {'💀 Kod motoru soğuyor — bir sonraki istek için bekle' if _is_hacker else '🐟 Sazan AI soğuyor — biraz bekle'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _cd_bar.markdown(
            f"""
            <div style="height:6px;border-radius:4px;background:rgba(255,255,255,0.08);overflow:hidden;margin-top:4px;">
              <div style="height:100%;width:{_pct*100:.1f}%;border-radius:4px;
                background:{'linear-gradient(90deg,#00ff41,#00cc33)' if _is_hacker else 'linear-gradient(90deg,#f97316,#facc15)'};
                transition:width 0.9s linear;
                box-shadow:{'0 0 8px #00ff41' if _is_hacker else '0 0 8px #f97316'};"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if _secs_left <= 0:
            break
        time.sleep(1)

    _cd_placeholder.empty()
    _cd_bar.empty()
    st.session_state.cooldown_until = 0.0
    st.rerun()

else:
    # ── Normal giriş akışı ────────────────────────────────────────────
    _chat_placeholder = "💀 Kod yaz, hack et, inşa et..." if _is_hacker else "Sazan AI'a bir şey sor..."
    typed_prompt = st.chat_input(_chat_placeholder)
    prompt = typed_prompt or st.session_state.pending_prompt
    if st.session_state.pending_prompt and not typed_prompt:
        st.session_state.pending_prompt = None

    if prompt:
        active_messages.append({"role": "user", "content": prompt})

        model_label = st.session_state.active_model_label if is_member else GUEST_MODEL_LABEL
        model_cfg   = AI_MODELS.get(model_label, AI_MODELS[GUEST_MODEL_LABEL])

        _spinner_text = "💀 Kod derleniyor..." if _is_hacker else "Sazan AI düşünüyor..."
        with st.spinner(_spinner_text):
            cur_lang = st.session_state.get("active_lang_code", "Türkçe 🇹🇷")
            ans = SazanAIConception.query_agent(
                prompt, active_messages, cur_lang, model_cfg,
                hacker_mode=_is_hacker,
            )
            active_messages.append({"role": "assistant", "content": ans})

            # ── Kod yanıtı mı? → cooldown başlat ──────────────────────
            _found_langs = set(re.findall(r"```(\w+)", ans))
            if _found_langs & _CODE_LANGS:
                st.session_state.cooldown_until = time.time() + _COOLDOWN_S

            html_blocks = re.findall(r"```html\s*(.*?)\s*```", ans, re.DOTALL)
            if html_blocks and is_member:
                entry = SazanGameLibrary.add_game(user, prompt, html_blocks[0])
                st.toast(f"📚 Oyun kütüphaneye kaydedildi: {entry['title']}")

            if is_member:
                SazanChatStore.save_sessions(user, st.session_state.chat_sessions)

            st.rerun()
