# ================================================================================
# ███████╗ █████╗ ███████╗ █████╗ ███╗  ██╗     ██████╗ ███████╗
# ██╔════╝██╔══██╗╚══███╔╝██╔══██╗████╗  ██║     ██╔═══██╗██╔════╝
# ███████╗███████║  ███╔╝ ███████║██╔██╗ ██║     ██║   ██║███████╗
# ╚════██║██╔══██║ ███╔╝  ██╔══██║██║╚██╗██║     ██║   ██║╚════██║
# ███████║██║  ██║███████╗██║  ██║██║ ╚████║     ╚██████╔╝███████║
# ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝      ╚═════╝ ╚══════╝
#        👑 SAZAN AI ENTERPRISE STUDIO - GAME ENGINE SUPREME v115.0 👑
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
    page_title="Sazan AI Enterprise Game Overlord v115.0",
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
AI_MODELS = {
    "🏆 Kalite Modu (Llama 3.3 70B)": "llama-3.3-70b-versatile",
    "⚡ Hız Modu (Llama 3.1 8B Instant)": "llama-3.1-8b-instant",
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
    def query_agent(prompt, history, target_lang, model="llama-3.3-70b-versatile"):
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
        "active_ai_model": "🏆 Kalite Modu (Llama 3.3 70B)",
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
        "<h2 style='text-align: center; color:#38bdf8; margin-top:60px;'>🐟 SAZAN AI OVERLORD</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color:#64748b; font-weight:bold;'>"
        "🛡️ KUANTUM OYUN STÜDYOSU AKTİF (v115.0)</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='max-width: 480px; margin: 0 auto; background: #090f21; padding: 25px; "
        "border-radius: 16px; border: 1px solid #1e293b;'>",
        unsafe_allow_html=True,
    )

    identity = st.text_input("Kullanıcı Kimlik Doğrulama Adı:", max_chars=15, key="unique_login_gate")
    if st.button("Güvenli Oturumu Başlat", use_container_width=True):
        username_clean = identity.strip()
        if username_clean:
            db = KurumsalVeriAmbari.load_json(ECONOMY_FILE, {})
            current_device = get_device_fingerprint()
            if username_clean in db:
                locked_device = db[username_clean].get("device_lock")
                if locked_device and locked_device != current_device:
                    st.error("🚨 ERİŞİM ENGELLENDİ: Bu hesap başka bir siber donanıma kilitlidir!")
                    st.stop()
                else:
                    db[username_clean]["device_lock"] = current_device
                    KurumsalVeriAmbari.save_json(ECONOMY_FILE, db)
                    st.session_state.username = username_clean
                    st.rerun()
            else:
                st.session_state.username = username_clean
                SazanBank.get_account(username_clean)
                st.success("🎉 Başarılı: Hesap doğrulandı!")
                time.sleep(0.4)
                st.rerun()
        else:
            st.warning("Lütfen bir kullanıcı adı girin.")
    st.markdown("</div>", unsafe_allow_html=True)
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
        help="Kalite Modu daha detaylı ve tutarlı kod üretir ama daha yavaştır. "
        "Hız Modu daha çabuk cevap verir, basit oyunlar için idealdir.",
    )

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
    t1, t2, t3, t4, t5, t6 = st.tabs(
        [
            "🛒 Ekipman Deposu",
            "🏦 Kasa & Kredi Merkezi",
            "📊 Finansal Borsa",
            "⛏️ Kuantum Madencilik",
            "📚 Oyun Kütüphanem",
            "🖨️ 3D Baskı Atölyesi",
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

    with t6:
        st.markdown(
            "🖨️ Bir görsel yükle; Sazan onu gri tonlamalı bir **yükseklik haritasına** "
            "çevirip 3D yazıcında basabileceğin kapalı (watertight) bir **.stl kabartma "
            "modeli** üretsin. Bu teknik bir *lityofan/rölyef* dönüşümüdür — görseli tam "
            "bir 3D nesneye değil, kabartmalı bir yüzeye çevirir."
        )

        uploaded_img = st.file_uploader(
            "Görsel Yükle (PNG / JPG)", type=["png", "jpg", "jpeg"], key="stl_uploader"
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
            st.info("Başlamak için yukarıdan bir görsel yükle.")

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 12. HUD KONTROLLERİ (HIZLI ERİŞİM MENÜSÜ)
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
            st.session_state.get("active_ai_model", "🏆 Kalite Modu (Llama 3.3 70B)"),
            "llama-3.3-70b-versatile",
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
