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
# CSS CUSTOMIZADO PARA ESTILO E MENU
# ========================
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            background-color: #0d1117;
            color: white;
        }
        .main-container {
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.85));
            padding: 2rem;
            border-radius: 15px;
            max-width: 800px;
            margin: auto;
            box-shadow: 0px 0px 15px #222;
        }
        .title {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 10px;
            color: #e6c300;
        }
        .menu {
            text-align: center;
            margin-bottom: 2rem;
        }
        .menu a {
            margin: 0 1rem;
            text-decoration: none;
            font-weight: bold;
            color: #e6c300;
            cursor: pointer;
        }
        .section {
            margin-top: 30px;
        }
        .collapsible {
            background-color: #20232a;
            color: white;
            cursor: pointer;
            padding: 18px;
            width: 100%;
            border: none;
            text-align: left;
            outline: none;
            font-size: 15px;
        }
        .active, .collapsible:hover {
            background-color: #333;
        }
        .content {
            padding: 0 18px;
            display: none;
            overflow: hidden;
            background-color: #1e1e1e;
            border-left: 5px solid #e6c300;
        }
        .discord-button {
            display: block;
            text-align: center;
            margin-top: 30px;
        }
        .discord-button a {
            background-color: #5865F2;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
        }
        .discord-button a:hover {
            background-color: #4752c4;
        }
        @media screen and (max-width: 600px) {
            .main-container {
                padding: 1rem;
            }
        }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const items = document.getElementsByClassName("collapsible");
            for (let i = 0; i < items.length; i++) {
                items[i].addEventListener("click", function () {
                    this.classList.toggle("active");
                    const content = this.nextElementSibling;
                    if (content.style.display === "block") {
                        content.style.display = "none";
                    } else {
                        content.style.display = "block";
                    }
                });
            }
        });
    </script>
""", unsafe_allow_html=True)

# ========================
# CONTEÚDO DA LANDING PAGE
# ========================
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<div class='title'>SafeZone</div>", unsafe_allow_html=True)

# Menu
st.markdown("""
<div class='menu'>
    <a href="#sobre">SOBRE</a>
    <a href="#videos">VIDEOS</a>
    <a href="#recrutamento">RECRUTAMENTO</a>
</div>
""", unsafe_allow_html=True)

# SOBRE
titulo_sobre = "<div class='section' id='sobre'>"
conteudo_sobre = """
<button class="collapsible">🌍 Sobre a Guilda</button>
<div class="content">
    <p><strong>🎯 Missão da SafeZone</strong><br>
    Criar um ambiente maduro e organizado para jogadores que desejam evoluir em grupo. Aqui, respeitamos o tempo de cada um, priorizamos a união e buscamos excelência sem pressão tóxica. Jogamos com propósito, não por obrigação.</p>

    <p><strong>🛡️ O que você encontrará aqui:</strong></p>
    <ul>
        <li>✅ ZVZ com a aliança MANDATORY</li>
        <li>✅ PVP small scale em outposts, Avalons e open world</li>
        <li>✅ Fama em grupo e World Boss</li>
        <li>✅ Reuniões de coleta organizadas</li>
        <li>✅ Mentoria para novos jogadores</li>
        <li>✅ Discord ativo e bem estruturado</li>
    </ul>

    <p>Se você procura um time onde todos têm voz, onde a organização é prioridade e a diversão anda junto com o crescimento, a SafeZone é seu lugar!</p>
</div>
</div>
"""
st.markdown(titulo_sobre, unsafe_allow_html=True)
st.markdown(conteudo_sobre, unsafe_allow_html=True)

# VIDEOS
st.markdown("<div class='section' id='videos'>", unsafe_allow_html=True)
st.markdown("""
<button class="collapsible">🎬 Vídeos da Guilda</button>
<div class="content">
    <p>Assista ao nosso vídeo mais recente:</p>
    <iframe width="100%" height="315" src="https://www.youtube.com/embed/tgbNymZ7vqY" frameborder="0" allowfullscreen></iframe>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# RECRUTAMENTO
st.markdown("<div class='section' id='recrutamento'>", unsafe_allow_html=True)
st.markdown("""
<button class="collapsible">📋 Formulário de Recrutamento</button>
<div class="content">
""", unsafe_allow_html=True)

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
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

st.markdown("""
<div class='discord-button'>
    <a href='https://discord.gg/FApJNJ4dXU' target='_blank'>Entrar no Discord da Guilda</a>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # fecha main-container
