from scripts import preprocess, model, comparisons

print("🔄 Carregando e processando dados...")
df = preprocess.load_dataset()
preprocess.save_clean_data(df)

print("📈 Executando previsão de vendas futuras:")
model.prever_vendas_jogo_interativo(df)

print("🖼️ Execute: Rscript scripts/analysis.R para gerar os gráficos.")

print("\n📊 Comparações especiais:")
comparisons.top10_global_by_name(df)


# Adicionando a comparação interativa conforme seu pedido
print("\n📊 Iniciando comparação interativa de jogos:")
if df is not None:
    comparisons.comparar_dois_jogos(df)
else:
    print("Não foi possível carregar os dados para comparação.")

print("\n🖼️ Lembre-se de executar: Rscript scripts/analysis.R para gerar os gráficos.")