import pandas as pd  # Importa o pandas para manipulação de dados

# Função para carregar o dataset e realizar a limpeza básica
def load_dataset(path='dados/vgsales.csv'):
    df = pd.read_csv(path)  # Lê o arquivo CSV
    df = df.dropna(subset=['Year', 'Global_Sales'])  # Remove linhas com valores ausentes em 'Year' e 'Global_Sales'
    df['Year'] = df['Year'].astype(int)  # Converte a coluna 'Year' para inteiro
    return df  # Retorna o dataframe limpo

# Função para salvar o dataset limpo em um novo arquivo
def save_clean_data(df, path='dados/clean_vgsales.csv'):
    df.to_csv(path, index=False)  # Salva o dataframe sem o índice como coluna

# Executa as funções apenas se o arquivo for executado diretamente
if __name__ == "__main__":
    df = load_dataset()  # Carrega e limpa os dados
    save_clean_data(df)  # Salva o resultado no caminho especificado
