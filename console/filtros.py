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