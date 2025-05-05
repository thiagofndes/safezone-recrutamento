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
sheet = client.open("Recrutamento SafeZone").sheet1



# ========================
# TÍTULO E FUNDO
# ========================
st.set_page_config(page_title="SafeZone - Recrutamento", layout="centered")

st.markdown("""
    <style>
        body {
            background-image: url('https://albiononline.com/assets/images/wallpapers/avalon.jpg');
            background-size: cover;
        }
        .main {
            background-color: rgba(0,0,0,0.7);
            padding: 2rem;
            border-radius: 10px;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main'>", unsafe_allow_html=True)
st.title("🏰 SafeZone - Formulário de Recrutamento")
st.markdown("**Seja bem-vindo!** Preencha os dados abaixo para analisarmos sua entrada na guilda.")

# ========================
# FORMULÁRIO
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

st.markdown("</div>", unsafe_allow_html=True)