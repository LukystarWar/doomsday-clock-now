import os
import requests

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

def obter_noticias_gnews() -> str:
    url = f"https://gnews.io/api/v4/top-headlines?lang=pt&max=5&topic=world&token={GNEWS_API_KEY}"

    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()

        artigos = dados.get("articles", [])
        if not artigos:
            return "- [Erro] Nenhuma notícia recebida da API GNews."

        noticias = [f"- {artigo.get('title', '').strip()}" for artigo in artigos]
        return "\n".join(noticias)

    except Exception as e:
        return f"- [Erro ao obter notícias: {e}]"
