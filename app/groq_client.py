import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def analisar_noticias(texto_noticias):
    prompt = f"""
Você é um analista do Relógio do Juízo Final. Abaixo estão manchetes de notícias altamente sensíveis e perigosas. Sua missão é calcular, com urgência e precisão, quanto tempo falta para a meia-noite — o ponto simbólico de colapso global.

📌 Critério de avaliação:
- Mísseis, guerra ou tensões nucleares → **perigo extremo**
- Use apenas **SEGUNDOS**
- Valor **não deve ultrapassar 120 segundos**

⏱️ Intervalos:
- 0 a 60 seg → Destruição iminente
- 61 a 120 seg → Perigo extremo

Formato obrigatório:
Tempo para a meia-noite: X segundos  
Nível de risco: [Estável | Aumentando | Perigo Iminente]  
Análise: [resumo técnico e direto]

Manchetes:
{texto_noticias}
"""



    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
    "model": "llama3-70b-8192",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.3,
    "top_p": 1.0,
    "max_tokens": 200
    }


    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    return data["choices"][0]["message"]["content"]
