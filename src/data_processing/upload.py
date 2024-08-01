import sqlite3
import pandas as pd
import os

# Função para carregar o CSV e criar uma tabela no banco de dados SQLite3
def upload_csv_to_sqlite(csv_file, db_name, table_name):
    # Verificar se o arquivo CSV existe
    if not os.path.exists(csv_file):
        print(f"Erro: O arquivo CSV '{csv_file}' não existe.")
        return
    
    # Verificar se o diretório do banco de dados existe, se não, criar
    db_dir = os.path.dirname(db_name)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Conecte-se ao banco de dados SQLite3 (ou crie um novo banco de dados)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Leia o arquivo CSV usando o Pandas
    colnames = ['data', 'quilometragem', 'tempo_min', 'calorias']
    df = pd.read_csv(csv_file, names=colnames)
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%y')
    df['quilometragem'] = df['quilometragem'].astype(str).str.replace(',', '.').astype(float)
    df['dia_semana'] = df['data'].dt.day_name()
    
    # Carregue os dados do DataFrame no banco de dados SQLite3
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    # Feche a conexão com o banco de dados
    conn.close()
    print(f"Dados do arquivo {csv_file} foram carregados na tabela {table_name} do banco de dados {db_name} com sucesso.")

# Exemplo de uso
csv_file = "/home/selaranjeira/Desktop/loc_proj/desemp_esportivo/data/run_data.csv"
db_name = '/home/selaranjeira/Desktop/loc_proj/desemp_esportivo/data/runningDB.sqlite3'

table_name = 'running_data'

upload_csv_to_sqlite(csv_file, db_name, table_name)
