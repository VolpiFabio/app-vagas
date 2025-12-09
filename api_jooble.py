import http.client
import json
import os
from dotenv import load_dotenv

load_dotenv()

def buscar_vagas(termo_busca, localizacao):
    host = 'br.jooble.org'
    key = os.getenv('jobble_api_key')
    connection = http.client.HTTPConnection(host)
    #request headers
    headers = {"Content-type": "application/json"}
    #json query
    body = f'{{"keywords": "{termo_busca}", "location": "{localizacao}" }}'
    connection.request('POST','/api/' + key, body, headers)
    response = connection.getresponse()
    dados = response.read()
    vagas = json.loads(dados)
    return vagas