import requests 
import time
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
dados_filtrados['Data da Compra'] = pd.to_datetime(dados_filtrados['Data da Compra'], format='%d/%m/%Y')


#4. DATA VISUALIZATION
@st.cache_data
def convert_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def success_message():
    success = st.success('File downloaded successfully.')
    time.sleep(5)
    success.empty()

st.title(":blue[Sales Dashboard] :dart", help="This is the main title")
st.write("This is a demo dashboard for book sales around Brazilian territory.")


with st.expander('Colunas'):
    colunas = st.multiselect('Select Columns', list(dados_filtrados.columns), list(dados_filtrados.columns))

st.sidebar.title('Filters')    
with st.sidebar.expander('Product Name'):
    produtos = st.multiselect('Products:', dados_filtrados['Produto'].unique(),  dados_filtrados['Produto'].unique())

with st.sidebar.expander('Product Category'):
    produtos_category = st.multiselect('Products:', dados_filtrados['Categoria do Produto'].unique(),  dados_filtrados['Categoria do Produto'].unique())

with st.sidebar.expander('Product Price'):
    preco = st.slider('Select Price:', 0, 5000, (0, 5000))

with st.sidebar.expander('Delivery Price'):
    delivery_preco = st.slider('Select Delivery Price:', 0, 5000, (0, 5000))    

with st.sidebar.expander('Date'):
    data_da_compra = st.date_input('Select date:', (dados_filtrados['Data da Compra'].min(), dados_filtrados['Data da Compra'].max()))

with st.sidebar.expander('Salesperson'):
    salesperson = st.multiselect('Salesperson:', dados_filtrados['Vendedor'].unique(),  dados_filtrados['Vendedor'].unique())

with st.sidebar.expander('State'):
    state = st.multiselect('State:', dados_filtrados['Local da compra'].unique(),  dados_filtrados['Local da compra'].unique())  

with st.sidebar.expander('Rate'):
    rate = st.slider('Select Product Rate:', 0, 5, (0, 5))

with st.sidebar.expander('Payment Type'):
    payment_type = st.multiselect('Payment Type:', dados_filtrados['Tipo de pagamento'].unique(),  dados_filtrados['Tipo de pagamento'].unique()) 

with st.sidebar.expander('Shares'):
    shares = st.slider('Select shares:', 0, 20, (0, 20))
  

query = '''
Produto in @produtos and \
`Categoria do Produto` in @produtos_category and \
@preco[0] <= Preço <= @preco[1] and \
@delivery_preco[0] <= Frete <= @delivery_preco[1] and \
@data_da_compra[0] <= `Data da Compra` <= @data_da_compra[1] and \
Vendedor in @salesperson and \
`Local da compra` in @state and \
@rate[0]<= `Avaliação da compra` <= @rate[1] and \
`Tipo de pagamento` in @payment_type and \
@shares[0] <= `Quantidade de parcelas` <= @shares[1]
'''

dados_filtrados = dados_filtrados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados, use_container_width=True)
st.markdown(f'The table has :blue[{dados_filtrados.shape[0]}] lines and :blue[{dados_filtrados.shape[1]}] columns.')
st.markdown('Write filename:')
col1, col2 = st.columns(2)

with col1: 
    nome_arquivo = st.text_input('', label_visibility='collapsed', value='dados')
    nome_arquivo += '.csv'

with col2:
    st.download_button("Download Data", data=convert_csv(dados_filtrados), file_name=nome_arquivo, mime='text/csv', on_click=success_message)




    