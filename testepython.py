import streamlit as st
import pandas as pd
import json, gspread, random, string
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

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

# 4️⃣ Horário BR/UTC
now = datetime.utcnow()
br_time = (now - pd.Timedelta(hours=3)).strftime("%H:%M")
utc_time = now.strftime("%H:%M")

# 5️⃣ CSS adicional
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
.login-link {
  text-align: center;
  margin-top: 1rem;
}
.login-link a {
  color: #e6c300;
  font-weight: bold;
  text-decoration: none;
  font-size: 1rem;
}
.login-link a:hover {
  text-decoration: underline;
}
.login-button {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}
.discord-link img {
  width: 25px;
  height: 25px;
}
</style>
""", unsafe_allow_html=True)

# 6️⃣ Layout em colunas
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

        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.show_register:
        st.markdown('<div class="login-link"><a href="/">Voltar ao login</a></div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="login-button"><a href="/?page=admin" class="login-link">🔐 Ir para login/cadastro</a></div>',unsafe_allow_html=True)
        
# 7️⃣ Conteúdo principal
with col_content:
    st.markdown("""
    <div class="banner">
      <img src="https://github.com/thiagofndes/safezone-recrutamento/raw/main/images/BVANNER.png" alt="Banner">
    </div>
    """, unsafe_allow_html=True)

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

    if "user" not in st.session_state or st.session_state.get("role", 0) == 1:
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
    else:
        st.info("Você já é membro da SafeZone. Não é necessário preencher o formulário novamente.")

    with st.expander("🗣️ Deixe seu feedback para a guilda"):
        st.text_input("Seu nome (opcional):")
        st.text_area("Mensagem:")
        st.button("Enviar Feedback")

    st.markdown(f"""
      <div class="discord-link">
        <a href="https://discord.gg/FApJNJ4dXU" target="_blank">
          <img src="https://logodownload.org/wp-content/uploads/2017/11/discord-logo-0.png" alt="Discord">
        </a>
      </div>
      <div style="text-align:left;color:gray;font-size:0.8rem;margin-bottom:1rem;">
        SafeZone – Guilda BR de Albion Online | Desde 2023 | MANDATORY Alliance
      </div>
      <div class="footer">
        SafeZone © 2025 · Horário BR: <b>{br_time}</b> · Horário UTC: <b>{utc_time}</b><br>
        <a href="https://albiononline.com" target="_blank">Albion Online</a> · 
        <a href="https://discord.gg/FApJNJ4dXU" target="_blank">Nosso Discord</a> · 
        <a href="#">Termos</a>
      </div>
      <style>
      .footer {{
        background: rgba(0,0,0,0.6);
        text-align: center;
        padding: 0.6rem;
        margin-top: 1rem;
        font-size: 0.8rem;
        color: #ccc;
        border-top: 1px solid #333;
      }}
      .footer a {{
        color: #e6c300;
        text-decoration: none;
        margin: 0 0.5rem;
      }}
      .footer a:hover {{ text-decoration: underline; }}
      </style>
    """, unsafe_allow_html=True)
