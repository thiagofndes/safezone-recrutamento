# main.py
import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ========================
# 1️⃣ CONFIGURAÇÃO DA PÁGINA
# ========================
st.set_page_config(page_title="SafeZone - Recrutamento", layout="wide")

# ========================
# 2️⃣ CSS GLOBAL + LOGIN BOX
# ========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&display=swap');

    html, body, [class*="css"] {
        margin: 0; padding: 0; min-height: 100vh;
        font-family: 'Cinzel', serif;
    }

    /* Fundo geral */
    .stApp {
        background: url('https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/FUNDO.png?raw=true')
                    center/cover fixed no-repeat;
        color: white;
        position: relative; /* para conter o login-wrapper */
    }

    /* Banner */
    .banner {
        text-align: center;
        padding: 2rem 0 1rem 0;
        margin-bottom: 1rem;
    }
    .banner img {
        width: 50%; max-width: 300px; display: inline-block;
        object-fit: cover; border-radius: 10px;
    }

    /* BLOCO PRETO atrás dos textos */
    .main-container {
        background-color: rgba(0,0,0,0.6);
        padding: 2rem; border-radius: 12px;
        max-width: 900px; margin: 0 auto 2rem;
        box-shadow: 0 0 15px #000;
    }

    /* Título e menu */
    .title { font-size: 3rem; text-align: center; color: #e6c300; margin: 1rem 0 0.5rem; }
    .menu {
        display: flex; justify-content: center;
        gap: 2rem; margin-bottom: 2rem;
    }
    .menu a {
        color: #e6c300; font-weight: bold; text-decoration: none;
    }
    .menu a:hover { color: #fff; }

    /* Seções (Sobre, Expanders) */
    #sobre, div[data-testid="stExpander"] {
        background-color: rgba(0,0,0,0.6) !important;
        padding: 1rem 1.5rem !important;
        border-radius: 12px !important;
        margin: 1.5rem auto !important;
        max-width: 900px !important;
    }

    /* Ícone Discord */
    .discord-link {
        text-align: center; margin: 2rem 0;
    }
    .discord-link img {
        width: 40px; height: auto; cursor: pointer;
    }

    /* ===== LOGIN BOX ===== */
    .login-wrapper {
        position: absolute;
        top: 1rem;
        right: 1rem;
        width: 280px;
        z-index: 999;
    }
    .login-box {
        background: rgba(0,0,0,0.8);
        border: 1px solid #e6c300;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 0 10px #000;
    }
    .login-box .stTextInput>div>div>input {
        width: 100% !important;
        margin-bottom: 0.5rem !important;
        padding: 0.4rem !important;
        border-radius: 4px !important;
        border: none !important;
    }
    .login-box button[kind="formSubmit"] {
        width: 100% !important;
        margin-top: 0.5rem !important;
        background: #e6c300 !important;
        color: #000 !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: bold !important;
    }
    .login-links {
        text-align: center; margin-top: 0.5rem;
    }
    .login-links a {
        color: #e6c300; text-decoration: none; font-size: 0.85rem; margin: 0 0.2rem;
    }
    .login-links a:hover { text-decoration: underline; }

    /* Responsivo */
    @media (max-width: 600px) {
        .banner { padding: 1.5rem 0; }
        .menu   { flex-direction: column; }
        .login-wrapper {
            position: relative;
            top: auto; right: auto;
            width: 100%; margin: 1rem auto 0 auto;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========================
# 3️⃣ FORMULÁRIO DE LOGIN FLOTANTE
# ========================
st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
with st.form(key="top_login_form", clear_on_submit=False):
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    user = st.text_input("Usuário", key="top_user", placeholder="seu_usuario")
    pwd  = st.text_input("Senha",   key="top_pwd", type="password", placeholder="••••••••")
    captcha = st.text_input("Captcha: 3 + 4 = ?", key="top_captcha", placeholder="Resposta")
    submit = st.form_submit_button("Entrar")
    if submit:
        # Aqui você dispara sua função de autenticação real:
        st.success(f"Você tentou login como **{user}** (captcha: **{captcha}**)")
    st.markdown("""
        <div class="login-links">
            <a href="#">Esqueci minha senha</a> |
            <a href="#">Criar conta</a>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ========================
# 4️⃣ GOOGLE SHEETS (CRUD)
# ========================
SCOPE = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
creds      = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client     = gspread.authorize(creds)
sheet      = client.open_by_key("1xRVuph9Y-6KMnEKmds17llmKYXSoaYTP2WCZkQRYtU0").worksheet("Página1")

# ========================
# 5️⃣ CONTEÚDO PRINCIPAL
# ========================

# — Banner —
st.markdown("""
<div class="banner">
    <img src="https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/BVANNER.png?raw=true"
         alt="Banner da Guilda">
</div>
""", unsafe_allow_html=True)

# — Texto no BLOCO PRETO —
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# — Título e menu —
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

# — Sobre a Guilda —
st.markdown('<div id="sobre">', unsafe_allow_html=True)
st.markdown("## Sobre a Guilda")
st.markdown("- **Missão:** Formar uma comunidade madura, respeitosa e com espírito de equipe, focada em PvP e crescimento constante.")
st.markdown("- **Benefícios:** Calls de qualidade, presença em ZVZ com a MANDATORY, apoio ao crescimento de membros novos e veteranos.")
st.markdown("- **Staff:**\n  - GM: SafiraSkins\n  - Braço direito: Taigona\n  - Conselho: MateusBrito\n  - Recrutador: TargaryeR0X")
st.markdown("- **Horários de pico:** BR: 19h - 23h | UTC: 22h - 02h")
st.markdown("</div>", unsafe_allow_html=True)

# — Vídeos da Guilda —
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
    st.image("https://albiononline.com/assets/images/news/2023-01-AlbionGuildSeason/Winner.jpg", use_column_width=True)
    st.image("https://albiononline.com/assets/images/news/2021-Season14/mid.jpg", use_column_width=True)

# — Formulário de Recrutamento —
with st.expander("📋 Formulário de Recrutamento"):
    with st.form(key="recrutamento_form"):
        nome     = st.text_input("🧑 Nome do personagem")
        classe   = st.selectbox("⚔️ Classe favorita", ["Melee","Range","Healer","Tank","Suporte"])
        fama_pvp = st.text_input("🔥 Fama PVP (ex: 2.5m, 1.2b)")
        fama_pve = st.text_input("🛡️ Fama PVE (ex: 4m, 500k)")
        enviar   = st.form_submit_button("🚀 Enviar dados")
        if enviar and nome and fama_pvp and fama_pve:
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            sheet.append_row([nome, classe, fama_pvp, fama_pve, timestamp])
            st.success(f"✅ Cadastro enviado com sucesso! Bem-vindo(a), {nome}!")
            st.markdown("[Clique aqui para acessar o Discord da Guilda](https://discord.gg/FApJNJ4dXU)")
        elif enviar:
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
