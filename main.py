# main.py
import streamlit as st
from login import show_login
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1️⃣ CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SafeZone - Recrutamento", layout="wide")

# 2️⃣ AUTENTICAÇÃO
if not show_login():
    st.stop()  # interrompe se não logado

user = st.session_state.user
role = st.session_state.role

# 3️⃣ GOOGLE SHEETS (CRUD)
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key("1xRVuph9Y-6KMnEKmds17llmKYXSoaYTP2WCZkQRYtU0").worksheet("Página1")

# 4️⃣ CSS GLOBAL
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&display=swap');
    html, body, [class*="css"] {
        margin: 0; padding: 0; min-height: 100vh;
        font-family: 'Cinzel', serif;
    }
    .stApp {
        background: url('https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/FUNDO.png?raw=true')
                    center/cover fixed no-repeat;
        color: white;
    }
    .banner {
        text-align: center; padding: 2rem 0 1rem 0; margin-bottom: 1rem;
    }
    .banner img {
        width: 50%; max-width: 300px; height: auto;
        object-fit: cover; border-radius: 10px; display: inline-block;
    }
    .main-container {
        background-color: rgba(0,0,0,0.6);
        padding: 2rem; border-radius: 12px;
        max-width: 900px; margin: 0 auto 2rem auto;
        box-shadow: 0 0 15px #000;
    }
    .title {
        font-size: 3rem; text-align: center;
        color: #e6c300; margin: 1rem 0 0.5rem 0;
    }
    .menu {
        display: flex; justify-content: center;
        gap: 2rem; margin-bottom: 2rem;
    }
    .menu a {
        color: #e6c300; font-weight: bold;
        text-decoration: none;
    }
    .menu a:hover { color: #fff; }
    #sobre, div[data-testid="stExpander"] {
        background-color: rgba(0,0,0,0.6) !important;
        padding: 1rem 1.5rem !important;
        border-radius: 12px !important;
        margin: 1.5rem auto !important;
        max-width: 900px !important;
    }
    .discord-link {
        text-align: center; margin: 2rem 0;
    }
    .discord-link img {
        width: 40px; height: auto; cursor: pointer;
    }
    @media (max-width: 600px) {
        .banner { padding: 1.5rem 0; }
        .menu   { flex-direction: column; }
    }
</style>
""", unsafe_allow_html=True)

# 5️⃣ SIDEBAR: USUÁRIO E LOGOUT
st.sidebar.write(f"👤 Usuário: **{user}** ({role})")
if st.sidebar.button("Logout"):
    for key in ("logged_in", "user", "role"):
        st.session_state.pop(key, None)
    st.experimental_rerun()

# 6️⃣ CONTEÚDO PRINCIPAL

# — Banner —
st.markdown("""
<div class="banner">
    <img src="https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/BVANNER.png?raw=true"
         alt="Banner da Guilda">
</div>
""", unsafe_allow_html=True)

# — Tudo em volta do texto fica no BLOCO PRETO —
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# — Título e Menu —
st.markdown('<div class="title">SafeZone</div>', unsafe_allow_html=True)
st.markdown("""
<div class="menu">
    <a href="#sobre">SOBRE</a>
    <a href="#videos">VÍDEOS</a>
    <a href="#depoimento-de-membros">DEPOIMENTO DE MEMBROS</a>
    <a href="#galeria">GALERIA</a>
    <a href="#recrutamento">RECRUTAMENTO</a>
</div>
""", unsafe_allow_html=True)

# — Sobre a Guilda (fixo) —
st.markdown('<div id="sobre">', unsafe_allow_html=True)
st.markdown("## Sobre a Guilda")
st.markdown("- **Missão:** Formar uma comunidade madura, respeitosa e com espírito de equipe, focada em PvP e crescimento constante.")
st.markdown("- **Benefícios:** Calls de qualidade, presença em ZVZ com a MANDATORY, apoio ao crescimento de membros novos e veteranos.")
st.markdown("- **Staff:**\n  - GM: SafiraSkins\n  - Braço direito: Taigona\n  - Conselho: MateusBrito\n  - Recrutador: TargaryeR0X")
st.markdown("- **Horários de pico:** BR: 19h - 23h | UTC: 22h - 02h")
st.markdown("</div>", unsafe_allow_html=True)

# — Vídeos —
with st.expander("🎞️ Vídeos da Guilda"):
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# — Depoimento de Membros —
with st.expander("💬 Depoimento de Membros"):
    st.markdown("**MatheusBritoO:** \"Jogar com a SafeZone é sinônimo de risadas, estratégia e vitória. Aqui eu realmente me divirto.\"")
    st.markdown("**TargaryeR0X:** \"O PvP aqui é diferenciado! Os callers são experientes e organizados, a emoção é garantida.\"")
    st.markdown("**Reduzeh:** \"Minha primeira guilda no Albion! O pessoal me ajudou desde o começo, e cada dia é uma nova aventura.\"")
    st.markdown("**Xandinho:** \"Nunca pensei que começar no Albion pudesse ser tão legal. A galera aqui me acolheu de verdade.\"")

# — Galeria de Imagens —
with st.expander("🖼️ Galeria de Imagens"):
    st.image("https://albiononline.com/assets/images/news/2023-01-AlbionGuildSeason/Winner.jpg",
             use_column_width=True)
    st.image("https://albiononline.com/assets/images/news/2021-Season14/mid.jpg",
             use_column_width=True)

# — Formulário de Recrutamento —
with st.expander("📋 Formulário de Recrutamento"):
    with st.form(key="recrutamento_form"):
        nome     = st.text_input("🧑 Nome do personagem")
        classe   = st.selectbox("⚔️ Classe favorita", ["Melee", "Range", "Healer", "Tank", "Suporte"])
        fama_pvp = st.text_input("🔥 Fama PVP (ex: 2.5m, 1.2b)")
        fama_pve = st.text_input("🛡️ Fama PVE (ex: 4m, 500k)")
        enviar   = st.form_submit_button("🚀 Enviar dados")
        if enviar:
            if nome and fama_pvp and fama_pve:
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                sheet.append_row([nome, classe, fama_pvp, fama_pve, timestamp])
                st.success(f"✅ Cadastro enviado com sucesso! Bem-vindo(a), {nome}!")
                st.markdown("[Clique aqui para acessar o Discord da Guilda](https://discord.gg/FApJNJ4dXU)")
            else:
                st.error("Por favor, preencha todos os campos obrigatórios.")

# — Feedback —
with st.expander("🗣️ Deixe seu feedback para a guilda"):
    st.text_input("Seu nome (opcional):")
    st.text_area("Mensagem:")
    st.button("Enviar Feedback")

# — Fecha BLOCO PRETO —
st.markdown("</div>", unsafe_allow_html=True)

# — Rodapé (sem bloco preto) —
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
