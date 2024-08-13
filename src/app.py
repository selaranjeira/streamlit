import streamlit as st
import pandas as pd
from PIL import Image
from data_processing.data_utils import carregar_dados
from visualization.plots import (
    criar_grafico,
    criar_grafico_barra_horizontal,
    criar_grafico_barras_verticais,
    calcular_calorias_mensais,
    calcular_km_mensais,
)

def main():
    # Carregar os dados
    df = carregar_dados()

    with st.sidebar:
        st.subheader("Sérgio Laranjeira")
        logo_teste = Image.open("src/imagens/guerreiros.png")
        st.image(logo_teste)

    # Filtros
    meses = df['data'].dt.strftime('%Y-%m').unique()
    meses = sorted(list(meses))
    meses = ['Todos os Meses'] + meses
    filtro_mes = st.sidebar.selectbox("Selecione o Mês", meses)

    semanas = df['data'].dt.strftime('%U-%Y').unique()
    filtro_semana = st.sidebar.selectbox("Selecione a Semana", ['Todas as Semanas'] + list(semanas))

    visao = st.sidebar.radio("Selecione a Visão", ["Visão KM", "Visão Calorias"])

    # Filtragem de dados
    if filtro_mes != 'Todos os Meses':
        df = df[df['data'].dt.strftime('%Y-%m') == filtro_mes]

    if filtro_semana != 'Todas as Semanas':
        df = df[df['data'].dt.strftime('%U-%Y') == filtro_semana]

    # Cálculo de dias úteis e ausentes
    dias_uteis = df[df['quilometragem'] > 0].shape[0]
    dias_ausentes = df[df['quilometragem'] == 0].shape[0]

    # Exibir os cards
    st.write("### Métricas Gerais")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Média de Calorias geral", f"{df['calorias'].mean():.2f}")
    with col2:
        st.metric("Média de Calorias dias úteis", f"{df[df['calorias'] > 0]['calorias'].mean():.2f}")
    with col3:
        st.metric("Média de Calorias por Minuto", f"{df['calorias_por_minuto'].mean():.2f}")
    with col4:
        st.metric("Dias Úteis", f"{dias_uteis}")
    with col5:
        st.metric("Dias Ausentes", f"{dias_ausentes}")

    # Gráficos
    if visao == "Visão KM":
        valores_corrente = df.groupby(df['data'].dt.to_period('M'))['quilometragem'].sum().iloc[-1]
        valores_anterior = df.groupby(df['data'].dt.to_period('M'))['quilometragem'].sum().iloc[-2]
        titulo_grafico = "Média de KM por Dia"
        
    else:
        valores_corrente = df.groupby(df['data'].dt.to_period('M'))['calorias'].sum().iloc[-1]
        valores_anterior = df.groupby(df['data'].dt.to_period('M'))['calorias'].sum().iloc[-2]
        titulo_grafico = "Média de Calorias por Dia"

    st.write("### Gráfico de Barras Verticais")
    st.plotly_chart(criar_grafico_barras_verticais(valores_corrente, valores_anterior, titulo_grafico))

    st.write("### Gráfico de Barras Horizontais")
    df_agrupado = df.groupby(df['data'].dt.dayofweek)['calorias'].sum() if visao == "Visão Calorias" else df.groupby(df['data'].dt.dayofweek)['quilometragem'].sum()
    st.plotly_chart(criar_grafico_barra_horizontal(df_agrupado, titulo_grafico))

    # Manter o gráfico de linha original
    st.write("### Evolução Diária de Calorias")
    fig_calorias = criar_grafico(df, df['calorias'].mean(), df[df['calorias'] > 0]['calorias'].mean())
    st.plotly_chart(fig_calorias)

if __name__ == "__main__":
    main()
