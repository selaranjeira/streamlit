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
    criar_graficos_mensais_comparativos
)

def main():
    # Carregar os dados
    df = carregar_dados()

    with st.sidebar:
        st.subheader("Sérgio Laranjeira")
        logo_teste = Image.open("src/imagens/guerreiros.png")
        st.image(logo_teste)
    
    # Adicionar a seleção de meses com a opção 'Todos os Meses'
    meses = df['data'].dt.strftime('%Y-%m').unique()
    meses = sorted(list(meses))  # Garantir que os meses estejam ordenados
    meses = ['Todos os Meses'] + meses
    filtro_mes = st.sidebar.selectbox("Selecione o Mês", meses)

    # Filtrar os dados com base no mês selecionado
    if filtro_mes == 'Todos os Meses':
        df_filtrado = df
    else:
        df_filtrado = df[df['data'].dt.strftime('%Y-%m') == filtro_mes]

    # Calcular as médias e métricas
    media_calorias_com_zeros = df_filtrado['calorias'].mean()
    media_calorias_sem_zeros = df_filtrado[df_filtrado['calorias'] > 0]['calorias'].mean()
    media_km = df_filtrado['quilometragem'].mean()
    media_km_sem_zeros = df_filtrado[df_filtrado['quilometragem'] > 0]['quilometragem'].mean()
    media_calorias_por_minuto = df_filtrado['calorias_por_minuto'].mean()
    media_km_por_minuto = df_filtrado['km_por_minuto'].mean()

    # Calcular metas mensais
    calorias_mensais = calcular_calorias_mensais(df)
    quilometragem_mensal = calcular_km_mensais(df)

    # Exibir as métricas em 3 colunas na primeira e segunda linha
    st.write("### Métricas Calorias e KM")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Média de Calorias geral", f"{media_calorias_com_zeros:.2f}")
    with col2:
        st.metric("Média de Calorias dias úteis", f"{media_calorias_sem_zeros:.2f}")
    with col3:
        st.metric("Média de Calorias por Minuto", f"{media_calorias_por_minuto:.2f}")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Média km geral", f"{media_km:.2f}")
    with col5:
        st.metric("Média km útil", f"{media_km_sem_zeros:.2f}")
    with col6:
        st.metric("Média de Km por Minuto", f"{media_km_por_minuto:.2f}")

    # Exibir os gráficos de metas mensais
    st.write("### Metas Mensais")
    col7, col8 = st.columns(2)
    if filtro_mes == 'Todos os Meses':
        with col7:
            for fig in criar_graficos_mensais_comparativos(calorias_mensais, tipo='calorias'):
                st.plotly_chart(fig)
        with col8:
            for fig in criar_graficos_mensais_comparativos(quilometragem_mensal, tipo='quilometragem'):
                st.plotly_chart(fig)
    else:
        with col7:
            fig_calorias = criar_graficos_mensais_comparativos(calorias_mensais, tipo='calorias', filtro_mes=filtro_mes)
            if fig_calorias:
                st.plotly_chart(fig_calorias[0])
        with col8:
            fig_km = criar_graficos_mensais_comparativos(quilometragem_mensal, tipo='quilometragem', filtro_mes=filtro_mes)
            if fig_km:
                st.plotly_chart(fig_km[0])

    # Exibir os gráficos de barras horizontais
    st.write("### Gráficos por Dia da Semana")
    media_calorias_por_dia_semana = df_filtrado.groupby('dia_semana')['calorias_por_minuto'].mean().sort_values(ascending=False)
    media_km_por_dia_semana = df_filtrado.groupby('dia_semana')['km_por_minuto'].mean().sort_values(ascending=False)
    
    fig_calorias = criar_grafico_barra_horizontal(media_calorias_por_dia_semana, 'Média de Calorias por Minuto por Dia da Semana')
    fig_km = criar_grafico_barra_horizontal(media_km_por_dia_semana, 'Média de Km por Minuto por Dia da Semana')
    
    st.plotly_chart(fig_calorias)
    st.plotly_chart(fig_km)

    # Exibir o gráfico de linha
    st.write("### Evolução Diária de Calorias")
    fig_calorias = criar_grafico(df_filtrado, media_calorias_com_zeros, media_calorias_sem_zeros)
    st.plotly_chart(fig_calorias)

if __name__ == "__main__":
    main()
