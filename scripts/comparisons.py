import pandas as pd

def load_data(path='dados/vgsales.csv'):
    df = pd.read_csv(path)
    df = df.dropna(subset=['Year', 'Global_Sales'])
    df['Year'] = df['Year'].astype(int)
    return df

def formatar_vendas_milhoes(df):
    df['Global_Sales'] = df['Global_Sales'].round(2).astype(str) + " milhões"
    return df

def top10_global_by_name(df):
    grouped = df.groupby("Name")["Global_Sales"].sum().reset_index()
    grouped = grouped.sort_values(by="Global_Sales", ascending=False).head(10)
    grouped = formatar_vendas_milhoes(grouped)
    print("\n🎮 Top 10 jogos mais vendidos (unificando plataformas):\n")
    print(grouped.to_string(index=False))

def comparar_dois_jogos(df):

    if df is None or df.empty:
        print("O DataFrame está vazio. Não é possível realizar a comparação.")
        return

    print("\n" + "="*50)
    print("         🎮 Comparador Interativo de Jogos 🎮")
    print("="*50)

    try:
        while True:
            game1_name = input("\n➡️  Digite o nome do primeiro jogo: ")
            game1_data = df[df['Name'].str.contains(game1_name, case=False, na=False)]
            if not game1_data.empty:
                break
            print(f"❌ Jogo '{game1_name}' não encontrado. Por favor, tente novamente.")

        while True:
            game2_name = input("➡️  Digite o nome do segundo jogo: ")
            game2_data = df[df['Name'].str.contains(game2_name, case=False, na=False)]
            if not game2_data.empty:
                break
            print(f"❌ Jogo '{game2_name}' não encontrado. Por favor, tente novamente.")

        display_name1 = game1_data['Name'].iloc[0]
        display_name2 = game2_data['Name'].iloc[0]

        print("\n" + "-"*50)
        print(f"📊 Comparando '{display_name1}' vs '{display_name2}'")
        print("-" * 50)

        print(f"\n✅ Informações para: {display_name1}")
        print(game1_data.to_string(index=False))

        print(f"\n✅ Informações para: {display_name2}")
        print(game2_data.to_string(index=False))

        game1_total_sales = game1_data['Global_Sales'].sum()
        game2_total_sales = game2_data['Global_Sales'].sum()

        print("\n" + "="*50)
        print("            🏆 Resumo da Comparação 🏆")
        print("="*50)
        print("\n📈 Vendas Globais Consolidadas (somando todas as plataformas):")
        print(f"  - {display_name1}: {game1_total_sales:.2f} milhões")
        print(f"  - {display_name2}: {game2_total_sales:.2f} milhões")

        diff = abs(game1_total_sales - game2_total_sales)
        if game1_total_sales > game2_total_sales:
            print(f"\n🎉 '{display_name1}' vendeu {diff:.2f} milhões de cópias a mais globalmente.")
        elif game2_total_sales > game1_total_sales:
            print(f"\n🎉 '{display_name2}' vendeu {diff:.2f} milhões de cópias a mais globalmente.")
        else:
            print("\n⚖️ Ambos os jogos tiveram um total de vendas globais idêntico!")
        print("\n" + "="*50)

    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a comparação: {e}")

if __name__ == "__main__":
    df = load_data()
    top10_global_by_name(df)
    comparar_dois_jogos(df)