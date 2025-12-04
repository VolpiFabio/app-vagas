import http.client
import json

def buscar_vagas(termo_busca, localizacao):
    host = 'br.jooble.org'
    key = '1f68e204-af0b-4c18-b9fd-ccdc663e3254'
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