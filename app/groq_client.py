import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def analisar_noticias(texto_noticias):
    prompt = f"""
Você é um analista do Relógio do Juízo Final. Abaixo estão manchetes de notícias sensíveis. Sua missão é analisar cada uma e estimar quanto tempo falta para a meia-noite (colapso global).

📌 Critério de avaliação:
- Guerra, tensões nucleares, conflitos extremos → mais perto da meia-noite
- Use apenas **SEGUNDOS**
- Valor **entre 0 e 120**

⏱️ Intervalos:
- 0 a 60 → Perigo Iminente
- 61 a 120 → Aumentando

🧠 Responda exclusivamente em JSON com o seguinte formato:

```json
[
  {{
    "manchete": "Título da notícia",
    "tempo_para_meianoite": 90,
    "nivel_de_risco": "Aumentando",
    "analise": "Breve análise da situação, de 1 a 3 linhas no máximo."
  }},
  {{
    "manchete": "...",
    "tempo_para_meianoite": ...,
    "nivel_de_risco": "...",
    "analise": "..."
  }}
]
```

🔒 NÃO EXPLIQUE NADA. Apenas retorne o JSON válido.

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
        "max_tokens": 512
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]

        # Valida se é JSON
        try:
            resultado = json.loads(content)
            if isinstance(resultado, list) and all("manchete" in item for item in resultado):
                return resultado
            else:
                raise ValueError("Formato inesperado no conteúdo da IA.")
        except json.JSONDecodeError:
            raise ValueError("Resposta da IA não é um JSON válido.")

    except Exception as e:
        print("Erro ao processar resposta da IA:", str(e))
        return [{
            "manchete": "Erro ao processar notícias",
            "tempo_para_meianoite": 999,
            "nivel_de_risco": "Indefinido",
            "analise": "A IA falhou ao interpretar as notícias. Tente novamente mais tarde."
        }]