import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Administração - SafeZone", layout="wide")

# Autentica com Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["GOOGLE_SERVICE_ACCOUNT"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client = gspread.authorize(creds)

spreadsheet_id = "1xRVuph9Y-6KMnEKmds17llmKYXSoaYTP2WCZkQRYtU0"
users_ws = client.open_by_key(spreadsheet_id).worksheet("LOGIN")

# Verifica permissão
if "user" not in st.session_state or st.session_state.get("role", 0) != 3:
    st.warning("Você não tem permissão para acessar esta página.")
    st.stop()

# Estilo personalizado
st.markdown("""
    <style>
    .stApp {
        background: url('https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/FUNDO.png?raw=true')
                    center/cover fixed no-repeat;
        color: white;
    }
    .admin-box {
        background: rgba(0,0,0,0.75);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 0 10px #000;
        margin-bottom: 1rem;
        border: 1px solid #e6c300;
    }
    .admin-title {
        font-size: 2rem;
        text-align: center;
        margin-bottom: 1rem;
        color: #e6c300;
    }
    </style>
""", unsafe_allow_html=True)

# Conteúdo principal
st.markdown('<div class="admin-box">', unsafe_allow_html=True)
st.markdown('<div class="admin-title">👑 Painel de Administração</div>', unsafe_allow_html=True)
st.success(f"Administrador logado: {st.session_state['user']}")
st.markdown('</div>', unsafe_allow_html=True)

# Carrega dados
records = users_ws.get_all_records()
df = pd.DataFrame(records)

if df.empty:
    st.info("Nenhum usuário cadastrado ainda.")
else:
    st.subheader("👥 Gerenciamento de Usuários")
    for i, row in df.iterrows():
        with st.expander(f"👤 {row['nome']} | Nível: {row['nivel']}"):
            novo_nome = st.text_input(f"Nome {i}", value=row["nome"], key=f"admin_nome_{i}")
            nova_senha = st.text_input(f"Senha {i}", value=row["password"], key=f"admin_senha_{i}")
            novo_email = st.text_input(f"E-mail {i}", value=row["email"], key=f"admin_email_{i}")
            novo_nivel = st.selectbox(f"Nível {i}", [1, 2, 3], index=int(row["nivel"])-1, key=f"admin_nivel_{i}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"💾 Salvar {i}"):
                    users_ws.update(f"A{i+2}", [[novo_nome, nova_senha, novo_nivel, novo_email, row["data"]]])
                    st.success(f"Usuário {novo_nome} atualizado.")
                    st.experimental_rerun()
            with col2:
                if st.button(f"❌ Deletar {i}"):
                    users_ws.delete_rows(i + 2)
                    st.warning(f"Usuário {row['nome']} removido.")
                    st.experimental_rerun()
