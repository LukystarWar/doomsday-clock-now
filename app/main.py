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
# Botão de análise
if st.button("🔄 Atualizar relógio com base nas notícias"):
    try:
        resposta = analisar_noticias(noticias)  # Agora retorna uma lista de dicionários

        if not isinstance(resposta, list) or not resposta or "tempo_para_meianoite" not in resposta[0]:
            st.error("❌ A IA não respondeu no formato esperado. Tente novamente.")
            st.code(resposta)
        else:
            # Pegamos a análise mais crítica (menor tempo para meia-noite)
            analise_critica = min(resposta, key=lambda x: x["tempo_para_meianoite"])

            tempo_em_segundos = analise_critica["tempo_para_meianoite"]
            risco = analise_critica["nivel_de_risco"]
            analise_texto = analise_critica["analise"]

            atualizado_em = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            st.success(f"⏳ Tempo para a meia-noite: {tempo_em_segundos} segundos")
            st.info(f"🔴 Nível de risco: {risco}")
            st.markdown("### 🧠 Análise da IA")
            st.write(analise_texto)
            st.caption(f"Atualizado em {atualizado_em}")

            # Exibir todas as análises
            with st.expander("🔍 Ver todas as análises"):
                for item in resposta:
                    st.markdown(f"**📰 {item['manchete']}**")
                    st.markdown(f"- ⏱️ Tempo: **{item['tempo_para_meianoite']}s**")
                    st.markdown(f"- ⚠️ Risco: **{item['nivel_de_risco']}**")
                    st.markdown(f"- 🧠 Análise: {item['analise']}")
                    st.markdown("---")

    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")

