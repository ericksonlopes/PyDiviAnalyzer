import streamlit as st

from py_invest_analyser.controllers.my_investment import minha_analise

st.set_page_config(page_title='PyInvestAnalyser', page_icon='📊', layout='wide')

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('PyInvestAnalyser')


def segunda_tela():
    st.title("Segunda Tela")
    st.write("Esta é a segunda tela.")


st.sidebar.title("Menu de Navegação")

opcao_selecionada = st.sidebar.radio("Selecione uma tela:", ["Tela Inicial", "Segunda Tela", "Terceira Tela"])

if opcao_selecionada == "Tela Inicial":
    minha_analise()
elif opcao_selecionada == "Segunda Tela":
    segunda_tela()
