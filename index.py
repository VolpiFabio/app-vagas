import streamlit as st
import requests
from api_jobble import buscar_vagas
from api_careerjet import buscar_vagas_careerjet
import re

@st.cache_data
def carregar_cidades():
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    response = requests.get(url)
    cidades = response.json()
    
    lista_cidades = []
    for c in cidades:
        try:
            cidade_uf = f"{c['nome']} - {c['microrregiao']['mesorregiao']['UF']['sigla']}"
            lista_cidades.append(cidade_uf)
        except:
            pass  # ignora se der erro
    
    return lista_cidades

def buscar_todas_vagas(texto, cidade):
    # Extrai só o nome da cidade para a Careerjet
    cidade_nome = cidade.split(' - ')[0] if cidade and ' - ' in cidade else cidade

    vagas_jobble = buscar_vagas(texto, cidade) if texto else {'jobs': []}
    vagas_careerjet = buscar_vagas_careerjet(texto, cidade_nome) if texto else []

    # Combina as listas e retorna no formato esperado pelo seu código
    todas_vagas = vagas_jobble.get('jobs', []) + vagas_careerjet    
    return {'jobs': todas_vagas}

st.title('Buscador de Vagas')

texto = st.text_input(
    label='Dgite a vaga a ser pesquisada'
)

st.sidebar.header('Filtros')

todas_cidades = carregar_cidades()

tipo = st.sidebar.selectbox(
    label='Tipo de vaga',
    options=['','Estagio', 'CLT', 'PJ', 'Temporario', 'Freelancer', 'Outros'],
    index=0
)

estado = st.sidebar.selectbox(
    label='Estado da vaga',
    options=['','Ativa', 'Finalizada'],
    index=0
)

cidade = st.sidebar.selectbox(
    label='Cidade',
    options=[''] + todas_cidades,
    index=0
)

data_inicial = st.sidebar.date_input(
    label='Data inicial',
    value=None,
    max_value=None,
    min_value=None,
    key=None
)

data_final = st.sidebar.date_input(
    label='Data final',
    value=None,
    max_value=None,
    min_value=None,
    key=None
)

if st.button('🔎 Pesquisar'):
    st.write('Pesquisando...')
    resultados = buscar_todas_vagas(texto, cidade)

    for vaga in resultados['jobs']:
        with st.container():
            st.subheader(vaga['title'])
            st.write(f"**Empresa:** {vaga['company']}")
            st.write(f"**Localização:** {vaga['location']}")
            st.write(f"**Tipo:** {vaga['type']}")

            descricao_limpa = re.sub('<[^<]+?>', '', vaga['snippet'])
            descricao_limpa = descricao_limpa.replace('&nbsp;', ' ')

            with st.expander('Ver descrição'):
                st.write(descricao_limpa)

            st.markdown("*Para ver a descrição completa, clique no botão abaixo*")

            st.link_button("Ver vaga", vaga['link'])
            st.divider()