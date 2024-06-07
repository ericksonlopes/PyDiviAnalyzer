import concurrent.futures
import io

import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt

from config import Logger
from py_invest_analyser.models import RealEstateFundsModel, StockModel
from py_invest_analyser.scrapers import ExtractInfoFromREF, ExtractInfoFromStock


def minha_analise():
    def generate_data_fiis(actives):
        result_actives = []

        logger = Logger().logger

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(ExtractInfoFromREF().get_info_active, active) for active in actives]

            for future in concurrent.futures.as_completed(futures):

                try:
                    active = future.result()

                    if isinstance(active, str):
                        active = ExtractInfoFromREF().get_active_keys_indicators(active)

                    result_actives.append(active)
                except Exception as e:
                    logger.error(f"Error to get information for active {active.name}")
                    logger.error(e)

        return pd.DataFrame(result_actives)

    def generate_data_stock(actives):
        result_actives = []

        logger = Logger().logger

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(ExtractInfoFromStock().get_info_active, active) for active in actives]

            for future in concurrent.futures.as_completed(futures):

                try:
                    active = future.result()

                    if isinstance(active, str):
                        active = ExtractInfoFromStock().get_active_keys_indicators(active)

                    result_actives.append(active)
                except Exception as e:
                    logger.error(f"Error to get information for active {active.name}")
                    logger.error(e)

        return pd.DataFrame(result_actives)

    data = st.file_uploader('Escolha o arquivo para analise de dados', type=['csv'])

    if data is None:
        st.warning(
            """
            Por favor, escolha um arquivo para analise de dados."):
            """)
        st.stop()

    content = data.read().decode('latin-1')
    content_lines = content.split('\n')
    content_without_first_line = '\n'.join(content_lines[1:])

    df = pd.read_csv(io.StringIO(content_without_first_line), sep=';')

    with st.expander("Visualizar dados brutos"):
        st.dataframe(df)

    st.title('Fundos Imobiliários')

    df = df[['TIPO DE INVESTIMENTO', 'DESCRIÇÃO', 'VALOR BRUTO', "QUANTIDADE"]]

    fiis = df[df['TIPO DE INVESTIMENTO'] == 'FII'].copy()

    with st.spinner('Loading...'):
        df_infos_fiis = generate_data_fiis(fiis['DESCRIÇÃO'].unique())

    df_infos_fiis.columns = RealEstateFundsModel.get_meaning_of_fields().values()

    with st.expander("Visualizar dados brutos"):
        st.dataframe(df_infos_fiis)

    df_infos_fiis = df_infos_fiis[
        ["Nome", "Cotação", "Dividend Yield", "P/VP", "VAL. PATRIMONIAL P/ COTA", 'SEGMENTO', "Valorização",
         "ÚLTIMO RENDIMENTO"]]

    fiis["ULT. RENDIMENTO"] = fiis["DESCRIÇÃO"].map(df_infos_fiis.set_index("Nome")["ÚLTIMO RENDIMENTO"])
    fiis['VALORIZAÇÃO'] = fiis["DESCRIÇÃO"].map(df_infos_fiis.set_index("Nome")["Valorização"])
    fiis["SEGMENTO"] = fiis["DESCRIÇÃO"].map(df_infos_fiis.set_index("Nome")["SEGMENTO"])
    fiis["COTAÇÃO"] = fiis["DESCRIÇÃO"].map(df_infos_fiis.set_index("Nome")["Cotação"])
    fiis["P/VP"] = fiis["DESCRIÇÃO"].map(df_infos_fiis.set_index("Nome")["P/VP"])
    fiis["DIVIDEND YIELD"] = fiis["DESCRIÇÃO"].map(df_infos_fiis.set_index("Nome")["Dividend Yield"])

    fiis["P/VP"] = fiis["P/VP"].str.replace(',', '.')
    fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].str.replace('.', '')
    fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].str.replace('R$ ', '')
    fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].str.replace(',', '.')
    fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].astype(float)

    fiis["COTAÇÃO"] = fiis["COTAÇÃO"].str.replace(',', '.')
    fiis["COTAÇÃO"] = fiis["COTAÇÃO"].str.replace('R$ ', '')
    fiis['COTAÇÃO'] = fiis['COTAÇÃO'].astype(float)

    fiis["VALORIZAÇÃO"] = fiis["VALORIZAÇÃO"].str.replace(',', '.')
    fiis["VALORIZAÇÃO"] = fiis["VALORIZAÇÃO"].str.replace('-', "0")
    fiis["VALORIZAÇÃO"] = fiis["VALORIZAÇÃO"].str.replace('%', '')
    fiis["VALORIZAÇÃO"] = fiis["VALORIZAÇÃO"].astype(float)

    fiis['QUANTIDADE'] = fiis['QUANTIDADE'].str.replace(',0', '')
    fiis['QUANTIDADE'] = fiis['QUANTIDADE'].astype(int)

    fiis["DIVIDEND YIELD"] = fiis["DIVIDEND YIELD"].str.replace(',', '.')
    fiis["DIVIDEND YIELD"] = fiis["DIVIDEND YIELD"].str.replace('%', '')
    fiis["DIVIDEND YIELD"] = fiis["DIVIDEND YIELD"].astype(float)

    fiis['ULT. RENDIMENTO'] = fiis['ULT. RENDIMENTO'].str.replace('.', '')
    fiis['ULT. RENDIMENTO'] = fiis['ULT. RENDIMENTO'].str.replace('R$ ', '')
    fiis['ULT. RENDIMENTO'] = fiis['ULT. RENDIMENTO'].str.replace(',', '.')
    fiis['ULT. RENDIMENTO'] = fiis['ULT. RENDIMENTO'].astype(float)

    fiis.drop(columns=['TIPO DE INVESTIMENTO'], inplace=True)

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Total de Investimento", value=f"R$ {fiis['VALOR BRUTO'].sum():,.2f}")

    with col2:
        total_rendimento = fiis['ULT. RENDIMENTO'] * fiis['QUANTIDADE']
        st.metric(label="Total de Rendimento(último mês)", value=f"R$ {total_rendimento.sum():,.2f}")

    with col3:
        porcentagem_mes = (total_rendimento.sum() / fiis['VALOR BRUTO'].sum()) * 100
        st.metric(label=f"Rendimento Mensal(%)", value=f"{porcentagem_mes:,.2f}%")

    with col4:
        maior = fiis['VALOR BRUTO'].values.max()
        nome = fiis[fiis['VALOR BRUTO'] == maior]['DESCRIÇÃO'].values[0]

        st.metric(label=f"Maior posição ({nome})", value=f"R$ {maior:,.2f}")

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        media_dividend_yield = fiis['DIVIDEND YIELD'].mean()
        st.metric(label=f"Dividend Yield Médio (12M)", value=f"{media_dividend_yield:,.2f}%")

    with col6:
        media_valorizacao = fiis['VALORIZAÇÃO'].mean()
        st.metric(label=f"Valorização Média (12M)", value=f"{media_valorizacao:,.2f}%")

    with col7:
        st.metric(label="P/VP Médio", value=f"{fiis['P/VP'].astype(float).mean():,.2f}")

    with col8:
        st.metric(label="Total de Ativos", value=f"{len(fiis)}")

    def bigger_than_pvp(value):
        if float(value) < 1.0:
            return 'background-color: green'

        if float(value) > 1.0:
            return 'background-color: Firebrick'

    def bigger_than_val(value):
        if float(value) > 0:
            return 'background-color: green'

        if float(value) < 0:
            return 'background-color: Firebrick'

    styled_df_fiis = fiis.style
    styled_df_fiis = styled_df_fiis.format({
        'VALOR BRUTO': 'R${:,.2f}',
        'VALORIZAÇÃO': '{:.2f}%',
        'COTAÇÃO': 'R$ {:,.2f}',
        'DIVIDEND YIELD': '{:.2f}%',
        'ULT. RENDIMENTO': 'R$ {:,.2f}',
    })

    styled_df_fiis = styled_df_fiis.map(bigger_than_pvp, subset=['P/VP'])
    styled_df_fiis = styled_df_fiis.map(bigger_than_val, subset=['VALORIZAÇÃO'])

    st.dataframe(styled_df_fiis, use_container_width=True)

    st.title('Gráficos Por:')

    col1, col2, col3 = st.columns(3)

    # Tamanho fixo para as figuras
    fig_width = 300
    fig_height = 300

    with col1:
        fig1, ax1 = plt.subplots(figsize=(fig_width / 100, 370 / 100))
        # fig1, ax1 = plt.subplots(figsize=(fig_width / 100, fig_height - 30 / 100))
        ax1.pie(fiis['VALOR BRUTO'], labels=fiis['DESCRIÇÃO'], autopct='%1.1f%%')
        ax1.axis('equal')
        st.pyplot(fig1)

    with col2:
        segmentos = fiis.groupby('SEGMENTO').sum().reset_index()
        segmentos.sort_values(by=['VALOR BRUTO'], inplace=True, ascending=False)

        fig2, ax2 = plt.subplots(figsize=(fig_width / 100, fig_height / 60.5))
        ax2.pie(segmentos["VALOR BRUTO"], labels=segmentos["SEGMENTO"], autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)

    with col3:
        seg_valor = fiis.groupby('SEGMENTO').sum().reset_index().sort_values(by=['VALOR BRUTO'], ascending=False)
        st.dataframe(seg_valor[["SEGMENTO", "VALOR BRUTO"]], use_container_width=True)

    st.title('Ações')

    # filtrando apenas ações
    acao = df[df['TIPO DE INVESTIMENTO'] == 'Ação'].copy()

    with st.spinner('Loading...'):
        df_infos_acao = generate_data_stock(acao['DESCRIÇÃO'].unique())

    # dropando colunas que não serão utilizadas
    df_infos_acao = df_infos_acao.drop(columns=["p_vp", "dividend_yield_stock"])

    # renomeando colunas
    df_infos_acao.columns = StockModel.get_meaning_of_fields().values()

    with st.expander("Visualizar dados brutos"):
        st.dataframe(df_infos_acao, use_container_width=True)

    # reordenando colunas
    df_infos_acao = df_infos_acao[["Nome", "Cotação", "Dividend Yield", "P/VP", "Valorização"]]

    # dropando colunas que não serão utilizadas
    acao.drop(columns=['TIPO DE INVESTIMENTO'], inplace=True)

    # adicionando colunas com informações das ações
    acao['VALORIZAÇÃO'] = acao["DESCRIÇÃO"].map(df_infos_acao.set_index("Nome")["Valorização"])
    acao["COTAÇÃO"] = acao["DESCRIÇÃO"].map(df_infos_acao.set_index("Nome")["Cotação"])
    acao["P/VP"] = acao["DESCRIÇÃO"].map(df_infos_acao.set_index("Nome")["P/VP"])
    acao["DIVIDEND YIELD"] = acao["DESCRIÇÃO"].map(df_infos_acao.set_index("Nome")["Dividend Yield"])

    # formatando colunas
    acao["P/VP"] = acao["P/VP"].str.replace(',', '.')
    acao['VALOR BRUTO'] = acao['VALOR BRUTO'].str.replace('.', '')
    acao['VALOR BRUTO'] = acao['VALOR BRUTO'].str.replace('R$ ', '')
    acao['VALOR BRUTO'] = acao['VALOR BRUTO'].str.replace(',', '.')
    acao['VALOR BRUTO'] = acao['VALOR BRUTO'].astype(float)

    acao["COTAÇÃO"] = acao["COTAÇÃO"].str.replace(',', '.')
    acao["COTAÇÃO"] = acao["COTAÇÃO"].str.replace('R$ ', '')
    acao['COTAÇÃO'] = acao['COTAÇÃO'].astype(float)

    acao["VALORIZAÇÃO"] = acao["VALORIZAÇÃO"].str.replace(',', '.')
    acao["VALORIZAÇÃO"] = acao["VALORIZAÇÃO"].str.replace('%', '')
    acao["VALORIZAÇÃO"] = acao["VALORIZAÇÃO"].astype(float)

    acao['QUANTIDADE'] = acao['QUANTIDADE'].str.replace(',0', '')
    acao['QUANTIDADE'] = acao['QUANTIDADE'].astype(int)

    # acao["DIVIDEND YIELD"] = acao["DIVIDEND YIELD"].str.replace(',', '.')
    # acao["DIVIDEND YIELD"] = acao["DIVIDEND YIELD"].str.replace('%', '')
    # acao["DIVIDEND YIELD"] = acao["DIVIDEND YIELD"].str.replace('-', None)
    # acao["DIVIDEND YIELD"] = acao["DIVIDEND YIELD"].astype(float)

    # aplicando formatação
    styled_df_acao = acao.style
    styled_df_acao = styled_df_acao.format({
        'VALOR BRUTO': 'R${:,.2f}',
        'VALORIZAÇÃO': '{:.2f}%',
        'COTAÇÃO': 'R$ {:,.2f}',
        # 'DIVIDEND YIELD': '{:.2f}%'
    })

    styled_df_acao = styled_df_acao.map(bigger_than_pvp, subset=['P/VP'])
    styled_df_acao = styled_df_acao.map(bigger_than_val, subset=['VALORIZAÇÃO'])

    st.dataframe(styled_df_acao, use_container_width=True)
