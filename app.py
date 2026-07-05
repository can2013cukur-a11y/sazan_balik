# ================================================================================
#   🐟  S A Z A N   A I   —   v120.0  "AURORA"
#   Modern, Gemini esintili sohbet deneyimi.
#   Ekonomi / bakiye / RPG sistemleri tamamen kaldırıldı.
#   Misafir: sohbet + tek sabit model. Üye: 7 model + görsel üretimi + 3D baskı.
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
from datetime import datetime

import numpy as np
from PIL import Image
from stl import mesh as stl_mesh

from groq import Groq

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

# =====================================================================
# 3. VERİ DEPOLARI
# =====================================================================
DATA_DIR = "sazan_data"
os.makedirs(DATA_DIR, exist_ok=True)

AUTH_FILE = os.path.join(DATA_DIR, "sazan_auth.json")
CHATS_FILE = os.path.join(DATA_DIR, "sazan_chats.json")
GAMES_LIBRARY_FILE = os.path.join(DATA_DIR, "sazan_games_library.json")
IMAGE_GALLERY_FILE = os.path.join(DATA_DIR, "sazan_image_gallery.json")


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

# =====================================================================
# 4. KİMLİK DOĞRULAMA (GMAIL + ŞİFRE)
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
        }
        SazanAuth._save(db)

    @staticmethod
    def verify(email: str, password: str) -> bool:
        rec = SazanAuth._load().get(email.strip().lower())
        if not rec:
            return False
        return SazanAuth._hash(password, rec["salt"]) == rec["password_hash"]


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
if "GROQ_API_KEY" not in st.secrets:
    st.error(
        "🚨 GROQ_API_KEY bulunamadı!\n\n"
        "`.streamlit/secrets.toml` dosyanıza (yerelde) veya Streamlit Cloud "
        "'Settings > Secrets' bölümüne şunu ekleyin:\n\n"
        'GROQ_API_KEY = "gsk_sizin_anahtariniz"'
    )
    st.stop()

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Misafirler bu tek modeli kullanır. Üyeler aşağıdaki 7 modelin tamamına erişir.
GUEST_MODEL_LABEL = "⚡ Sazan Hız"

AI_MODELS = {
    "⚡ Sazan Hız": {
        "id": "openai/gpt-oss-20b",
        "effort": "low",
        "temp": 0.55,
        "desc": "Anında yanıt veren en hızlı model. Günlük sohbetler için ideal.",
    },
    "🧠 Sazan Dengeli": {
        "id": "openai/gpt-oss-120b",
        "effort": "medium",
        "temp": 0.4,
        "desc": "Hız ve akıl yürütme gücü arasında dengeli, günlük kullanım için önerilir.",
    },
    "👑 Sazan Ultra": {
        "id": "openai/gpt-oss-120b",
        "effort": "high",
        "temp": 0.3,
        "desc": "En güçlü akıl yürütme motoru. Karmaşık kod ve oyun üretimi için.",
    },
    "🔬 Sazan Derin Analiz": {
        "id": "openai/gpt-oss-120b",
        "effort": "high",
        "temp": 0.15,
        "desc": "Adım adım, titiz ve uzun analitik yanıtlar üretir.",
    },
    "🎨 Sazan Görsel Akıl": {
        "id": "qwen/qwen3.6-27b",
        "effort": "default",
        "temp": 0.5,
        "desc": "Çok modlu düşünce yapısı; yaratıcı ve görsel-duyarlı yanıtlarda güçlü.",
    },
    "🛡️ Sazan Güvenli Mod": {
        "id": "openai/gpt-oss-safeguard-20b",
        "effort": "medium",
        "temp": 0.35,
        "desc": "Ekstra güvenlik katmanlı, hassas konularda temkinli yanıtlar.",
    },
    "🌐 Sazan Ajan (Compound)": {
        "id": "groq/compound",
        "effort": None,
        "temp": 0.4,
        "desc": "Gerektiğinde otomatik web araması ve kod çalıştırma araçlarını kullanabilir.",
    },
}

