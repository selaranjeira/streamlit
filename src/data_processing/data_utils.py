import pandas as pd
import sqlite3

def carregar_dados():
    conn = sqlite3.connect('../../data/runningDB.sqlite3')
    df = pd.read_sql_query("SELECT * FROM running_data", conn)
    conn.close()
    
    # tratamento
    df['data'] = pd.to_datetime(df['data'])
    df['quilometragem'] = df['quilometragem'].astype(float)
    
    # Calcular calorias por minuto e km por minuto
    df['calorias_por_minuto'] = df['calorias'] / df['tempo_min']
    df['km_por_minuto'] = df['quilometragem'] / df['tempo_min']
    df['dia_semana'] = df['data'].dt.day_name()
    
    return df


# def carregar_dados():
#     # Supondo que o arquivo CSV esteja na pasta 'data'
#     df = pd.read_csv('data/dados.csv', parse_dates=['data'])

#     # Converter a coluna 'data' para o tipo datetime
#     df['data'] = pd.to_datetime(df['data'])

#     # Adicionar coluna de dia da semana
#     df['dia_semana'] = df['data'].dt.day_name()

#     return df


def calcular_metricas(df):
    # Calcula as métricas desejadas
    media_calorias_com_zeros = df['calorias'].mean()
    media_calorias_sem_zeros = df[df['calorias'] > 0]['calorias'].mean()
    media_quilometragem = df['quilometragem'].mean()
    media_calorias_por_minuto = (df['calorias'] / df['tempo_min']).mean()
    media_km_por_minuto = (df['quilometragem'] / df['tempo_min']).mean()

    # Média por dia da semana
    media_calorias_por_dia_semana = df.groupby(df['data'].dt.day_name())['calorias'].mean().sort_index()
    media_km_por_dia_semana = df.groupby(df['data'].dt.day_name())['quilometragem'].mean().sort_index()

    # Retorna as métricas calculadas
    metricas = {
        'media_calorias_com_zeros': media_calorias_com_zeros,
        'media_calorias_sem_zeros': media_calorias_sem_zeros,
        'media_quilometragem': media_quilometragem,
        'media_calorias_por_minuto': media_calorias_por_minuto,
        'media_km_por_minuto': media_km_por_minuto,
        'media_calorias_por_dia_semana': media_calorias_por_dia_semana,
        'media_km_por_dia_semana': media_km_por_dia_semana
    }

    return df, metricas
