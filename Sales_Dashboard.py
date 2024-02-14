import requests 
import numpy as np 
import pandas as pd 
import seaborn as sns 
import streamlit as st 
import plotly.express as px 

#1. BASIC CONFIGS
st.set_page_config(layout='wide', page_title='Sales Dashboard', page_icon="C:\\Users\\z004s8rp\\Desktop\\sales.png")


#2. GATHERING DATA
url='https://labdados.com/produtos'
regioes = ['Brasil', 'Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']
response= requests.get(url)
data = pd.DataFrame.from_dict(response.json())


#3. DATA PROCESSING 
str_filter = 'livros'
dados_filtrados = data[data['Categoria do Produto'] == str_filter]

### Sales per State
dados_filtrados_por_estado = dados_filtrados.groupby('Local da compra')[['Preço']].sum()
dados_filtrados_latitude_logitude = dados_filtrados.groupby('Local da compra')[['lat','lon']].first()
dados_filtrados_por_estado = pd.concat([dados_filtrados_por_estado, dados_filtrados_latitude_logitude], axis=1)
dados_filtrados_por_estado = dados_filtrados_por_estado.sort_values('Preço', ascending=False)

fig_receita_por_estados = px.bar(dados_filtrados_por_estado['Preço'],
                                text_auto=True,
                                title='Top Estados')
fig_mapa_receita_por_estados = px.scatter_geo(dados_filtrados_por_estado,
                                                lat='lat',
                                                lon='lon',
                                                size='Preço',
                                                scope='south america')


### Sales per Salesperson
dados_filtrados_por_vendedores = dados_filtrados.groupby('Vendedor')[['Preço']].sum() 
dados_filtrados_por_vendedores_count = dados_filtrados.groupby('Vendedor')[['Preço']].count() 


#4. DATA VISUALIZATION
st.title(":blue[Sales Dashboard] :dart", help="This is a infotip.")
st.write("This is a demo dashboard for book sales around Brazilian territory.")
aba1, aba2 = st.tabs(['Revenue', 'Sales staff'])

with aba1:

    st.write("Revenue of book sales per state.")
    col1, col2, col3 = st.columns([1,4,1])
    col1.dataframe(dados_filtrados_por_estado['Preço'], use_container_width=True)
    col2.plotly_chart(fig_receita_por_estados, use_container_width=True)
    col3.plotly_chart(fig_mapa_receita_por_estados, use_container_width=True)

with aba2:    
    #st.dataframe(dados_filtrados, use_container_width=True)
    qtd_vendedores = st.number_input("Sales Staff", 2, 10, 5)
    fig_receita_por_vendedores = px.bar(dados_filtrados_por_vendedores['Preço'].sort_values(ascending=False).head(qtd_vendedores),
                                    text_auto=True,
                                    title='Top Sales per Revenue',
                                    orientation='h')

    fig_receita_por_vendedores_count = px.bar(dados_filtrados_por_vendedores_count['Preço'].sort_values(ascending=False).head(qtd_vendedores),
                                    text_auto=True,
                                    title='Top Sales per Amount of Sales',
                                    orientation='h')

    st.write("Revenue of book sales per salesperson.")
    col1, col2, col3 = st.columns([2,4,4])
    col1.dataframe(dados_filtrados_por_vendedores['Preço'].sort_values(ascending=False), use_container_width=True)    
    col2.plotly_chart(fig_receita_por_vendedores, use_container_width=True)
    col3.plotly_chart(fig_receita_por_vendedores_count, use_container_width=True)


    