MAX_CONTINUATIONS = 4
DEFAULT_MAX_TOKENS = 3000  # TPM limitine takılmamak için ölçülü tutuluyor (continuation ile tamamlanır)
MIN_MAX_TOKENS = 700


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
    def _tek_istek(messages, model_cfg, max_tokens=DEFAULT_MAX_TOKENS):
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
        try:
            return groq_client.chat.completions.create(**kwargs)
        except Exception as e:
            err_text = str(e).lower()
            if "reasoning_effort" in err_text or "unsupported" in err_text:
                # reasoning_effort desteklemeyen bir model olabilir — onsuz tekrar dene
                kwargs.pop("reasoning_effort", None)
                return groq_client.chat.completions.create(**kwargs)
            if "rate_limit_exceeded" in err_text or "413" in err_text or "too large" in err_text:
                # TPM limiti aşıldı — daha küçük bir max_tokens ile tekrar dene
                smaller = max(MIN_MAX_TOKENS, int(max_tokens * 0.5))
                if smaller < max_tokens:
                    kwargs["max_tokens"] = smaller
                    return groq_client.chat.completions.create(**kwargs)
            raise

    @staticmethod
    def query_agent(prompt, history, target_lang, model_cfg):
        lowered = prompt.lower()
        if any(k in lowered for k in ["can muhammed çukur", "yapımcın kim", "yapımcısı", "kim yaptı"]):
            return (
                "Beni Can Muhammed Çukur tasarladı ve geliştirdi. "
                f"[Yanıt dili: {target_lang}]"
            )

        sys_prompt = (
            "Sen Sazan AI adında, sıcak, net ve yardımsever genel amaçlı bir yapay zeka "
            "asistanısın. Kullanıcıyla doğal bir sohbet dilinde konuş, sorularını dikkatle "
            "analiz et ve doğrudan, faydalı yanıtlar ver.\n\n"
            "OYUN ÜRETİMİ ÖZEL YETENEĞİ:\n"
            "Kullanıcı senden bir oyun/mini-uygulama isterse, tek bir HTML dosyası içinde "
            "çalışan, profesyonel kalitede bir oyun inşa et:\n"
            "1. Menü, oynanış, duraklatma ve 'oyun bitti' ekranlarını içeren net bir durum "
            "makinesi (state machine) kullan.\n"
            "2. Temiz, okunabilir ES6+ JavaScript yaz; requestAnimationFrame tabanlı, "
            "delta-time uygulayan düzgün bir oyun döngüsü kur.\n"
            "3. Hem klavye hem dokunmatik kontrolleri destekle; canvas boyutu responsive olsun.\n"
            "4. Dış CDN/script/görsel/ses linki KULLANMA; oyun tamamen bağımsız ve tek dosyada "
            "offline çalışabilmeli (base64 data-URI olarak açılacak).\n"
            "5. Görseller için Canvas çizimleri, CSS gradyanları veya basit şekiller kullan.\n"
            "6. Kodu asla yarım bırakma; eksiksiz ve çalışır durumda bitir.\n"
            "7. Ürettiğin HTML kodunu KESİNLİKLE tek bir ```html ... ``` bloğu içine al.\n\n"
            "Oyun dışı tüm sohbet, açıklama ve yanıtlarını şu dilde yaz: " + target_lang
        )

        messages = [{"role": "system", "content": sys_prompt}]
        # Not: geçmişteki büyük HTML oyun kodları bağlamdan kısaltılır ki TPM
        # (dakika başına token) limitine takılmayalım. Son 6 mesajla sınırlı tutulur.
        for m in history[-6:-1]:
            messages.append({"role": m["role"], "content": _kisalt_gecmis_icerik(m["content"])})
        messages.append({"role": "user", "content": prompt})

        try:
            res = SazanAIConception._tek_istek(messages, model_cfg)
            combined = res.choices[0].message.content or ""
            finish_reason = res.choices[0].finish_reason

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
                res2 = SazanAIConception._tek_istek(messages, model_cfg)
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
            res = groq_client.chat.completions.create(
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
# 9. OTURUM DURUMU BAŞLATICI
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
        "img_forge_last_result": None,
        "img_forge_enhanced_prompt": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_session_state()
is_member = bool(st.session_state.username)
is_guest = st.session_state.guest_active and not is_member

# =====================================================================
# 10. GİRİŞ EKRANI (üye değil VE misafir modunda değilse)
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

            tab_login, tab_signup = st.tabs(["➡️ Giriş Yap", "🆕 Hesap Oluştur"])

            with tab_login:
                login_email = st.text_input("📧 Gmail Adresin", key="login_email_input", placeholder="[email protected]")
                login_pw = st.text_input("🔑 Şifren", type="password", key="login_pw_input")
                if st.button("Giriş Yap", use_container_width=True, type="primary", key="login_submit_btn"):
                    email_clean = login_email.strip()
                    if not email_clean or not login_pw:
                        st.error("⚠️ Lütfen e-posta ve şifreni gir.")
                    elif not SazanAuth.is_valid_gmail(email_clean):
                        st.error("❌ Geçersiz e-posta! '@gmail.com' ile biten bir adres gir.")
                    elif not SazanAuth.email_exists(email_clean):
                        st.error("❌ Bu Gmail adresine kayıtlı bir hesap yok. Önce kayıt ol.")
                    elif not SazanAuth.verify(email_clean, login_pw):
                        st.error("❌ Şifre yanlış! Lütfen tekrar dene.")
                    else:
                        st.session_state.username = email_clean.lower()
                        st.session_state.guest_active = False
                        st.session_state.chat_sessions = SazanChatStore.get_sessions(email_clean.lower())
                        st.session_state.current_chat = list(st.session_state.chat_sessions.keys())[0]
                        st.session_state.active_model_label = "🧠 Sazan Dengeli"
                        st.success("🎉 Giriş başarılı! Yönlendiriliyorsun...")
                        time.sleep(0.4)
                        st.rerun()

            with tab_signup:
                signup_email = st.text_input("📧 Gmail Adresin", key="signup_email_input", placeholder="[email protected]")
                signup_pw = st.text_input("🔑 Şifre Belirle (en az 6 karakter)", type="password", key="signup_pw_input")
                signup_pw_confirm = st.text_input("🔑 Şifreni Tekrar Gir", type="password", key="signup_pw_confirm_input")
                if st.button("Hesap Oluştur", use_container_width=True, type="primary", key="signup_submit_btn"):
                    email_clean = signup_email.strip()
                    if not email_clean or not signup_pw or not signup_pw_confirm:
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
                        st.session_state.username = email_clean.lower()
                        st.session_state.guest_active = False
                        st.session_state.chat_sessions = SazanChatStore.get_sessions(email_clean.lower())
                        st.session_state.current_chat = list(st.session_state.chat_sessions.keys())[0]
                        st.session_state.active_model_label = "🧠 Sazan Dengeli"
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
# 11. SIDEBAR
# =====================================================================
with st.sidebar:
    if is_member:
        st.markdown(f"<h3 style='color:#22d3ee; text-align:center;'>🐟 {user}</h3>", unsafe_allow_html=True)
        if st.button("🚪 Çıkış Yap", use_container_width=True):
            for k in ["username", "guest_active", "chat_sessions", "current_chat"]:
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
        st.markdown(
            f"<div class='model-pill'><b>{model_label}</b><br><span>{AI_MODELS[model_label]['desc']}</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.session_state.active_model_label = GUEST_MODEL_LABEL
        st.markdown(
            f"<div class='model-pill'><b>{GUEST_MODEL_LABEL}</b><br>"
            f"<span>{AI_MODELS[GUEST_MODEL_LABEL]['desc']}</span></div>",
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
    st.markdown("**🌐 Dil**")
    st.selectbox("Çeviri:", list(DIL_MATRISI.keys()), key="active_lang_code", label_visibility="collapsed")

# =====================================================================
# 12. ANA BAŞLIK
# =====================================================================
active_messages = st.session_state.chat_sessions.setdefault(st.session_state.current_chat, [])

if not active_messages:
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
                f'<a href="{game_url}" target="_blank" class="launch-game-btn">🎮 Oyunu Yeni Sekmede Başlat</a>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "⬇️ Oyunu .html Olarak İndir",
                data=game_code,
                file_name=f"sazan_oyun_{idx}.html",
                mime="text/html",
                key=f"dl_{st.session_state.current_chat}_{idx}",
            )
            with st.expander("🛠️ Kaynak Kodu Görüntüle"):
                st.code(game_code, language="html")
        else:
            st.markdown(content)

# =====================================================================
# 13. GÖRSEL ÜRETİM ATÖLYESİ (SADECE ÜYE)
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
# 14. 3D BASKI ATÖLYESİ (SADECE ÜYE)
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
# 15. OYUN KÜTÜPHANEM (SADECE ÜYE)
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
# 16. SOHBET GİRDİSİ VE YANIT MOTORU
# =====================================================================
typed_prompt = st.chat_input("Sazan AI'a bir şey sor...")
prompt = typed_prompt or st.session_state.pending_prompt
if st.session_state.pending_prompt and not typed_prompt:
    st.session_state.pending_prompt = None

if prompt:
    active_messages.append({"role": "user", "content": prompt})

    model_label = st.session_state.active_model_label if is_member else GUEST_MODEL_LABEL
    model_cfg = AI_MODELS.get(model_label, AI_MODELS[GUEST_MODEL_LABEL])

    with st.spinner("Sazan AI düşünüyor..."):
        cur_lang = st.session_state.get("active_lang_code", "Türkçe 🇹🇷")
        ans = SazanAIConception.query_agent(prompt, active_messages, cur_lang, model_cfg)
        active_messages.append({"role": "assistant", "content": ans})

        html_blocks = re.findall(r"```html\s*(.*?)\s*```", ans, re.DOTALL)
        if html_blocks and is_member:
            entry = SazanGameLibrary.add_game(user, prompt, html_blocks[0])
            st.toast(f"📚 Oyun kütüphaneye kaydedildi: {entry['title']}")

        if is_member:
            SazanChatStore.save_sessions(user, st.session_state.chat_sessions)

        st.rerun()
