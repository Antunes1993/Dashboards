import requests
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px

# 1. BASIC CONFIGS
st.set_page_config(layout='wide', page_title='SAP Consolidation Tool', page_icon="comos_logo.png")

# 2. TÍTULO E IMAGEM
col1, col2 = st.columns([8, 1])
with col1:
    st.title(":blue[SAP Consolidation Tool]")
#with col2:
    #st.image("arauco_logo.png", use_container_width=True)




uploaded_file = st.file_uploader("Selecione um arquivo .txt", type=["txt"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8', engine='python')
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, sep=';', encoding='latin-1', engine='python')

    st.header(":blue[Resultados]")

    # 4. FILTROS NO SIDEBAR
    st.sidebar.header("Filtros")

    colunas_filtro = [
        'Atributo_estrutura_SAP',
        'Atributo_BaseObject_AtivoPreenchido',
        'Local_Instalacao_Criado',
        'Ativo_Criado',
        'LinkObject_Criado',
        'Link_Realizado',
        'Status_Final'
    ]

    filtros = {}
    for col in colunas_filtro:
        if col in df.columns:
            valores_unicos = df[col].dropna().unique().tolist()
            filtros[col] = st.sidebar.multiselect(f"{col}:", sorted(valores_unicos))

    # 5. APLICAÇÃO DOS FILTROS
    for col, valores in filtros.items():
        if valores:
            df = df[df[col].isin(valores)]

    # 6. EXIBIÇÃO DO DATAFRAME
    dataframe_filtrado = df.query("Atributo_estrutura_SAP == True and Status_Final == 'NOK'")
    numero_inconsistencias = dataframe_filtrado.shape[0]
    numero_total = df.shape[0]
    numero_consistentes = numero_total - numero_inconsistencias

    if numero_inconsistencias > 0:
        st.write(f":red[Número de elementos inconsistentes: {numero_inconsistencias}]")
    else:
        st.write(f":green[Tudo certo! Nenhuma inconsistencia detectada.]")
    st.dataframe(df)

    dados_pizza = pd.DataFrame({
        'Status': ['Consistentes', 'Inconsistentes'],
        'Quantidade': [numero_consistentes, numero_inconsistencias]
    })

    fig = px.pie(
        dados_pizza,
        names='Status',
        values='Quantidade',
        title='Distribuição de Consistência dos Registros',
        hole=0.3
    )
    fig.update_traces(textinfo='percent+label')

    if numero_inconsistencias > 0:
        col1, col2, col3 = st.columns([5, 1,  4])
        with col1:
            st.header(":red[Inconsistencias detectadas:]")
            st.dataframe(dataframe_filtrado.iloc[:, :2])
        with col3:
            st.plotly_chart(fig, use_container_width=True)
    