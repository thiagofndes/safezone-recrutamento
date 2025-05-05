import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ========================
# CONFIGURAÇÃO DO GOOGLE SHEETS COM SEGREDOS
# ========================
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client = gspread.authorize(creds)

# Use o ID da planilha diretamente para evitar erro de título
spreadsheet_id = "1xRVuph9Y-6KMnEKmds17llmKYXSoaYTP2WCZkQRYtU0"
sheet = client.open_by_key(spreadsheet_id).worksheet("Página1")

# ========================
# CONFIGURAÇÃO DE PÁGINA
# ========================
st.set_page_config(page_title="SafeZone - Recrutamento", layout="centered")

# ========================
# ESTILIZAÇÃO COM CSS EMBUTIDO
# ========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&display=swap');
    html, body, [class*="css"] {
        margin: 0; padding: 0;
        font-family: 'Cinzel', serif;
        background-image: url('https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/FUNDO.png?raw=true');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: white;
    }
    .time-display {
        position: fixed;
        top: 1rem;
        right: 2rem;
        font-size: 1rem;
        background: rgba(0,0,0,0.6);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        z-index: 99;
    }
    .main-container {
        position: relative;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 2rem;
        border-radius: 15px;
        max-width: 900px;
        margin: 4rem auto 2rem;
        box-shadow: 0px 0px 15px #000;
        z-index: 1;
    }
    .title {
        font-size: 3rem;
        text-align: center;
        color: #e6c300;
        margin-bottom: 1rem;
    }
    .menu {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 2rem;
    }
    .menu a {
        color: #e6c300;
        font-weight: bold;
        text-decoration: none;
    }
    .menu a:hover {
        color: #fff;
        transition: color 0.3s ease-in-out;
    }
    .banner {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .banner img {
        width: 50%;
        max-width: 300px;
        height: auto;
        object-fit: cover;
        border-radius: 10px;
    }
    .about-section {
        margin-bottom: 2rem;
        padding: 1rem;
        background: rgba(30, 30, 30, 0.7);
        border-radius: 8px;
    }
    .footer {
        margin-top: 4rem;
        text-align: center;
        font-size: 0.8rem;
        color: gray;
    }
    .discord-link {
        text-align: center;
        margin-top: 1.5rem;
    }
    .discord-link img {
        width: 40px;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .discord-link img:hover {
        transform: scale(1.1);
    }
    @media screen and (max-width: 600px) {
        .menu { flex-direction: column; align-items: center; }
        .banner img { width: 80%; }
        .time-display { right: 1rem; font-size: 0.9rem; }
    }
</style>
""", unsafe_allow_html=True)

# Exibição fixa de horários de pico
st.markdown("<div class='time-display'>BR: 19h - 23h | UTC: 22h - 02h</div>", unsafe_allow_html=True)

# ========================
# CONTEÚDO DA PÁGINA
# ========================
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# Animação Lottie antes do banner
st.markdown("""
<div class='banner'>
  <lottie-player src='https://assets2.lottiefiles.com/packages/lf20_touohxv0.json' background='transparent' speed='1' style='width:400px; height:200px; margin:auto;' loop autoplay></lottie-player>
</div>
""", unsafe_allow_html=True)

# Banner principal
st.markdown("""
<div class='banner'>
    <img src='https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/BVANNER.png?raw=true' alt='Banner da Guilda'>
</div>
""", unsafe_allow_html=True)

# Título
st.markdown("<div class='title'>SafeZone</div>", unsafe_allow_html=True)

# Menu de navegação
st.markdown("""
<div class='menu'>
    <a href='#sobre'>SOBRE</a>
    <a href='#videos'>VÍDEOS</a>
    <a href='#depoimentos'>DEPOIMENTOS</a>
    <a href='#galeria'>GALERIA</a>
    <a href='#recrutamento'>RECRUTAMENTO</a>
</div>
""", unsafe_allow_html=True)

# Seção fixa Sobre a Guilda
st.markdown("""
<div class='about-section' id='sobre'>
  <h2>Sobre a Guilda</h2>
  <p><strong>Missão:</strong> Formar uma comunidade madura, respeitosa e com espírito de equipe, focada em PvP e crescimento constante.</p>
  <p><strong>Benefícios:</strong> Calls de qualidade, presença em ZVZ com a MANDATORY, apoio ao crescimento de membros novos e veteranos.</p>
  <p><strong>Staff:</strong><br>- GM: SafiraSkins<br>- Braço direito: Taigona<br>- Conselho: MateusBrito<br>- Recrutador: Targaryen</p>
</div>
""", unsafe_allow_html=True)

# Expanders restantes
with st.expander("🎞️ Vídeos da Guilda", expanded=False):
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

with st.expander("💬 Depoimentos da Guilda", expanded=False):
    st.markdown("**MatheusBritoO:** \"Jogar com a SafeZone é sinônimo de risadas, estratégia e vitória. Aqui eu realmente me divirto.\"")
    st.markdown("**TargaryeR0X:** \"O PvP aqui é diferenciado! Os callers são experientes e organizados, a emoção é garantida.\"")
    st.markdown("**Reduzeh:** \"Minha primeira guilda no Albion! O pessoal me ajudou desde o começo, e cada dia é uma nova aventura.\"")
    st.markdown("**Xandinho:** \"Nunca pensei que começar no Albion pudesse ser tão legal. A galera aqui me acolheu de verdade.\"")

with st.expander("🖼️ Galeria de Imagens", expanded=False):
    st.image("https://albiononline.com/assets/images/news/2023-01-AlbionGuildSeason/Winner.jpg", use_column_width=True)
    st.image("https://albiononline.com/assets/images/news/2021-Season14/mid.jpg", use_column_width=True)

with st.expander("📋 Formulário de Recrutamento", expanded=False):
    with st.form(key="recrutamento_form"):
        nome = st.text_input("🧑 Nome do personagem")
        classe = st.selectbox("⚔️ Classe favorita", ["Melee", "Range", "Healer", "Tank", "Suporte"])
        fama_pvp = st.text_input("🔥 Fama PVP (ex: 2.5m, 1.2b)")
        fama_pve = st.text_input("🛡️ Fama PVE (ex: 4m, 500k)")
        enviar = st.form_submit_button("🚀 Enviar dados")

        if enviar:
            if nome and fama_pvp and fama_pve:
                data_envio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                sheet.append_row([nome, classe, fama_pvp, fama_pve, data_envio])
                st.success(f"✅ Cadastro enviado com sucesso! Bem-vindo(a), {nome}!")
                st.markdown("[Clique aqui para acessar o Discord da Guilda](https://discord.gg/FApJNJ4dXU)")
            else:
                st.error("Por favor, preencha todos os campos obrigatórios.")

# Feedback
with st.expander("🗣️ Deixe seu feedback para a guilda (em breve)"):
    st.text_input("Seu nome (opcional):")
    st.text_area("Mensagem:")
    st.button("Enviar Feedback")

# Discord & Footer
st.markdown("<div class='discord-link'><a href='https://discord.gg/FApJNJ4dXU' target='_blank'><img src='https://logodownload.org/wp-content/uploads/2017/11/discord-logo-0.png' alt='Discord'></a></div>", unsafe_allow_html=True)
st.markdown("<div class='footer'>SafeZone - Guilda BR de Albion Online | Desde 2023 | MANDATORY Alliance</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
