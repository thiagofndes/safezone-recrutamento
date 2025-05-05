import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ========================
# CONFIG GOOGLE SHEETS
# ========================
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key("1xRVuph9Y-6KMnEKmds17llmKYXSoaYTP2WCZkQRYtU0").worksheet("Página1")

# ========================
# CONFIG PÁGINA
# ========================
st.set_page_config(page_title="SafeZone - Recrutamento", layout="wide")

# ========================
# CSS
# ========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cinzel', serif;
        margin:0; padding:0; min-height:100vh;
    }
    /* fundo geral */
    .stApp {
        background: url('https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/FUNDO.png?raw=true') center/cover fixed no-repeat;
        color: #fff;
    }
    /* BLOCO PRETO atrás dos textos */
    .main-container {
        background-color: rgba(0,0,0,0.6);
        padding: 2rem;
        border-radius: 12px;
        max-width: 900px;
        margin: 2rem auto;
        box-shadow: 0 0 15px #000;
    }
    /* banner */
    .banner {
        width:100vw; height:40vh;
        background: url('https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/BVANNER.png?raw=true') center/contain no-repeat;
    }
    /* título e menu */
    .title {
        font-size:3rem; text-align:center; color:#e6c300; margin-top:1rem;
    }
    .menu {
        display:flex; justify-content:center; gap:2rem; margin-bottom:2rem;
    }
    .menu a {
        color:#e6c300; font-weight:bold; text-decoration:none;
    }
    .menu a:hover { color:#fff; }
    /* discord */
    .discord-link {
        text-align:center; margin:2rem 0;
    }
    .discord-link img {
        width:40px; height:auto;
    }
    @media (max-width:600px) {
        .banner { height:30vh; }
        .menu { flex-direction:column; }
    }
</style>
""", unsafe_allow_html=True)

# ========================
# CONTEÚDO
# ========================

# Banner full-width
st.markdown("<div class='banner'></div>", unsafe_allow_html=True)

# Tudo que é texto fica dentro do BLOCO PRETO
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# Título e menu
st.markdown("<div class='title'>SafeZone</div>", unsafe_allow_html=True)
st.markdown("""
<div class='menu'>
  <a href="#sobre">SOBRE</a>
  <a href="#videos">VÍDEOS</a>
  <a href="#depoimentos">DEPOIMENTOS</a>
  <a href="#galeria">GALERIA</a>
  <a href="#recrutamento">RECRUTAMENTO</a>
</div>
""", unsafe_allow_html=True)

# Sobre a Guilda (agora fixa)
st.markdown('<div id="sobre">', unsafe_allow_html=True)
st.markdown("## Sobre a Guilda")
st.markdown("- **Missão:** Formar uma comunidade madura, respeitosa e com espírito de equipe, focada em PvP e crescimento constante.")
st.markdown("- **Benefícios:** Calls de qualidade, presença em ZVZ com a MANDATORY, apoio ao crescimento de membros novos e veteranos.")
st.markdown("- **Staff:** GM: SafiraSkins | Braço direito: Taigona | Conselho: MateusBrito | Recrutador: Targaryen")
st.markdown("- **Horários de pico:** BR: 19h - 23h | UTC: 22h - 02h")
st.markdown("</div>", unsafe_allow_html=True)

# Vídeos
with st.expander("🎞️ Vídeos da Guilda"):
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Depoimentos
with st.expander("💬 Depoimentos da Guilda"):
    st.markdown("> **MatheusBritoO:** \"Jogar com a SafeZone é sinônimo de risadas, estratégia e vitória.\"")
    st.markdown("> **TargaryeR0X:** \"O PvP aqui é diferenciado! Os callers são experientes e organizados.\"")
    st.markdown("> **Reduzeh:** \"Minha primeira guilda no Albion foi incrível.\"")
    st.markdown("> **Xandinho:** \"A SafeZone me acolheu de verdade desde o primeiro dia.\"")

# Galeria
with st.expander("🖼️ Galeria de Imagens"):
    st.image("https://albiononline.com/assets/images/news/2023-01-AlbionGuildSeason/Winner.jpg", use_column_width=True)
    st.image("https://albiononline.com/assets/images/news/2021-Season14/mid.jpg", use_column_width=True)

# Formulário de Recrutamento
with st.expander("📋 Formulário de Recrutamento"):
    with st.form(key="form"):
        nome = st.text_input("🧑 Nome do personagem")
        classe = st.selectbox("⚔️ Classe favorita", ["Melee","Range","Healer","Tank","Suporte"])
        fama_pvp = st.text_input("🔥 Fama PVP (ex: 2.5m)")
        fama_pve = st.text_input("🛡️ Fama PVE (ex: 4m)")
        enviar = st.form_submit_button("🚀 Enviar")
        if enviar and nome and fama_pvp and fama_pve:
            sheet.append_row([nome, classe, fama_pvp, fama_pve, datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
            st.success(f"✅ Bem-vindo(a), {nome}!")
            st.markdown("[Discord](https://discord.gg/FApJNJ4dXU)")

# Fecha o BLOCO PRETO
st.markdown("</div>", unsafe_allow_html=True)

# Rodapé sem bloco preto
st.markdown("""
<div class="discord-link">
  <a href="https://discord.gg/FApJNJ4dXU" target="_blank">
    <img src="https://logodownload.org/wp-content/uploads/2017/11/discord-logo-0.png" alt="Discord">
  </a>
</div>
<div style="text-align:center; color:gray; font-size:0.8rem; margin-bottom:2rem;">
  SafeZone – Guilda BR de Albion Online | Desde 2023 | MANDATORY Alliance
</div>
""", unsafe_allow_html=True)
