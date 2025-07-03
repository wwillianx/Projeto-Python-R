# Importa a biblioteca pandas, usada para manipulação de dados em tabelas (DataFrames)
import pandas as pd

# Função para carregar os dados do arquivo CSV
def load_data(path='dados/vgsales.csv'):
    df = pd.read_csv(path)  # Lê o arquivo CSV e armazena em um DataFrame
    df = df.dropna(subset=['Year', 'Global_Sales'])  # Remove registros onde o ano ou as vendas globais estão ausentes
    df['Year'] = df['Year'].astype(int)  # Converte a coluna 'Year' para inteiro
    return df  # Retorna o DataFrame limpo

# Função para formatar os valores de vendas globais com texto e duas casas decimais
def formatar_vendas_milhoes(df):
    df['Global_Sales'] = df['Global_Sales'].round(2).astype(str) + " milhões"
    return df  # Retorna o DataFrame com os valores formatados

# Função que mostra o Top 10 de jogos mais vendidos, agrupando por nome (independente da plataforma)
def top10_global_by_name(df):
    grouped = df.groupby("Name")["Global_Sales"].sum().reset_index()  # Agrupa por nome do jogo e soma as vendas globais
    grouped = grouped.sort_values(by="Global_Sales", ascending=False).head(10)  # Ordena em ordem decrescente e pega os 10 primeiros
    grouped = formatar_vendas_milhoes(grouped)  # Formata os valores de vendas
    print("\n🎮 Top 10 jogos mais vendidos (unificando plataformas):\n")
    print(grouped.to_string(index=False))  # Exibe o DataFrame formatado, sem o índice

# Função que permite comparar dois jogos com base nas vendas globais
def comparar_dois_jogos(df):

    # Verifica se o DataFrame está vazio ou nulo
    if df is None or df.empty:
        print("O DataFrame está vazio. Não é possível realizar a comparação.")
        return

    print("\n" + "="*50)
    print("         🎮 Comparador Interativo de Jogos 🎮")
    print("="*50)

    try:
        # Loop até encontrar um nome válido para o primeiro jogo
        while True:
            game1_name = input("\n➡️  Digite o nome do primeiro jogo: ")
            # Procura o jogo (sem diferenciar maiúsculas e minúsculas)
            game1_data = df[df['Name'].str.contains(game1_name, case=False, na=False)]
            if not game1_data.empty:
                break  # Sai do loop se encontrou
            print(f"❌ Jogo '{game1_name}' não encontrado. Por favor, tente novamente.")

        # Mesmo processo para o segundo jogo
        while True:
            game2_name = input("➡️  Digite o nome do segundo jogo: ")
            game2_data = df[df['Name'].str.contains(game2_name, case=False, na=False)]
            if not game2_data.empty:
                break
            print(f"❌ Jogo '{game2_name}' não encontrado. Por favor, tente novamente.")

        # Captura os nomes exatos para exibição
        display_name1 = game1_data['Name'].iloc[0]
        display_name2 = game2_data['Name'].iloc[0]

        print("\n" + "-"*50)
        print(f"📊 Comparando '{display_name1}' vs '{display_name2}'")
        print("-" * 50)

        # Exibe os dados do primeiro jogo
        print(f"\n✅ Informações para: {display_name1}")
        print(game1_data.to_string(index=False))

        # Exibe os dados do segundo jogo
        print(f"\n✅ Informações para: {display_name2}")
        print(game2_data.to_string(index=False))

        # Soma total de vendas globais de cada jogo
        game1_total_sales = game1_data['Global_Sales'].sum()
        game2_total_sales = game2_data['Global_Sales'].sum()

        print("\n" + "="*50)
        print("            🏆 Resumo da Comparação 🏆")
        print("="*50)
        print("\n📈 Vendas Globais Consolidadas (somando todas as plataformas):")
        print(f"  - {display_name1}: {game1_total_sales:.2f} milhões")
        print(f"  - {display_name2}: {game2_total_sales:.2f} milhões")

        # Compara as vendas e mostra quem vendeu mais
        diff = abs(game1_total_sales - game2_total_sales)
        if game1_total_sales > game2_total_sales:
            print(f"\n🎉 '{display_name1}' vendeu {diff:.2f} milhões de cópias a mais globalmente.")
        elif game2_total_sales > game1_total_sales:
            print(f"\n🎉 '{display_name2}' vendeu {diff:.2f} milhões de cópias a mais globalmente.")
        else:
            print("\n⚖️ Ambos os jogos tiveram um total de vendas globais idêntico!")
        print("\n" + "="*50)

    except Exception as e:
        # Caso aconteça algum erro inesperado
        print(f"Ocorreu um erro inesperado durante a comparação: {e}")

# Bloco principal: executado quando o script é rodado diretamente
if __name__ == "__main__":
    df = load_data()  # Carrega os dados
    top10_global_by_name(df)  # Exibe o top 10
    comparar_dois_jogos(df)  # Inicia o comparador interativo