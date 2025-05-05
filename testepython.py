# testepython.py
import streamlit as st
import json, gspread, random, string
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1️⃣ Configuração da página
st.set_page_config(page_title="SafeZone - Recrutamento", layout="wide")

# 2️⃣ Gera um captcha aleatório
if "captcha_key" not in st.session_state:
    st.session_state.captcha_key = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )

# 3️⃣ CSS global + estilização de expanders e login box
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&display=swap');
  html, body, [class*="css"] {
    margin:0; padding:0; min-height:100vh;
    font-family:'Cinzel', serif;
  }
  .stApp {
    background: url('https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/FUNDO.png?raw=true')
                center/cover fixed no-repeat;
    color:white;
  }

  /* LOGIN BOX */
  .login-box {
    background: rgba(0,0,0,0.8);
    border: 1px solid #e6c300;
    padding: 1rem; border-radius: 8px;
    box-shadow: 0 0 10px #000;
    margin-top:1rem;
  }
  .login-box .stTextInput>div>div>input {
    width:100% !important; margin-bottom:0.5rem!important;
    padding:0.4rem!important; border-radius:4px!important; border:none!important;
  }
  .login-box button[kind="formSubmit"] {
    width:100% !important; margin-top:0.5rem!important;
    background:#e6c300!important; color:#000!important; border:none!important;
    border-radius:4px!important; font-weight:bold!important;
  }
  .login-links { text-align:center; margin-top:0.5rem; }
  .login-links a {
    color:#e6c300; text-decoration:none; font-size:0.85rem; margin:0 0.2rem;
  }
  .login-links a:hover { text-decoration:underline; }

  /* BANNER */
  .banner { text-align:center; padding:2rem 0 1rem; margin-bottom:1rem; }
  .banner img { width:50%; max-width:300px; border-radius:10px; }

  /* TÍTULO & MENU */
  .title {
    font-size:3rem; text-align:center; color:#e6c300; margin:1rem 0 0.5rem;
  }
  .menu {
    display:flex; justify-content:center; gap:2rem; margin-bottom:2rem;
  }
  .menu a {
    color:#e6c300; font-weight:bold; text-decoration:none;
  }
  .menu a:hover { color:#fff; }

  /* EXPANDERS */
  div[data-testid="stExpander"] {
    background: rgba(0,0,0,0.6) !important;
    padding: 1rem 1.5rem !important;
    border-radius: 12px !important;
    margin: 1rem 0 !important;
    width: 100% !important;
  }

  /* DISCORD ICON */
  .discord-link { text-align:left; margin:2rem 0; }
  .discord-link img { width:40px; cursor:pointer; }

  @media(max-width:600px){
    .menu { flex-direction:column; }
    .login-box { margin-top:0.5rem; }
  }
</style>
""", unsafe_allow_html=True)

# 4️⃣ Layout em colunas (conteúdo / login)
col_content, col_login = st.columns([3,1], gap="small")

# — login na coluna direita —
with col_login:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("### Login SafeZone", unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=False):
        user_in    = st.text_input("Usuário", placeholder="seu_usuario")
        pwd_in     = st.text_input("Senha", type="password", placeholder="••••••••")
        st.write(f"🔐 **Captcha:** {st.session_state.captcha_key}")
        captcha_in = st.text_input("Digite o captcha", placeholder="XXXXX")
        submit     = st.form_submit_button("Entrar")
        if submit:
            if captcha_in == st.session_state.captcha_key:
                st.success(f"Bem-vindo, **{user_in}**!")
            else:
                st.error("Captcha incorreto, tente novamente.")
    st.markdown("""
      <div class="login-links">
        <a href="#">Esqueci minha senha</a> |
        <a href="#">Criar conta</a>
      </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# — TODO o resto na coluna esquerda —
with col_content:
    # — Google Sheets (CRUD) —
    SCOPE      = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
    creds      = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
    client     = gspread.authorize(creds)
    sheet      = client.open_by_key(
        "1xRVuph9Y-6KMnEKmds17llmKYXSoaYTP2WCZkQRYtU0"
    ).worksheet("Página1")

    # — Banner —
    st.markdown("""
    <div class="banner">
      <img src="https://github.com/thiagofndes/safezone-recrutamento/blob/main/images/BVANNER.png?raw=true" alt="Banner">
    </div>
    """, unsafe_allow_html=True)

    # — Título & Menu —
    st.markdown('<div class="title">SafeZone</div>', unsafe_allow_html=True)
    st.markdown("""
      <div class="menu">
        <a href="#sobre">SOBRE</a>
        <a href="#videos">VÍDEOS</a>
        <a href="#depoimento-de-membros">DEPOIMENTO DE MEMBROS</a>
        <a href="#galeria">GALERIA</a>
        <a href="#recrutamento">RECRUTAMENTO</a>
      </div>
    """, unsafe_allow_html=True)

    # — Sobre a Guilda —
    with st.expander("📌 Sobre a Guilda", expanded=True):
        st.markdown("- **Missão:** Formar comunidade madura, respeitosa e com espírito de equipe focada em PvP.")
        st.markdown("- **Benefícios:** Calls de qualidade, apoio a novos e veteranos.")
        st.markdown("- **Staff:** GM: SafiraSkins | Braço direito: Taigona | Conselho: MateusBrito | Recrutador: TargaryeR0X")
        st.markdown("- **Horários de pico:** BR: 19h-23h | UTC: 22h-02h")

    # — Vídeos da Guilda —
    with st.expander("🎞️ Vídeos da Guilda"):
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    # — Depoimento de Membros —
    with st.expander("💬 Depoimento de Membros"):
        st.markdown("**MatheusBritoO:** \"Jogar com a SafeZone é sinônimo de risadas e vitória.\"")
        st.markdown("**TargaryeR0X:** \"O PvP aqui é diferenciado! Os callers são experientes e organizados.\"")
        st.markdown("**Reduzeh:** \"Minha primeira guilda no Albion! Cada dia é uma aventura.\"")
        st.markdown("**Xandinho:** \"Nunca pensei que começar no Albion fosse tão legal.\"")

    # — Galeria de Imagens —
    with st.expander("🖼️ Galeria de Imagens"):
        st.image(
            "https://albiononline.com/assets/images/news/2023-01-AlbionGuildSeason/Winner.jpg",
            use_column_width=True
        )
        st.image(
            "https://albiononline.com/assets/images/news/2021-Season14/mid.jpg",
            use_column_width=True
        )

    # — Formulário de Recrutamento —
    with st.expander("📋 Formulário de Recrutamento"):
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

    # — Feedback —
    with st.expander("🗣️ Deixe seu feedback para a guilda"):
        st.text_input("Seu nome (opcional):")
        st.text_area("Mensagem:")
        st.button("Enviar Feedback")

    # — Rodapé —
    st.markdown("""
      <div class="discord-link">
        <a href="https://discord.gg/FApJNJ4dXU" target="_blank">
          <img src="https://logodownload.org/wp-content/uploads/2017/11/discord-logo-0.png" alt="Discord">
        </a>
      </div>
      <div style="text-align:left;color:gray;font-size:0.8rem;margin-bottom:2rem;">
        SafeZone – Guilda BR de Albion Online | Desde 2023 | MANDATORY Alliance
      </div>
    """, unsafe_allow_html=True)
