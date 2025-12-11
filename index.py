import streamlit as st
import requests
from api_jooble import buscar_vagas
import re
from datetime import datetime

if 'buscar_ativo' not in st.session_state:
    st.session_state.buscar_ativo = False
if 'resultado_buscar' not in st.session_state:
    st.session_state.resultado_buscar = None
if 'search_text' not in st.session_state:
    st.session_state.search_text = ''
if 'search_city' not in st.session_state:
    st.session_state.search_city = ''
if 'search_data_inicial' not in st.session_state:
    st.session_state.search_data_inicial = None
if 'search_data_final' not in st.session_state:
    st.session_state.search_data_final = None

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

col1, col2 = st.columns([1,1])

with col1:
    if not st.session_state.buscar_ativo:
        if st.button('🔎 Pesquisar'):

            st.session_state.search_text = texto
            st.session_state.search_city = cidade
            st.session_state.search_data_inicial = data_inicial
            st.session_state.search_data_final = data_final

            st.session_state.buscar_ativo = True
            st.rerun()
    
with col2:
    
    if st.button('❌ Cancelar Busca'):
        st.session_state.buscar_ativo = False 
        st.session_state.resultado_buscar = None 
        st.rerun()


if st.session_state.buscar_ativo:
    
    texto_busca = st.session_state.search_text
    cidade_busca = st.session_state.search_city
    data_inicial_busca = st.session_state.search_data_inicial
    data_final_busca = st.session_state.search_data_final
    
    resultados = buscar_todas_vagas(texto_busca, cidade_busca)

    if cidade_busca:
        cidade_nome = cidade_busca.split(' - ')[0].lower()
        resultados['jobs'] = [
            cid for cid in resultados['jobs']
            if cidade_nome in cid.get('location', '').lower()
        ]
    
    if data_inicial_busca:
        resultados['jobs'] = [
            dta for dta in resultados['jobs']
            if datetime.fromisoformat (dta['updated']).date() >= data_inicial_busca
        ]
        
    if data_final_busca:
        resultados['jobs'] = [
            dtaf for dtaf in resultados['jobs']
            if datetime.fromisoformat (dtaf['updated']).date() <= data_final_busca
        ]
    
    if texto_busca:
        resultados['jobs'] = [
            tv for tv in resultados['jobs']
            if texto_busca.lower() in tv.get('title', '').lower()
        ]
        
    st.session_state.resultado_buscar = resultados
    st.session_state.buscar_ativo = False
    st.success("Busca concluída!")
    st.rerun()


if st.session_state.resultado_buscar and not st.session_state.buscar_ativo:
    
    resultados_a_exibir = st.session_state.resultado_buscar

    if not resultados_a_exibir['jobs']:
        st.warning("Nenhuma vaga encontrada com os critérios especificados.")
        
    for vaga in resultados_a_exibir['jobs']:
        with st.container():
            fonte = vaga.get('source') or 'Não Informado'
            st.markdown(f"**Fonte:** {fonte}")
            
            st.subheader(vaga['title'])
            
            empresa = vaga.get('company') or 'Não Informado'
            st.write(f"**Empresa:** {empresa}")
            
            localizacao = vaga.get('location') or 'Não Informado'
            st.write(f"**Localização:** {localizacao}")
            
            tipo_vaga = vaga.get('type') or 'Não Informado'
            st.write(f"**Tipo:** {tipo_vaga}")
            
            data_pura = datetime.fromisoformat(vaga['updated']).date()
            st.write(f"**Data:**", data_pura)

            descricao_limpa = re.sub('<[^<]+?>', '', vaga.get('snippet', 'Não Informado'))
            descricao_limpa = descricao_limpa.replace('&nbsp;', ' ')

            with st.expander('Ver descrição'):
                st.write(descricao_limpa)

            st.markdown("*Para ver a descrição completa, clique no botão abaixo*")

            st.link_button("Ver vaga", vaga.get('link', 'Não Informado'))
            st.divider()