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
sheet = client.open_by_key(spreadsheet_id).worksheet("Pagina1")

# ========================
# CONFIGURAÇÃO DE PÁGINA
# ========================
st.set_page_config(page_title="SafeZone - Recrutamento", layout="centered")

# ========================
# CSS CUSTOMIZADO PARA ESTILO
# ========================
st.markdown("""
    <style>
        * { box-sizing: border-box; }
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            background-color: #0d1117;
            color: white;
        }
        .main-container {
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.85));
            padding: 2rem;
            border-radius: 15px;
            max-width: 600px;
            margin: auto;
            box-shadow: 0px 0px 15px #222;
        }
        .title {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 10px;
            color: #e6c300;
        }
        .subtitle {
            text-align: center;
            margin-bottom: 30px;
        }
        .info-box {
            margin-top: 40px;
            padding: 1rem;
            background: rgba(255,255,255,0.05);
            border-left: 5px solid #e6c300;
            border-radius: 8px;
            font-size: 0.95rem;
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
""", unsafe_allow_html=True)

# ========================
# CONTEÚDO DA LANDING PAGE
# ========================
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<div class='title'>SafeZone</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Formulário de Recrutamento</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='info-box'>
        <strong>🌍 Sobre a Guilda:</strong><br>
        A SafeZone é uma guilda brasileira voltada para jogadores adultos que prezam pelo respeito, crescimento coletivo e diversão. Nosso foco inclui ZVZs com a Mandatory, PVP small scale, coleta, fame em World Boss, Avalons e caçadas. Procuramos jogadores comprometidos, que jogam com propósito, respeitando o time e valorizando a evolução conjunta.
        <br><br>
        Se você quer jogar com organização e propósito, aqui é o seu lugar.
    </div>
""", unsafe_allow_html=True)

# ========================
# FORMULÁRIO DE RECRUTAMENTO
# ========================
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

# ========================
# LINK PARA DISCORD
# ========================
st.markdown("""
<div class='discord-button'>
    <a href='https://discord.gg/FApJNJ4dXU' target='_blank'>Entrar no Discord da Guilda</a>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
