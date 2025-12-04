import streamlit as st
import requests

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

if st.button('Pesquisar'):
    st.write('Pesquisando...')
    st.write(texto)
    st.write(tipo)
    st.write(estado)
    st.write(data_inicial)    
    st.write(data_final)    