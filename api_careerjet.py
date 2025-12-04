import requests
from typing import List, Dict

API_KEY = ""
HOSTNAME = 'search.api.careerjet.net'
PATH = '/v4/query'

def obter_ip_real() -> str:
    """Função para obter o IP público real da máquina"""
    try:
        response = requests.get('https://httpbin.org/ip', timeout=3)
        return response.json()['origin']
    except:
        # Coloque aqui seu IP autorizado como fallback
        return '186.223.122.151'

def buscar_vagas_careerjet(keywords: str, location: str = "Brasil", page: int = 1) -> List[Dict]:
    user_ip = obter_ip_real()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    referer = 'https://app-vagas-jm4srwhjksqb36gpfvkb2j.streamlit.app/find-jobs/'

    params = {
        'locale_code': 'pt_BR',
        'keywords': keywords,
        'location': location if location else 'Brasil',
        'page': page,
        'user_ip': user_ip,
        'user_agent': user_agent,
    }

    headers = {
        'content-type': 'application/json',
        'Referer': referer,
    }

    try:
        response = requests.get(
            url=f'https://{HOSTNAME}{PATH}',
            params=params,
            auth=(API_KEY, ''),  # Basic Auth com API Key como usuário e senha vazia
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if data.get('jobs'):
            return formatar_vagas_careerjet(data['jobs'])
        else:
            return []
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP Careerjet: {e.response.status_code} - {e.response.text}")
        return []
    except Exception as e:
        print(f"Erro na API Careerjet: {e}")
        return []

def formatar_vagas_careerjet(jobs_raw: List[Dict]) -> List[Dict]:
    vagas_formatadas = []

    for job in jobs_raw:
        vaga = {
            'title': job.get('title', 'Título não disponível'),
            'company': job.get('company_name', job.get('company', 'Empresa não informada')),
            'location': job.get('location', ', '.join(job.get('locations', []))),
            'snippet': job.get('description', ''),
            'link': job.get('url', ''),
            'type': job.get('job_type', ''),
            'source': 'Careerjet',
            'url': job.get('url', '')
        }
        vagas_formatadas.append(vaga)

    return vagas_formatadas

# descontinuada por enquanto