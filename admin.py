import streamlit as st
import pandas as pd
import json, gspread, random, string, requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit_lottie as st_lottie

# 1️⃣ Configuração da página
st.set_page_config(page_title="SafeZone - Recrutamento", layout="wide")

# 2️⃣ Gera um captcha aleatório (5 chars)
if "captcha_key" not in st.session_state:
    st.session_state.captcha_key = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )

# 3️⃣ Conecta ao Google Sheets e carrega aba LOGIN
@st.cache_data(ttl=60)
def carregar_usuarios():
    SCOPE = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["GOOGLE_SERVICE_ACCOUNT"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
    client = gspread.authorize(creds)
    users_ws = client.open_by_key("1xRVuph9Y-6KMnEKmds17llmKYXSoaYTP2WCZkQRYtU0").worksheet("LOGIN")
    dados = users_ws.get_all_records()
    df = pd.DataFrame(dados)
    if df.empty:
        df = pd.DataFrame(columns=["nome", "password", "nivel", "email", "data"])
    return client, users_ws, df

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottie_url("https://lottie.host/27c0bd94-7a00-4433-80f6-bad7b0e4be5e/HMuVobExgh.json")

client, users_ws, users_df = carregar_usuarios()
spreadsheet_id = "1xRVuph9Y-6KMnEKmds17llmKYXSoaYTP2WCZkQRYtU0"

# 4️⃣ CSS global
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&display=swap');
  html, body, [class*="css"] {
    margin:0; padding:0; font-family:'Cinzel', serif; min-height:100vh;
  }
  .stApp {
    background: url('https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/FUNDO.png?raw=true')
                center/cover fixed no-repeat;
    color:white;
  }
  .login-box {
    background: rgba(0,0,0,0.8); border:1px solid #e6c300;
    padding:0.8rem; border-radius:8px; box-shadow:0 0 10px #000;
    margin-top:0.5rem;
  }
  .login-box .stTextInput>div>div>input {
    margin-bottom:0.4rem!important; padding:0.3rem!important;
    border-radius:4px!important; border:none!important;
  }
  .login-box button[kind="formSubmit"] {
    margin-top:0.4rem!important; padding:0.4rem!important;
  }
  .login-links { margin-top:0.4rem; text-align:center; }
  .login-links a { margin:0 0.1rem; font-size:0.8rem; color:#e6c300; }
  .login-links a:hover { text-decoration:underline; }
  .banner {
    text-align:center; padding:1rem 0 0.5rem; margin-bottom:0.5rem;
  }
  .banner img { width:100%; max-width:450px; height:auto; border-radius:10px; }
  .title {
    font-size:2.5rem; margin:0.8rem 0 0.4rem; text-align:center; color:#e6c300;
  }
  div[data-testid="stExpander"] {
    background:rgba(0,0,0,0.6)!important;
    padding:0.6rem 1rem!important;
    border-radius:10px!important;
    margin:0.6rem 0!important;
    max-width:900px!important;
  }
  .discord-link { text-align:left; margin:1rem 0; }
  .discord-link img { width:35px; }
  .footer {
    background: rgba(0,0,0,0.6);
    text-align: center;
    padding: 0.6rem;
    margin-top: 1rem;
    font-size: 0.8rem;
    color: #ccc;
    border-top: 1px solid #333;
  }
  .footer a {
    color: #e6c300;
    text-decoration: none;
    margin: 0 0.5rem;
  }
  .footer a:hover { text-decoration: underline; }
  @media(max-width:600px){
    .login-box { margin-top:0.3rem; }
  }
</style>
""", unsafe_allow_html=True)

# ✅ Exibe animação com proteção
if lottie_animation and isinstance(lottie_animation, dict) and "v" in lottie_animation:
    st_lottie.st_lottie(lottie_animation, height=150, key="animation")
else:
    st.warning("❗ Animação inválida ou não carregada.")
