import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
NOTICIAS_PATH = os.path.join(DATA_DIR, "noticias.txt")
DATA_FILE_PATH = os.path.join(DATA_DIR, "ultima_atualizacao.txt")

def atualizar_noticias_diariamente(noticias_texto):
    hoje = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
            ultima_data = f.read().strip()
        if ultima_data == hoje:
            return False  # Já atualizado hoje

    if noticias_texto != "forcar_verificacao":
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(NOTICIAS_PATH, "w", encoding="utf-8") as f:
            f.write(noticias_texto)
        with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(hoje)

    return True
