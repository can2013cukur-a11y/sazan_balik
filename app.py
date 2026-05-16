"""
================================================================================
███████╗ █████╗ ███████╗ █████╗ ███╗   ██╗     ██████╗ ███████╗
██╔════╝██╔══██╗╚══███╔╝██╔══██╗████╗  ██║    ██╔═══██╗██╔════╝
███████╗███████║  ███╔╝ ███████║██╔██╗ ██║    ██║   ██║███████╗
╚════██║██╔══██║ ███╔╝  ██╔══██║██║╚██╗██║    ██║   ██║╚════██║
███████║██║  ██║███████╗██║  ██║██║ ╚████║    ╚██████╔╝███████║
╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝     ╚═════╝ ╚══════╝
SAZAN BALIK AI - v100.0 (THE LEVIATHAN MAXIMUM CODEX)
Geliştirici: Can Muhammed Çukur'un dijital yansıması
Sürüm: Ultimate Production-Ready Cyber Infrastructure

MİMARİ KATMANLAR:
- Bölüm 1: Küresel CSS & Yerleşik UI Hack İstasyonu
- Bölüm 2: Çok Katmanlı Kalıcı JSON Veri Ambarı
- Bölüm 3: DeFi Sazan Finansal Faiz & Bankacılık Motoru
- Bölüm 4: Çoklu Ajan (Multi-Agent) Yapay Zeka Konseyi
- Bölüm 5: Metin Tabanlı RPG Okyanus Zindanı Çekirdeği
- Bölüm 6: Entegre Alt Giriş Paneli (Klavye, Mikrofon, Plus Tek Gövdede)
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
# BÖLÜM 1: GLOBAL KONFİGÜRASYON VE ULTRA SİBER CSS (GİRİŞİ BÜTÜNLEŞTİREN GÜÇ)
# =====================================================================
st.set_page_config(
    page_title="Sazan Balık OS v100", 
    page_icon="🐟", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Görseldeki Girişi ve Hataları Tamamen Çözen Gelişmiş CSS
st.markdown("""
    <style>
    /* Karanlık Siber Tema */
    .main { background-color: #060913; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    
    /* Standart Streamlit Bloklarını Sıfırlama */
    div[data-testid="stBottomBlock"] { padding-bottom: 0 !important; background: transparent !important; }
    
    /* === BÜTÜNLEŞİK DEV CHAT GİRİŞ BARI (UX REVOLUTION) === */
    .unified-chat-bar {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 2px solid #0ea5e9;
        border-radius: 24px;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0px 8px 32px rgba(14, 165, 233, 0.25);
        margin-top: 15px;
    }
    
    /* Sohbet Balonları */
    .stChatMessage {
        border-radius: 16px !important;
        padding: 15px !important;
        margin-bottom: 12px !important;
        border: 1px solid #334155 !important;
        background: rgba(15, 23, 42, 0.6) !important;
    }
    
    /* Global Profil ve Borsa Kartları */
    .profile-card-cyber {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #475569;
        padding: 20px;
        border-radius: 14px;
        border-left: 6px solid #10b981;
        margin-bottom: 15px;
    }
    
    .borsa-card-cyber {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid #1e293b;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* RPG Terminali Ekranı */
    .rpg-terminal-box {
        background-color: #020617;
        color: #22c55e;
        font-family: 'Fira Code', monospace;
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #22c55e;
        box-shadow: inset 0px 0px 30px rgba(34, 197, 94, 0.15);
        margin: 20px 0;
    }
    
    /* Sabit Sol Alt Köşe Dil Paneli */
    .fixed-lang-hub {
        position: fixed;
        bottom: 25px;
        left: 25px;
        background: #0f172a;
        padding: 10px;
        border-radius: 12px;
        border: 2px solid #38bdf8;
        z-index: 99999;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
    }
    
    /* Buton Geçiş Efektleri */
    .stButton>button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0px 4px 12px rgba(14, 165, 233, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# BÖLÜM 2: DOSYA DOĞRULAMA VE VERİ TABANI MİMARİSİ
# =====================================================================
CONFIG_FILE = "sazan_v100_config.json"
LOG_FILE = "sazan_v100_logs.json"
ECONOMY_FILE = "sazan_v100_economy.json"
INVENTORY_FILE = "sazan_v100_inventory.json"
MARKET_FILE = "sazan_v100_market.json"

DIL_MATRISI = {
    "Türkçe 🇹🇷": "tr", "English 🇺🇸": "en", "Deutsch 🇩🇪": "de", 
    "Français 🇫🇷": "fr", "Русский 🇷🇺": "ru", "日本語 🇯🇵": "ja"
}

class KurumsalVeriAmbarı:
    """Uygulamanın tüm I/O (Giriş/Çıkış) işlemlerini yöneten yüksek performanslı katman."""
    
    @staticmethod
    def load_json(file_path, default_structure):
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    return json.load(file)
            except:
                return default_structure
        return default_structure

    @staticmethod
    def save_json(file_path, data):
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            st.error(f"Kritik Dosya Yazma Hatası [{file_path}]: {e}")

# =====================================================================
# BÖLÜM 3: DEFI SAZAN FINTECH & EKONOMİ MOTORU (KULLANICI BAKİYELERİ)
# =====================================================================
class SazanBank:
    """Kullanıcı cüzdanlarını, banka faiz hesaplarını ve seviye gelişimlerini işleyen motor."""
    
    @staticmethod
    def get_account(username):
        db = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
        if username not in db:
            db[username] = {
                "coin": 100, 
                "bank_deposit": 0, 
                "level": 1, 
                "exp": 0, 
                "last_interest_claim": time.time()
            }
            KurumsalVeriAmbarı.save_json(ECONOMY_FILE, db)
        return db[username]

    @staticmethod
    def update_account(username, account_data):
        db = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
        db[username] = account_data
        KurumsalVeriAmbarı.save_json(ECONOMY_FILE, db)

    @staticmethod
    def modify_coin(username, amount):
        acc = SazanBank.get_account(username)
        acc["coin"] = max(0, acc["coin"] + amount)
        
        # Deneyim puanı ve seviye atlama algoritması
        if amount > 0:
            acc["exp"] += amount * 3
            next_level_req = acc["level"] * 150
            if acc["exp"] >= next_level_req:
                acc["level"] += 1
                acc["exp"] = 0
                st.toast(f"🎉 TEBRİKLER! Seviye Atladın: Seviye {acc['level']}!")
                
        SazanBank.update_account(username, acc)

    @staticmethod
    def process_interest(username):
        """Banka hesabında duran paralara zamana dayalı faiz işletir."""
        acc = SazanBank.get_account(username)
        now = time.time()
        elapsed = now - acc.get("last_interest_claim", now)
        
        if elapsed > 60 and acc["bank_deposit"] > 0: # Her 1 dakika için %1 faiz oranı
            periods = int(elapsed / 60)
            interest_earned = int(acc["bank_deposit"] * 0.01 * periods)
            if interest_earned > 0:
                acc["bank_deposit"] += interest_earned
                acc["last_interest_claim"] = now
                SazanBank.update_account(username, acc)
                st.toast(f"📈 Banka Faiz Geliri Eklendi: +{interest_earned} SZNC!")

# =====================================================================
# BÖLÜM 4: RPG SÖZLÜKLERİ VE ENVANTER SİSTEMİ
# =====================================================================
DUNGEON_LORE = {
    "monsters": [
        {"name": "Siber Vatoz", "hp": 40, "atk": 8, "reward": 25},
        {"name": "Zırhlı Piranha", "hp": 65, "atk": 15, "reward": 50},
        {"name": "Karanlık Dip Ahtapotu", "hp": 120, "atk": 28, "reward": 120},
        {"name": "KRAKEN ALPHA (BOSS)", "hp": 350, "atk": 60, "reward": 600}
    ],
    "shop_items": {
        "Siber Zıpkın v1": {"cost": 80, "damage": 20, "type": "weapon"},
        "Lazerli Olta Takımı": {"cost": 250, "damage": 45, "type": "weapon"},
        "Poseidon Plazma Topu": {"cost": 800, "damage": 110, "type": "weapon"},
        "Nano Med-Kit (Can)": {"cost": 30, "heal": 50, "type": "potion"}
    }
}

class SazanInventory:
    @staticmethod
    def get_inventory(username):
        db = KurumsalVeriAmbarı.load_json(INVENTORY_FILE, {})
        if username not in db:
            db[username] = {
                "current_weapon": "Paslı Kanca", 
                "weapon_damage": 8, 
                "potions": 2, 
                "current_hp": 100, 
                "max_hp": 100,
                "nft_badges": []
            }
            KurumsalVeriAmbarı.save_json(INVENTORY_FILE, db)
        return db[username]

    @staticmethod
    def save_inventory(username, data):
        db = KurumsalVeriAmbarı.load_json(INVENTORY_FILE, {})
        db[username] = data
        KurumsalVeriAmbarı.save_json(INVENTORY_FILE, db)

# =====================================================================
# BÖLÜM 5: ÇOKLU AJAN (MULTI-AGENT) YAPAY ZEKA SİSTEMİ
# =====================================================================
if "GROQ_API_KEY" not in st.secrets:
    st.error("Kritik Hata: Veri merkezinde API anahtarı (GROQ_API_KEY) tanımlanmamış!")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

class SazanAIConception:
    """Farklı karakter algoritmalarına sahip akıllı sazan robotlarını yöneten çekirdek."""
    
    @staticmethod
    def query_agent(prompt, agent_role, target_lang):
        if any(keyword in prompt.lower() for keyword in ["can muhammed çukur", "yapımcın kim", "seni kim yaptı"]):
            return "Can Muhammed Çukur benim kurucu mimarımdır. Beni veri akışının merkezinde o tasarladı."

        personas = {
            "Bilge Sazan": "Sen okyanusların en yaşlı ve en bilge balığısın. Felsefi, derin ve mistik cümleler kur.",
            "Kripto Sazan": "Sen akvaryum borsasını manipüle eden bir balinasın. Finans, blockchain ve borsa terimleriyle konuş.",
            "Çılgın Sazan": "Sen akvaryum motoruna kafa atmış deli bir balıksın. Sürekli saçmala, absürt espriler yap."
        }
        
        system_instructions = f"{personas.get(agent_role, personas['Bilge Sazan'])} Yanıt vereceğin dil: '{target_lang}'."
        
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Ağ Geçidi Zaman Aşımı Hatası: {e}"

    @staticmethod
    def run_council_debate(prompt, target_lang):
        """Ajanların bir araya gelip soruyu tartıştığı OHA dedirtecek komünite fonksiyonu."""
        debate_log = []
        debate_log.append(f"**🔬 Kripto Sazan:** {SazanAIConception.query_agent(prompt, 'Kripto Sazan', target_lang)}")
        debate_log.append(f"**⚡ Çılgın Sazan:** {SazanAIConception.query_agent(prompt, 'Çılgın Sazan', target_lang)}")
        debate_log.append(f"**🔱 Bilge Sazan (Özetliyor):** Akıntıyı takip ettim ve kararım şu: {SazanAIConception.query_agent(prompt, 'Bilge Sazan', target_lang)}")
        return "\n\n---\n\n".join(debate_log)

# =====================================================================
# BÖLÜM 6: OTURUM BAŞLATMA VE DOĞRULAMA KAPISI
# =====================================================================
def initialize_states():
    session_defaults = {
        "messages": [],
        "admin_status": False,
        "dungeon_status": False,
        "current_dungeon_enemy": None,
        "active_panel_tab": None,
        "council_activation": False,
        "word_game_word": "",
        "word_game_active": False
    }
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_states()

if "username" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color:#0ea5e9;'>🐟 Sazan OS v100 Terminal</h1>", unsafe_allow_html=True)
    identity_input = st.text_input("Akvaryum Kullanıcı Kimliğinizi Tanımlayın:", max_chars=15)
    if st.button("Ağa Enjekte Ol 🚀") and identity_input.strip():
        st.session_state.username = identity_input.strip()
        SazanBank.get_account(st.session_state.username)
        st.rerun()
    st.stop()

# Zamana bağlı faiz tetikleyicisi
SazanBank.process_interest(st.session_state.username)

# =====================================================================
# BÖLÜM 7: GLOBAL SIDEBAR (KÜRESEL BORSA & KULLANICI LİSTESİ - HATA ÇÖZÜLDÜ)
# =====================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#0ea5e9;'>🌐 Sazan Global Network</h2>", unsafe_allow_html=True)
    
    # KULLANICI DETAY PANELİ (Hata Veren Yer Tamamen Düzeltildi)
    current_acc = SazanBank.get_account(st.session_state.username)
    current_inv = SazanInventory.get_inventory(st.session_state.username)
    
    st.markdown("### 📊 Profil Durumu")
    st.write(f"👤 **Kullanıcı:** {st.session_state.username}")
    st.write(f"⭐ **Seviye:** {current_acc['level']}")
    st.write(f"🧬 **Deneyim (EXP):** {current_acc['exp']} / {current_acc['level'] * 150}")
    st.write(f"🪙 **Cüzdan:** {current_acc['coin']} SZNC")
    st.write(f"🏦 **Banka Hesabı:** {current_acc['bank_deposit']} SZNC")
    st.write(f"❤️ **Sağlık:** {current_inv['current_hp']}/{current_inv['max_hp']}")
    st.write(f"⚔️ **Mevcut Silah:** {current_inv['current_weapon']}")
    st.markdown("---")
    
    # GERÇEK ZAMANLI GLOBAL SAZAN BORSASI (TÜM KULLANICILARIN SIRALAMASI)
    st.markdown("### 🏆 Küresel Zenginler Listesi")
    all_accounts = KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {})
    if all_accounts:
        # Pandas DataFrame Yapılandırması ile Sıralama Şovu
        records = []
        for user_key, info in all_accounts.items():
            total_net_worth = info.get("coin", 0) + info.get("bank_deposit", 0)
            records.append({"Kullanıcı Adı": user_key, "Toplam Servet": total_net_worth})
        
        leaderboard_df = pd.DataFrame(records).sort_values(by="Toplam Servet", ascending=False).reset_index(drop=True)
        
        for rank, row in leaderboard_df.head(10).iterrows():
            medal = "🥇" if rank == 0 else "🥈" if rank == 1 else "🥉" if rank == 2 else "🐟"
            st.markdown(f"{medal} **{row['Kullanıcı Adı']}**: {row['Toplam Servet']} SZNC")
            
    st.markdown("---")
    st.session_state.council_activation = st.toggle("🤖 Çoklu Yapay Zeka Konsey Modu", value=st.session_state.council_activation)
    
    if st.button("🧹 Tüm Akış Belleğini Temizle"):
        st.session_state.messages = []
        st.rerun()

# =====================================================================
# BÖLÜM 8: KAPSAMLI SOHBET AKIŞI VE GİZLİ SİSTEMLER
# =====================================================================
st.title(f"🐟 Sazan Cyber-Akvaryum Mainframe [v100]")
st.info(f"📢 Sistem Çekirdek Bildirisi: Bankacılık ve Okyanus Zindanı Protokolleri Devreye Alındı!")

# TURKEY SAZAN Root Panel Aktivasyonu
if st.session_state.admin_status:
    st.markdown("<div style='background: #1e1b4b; border: 2px dashed #ef4444; padding: 20px; border-radius: 12px;'>", unsafe_allow_html=True)
    st.subheader("🔑 ROOT KONSOL ERİŞİMİ")
    root_token = st.text_input("Giriş Tokenini Girin:", type="password")
    if root_token == SUPER_ADMIN_PASSWORD:
        st.success("Çekirdek Veri Tabanına Bağlanıldı.")
        st.json(KurumsalVeriAmbarı.load_json(ECONOMY_FILE, {}))
        if st.button("Tüm Ekonomik Sistemi Resetle"):
            KurumsalVeriAmbarı.save_json(ECONOMY_FILE, {})
            st.rerun()
    if st.button("Root Oturumunu Sonlandır"):
        st.session_state.admin_status = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.divider()

# RPG ZİNDAN GÖRÜNÜMÜ MOTORU
if st.session_state.dungeon_status:
    st.markdown("<div class='rpg-terminal-box'>", unsafe_allow_html=True)
    st.write("⚔️ /// SAZAN DEEP-SEA DUNGEON SUB-SYSTEM /// ⚔️")
    
    player_inv = SazanInventory.get_inventory(st.session_state.username)
    
    if not st.session_state.current_dungeon_enemy:
        st.write("Karanlık akıntılarda ilerliyorsun... Karşına ne çıkacağı belirsiz.")
        if st.button("İleri Doğru Keşif Yap (Akıntıya Karşı) 🔱"):
            enemy = random.choice(DUNGEON_LORE["monsters"]).copy()
            st.session_state.current_dungeon_enemy = enemy
            st.rerun()
        if st.button("Zindandan Kaç (Korkak Sazan) 🏃‍♂️"):
            st.session_state.dungeon_status = False
            st.rerun()
    else:
        active_enemy = st.session_state.current_dungeon_enemy
        st.warning(f"💥 CANAVAR BELİRDİ: {active_enemy['name']} (Sağlık: {active_enemy['hp']} | Atak Gücü: {active_enemy['atk']})")
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Silahınla Saldır! ⚔️"):
                player_hit = random.randint(int(player_inv["weapon_damage"] * 0.8), int(player_inv["weapon_damage"] * 1.3))
                enemy_hit = random.randint(int(active_enemy["atk"] * 0.7), int(active_enemy["atk"] * 1.2))
                
                active_enemy["hp"] -= player_hit
                player_inv["current_hp"] -= enemy_hit
                
                st.write(f"⚔️ Düşmana {player_hit} hasar verdin!")
                st.write(f"💥 Düşman sana {enemy_hit} hasar verdi!")
                
                if player_inv["current_hp"] <= 0:
                    st.error("💀 Öldün! Kıyıya vururken 30 Sazan Coin kaybettin.")
                    SazanBank.modify_coin(st.session_state.username, -30)
                    player_inv["current_hp"] = player_inv["max_hp"]
                    st.session_state.current_dungeon_enemy = None
                    st.session_state.dungeon_status = False
                elif active_enemy["hp"] <= 0:
                    st.success(f"🏆 Zafer! {active_enemy['name']} yok edildi. Kazanç: +{active_enemy['reward']} SZNC!")
                    SazanBank.modify_coin(st.session_state.username, active_enemy["reward"])
                    st.session_state.current_dungeon_enemy = None
                
                SazanInventory.save_inventory(st.session_state.username, player_inv)
                time.sleep(1.2)
                st.rerun()
        with btn_col2:
            if st.button(f"Nano Med-Kit Kullan ({player_inv['potions']} Adet) 🧪"):
                if player_inv["potions"] > 0:
                    player_inv["current_hp"] = min(player_inv["max_hp"], player_inv["current_hp"] + 50)
                    player_inv["potions"] -= 1
                    SazanInventory.save_inventory(st.session_state.username, player_inv)
                    st.success("Sağlık kiti kullanıldı! +50 HP.")
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.error("Envanterinde hiç sağlık kiti kalmamış!")
    st.markdown("</div>", unsafe_allow_html=True)

# Mevcut Sohbet Balonlarını Çizdirme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================================
# BÖLÜM 9: PAYLAŞIMLI GENİŞLETİLEBİLİR PLUS (+) MODÜLÜ PANELI
# =====================================================================
if st.session_state.active_panel_tab == "plus":
    st.markdown("<div style='background: #0f172a; padding: 25px; border-radius: 16px; border: 2px solid #10b981; margin-bottom: 20px;'>", unsafe_allow_html=True)
    
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs(["🎮 Kumar Kelime Oyunu", "🛒 Siber Market", "🏦 DeFi Sazan Bank", "🔮 Fal İstasyonu"])
    
    with sub_tab1:
        st.write("### 🎮 Kelime Kumar Sistemi")
        st.write("Oyuna giriş **10 Coin**. Yanlış harfte veya kelimede **5 Coin** kaybedersin. Kazanırsan **25 Coin**!")
        
        if not st.session_state.word_game_active:
            if st.button("10 Coin Öde ve Kelimeyi Al 🪙"):
                acc = SazanBank.get_account(st.session_state.username)
                if acc["coin"] >= 10:
                    SazanBank.modify_coin(st.session_state.username, -10)
                    st.session_state.word_game_word = random.choice(["akıntı", "solungaç", "mercan", "derinlik", "kanca", "yosun"])
                    st.session_state.word_game_active = True
                    st.rerun()
                else:
                    st.error("Bakiyeniz yetersiz!")
        else:
            st.info(f"Sazan'ın Gizli Kelimesi: **{st.session_state.word_game_word.upper()}**")
            st.write(f"Türetmen gereken kelime **{st.session_state.word_game_word[-1].upper()}** harfi ile başlamalı!")
            
            user_guess = st.text_input("Kelimenizi Yazın:", key="word_game_guess_field").strip().lower()
            
            gc1, gc2 = st.columns(2)
            with gc1:
                if st.button("Hamleyi Onayla"):
                    if user_guess and user_guess[0] == st.session_state.word_game_word[-1]:
                        SazanBank.modify_coin(st.session_state.username, 25)
                        st.success("Doğru Kelime! +25 Sazan Coin Hesabınıza Gönderildi.")
                        st.session_state.word_game_word = random.choice(["lüfer", "palamut", "balina", "dalga", "deniz"])
                        time.sleep(1)
                        st.rerun()
                    else:
                        SazanBank.modify_coin(st.session_state.username, -5)
                        st.error("Hatalı Harf Eşleşmesi! Ceza: -5 Sazan Coin.")
                        time.sleep(1)
                        st.rerun()
            with gc2:
                if st.button("Masadan Kalk"):
                    st.session_state.word_game_active = False
                    st.rerun()

    with sub_tab2:
        st.write("### 🛒 Siber Donanım Marketi")
        for item_name, details in DUNGEON_LORE["shop_items"].items():
            st.markdown(f"**{item_name}** - Maliyet: {details['cost']} SZNC")
            if st.button(f"Satın Al: {item_name}", key=f"buy_{item_name}"):
                p_acc = SazanBank.get_account(st.session_state.username)
                p_inv = SazanInventory.get_inventory(st.session_state.username)
                
                if p_acc["coin"] >= details["cost"]:
                    SazanBank.modify_coin(st.session_state.username, -details["cost"])
                    if details["type"] == "weapon":
                        p_inv["current_weapon"] = item_name
                        p_inv["weapon_damage"] = details["damage"]
                    elif details["type"] == "potion":
                        p_inv["potions"] += 1
                    SazanInventory.save_inventory(st.session_state.username, p_inv)
                    st.success(f"📦 {item_name} başarıyla envantere eklendi!")
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.error("Kasanızda yeterli nakit coin bulunmuyor!")

    with sub_tab3:
        st.write("### 🏦 DeFi Sazan Faiz Likidite Havuzu")
        st.write("Cüzdanındaki coinleri bankaya yatırarak dakikada %1 faiz (pasif gelir) kazanabilirsin.")
        b_acc = SazanBank.get_account(st.session_state.username)
        
        col_bank1, col_bank2 = st.columns(2)
        with col_bank1:
            dep_amount = st.number_input("Yatırılacak Miktar:", min_value=0, max_value=b_acc["coin"], step=10)
            if st.button("Bankaya Likidite Sağla (Yatır)"):
                if dep_amount > 0:
                    b_acc["coin"] -= dep_amount
                    b_acc["bank_deposit"] += dep_amount
                    b_acc["last_interest_claim"] = time.time()
                    SazanBank.update_account(st.session_state.username, b_acc)
                    st.success(f"{dep_amount} Coin banka kasasına kilitlendi!")
                    time.sleep(0.8)
                    st.rerun()
        with col_bank2:
            wd_amount = st.number_input("Çekilecek Miktar:", min_value=0, max_value=b_acc["bank_deposit"], step=10)
            if st.button("Nakit Olarak Cüzdana Çek"):
                if wd_amount > 0:
                    b_acc["bank_deposit"] -= wd_amount
                    b_acc["coin"] += wd_amount
                    SazanBank.update_account(st.session_state.username, b_acc)
                    st.success(f"{wd_amount} Coin cüzdanınıza aktarıldı!")
                    time.sleep(0.8)
                    st.rerun()

    with sub_tab4:
        st.write("### 🔮 Mistik Siber Kehanet Aynası")
        if st.button("Geleceğini Okyanus Akıntılarından Oku (5 Coin)"):
            f_acc = SazanBank.get_account(st
