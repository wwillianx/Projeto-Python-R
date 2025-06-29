import pandas as pd
from sklearn.linear_model import LinearRegression
from difflib import get_close_matches

def prever_vendas_jogo_interativo(df):
    nome_input = input("Digite o nome do jogo para prever as vendas futuras: ").strip().lower()

    df['Name_lower'] = df['Name'].str.lower().str.strip()

    df_jogo = df[df['Name_lower'] == nome_input]

    if df_jogo.empty:
        nomes_possiveis = df['Name_lower'].unique().tolist()
        sugestoes = get_close_matches(nome_input, nomes_possiveis, n=3, cutoff=0.6)

        print(f"❌ Jogo '{nome_input}' não encontrado no dataset.")

        if sugestoes:
            print("🔍 Você quis dizer:")
            for s in sugestoes:
                original = df[df['Name_lower'] == s].iloc[0]['Name']
                print(f"  - {original}")
        else:
            print("🧩 Nenhum nome semelhante encontrado.")

        return

    df_jogo_ano = df_jogo.groupby('Year')['Global_Sales'].sum().reset_index()

    if len(df_jogo_ano) < 2:
        print(f"⚠️ Não há dados suficientes de vendas por ano para '{nome_input}' fazer previsão.")
        return

    X = df_jogo_ano[['Year']]
    y = df_jogo_ano['Global_Sales']

    model = LinearRegression()
    model.fit(X, y)

    anos_futuros = pd.DataFrame({'Year': [2025, 2026, 2027]})
    pred = model.predict(anos_futuros)

    nome_real = df_jogo.iloc[0]['Name']

    min_venda = 0.1  # mínimo de 0.1 milhão para vendas futuras

    print(f"\n🔮 Previsão de vendas do jogo '{nome_real}' (todas as plataformas):")
    for ano, venda in zip(anos_futuros['Year'], pred):
        venda_ajustada = max(venda, min_venda)  # garante mínimo 0.1
        print(f"  {ano}: {venda_ajustada:.2f} milhões de unidades")