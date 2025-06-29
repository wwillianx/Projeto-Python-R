from scripts import preprocess, model

print("🔄 Carregando e processando dados...")
df = preprocess.load_dataset()
preprocess.save_clean_data(df)

print("📈 Executando previsão de vendas futuras:")
model.predict_sales()

import scripts.comparisons as compare

# Comparações especiais
print("\n📊 Comparações especiais:")
compare.top10_global_by_name(df)
compare.top10_last_year(df)


print("\n🖼️ Execute: Rscript scripts/analysis.R para gerar os gráficos.")
