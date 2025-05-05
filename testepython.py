import streamlit as st
from PIL import Image
import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# CONFIGURAÇÃO
st.set_page_config(page_title="SAFEZONE Recrutamento", layout="centered")
UPLOAD_FOLDER = "uploads"
DB_PATH = "sqlite:///cadastros.db"

# GARANTIR PASTA DE UPLOAD
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# CONEXÃO COM BANCO
engine = create_engine(DB_PATH)

# CABEÇALHO
st.title("🛡️ S A F E Z O N E")
st.subheader("Unidos pela Glória em Albion Online")
st.markdown("---")

# SEÇÃO: SOBRE A GUILDA
with st.expander("📜 Quem Somos"):
    st.write(
        """
        A **S A F E Z O N E** é uma guilda brasileira formada por jogadores adultos,
        focados em PvP de qualidade, organização e respeito. 
        Nosso foco está na evolução em grupo e nos objetivos estratégicos dentro do mundo de Albion.
        """
    )

# SEÇÃO: ATIVIDADES
with st.expander("⚔️ Nossas Atividades"):
    st.markdown("**ZVZ** – Batalhas em larga escala com aliados.")
    st.markdown("**World Boss** – Caçadas semanais com premiações.")
    st.markdown("**Avalon** – PvP e fama em conteúdo médio/pequeno.")
    st.markdown("**Outposts** – Defesa e tomada de pontos táticos.")

# FORMULÁRIO DE RECRUTAMENTO
st.markdown("## ✍️ Formulário de Recrutamento")
with st.form("formulario_recrutamento"):
    nome = st.text_input("Nome do Personagem")
    classe = st.selectbox("Classe Favorita", ["Melee", "Range", "Healer", "Tank", "Suporte"])
    fama_pvp = st.text_input("Fama PVP", placeholder="Ex: 2.5m, 500k, 1b")
    fama_pve = st.text_input("Fama PVE", placeholder="Ex: 4m, 1.2b, 700k")
    imagem = st.file_uploader("Upload da imagem de fama", type=["png", "jpg", "jpeg"])
    submit = st.form_submit_button("Enviar")

    if submit:
        if nome and fama_pvp and fama_pve and imagem:
            # SALVAR IMAGEM
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"{nome}_{timestamp}.{imagem.name.split('.')[-1]}"
            caminho_imagem = os.path.join(UPLOAD_FOLDER, nome_arquivo)
            with open(caminho_imagem, "wb") as f:
                f.write(imagem.getbuffer())

            # SALVAR DADOS NO BANCO
            df = pd.DataFrame([{
                "nome": nome,
                "classe": classe,
                "fama_pvp": fama_pvp,
                "fama_pve": fama_pve,
                "imagem": nome_arquivo,
                "data_envio": datetime.now()
            }])
            df.to_sql("recrutamentos", con=engine, if_exists="append", index=False)

            st.success(f"Cadastro enviado com sucesso! Bem-vindo(a), {nome}!")
            st.image(caminho_imagem, use_column_width=True)
        else:
            st.error("Preencha todos os campos e envie a imagem.")
