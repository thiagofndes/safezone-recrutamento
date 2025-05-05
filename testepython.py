import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ========================
# CONFIGURAÇÃO DO GOOGLE SHEETS COM SEGREDOS
# ========================
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
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
# ESTILIZAÇÃO
# ========================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&display=swap');
        html, body, [class*="css"] {
            font-family: 'Cinzel', serif;
            background-image: url('https://safezone-site.s3.amazonaws.com/FUNDO.png');
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
            color: white;
        }
        .main-container {
            background-color: rgba(0,0,0,0.85);
            padding: 2rem;
            border-radius: 15px;
            max-width: 900px;
            margin: auto;
            box-shadow: 0px 0px 15px #222;
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
        .banner {
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .banner img {
            width: 100%;
            max-width: 600px;
            border-radius: 15px;
        }
        .footer {
            margin-top: 4rem;
            text-align: center;
            font-size: 0.8rem;
            color: gray;
        }
        @media screen and (max-width: 600px) {
            .menu {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ========================
# CONTEÚDO DA PÁGINA
# ========================
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.markdown("""
<div class='banner'>
    <img src='https://safezone-site.s3.amazonaws.com/BVANNER.png' alt='Banner da Guilda'>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>SafeZone</div>", unsafe_allow_html=True)

# MENU
st.markdown("""
<div class='menu'>
    <a href="#sobre">SOBRE</a>
    <a href="#videos">VÍDEOS</a>
    <a href="#depoimentos">DEPOIMENTOS</a>
    <a href="#galeria">GALERIA</a>
    <a href="#recrutamento">RECRUTAMENTO</a>
</div>
""", unsafe_allow_html=True)

# SOBRE A GUILDA
with st.expander("🌍 Sobre a Guilda"):
    st.markdown("""
    **🎯 Missão da SafeZone**

    Criar um ambiente maduro e organizado para jogadores que desejam evoluir em grupo. Respeitamos o tempo de cada um, priorizamos a união e buscamos excelência sem pressão tóxica. Jogamos com propósito, não por obrigação.

    **🛡️ Benefícios para os jogadores:**
    - ✅ ZVZ com a aliança MANDATORY
    - ✅ PVP small scale em outposts, Avalons e open world
    - ✅ Fama em grupo e World Boss
    - ✅ Reuniões de coleta organizadas
    - ✅ Mentoria para novos jogadores
    - ✅ Discord ativo e bem estruturado

    **⏰ Horário de Atividade**
    - Horário BR: 19h às 23h
    - Horário UTC: 22h às 02h (UTC de Albion)

    **👑 Liderança da Guilda**
    - GM da Guilda: SafiraSkins
    - Braço direito: Taigona
    - Conselho: MateusBrito
    - Recrutador: Targaryen
    """)

# VIDEOS
with st.expander("🎬 Vídeos da Guilda"):
    st.markdown("Assista ao nosso vídeo mais recente:")
    st.video("https://www.youtube.com/watch?v=1Ne1hqOXKKI")

# DEPOIMENTOS
with st.expander("💬 Depoimentos da Guilda"):
    with st.container():
        st.markdown("**🧙‍♂️ MatheusBritoO**")
        st.success("\"Jogar com a galera da SafeZone é sempre diversão garantida. A galera é leve, organizada e cada conteúdo vira uma resenha. Mesmo nas runs mais tensas, tem sempre alguém pra fazer a gente rir. É aquele tipo de guilda que faz você querer logar todo dia.\"")

        st.markdown("**⚔️ TargaryeR0X**")
        st.info("\"Fazer PVP com a SafeZone é viciante. O caller tem experiência de sobra, sabe exatamente quando engajar, recuar e até ensinar quem tá começando. Me sinto seguro, mesmo nos fights mais intensos. A organização é absurda, parece até time profissional.\"")

        st.markdown("**🌱 Reduzeh**")
        st.warning("\"Comecei no Albion sem conhecer nada, e já de cara fui acolhido pela SafeZone. Aprendi a coletar, famear, montar build… tudo com o pessoal me ajudando. Hoje, cada dia no jogo é uma aventura nova. Melhor começo impossível!\"")

        st.markdown("**🔰 Xandinho**")
        st.success("\"Essa foi minha primeira guilda e, sinceramente, não poderia ter caído em lugar melhor. A galera é unida, prestativa e te dá suporte pra tudo — desde build até onde famear. Me senti em casa desde o primeiro dia. SafeZone é família.\"")

# GALERIA DE IMAGENS
with st.expander("🖼️ Galeria da Guilda"):
    st.image("https://cdn.albiononline.com/uploads/media/default/media/faction-warfare-1920x1080_1652453972.jpg", caption="ZVZ em Martlock")
    st.image("https://cdn.albiononline.com/uploads/media/default/media/avalonian-invasion-1920x1080_1575644555.jpg", caption="Avalon Smash!")

# RECRUTAMENTO
with st.expander("📋 Formulário de Recrutamento"):
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
                st.markdown("""
                    <div style='text-align: center; margin-top: 20px;'>
                        <a href='https://discord.gg/FApJNJ4dXU' target='_blank' style='background-color: #5865F2; padding: 10px 20px; border-radius: 8px; color: white; font-weight: bold; text-decoration: none;'>Entrar no Discord da Guilda</a>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Por favor, preencha todos os campos obrigatórios.")

# FEEDBACK (ainda não funcional)
with st.expander("📣 Deixe seu feedback para a SafeZone"):
    st.text_area("Escreva aqui sua sugestão, crítica ou elogio")
    st.caption("Funcionalidade em desenvolvimento")

st.markdown("""
<div class='footer'>
    SafeZone - Guilda BR de Albion Online | Desde 2023 | MANDATORY Alliance
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # fecha main-container
