import streamlit as st
import pandas as pd
from data_processing.data_utils import carregar_dados
from visualization.plots import criar_grafico, criar_grafico_barra_horizontal

def criar_graficos_barras(df):
    # Gráfico de barras horizontais de calorias por minuto
    media_calorias_por_dia_semana = df.groupby('dia_semana')['calorias_por_minuto'].mean().sort_values(ascending=False)
    fig_calorias = criar_grafico_barra_horizontal(media_calorias_por_dia_semana, 'Média de Calorias por Minuto por Dia da Semana')
    
    # Gráfico de barras horizontais de km por minuto
    media_km_por_dia_semana = df.groupby('dia_semana')['km_por_minuto'].mean().sort_values(ascending=False)
    fig_km = criar_grafico_barra_horizontal(media_km_por_dia_semana, 'Média de Km por Minuto por Dia da Semana')

    return fig_calorias, fig_km

def main():
    # Carregar os dados
    df = carregar_dados()

    # Selecione o mês para filtrar
    meses = df['data'].dt.to_period('M').unique()
    meses = [period.strftime('%Y-%m') for period in meses]  # Formato 'YYYY-MM'
    meses.sort()
    
    # Adicionar uma opção para selecionar todos os meses
    meses = ['Todos os Meses'] + meses
    
    filtro_mes = st.sidebar.selectbox('Selecione o Mês', meses)

    if filtro_mes != 'Todos os Meses':
        periodo_selecionado = pd.Period(filtro_mes, freq='M')
        df = df[df['data'].dt.to_period('M') == periodo_selecionado]

    # Calcular as médias e métricas
    media_calorias_com_zeros = df['calorias'].mean()
    media_calorias_sem_zeros = df[df['calorias'] > 0]['calorias'].mean()
    media_km = df['quilometragem'].mean()
    media_calorias_por_minuto = df['calorias_por_minuto'].mean()
    media_km_por_minuto = df['km_por_minuto'].mean()

    # Criar gráficos de barras horizontais
    fig_calorias, fig_km = criar_graficos_barras(df)

    # Layout da página
    st.write("### Médias")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Média de Calorias (com zeros)", f"{media_calorias_com_zeros:.2f}")
    with col2:
        st.metric("Média de Calorias (sem zeros)", f"{media_calorias_sem_zeros:.2f}")
    with col3:
        st.metric("Média de Quilometragem", f"{media_km:.2f}")

    # Segunda linha para os outros cards
    st.write("### Outras Médias")
    col4, col5 = st.columns(2)
    with col4:
        st.metric("Média de Calorias por Minuto", f"{media_calorias_por_minuto:.2f}")
    with col5:
        st.metric("Média de Km por Minuto", f"{media_km_por_minuto:.2f}")

    # Gráficos de barras horizontais
    st.write("### Gráficos de Barras Horizontais")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_calorias, use_container_width=True)
    with col2:
        st.plotly_chart(fig_km, use_container_width=True)

    # Gráfico de linha
    st.write("### Gráfico de Calorias por Dia")
    fig_linha = criar_grafico(df, media_calorias_com_zeros, media_calorias_sem_zeros)
    st.plotly_chart(fig_linha, use_container_width=True)

if __name__ == "__main__":
    main()
