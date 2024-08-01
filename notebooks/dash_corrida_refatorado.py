import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
from upload import upload_csv_to_sqlite

# Função para carregar e processar os dados do banco de dados SQLite3
def carregar_dados(db_name, table_name):
    # Conecte-se ao banco de dados SQLite3
    conn = sqlite3.connect(db_name)
    
    # Leia os dados da tabela para um DataFrame do Pandas
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    
    # Feche a conexão com o banco de dados
    conn.close()
    
    # Realize as transformações necessárias
    df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d')  # Ajuste o formato de data conforme necessário
    df['quilometragem'] = df['quilometragem'].astype(float)
    df['dia_semana'] = df['data'].dt.day_name()
    
    return df

# Função para filtrar os dados ignorando valores 0
def filtrar_dados(df):
    return df[df['quilometragem'] > 0.0].copy()

# Função para calcular métricas e adicionar colunas ao DataFrame
def calcular_metricas(df):
    df['calorias_por_minuto'] = df['calorias'] / df['tempo_min']
    df['km_por_minuto'] = df['quilometragem'] / (df['tempo_min'] / 60)
    return df

# Função para calcular médias
def calcular_medias(df, df_filtrado):
    media_calorias_com_zeros = df['calorias'].mean()
    media_calorias_sem_zeros = df_filtrado['calorias'].mean()
    media_km = df_filtrado['quilometragem'].mean()
    media_cal = df_filtrado['calorias'].mean()
    media_calorias_por_minuto = df_filtrado['calorias_por_minuto'].mean()
    media_km_por_minuto = df_filtrado['km_por_minuto'].mean()
    return media_calorias_com_zeros, media_calorias_sem_zeros, media_km, media_cal, media_calorias_por_minuto, media_km_por_minuto

# Função para calcular médias por dia da semana
def calcular_medias_por_dia_semana(df_filtrado):
    df_semana_calorias = df_filtrado[['dia_semana', 'calorias_por_minuto']]
    media_calorias_por_dia_semana = df_semana_calorias.groupby('dia_semana')['calorias_por_minuto'].mean().sort_values(ascending=False)
    
    df_semana_km = df_filtrado[['dia_semana', 'km_por_minuto']]
    media_km_por_dia_semana = df_semana_km.groupby('dia_semana')['km_por_minuto'].mean().sort_values(ascending=False)
    
    return media_calorias_por_dia_semana, media_km_por_dia_semana

# Função para criar o gráfico
def criar_grafico(df, media_calorias_com_zeros, media_calorias_sem_zeros):
    plt.style.use('dark_background')
    plt.figure(figsize=(16, 8))

    # Plot das calorias por dia com cores condicionais
    colors = ['g' if calorias > media_calorias_sem_zeros else 'r' for calorias in df['calorias']]
    plt.plot(df['data'], df['calorias'], linestyle='-', color='white', label='Calorias')
    plt.scatter(df['data'], df['calorias'], color=colors, s=100)

    # Adição da linha da média de calorias desconsiderando valores zerados
    plt.axhline(y=media_calorias_sem_zeros, color='g', linestyle='--', label=f'Média de Calorias (sem zeros: {media_calorias_sem_zeros:.2f})')

    # Título e rótulos
    plt.title('Calorias por Dia com Médias', fontsize=16)
    plt.xlabel('Data', fontsize=14)
    plt.ylabel('Calorias', fontsize=14)

    # Rótulos dos pontos de dados
    for i, row in df.iterrows():
        plt.text(row['data'], row['calorias'] + 5, f"{row['calorias']}", ha='center', fontsize=10)

    # Legenda
    plt.legend()

    # Ajuste dos rótulos do eixo x para serem exibidos verticalmente
    plt.xticks(df['data'], df['data'].dt.strftime('%Y-%m-%d'), rotation=90, ha='right')

    # Exibição do gráfico
    plt.tight_layout()
    plt.show()

# Função principal para executar todo o fluxo
def main():
    # Caminho para o arquivo CSV e para o banco de dados SQLite3
    csv_file = "data/run_data.csv"
    db_name = 'data/runningDB.sqlite3'
    table_name = 'running_data'

    # Carregar os dados do CSV para o banco de dados
    upload_csv_to_sqlite(csv_file, db_name, table_name)

    # Carregar e processar dados do banco de dados
    df = carregar_dados(db_name, table_name)

    # Filtrar dados
    df_filtrado = filtrar_dados(df)

    # Calcular métricas
    df_filtrado = calcular_metricas(df_filtrado)

    # Calcular médias
    media_calorias_com_zeros, media_calorias_sem_zeros, media_km, media_cal, media_calorias_por_minuto, media_km_por_minuto = calcular_medias(df, df_filtrado)

    # Calcular médias por dia da semana
    media_calorias_por_dia_semana, media_km_por_dia_semana = calcular_medias_por_dia_semana(df_filtrado)

    # Exibir médias
    print(f'Média de Calorias (com zeros): {media_calorias_com_zeros:.2f}')
    print(f'Média de Calorias (sem zeros): {media_calorias_sem_zeros:.2f}')
    print(f'Média de Quilometragem: {media_km:.2f}')
    print(f'Média de Calorias: {media_cal:.2f}')
    print(f'Média de Calorias por Minuto: {media_calorias_por_minuto:.2f}')
    print(f'Média de Km por Minuto: {media_km_por_minuto:.2f}')
    print("\nMédia de Calorias por Minuto por Dia da Semana:")
    print(media_calorias_por_dia_semana)
    print("\nMédia de Km por Minuto por Dia da Semana:")
    print(media_km_por_dia_semana)

    # Criar gráfico
    criar_grafico(df, media_calorias_com_zeros, media_calorias_sem_zeros)

# Executar a função principal
if __name__ == "__main__":
    main()
