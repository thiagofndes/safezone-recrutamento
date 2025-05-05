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
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background-color: #0d1117;
            color: white;
        }
        .main-container {
            background-color: rgba(0,0,0,0.85);
            padding: 2rem;
            border-radius: 15px;
            max-width: 800px;
            margin: auto;
            box-shadow: 0px 0px 15px #222;
        }
        .title {
            font-size: 2.5rem;
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
st.markdown("<div class='title'>SafeZone</div>", unsafe_allow_html=True)

# MENU
st.markdown("""
<div class='menu'>
    <a href="#sobre">SOBRE</a>
    <a href="#videos">VÍDEOS</a>
    <a href="#depoimentos">DEPOIMENTOS</a>
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

    Se você procura um time onde todos têm voz, onde a organização é prioridade e a diversão anda junto com o crescimento, a SafeZone é seu lugar!
    """)

# VIDEOS
with st.expander("🎬 Vídeos da Guilda"):
    st.markdown("Assista ao nosso vídeo mais recente:")
    st.video("https://www.youtube.com/embed/tgbNymZ7vqY")

# DEPOIMENTOS
st.markdown("<div id='depoimentos'></div>", unsafe_allow_html=True)
st.markdown("## 💬 Depoimentos da Guilda")

with st.container():
    st.markdown("**🧙‍♂️ MatheusBritoO**")
    st.write("\"Jogar com a galera da SafeZone é sempre diversão garantida. A galera é leve, organizada e cada conteúdo vira uma resenha. Mesmo nas runs mais tensas, tem sempre alguém pra fazer a gente rir. É aquele tipo de guilda que faz você querer logar todo dia.\"")

    st.markdown("**⚔️ TargaryeR0X**")
    st.write("\"Fazer PVP com a SafeZone é viciante. O caller tem experiência de sobra, sabe exatamente quando engajar, recuar e até ensinar quem tá começando. Me sinto seguro, mesmo nos fights mais intensos. A organização é absurda, parece até time profissional.\"")

    st.markdown("**🌱 Reduzeh**")
    st.write("\"Comecei no Albion sem conhecer nada, e já de cara fui acolhido pela SafeZone. Aprendi a coletar, famear, montar build… tudo com o pessoal me ajudando. Hoje, cada dia no jogo é uma aventura nova. Melhor começo impossível!\"")

    st.markdown("**🔰 Xandinho**")
    st.write("\"Essa foi minha primeira guilda e, sinceramente, não poderia ter caído em lugar melhor. A galera é unida, prestativa e te dá suporte pra tudo — desde build até onde famear. Me senti em casa desde o primeiro dia. SafeZone é família.\"")

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

st.markdown("</div>", unsafe_allow_html=True)  # fecha main-container
