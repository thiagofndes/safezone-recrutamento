import streamlit as st
import pandas as pd
import json, gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime

# 1️⃣ Configuração da página
st.set_page_config(page_title="Login | SafeZone", layout="centered")

# 2️⃣ Conexão com Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["GOOGLE_SERVICE_ACCOUNT"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client = gspread.authorize(creds)

spreadsheet_id = "1xRVuph9Y-6KMnEKmds17llmKYXSoaYTP2WCZkQRYtU0"
users_ws = client.open_by_key(spreadsheet_id).worksheet("LOGIN")
records = users_ws.get_all_records()
users_df = pd.DataFrame(records)

if users_df.empty:
    users_df = pd.DataFrame(columns=["nome", "password", "nivel", "email", "data"])

# 3️⃣ CSS visual padronizado
st.markdown("""
<style>
body, .stApp {
  background: url('https://github.com/thiagofndes/safezone-recrutamento/raw/main/images/FUNDO.png') center/cover fixed no-repeat;
}
.banner img {
  width: 50%;
  max-width: 300px;
  height: auto;
  margin: auto;
  display: block;
  border-radius: 10px;
}
.login-box {
  background: rgba(0,0,0,0.65);
  padding: 1.5rem;
  border-radius: 10px;
  max-width: 400px;
  margin: auto;
  color: white;
  text-align: center;
  margin-top: 20px;
}
input, select {
  border-radius: 6px !important;
}
.botao-voltar {
    background-color: #e6c300;
    color: black;
    padding: 10px 20px;
    border-radius: 10px;
    font-weight: bold;
    border: none;
    margin-top: 20px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.botao-voltar:hover {
    background-color: #d4b000;
}
</style>
""", unsafe_allow_html=True)

# 4️⃣ Banner e título
st.markdown("""
<div class="banner">
  <img src="https://github.com/thiagofndes/safezone-recrutamento/raw/main/images/BVANNER.png" alt="Banner">
</div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>🔐 Área de Login</h2>", unsafe_allow_html=True)

# 5️⃣ Login Box
with st.form("login_form", clear_on_submit=False):
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    usuario = st.text_input("👤 Nome de usuário")
    senha   = st.text_input("🔑 Senha", type="password")
    login   = st.form_submit_button("Entrar")

    if login:
        user_row = users_df[users_df["nome"] == usuario]
        if not user_row.empty and user_row.iloc[0]["password"] == senha:
            st.session_state.user = usuario
            st.session_state.role = int(user_row.iloc[0]["nivel"])
            st.success(f"✅ Bem-vindo, {usuario}!")
            st.rerun()
        else:
            st.error("❌ Usuário ou senha incorretos.")
    st.markdown('</div>', unsafe_allow_html=True)

# 6️⃣ Botão voltar
if st.button("⬅️ Voltar para a Home", key="voltar", help="Retorna à página inicial"):
    switch_page("testepython")
