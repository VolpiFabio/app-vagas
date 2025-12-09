import streamlit as st
import requests
from api_jooble import buscar_vagas
import re
from datetime import datetime

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
            pass  
    
    return lista_cidades

def buscar_todas_vagas(texto, cidade):
    
    vagas_jobble = buscar_vagas(texto, cidade) if texto else {'jobs': []}

    
    todas_vagas = vagas_jobble.get('jobs', [])    
    return {'jobs': todas_vagas}

st.title('Buscador de Vagas')

texto = st.text_input(
    label='Dgite a vaga a ser pesquisada'
)


st.sidebar.header('Filtros')

todas_cidades = carregar_cidades()

tipo = st.sidebar.selectbox(
    label='Tipo de vaga',
    options=['', 'Efetivo', 'Contrato', 'Temporário', 'Estágio', 'Tempo integral'],
    index=0
)

# estado = st.sidebar.selectbox(
#     label='Estado da vaga',
#     options=['','Ativa', 'Finalizada'],
#     index=0
# )

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
    
    if cidade:
        cidade_nome = cidade.split(' - ')[0].lower()
        resultados['jobs'] = [
            cid for cid in resultados['jobs']
            if cidade_nome in cid.get('location', '').lower()
        ]
    
    if data_inicial:
        resultados['jobs'] = [
            dta for dta in resultados['jobs']
            if datetime.fromisoformat (dta['updated']).date() >= data_inicial
        ]
        
    if data_final:
        resultados['jobs'] = [
            dtaf for dtaf in resultados['jobs']
            if datetime.fromisoformat (dtaf['updated']).date() <= data_final
        ]
    
    if tipo:
        resultados['jobs'] = [
            tv for tv in resultados['jobs']
            if tipo.lower() in tv.get('type', '').lower()
        ]

    for vaga in resultados['jobs']:
        with st.container():
            fonte = vaga.get('source', 'Desconhecida')
            st.markdown(f"**Fonte:** {fonte}")
            st.subheader(vaga['title'])
            st.write(f"**Empresa:** {vaga.get('company', 'Não Informado')}")
            st.write(f"**Localização:** {vaga.get('location', 'Não Informado')}")
            st.write(f"**Tipo:** {vaga.get('type', 'Não Informado')}")
            
            data_pura = datetime.fromisoformat(vaga['updated']).date()
            st.write(f"**Data:**", data_pura)

            descricao_limpa = re.sub('<[^<]+?>', '', vaga.get('snippet', 'Não Informado'))
            descricao_limpa = descricao_limpa.replace('&nbsp;', ' ')

            with st.expander('Ver descrição'):
                st.write(descricao_limpa)

            st.markdown("*Para ver a descrição completa, clique no botão abaixo*")

            st.link_button("Ver vaga", vaga.get('link', 'Não Informado'))
            st.divider()