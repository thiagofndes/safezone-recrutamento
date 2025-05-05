# login.py
import streamlit as st

def show_login():
    """
    Exibe o formulário de login e controla o fluxo de autenticação em st.session_state.
    Retorna True se o login for bem-sucedido, False caso contrário.
    """
    # Se ainda não inicializamos a sessão de login, cria as variáveis:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user      = None
        st.session_state.role      = None

    # Se já estiver logado, pula direto
    if st.session_state.logged_in:
        return True

    # Configurações visuais
    st.title("🔐 SafeZone • Login")
    st.write("Por favor, entre com seu usuário e senha para acessar o site.")

    # --- Formulário de Login ---
    user = st.text_input("Usuário", placeholder="seu_usuario", key="login_user")
    pwd  = st.text_input("Senha", type="password", placeholder="••••••••", key="login_pwd")
    login_btn = st.button("Entrar")

    # Aqui você faria a verificação real contra seu banco de dados ou
    # Google Sheets de usuários. Como exemplo, vamos criar um dicionário
    # simples de usuários com papel (role):
    USERS = {
        "admin":      {"pwd":"admin123",      "role":"admin"},
        "recrutador": {"pwd":"recruta123",     "role":"recrutador"},
        "membro":     {"pwd":"membro123",      "role":"membro"},
    }

    # Ao clicar em “Entrar”:
    if login_btn:
        if user in USERS and USERS[user]["pwd"] == pwd:
            # Armazena na sessão
            st.session_state.logged_in = True
            st.session_state.user      = user
            st.session_state.role      = USERS[user]["role"]
            st.success(f"Bem-vindo, **{user}**! Papel: *{st.session_state.role}*")
            return True
        else:
            st.error("Usuário ou senha incorretos.")
            return False

    return False
