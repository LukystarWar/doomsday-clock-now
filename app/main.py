import os
import datetime
import streamlit as st
from groq_client import analisar_noticias
from news_fetcher import obter_noticias_gnews
from news_updater import atualizar_noticias_diariamente

# Caminhos corretos para acessar a pasta data (um nível acima da pasta app)
BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
NOTICIAS_PATH = os.path.join(DATA_DIR, "noticias.txt")

# Configuração da página
st.set_page_config(page_title="Doomsday Clock Now", layout="centered")
st.markdown("""
    <style>
    @media (max-width: 600px) {
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.4rem !important; }
        h3 { font-size: 1.2rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🕛 Doomsday Clock Now")
st.markdown("Atualização diária simulada com base em **notícias reais** e análise de IA via Groq.")

# Atualização de notícias se necessário
if not os.path.exists(NOTICIAS_PATH) or atualizar_noticias_diariamente("forcar_verificacao"):
    noticias = obter_noticias_gnews()
    atualizar_noticias_diariamente(noticias)
    st.success("📰 Notícias atualizadas com sucesso!")
else:
    with open(NOTICIAS_PATH, "r", encoding="utf-8") as f:
        noticias = f.read()
    st.info("✅ As notícias de hoje já foram carregadas anteriormente.")

st.markdown("### 📰 Notícias atuais analisadas")
st.code(noticias, language="text")

# Botão de análise
if st.button("🔄 Atualizar relógio com base nas notícias"):
    try:
        resposta = analisar_noticias(noticias)
        linhas = [linha.strip() for linha in resposta.split("\n") if linha.strip()]

        if len(linhas) < 2 or ":" not in linhas[0] or ":" not in linhas[1]:
            st.error("❌ A IA não respondeu no formato esperado. Tente novamente.")
            st.code(resposta)
        else:
            tempo_raw = linhas[0].split(":")[1].strip().lower()

            if "minuto" in tempo_raw:
                tempo_em_segundos = int("".join(filter(str.isdigit, tempo_raw))) * 60
            elif "segundo" in tempo_raw:
                tempo_em_segundos = int("".join(filter(str.isdigit, tempo_raw)))
            else:
                tempo_em_segundos = None

            risco = linhas[1].split(":")[1].strip()
            analise = "\n".join(linhas[2:]).replace("Análise: ", "").strip()

            atualizado_em = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            st.success(f"⏳ Tempo para a meia-noite: {tempo_em_segundos} segundos")
            st.info(f"🔴 Nível de risco: {risco}")
            st.markdown("### 🧠 Análise da IA")
            st.write(analise)
            st.caption(f"Atualizado em {atualizado_em}")

    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
