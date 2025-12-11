import requests
from dotenv import load_dotenv
import os

load_dotenv()

APP_ID = os.getenv("adzuna_id")
APP_KEY = os.getenv("adzuna_key")

def buscar_vagas_adzuna(termo=None, local=None, pagina=1, por_pagina=20):
    url = f'https://api.adzuna.com/v1/api/jobs/br/search/{pagina}'
    
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": por_pagina 
    }
    
    if termo:
        params["what"] = termo
    if local:
        params["where"] = local

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Erro {response.status_code}: {response.text}")

    return response.json()