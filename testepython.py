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
SCOPE = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["GOOGLE_SERVICE_ACCOUNT"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client = gspread.authorize(creds)

spreadsheet_id = "1xRVuph9Y-6KMnEKmds17llmKYXSoaYTP2WCZkQRYtU0"
users_ws = client.open_by_key(spreadsheet_id).worksheet("LOGIN")
records = users_ws.get_all_records()
users_df = pd.DataFrame(records)

if users_df.empty:
    users_df = pd.DataFrame(columns=["nome", "password", "nivel", "email", "data"])

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

# Função para carregar animação
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottie_url("https://lottie.host/27c0bd94-7a00-4433-80f6-bad7b0e4be5e/HMuVobExgh.json")

# 5️⃣ Layout em colunas
col_content, col_login = st.columns([3,1], gap="small")

with col_login:
    if "show_register" not in st.session_state:
        st.session_state.show_register = False

    def mostrar_login():
        st.session_state.show_register = False

    def mostrar_cadastro():
        st.session_state.show_register = True

    if "user" in st.session_state:
        nivel = st.session_state.role
        nome = st.session_state.user

        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown(f"### Seja bem-vindo, **{nome}**!", unsafe_allow_html=True)

        if nivel == 1:
            st.markdown("🔰 **Permissão:** Membro")
        elif nivel == 2:
            st.markdown("🛡️ **Permissão:** Recrutador")
        elif nivel == 3:
            st.markdown("👑 **Permissão:** Admin")

        if st.button("🚪 Sair"):
            del st.session_state["user"]
            del st.session_state["role"]
            st.rerun()

        if nivel == 3:
            st.markdown("---")
            st.markdown("👑 **Administração de Usuários**")

            records = users_ws.get_all_records()
            df_admin = pd.DataFrame(records)

            for i, row in df_admin.iterrows():
                with st.expander(f"👤 {row['nome']} | Nível: {row['nivel']}"):
                    novo_nome = st.text_input(f"Nome de usuário {i}", value=row["nome"], key=f"nome_{i}")
                    nova_senha = st.text_input(f"Senha {i}", value=row["password"], key=f"senha_{i}")
                    novo_email = st.text_input(f"E-mail {i}", value=row["email"], key=f"email_{i}")
                    novo_nivel = st.selectbox(f"Nível {i}", [1, 2, 3], index=row["nivel"] - 1, key=f"nivel_{i}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"💾 Salvar alterações {i}"):
                            users_ws.update(f"A{i+2}", [[novo_nome, nova_senha, novo_nivel, novo_email, row["data"]]])
                            st.success(f"Usuário {novo_nome} atualizado!")
                            st.rerun()
                    with col2:
                        if st.button(f"❌ Deletar usuário {i}"):
                            users_ws.delete_rows(i + 2)
                            st.warning(f"Usuário {row['nome']} removido!")
                            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.show_register:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("### Criar Conta", unsafe_allow_html=True)
        with st.form("register_form"):
            new_user = st.text_input("Novo usuário")
            new_pwd = st.text_input("Nova senha", type="password")
            confirm_pwd = st.text_input("Confirme a senha", type="password")
            new_email = st.text_input("E-mail")
            criar = st.form_submit_button("Criar Conta")

            if criar:
                records = users_ws.get_all_records()
                users_df = pd.DataFrame(records)
                if users_df.empty:
                    users_df = pd.DataFrame(columns=["nome", "password", "nivel", "email", "data"])

                if not new_user or not new_pwd or not confirm_pwd or not new_email:
                    st.error("Preencha todos os campos.")
                elif len(new_pwd) < 6:
                    st.error("A senha deve ter pelo menos 6 caracteres.")
                elif new_pwd != confirm_pwd:
                    st.error("As senhas não coincidem.")
                elif "@" not in new_email or "." not in new_email:
                    st.error("E-mail inválido.")
                elif new_user in users_df["nome"].values:
                    st.error("Usuário já existe.")
                else:
                    data_cadastro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    users_ws.append_row([new_user, new_pwd, 1, new_email, data_cadastro])
                    st.success(f"Conta de {new_user} criada com sucesso!")
                    st.session_state.show_register = False

        if st.button("🔙 Voltar ao login"):
            mostrar_login()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("### Login SafeZone", unsafe_allow_html=True)
        with st.form("login_form", clear_on_submit=False):
            user_in = st.text_input("Usuário", placeholder="seu_usuario")
            pwd_in = st.text_input("Senha", type="password", placeholder="••••••••")
            st.write(f"🔐 **Captcha:** {st.session_state.captcha_key}")
            captcha_in = st.text_input("Digite o captcha", placeholder="XXXXX")
            submit = st.form_submit_button("Entrar")

            if submit:
                records = users_ws.get_all_records()
                users_df = pd.DataFrame(records)
                if users_df.empty:
                    users_df = pd.DataFrame(columns=["nome", "password", "nivel", "email", "data"])

                row = users_df.loc[users_df["nome"] == user_in]
                if not row.empty:
                    correct_pwd = str(row["password"].values[0])
                    if pwd_in == correct_pwd and captcha_in == st.session_state.captcha_key:
                        st.success(f"Bem-vindo, **{user_in}**!")
                        st.session_state.user = user_in
                        st.session_state.role = int(row["nivel"].values[0])
                        st.rerun()
                    else:
                        st.error("Usuário, senha ou captcha incorretos.")
                else:
                    st.error("Usuário não encontrado.")

        st.markdown("""
          <div class="login-links">
            <a href="#">Esqueci minha senha</a>
          </div>
        """, unsafe_allow_html=True)

        if st.button("🌚 Criar nova conta"):
            mostrar_cadastro()

        st.markdown('</div>', unsafe_allow_html=True)

# 6️⃣ Conteúdo principal (público)
with col_content:
    st.markdown("""
    <div class="banner">
      <img src="https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/BVANNER.png?raw=true" alt="Banner">
    </div>
    """, unsafe_allow_html=True)

    st_lottie.st_lottie(lottie_animation, height=150, key="animation")

    st.markdown('<div class="title">SafeZone</div>', unsafe_allow_html=True)

    with st.expander("📌 Sobre a Guilda", expanded=True):
        st.markdown("- **Missão:** Formar comunidade madura, respeitosa e com espírito de equipe focada em PvP.")
        st.markdown("- **Benefícios:** Calls de qualidade, apoio a novos e veteranos.")
        st.markdown("- **Staff:** GM: SafiraSkins | Braço direito: Taigona | Conselho: MateusBrito | Recrutador: TargaryeR0X")
        st.markdown("- **Horários de pico:** BR: 19h-23h | UTC: 22h-02h")

    with st.expander("🎞️ Vídeos da Guilda"):
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    with st.expander("💬 Depoimento de Membros"):
        st.markdown("**MatheusBritoO:** \"Jogar com a SafeZone é sinônimo de risadas e vitória.\"")
        st.markdown("**TargaryeR0X:** \"O PvP aqui é diferenciado!\"")
        st.markdown("**Reduzeh:** \"Minha primeira guilda no Albion!\"")
        st.markdown("**Xandinho:** \"Albion nunca foi tão legal.\"")

    with st.expander("🖼️ Galeria de Imagens"):
        st.image("https://albiononline.com/assets/images/news/2023-01-AlbionGuildSeason/Winner.jpg", use_column_width=True)
        st.image("https://albiononline.com/assets/images/news/2021-Season14/mid.jpg", use_column_width=True)

    with st.expander("📋 Formulário de Recrutamento"):
        sheet = client.open_by_key(spreadsheet_id).worksheet("Página1")
        with st.form("recrutamento_form"):
            nome     = st.text_input("🧑 Nome do personagem")
            classe   = st.selectbox("⚔️ Classe favorita", ["Melee","Range","Healer","Tank","Suporte"])
            fama_pvp = st.text_input("🔥 Fama PVP (ex: 2.5m, 1.2b)")
            fama_pve = st.text_input("🛡️ Fama PVE (ex: 4m, 500k)")
            enviar   = st.form_submit_button("Enviar")
            if enviar and nome and fama_pvp and fama_pve:
                ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                sheet.append_row([nome, classe, fama_pvp, fama_pve, ts])
                st.success(f"✅ Cadastro de **{nome}** enviado!")
            elif enviar:
                st.error("Por favor, preencha todos os campos.")

    with st.expander("🗣️ Deixe seu feedback para a guilda"):
        st.text_input("Seu nome (opcional):")
        st.text_area("Mensagem:")
        st.button("Enviar Feedback")

    st.markdown("""
      <div class="discord-link">
        <a href="https://discord.gg/FApJNJ4dXU" target="_blank">
          <img src="https://logodownload.org/wp-content/uploads/2017/11/discord-logo-0.png" alt="Discord">
        </a>
      </div>
      <div style="text-align:left;color:gray;font-size:0.8rem;margin-bottom:1rem;">
        SafeZone – Guilda BR de Albion Online | Desde 2023 | MANDATORY Alliance
      </div>
      <div class="footer">
        SafeZone © 2025 · <a href="https://albiononline.com" target="_blank">Albion Online</a> · 
        <a href="https://discord.gg/FApJNJ4dXU" target="_blank">Nosso Discord</a> · 
        <a href="#">Termos</a>
      </div>
    """, unsafe_allow_html=True)
