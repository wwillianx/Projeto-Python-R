#TO DO  08/05
#1- Ler o arquivo em csv com pandas 
#2- Tratar esse dataframe 
#3- Dado preparado para analise
#4- Iniciar as analises


# Resolução do TO DO

#pip3 install rpy2
#pip3 install pandas

import pandas as pd
# 1- Ler o arquivo CSV com pandas
df_vgsales = pd.read_csv('vgsales.csv')

# 2- Tratar o dataframe
# Exemplo de tratamento:
# Preencher valores nulos (se houver) em colunas numéricas com 0
numeric_cols = df_vgsales.select_dtypes(include=['number']).columns
df_vgsales[numeric_cols] = df_vgsales[numeric_cols].fillna(0)

# Converter colunas categóricas para o tipo 'category' (opcional, para otimizar a memória)
categorical_cols = df_vgsales.select_dtypes(include=['object']).columns
df_vgsales[categorical_cols] = df_vgsales[categorical_cols].astype('category')

# 3- Dado preparado para análise
# O dataframe df_vgsales agora está pronto para análise.
# Você pode realizar diversas manipulações e análises exploratórias.
print("Dados preparados:")
print(df_vgsales.head()) # Exibe as primeiras linhas do dataframe
print(df_vgsales.info()) # Exibe informações sobre as colunas e tipos de dados

# 4- Iniciar as análises
# Exemplos de análises:

# a) Análise descritiva
print("\nAnálise Descritiva:")
print(df_vgsales.describe()) # Estatísticas descritivas das colunas numéricas

# b) Contagem de valores únicos em colunas categóricas
print("\nContagem de Valores Únicos:")
for col in categorical_cols:
    print(f"\nColuna: {col}")
    print(df_vgsales[col].value_counts())

# c) Agregação de dados
print("\nAgregação de Dados (Vendas por Gênero):")
print(df_vgsales.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False))

# Continuação com R (opcional, conforme o exemplo do código)
# Se você quiser continuar a análise com R:
from rpy2.robjects import pandas2ri, globalenv, r
from rpy2.robjects.packages import importr
pandas2ri.activate()
base = importr('base')
globalenv['df_vgsales'] = pandas2ri.py2rpy(df_vgsales)
r('print(head(df_vgsales))')