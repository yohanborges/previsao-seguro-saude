import streamlit as st
import pandas as pd
import joblib

# Configuração da página
st.set_page_config(page_title="Calculadora de Seguro de Saúde", page_icon="💰")

# Carregando o modelo
@st.cache_resource
def carregar_objetos():
    modelo = joblib.load('seguro_saude_modelo.pkl')
    colunas = joblib.load('colunas_seguro_saude.pkl')
    return modelo, colunas

modelo, colunas_do_modelo = carregar_objetos()

# Interface do site
st.title("🩺 Previsão de Custo de Seguro Saúde")
st.write("Preencha os dados abaixo para saber o valor estimado do seguro.")

# Colunas
idade = st.number_input("Idade", min_value=18, max_value=100, value=30)
imc = st.number_input("IMC (Ex: 25.5)", min_value=10.0, max_value=60.0, value=25.0)
filhos = st.selectbox("Quantidade de filhos", [0,1,2,3,4,5])
sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
fumante = st.radio("É fumante?", ["Sim", "Não"])
regiao = st.selectbox("Região", ["Northeast", "Northwest", "Southeast", "Southwest"])

# --- PROCESSAMENTO DE DADOS ---
if st.button("Calcular valor do seguro"):

    dados_entrada = pd.DataFrame(0, index=[0], columns=colunas_do_modelo)

    dados_entrada['age'] = idade
    dados_entrada['bmi'] = imc
    dados_entrada['children'] = filhos
    dados_entrada['sex'] = 1 if sexo == 'Masculino' else 0
    dados_entrada['smoker'] = 1 if fumante == 'Sim' else 0

    coluna_regiao = f"region_{regiao.lower()}"
    if coluna_regiao in dados_entrada.columns:
        dados_entrada[coluna_regiao] = 1

    resultado = modelo.predict(dados_entrada)[0]

    valor_formatado = f"R$ {resultado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    st.divider()
    st.write("O valor estimado é de:")
    st.header(f":green[{valor_formatado}]")
    st.balloons()
